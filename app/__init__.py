from flask import Flask
from .extensions import mongo
from .webhook import webhook_bp  # ✅ This will now work

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    mongo.init_app(app)

    app.register_blueprint(webhook_bp)

    return app
