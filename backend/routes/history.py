from flask import Blueprint, jsonify
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import db  # MongoDB instance

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_conversations():
    """Returns a list of all saved conversation sessions."""
    try:
        convs = list(db.conversations.find({}, {"_id": 0}).sort("created_at", -1))
        return jsonify({"conversations": convs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/history/<conversation_id>', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Returns all messages for a specific conversation session."""
    try:
        msgs = list(db.messages.find({"conversation_id": conversation_id}, {"_id": 0}).sort("timestamp", 1))
        return jsonify({"messages": msgs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500