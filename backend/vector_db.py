import os
import chromadb
from chromadb.utils import embedding_functions

# Initialize persistent Chroma client in backend/chroma_db
CHROMA_DATA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# Use sentence-transformers for local text embeddings
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create collection for enterprise knowledge base
kb_collection = chroma_client.get_or_create_collection(
    name="enterprise_kb",
    embedding_function=sentence_transformer_ef
)

def add_documents_to_vector_db(chunks, metadatas=None, ids=None):
    """Inserts processed text chunks into ChromaDB."""
    if ids is None:
        ids = [f"doc_{i}" for i in range(len(chunks))]
    
    kb_collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    return len(chunks)

def query_vector_db(query_text, n_results=3):
    """Retrieves top relevant context chunks for a user query."""
    results = kb_collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results