import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "helpdesk_ai")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def init_db():
    """Configures collection schemas, indexes, and initial setups."""
    try:
        client.admin.command('ping')
        
        db.conversations.create_index("user_id")
        db.conversations.create_index("created_at")
        db.messages.create_index("conversation_id")
        db.raw_data.create_index("source")
        
        print("Database schemas & indexes initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == "__main__":
    init_db()