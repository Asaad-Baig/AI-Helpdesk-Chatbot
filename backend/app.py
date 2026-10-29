import os
from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.admin import admin_bp
from routes.health import health_bp
from routes.history import history_bp
from routes.ingest import ingest_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")
app.register_blueprint(ingest_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)