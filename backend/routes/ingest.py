from flask import Blueprint, request, jsonify
from vector_db import query_vector_db

ingest_bp = Blueprint('ingest', __name__)

@ingest_bp.route("/search", methods=["POST"])
def search_kb():
    """Searches vector DB for relevant context chunks."""
    data = request.get_json() or {}
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query string is required"}), 400

    results = query_vector_db(query, n_results=3)
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    matches = []
    for doc, meta in zip(documents, metadatas):
        matches.append({"content": doc, "metadata": meta})

    return jsonify({"query": query, "results": matches}), 200