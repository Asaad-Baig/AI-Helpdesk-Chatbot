import os
import sys
import re
import json

# Add backend directory to import vector_db module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from vector_db import add_documents_to_vector_db  # type: ignore

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)        
    return text.strip()

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def process_file(file_path):
    if not os.path.exists(file_path):
        return

    filename = os.path.basename(file_path)

    # 1. Process Plain Text & Markdown
    if file_path.endswith(('.txt', '.md')):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)
        if not cleaned:
            return

        chunks = chunk_text(cleaned)
        doc_ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in chunks]

        count = add_documents_to_vector_db(chunks, metadatas=metadatas, ids=doc_ids)
        print(f"Processed {filename} -> Ingested {count} chunks into ChromaDB.")

    # 2. Process train_dataset_2.json & Structured JSON Files
    elif file_path.endswith('.json'):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle list of JSON items (like train_dataset_2.json)
            if isinstance(data, list):
                total_chunks = 0
                for idx, item in enumerate(data):
                    # Use 'clean_content' if available, otherwise fallback to 'content'
                    raw_text = item.get("clean_content") or item.get("content") or ""
                    cleaned = clean_text(raw_text)
                    if not cleaned:
                        continue

                    # Extract additional metadata present in train_dataset_2.json
                    source_url = item.get("source_url", filename)
                    intent = item.get("intent", "unknown")

                    chunks = chunk_text(cleaned)
                    doc_ids = [f"{filename}_item_{idx}_chunk_{i}" for i in range(len(chunks))]
                    metadatas = [
                        {
                            "source": filename,
                            "source_url": source_url,
                            "intent": intent
                        }
                        for _ in chunks
                    ]

                    count = add_documents_to_vector_db(chunks, metadatas=metadatas, ids=doc_ids)
                    total_chunks += count

                print(f"Processed {filename} -> Ingested {total_chunks} total chunks into ChromaDB.")

        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return

def run_ingestion():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

if __name__ == "__main__":
    run_ingestion()