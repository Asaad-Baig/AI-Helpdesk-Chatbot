from flask import Blueprint, jsonify, request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import db  # MongoDB connection instance

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/stats', methods=['GET'])
def get_dashboard_stats():
    """Returns system usage metrics and error logs for the Admin Dashboard."""
    try:
        total_conversations = db.conversations.count_documents({})
        total_messages = db.messages.count_documents({})
        error_logs = list(db.error_logs.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))
        feedback_stats = list(db.feedback.find({}, {"_id": 0}))

        return jsonify({
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "error_logs": error_logs,
            "feedback": feedback_stats,
            "status": "healthy"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve stats: {str(e)}"}), 500

@admin_bp.route('/admin/log_error', methods=['POST'])
def log_system_error():
    """Logs runtime exceptions and low-confidence fallbacks into MongoDB."""
    data = request.get_json() or {}
    db.error_logs.insert_one({
        "error_type": data.get("type", "RuntimeError"),
        "message": data.get("message", "Unknown error"),
        "timestamp": data.get("timestamp"),
        "query": data.get("query", "")
    })
    return jsonify({"status": "logged"}), 201