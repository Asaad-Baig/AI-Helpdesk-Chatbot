import datetime
from flask import Blueprint, jsonify
from database import client

health_bp = Blueprint('health', __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """System health check endpoint."""
    try:
        client.admin.command("ping")
        db_status = "Connected"
    except Exception as e:
        db_status = f"Disconnected: {str(e)}"

    return jsonify({
        "status": "Online",
        "service": "AI Helpdesk Backend API",
        "database": db_status,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200