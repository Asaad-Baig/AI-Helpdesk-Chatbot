from flask import Blueprint, request, jsonify, Response, stream_with_context
import requests
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_db import query_vector_db  # type: ignore
from database import db  # Import MongoDB connection

chat_bp = Blueprint('chat', __name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
DISTANCE_THRESHOLD = 1.2

SYSTEM_PROMPT_TEMPLATE = """
You are an Enterprise AI Helpdesk Support Assistant.
Answer the user's question strictly using ONLY the retrieved context below.

CRITICAL CONSTRAINTS:
- NEVER define or spell out acronyms unless explicitly written in the context.
- Refer to unknown acronyms or entities EXACTLY as they appear.
- If the context does not contain enough detail, state: "I cannot find a direct answer in the knowledge base."

---
RETRIEVED KNOWLEDGE BASE CONTEXT:
{context}
---

USER QUESTION:
{question}

YOUR RESPONSE:
"""

TITLE_PROMPT = """Classify the user's helpdesk message into a short topic label of 2-4 words
(for example: "Password Reset", "VPN Issue", "Software Installation", "Email Setup", "Leave Policy").
Reply with ONLY the label, no quotes, no punctuation, no explanation.

MESSAGE: {message}

LABEL:"""

def safe_db_insert(collection_name, document):
    """Helper function to insert documents and capture connection errors."""
    try:
        res = db[collection_name].insert_one(document)
        print(f"[SUCCESS] Document saved to '{collection_name}' with ID: {res.inserted_id}")
        return res
    except Exception as e:
        print(f"[ERROR] Failed to write to MongoDB '{collection_name}': {e}")
        return None

def generate_title(message):
    """Returns a short topic label for the first message, falling back to a truncated message."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": TITLE_PROMPT.format(message=message),
                "stream": False,
                "options": {"temperature": 0, "num_predict": 12}
            },
            timeout=30
        )
        title = response.json().get("response", "").strip().split("\n")[0]
        title = title.strip(' "\'.:')
        if title:
            return title[:40]
    except Exception as e:
        print(f"[ERROR] Title generation failed: {e}")
    return message[:30]    

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    conversation_id = data.get("conversation_id", "default_session")
    stream_mode = data.get("stream", False)

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # 1. Ensure conversation document exists
    try:
        existing = db.conversations.find_one({"conversation_id": conversation_id}, {"_id": 1})
        if not existing:
            db.conversations.insert_one({
                "conversation_id": conversation_id,
                "created_at": datetime.utcnow(),
                "title": generate_title(user_message)
            })
    except Exception as e:
        print(f"[ERROR] Conversation upsert failed: {e}")

    # 2. Save User Message to MongoDB
    safe_db_insert("messages", {
        "conversation_id": conversation_id,
        "sender": "user",
        "text": user_message,
        "timestamp": datetime.utcnow()
    })

    # 3. Vector Retrieval & Distance Check
    vector_results = query_vector_db(user_message, n_results=2)
    documents = vector_results.get("documents", [[]])[0]
    metadatas = vector_results.get("metadatas", [[]])[0]
    distances = vector_results.get("distances", [[]])[0]

    sources = list(set([m.get("source", "Unknown") for m in metadatas if m]))

    # Fallback Handling
    if not documents or (distances and min(distances) > DISTANCE_THRESHOLD):
        fallback_reply = "I cannot find a direct answer in the knowledge base."
        
        # Save Bot Fallback Message to MongoDB
        safe_db_insert("messages", {
            "conversation_id": conversation_id,
            "sender": "bot",
            "text": fallback_reply,
            "sources": [],
            "low_confidence": True,
            "timestamp": datetime.utcnow()
        })
        
        return jsonify({
            "reply": fallback_reply,
            "sources": [],
            "low_confidence": True
        }), 200

    retrieved_context = "\n\n".join(documents)
    formatted_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=retrieved_context, question=user_message)

    # 4. Stream Mode
    if stream_mode:
        def generate():
            full_reply = ""
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={"model": OLLAMA_MODEL, "prompt": formatted_prompt, "stream": True},
                    stream=True,
                    timeout=300
                )
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        token = chunk.get("response", "")
                        full_reply += token
                        yield f"data: {json.dumps({'token': token, 'sources': sources})}\n\n"
            except Exception as e:
                print(f"[ERROR] Streaming error from Ollama: {e}")
            finally:
                # Guarantees execution post-stream
                if full_reply.strip():
                    safe_db_insert("messages", {
                        "conversation_id": conversation_id,
                        "sender": "bot",
                        "text": full_reply,
                        "sources": sources,
                        "timestamp": datetime.utcnow()
                    })
                yield "data: [DONE]\n\n"

        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    # 5. Non-Streaming Mode
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": formatted_prompt, "stream": False},
            timeout=300
        )
        bot_reply = response.json().get("response", "").strip()

        # Save Bot Reply to MongoDB
        safe_db_insert("messages", {
            "conversation_id": conversation_id,
            "sender": "bot",
            "text": bot_reply,
            "sources": sources,
            "timestamp": datetime.utcnow()
        })

        return jsonify({"reply": bot_reply, "sources": sources, "low_confidence": False}), 200
    except Exception as e:
        return jsonify({"error": f"Ollama connection error: {str(e)}"}), 500