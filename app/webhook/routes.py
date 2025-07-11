from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo

# ✅ Define the Blueprint first
webhook_bp = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Initialize default values
    event_data = {
        "request_id": None,
        "author": None,
        "action": event_type.upper(),
        "from_branch": None,
        "to_branch": None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Handle PUSH event
    if event_type == "push":
        event_data["request_id"] = payload.get("after")
        event_data["author"] = payload.get("pusher", {}).get("name")
        branch = payload.get("ref", "").split("/")[-1]
        event_data["from_branch"] = branch
        event_data["to_branch"] = branch

    # Handle PULL_REQUEST event
    elif event_type == "pull_request":
        pr = payload.get("pull_request", {})
        event_data["request_id"] = str(pr.get("id"))
        event_data["author"] = pr.get("user", {}).get("login")
        event_data["from_branch"] = pr.get("head", {}).get("ref")
        event_data["to_branch"] = pr.get("base", {}).get("ref")

        # Detect MERGE action
        if payload.get("action") == "closed" and pr.get("merged"):
            event_data["action"] = "MERGE"

    else:
        return jsonify({"message": "Unsupported event type"}), 400

    # Insert into MongoDB
    mongo.db.events.insert_one(event_data)

    return jsonify({"message": "Event stored successfully"}), 200


@webhook_bp.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)
    formatted = []

    for e in events:
        action = e.get("action")
        author = e.get("author")
        from_branch = e.get("from_branch")
        to_branch = e.get("to_branch")
        timestamp = format_timestamp(e.get("timestamp"))

        if action == "PUSH":
            message = f'"{author}" pushed to "{to_branch}" on {timestamp}'
        elif action == "PULL_REQUEST":
            message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
        elif action == "MERGE":
            message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
        else:
            message = "Unknown action"

        formatted.append(message)

    return jsonify(formatted), 200


@webhook_bp.route('/', methods=["GET"])
def home():
    return render_template("index.html")


def format_timestamp(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", ""))
        return dt.strftime("%d %B %Y - %I:%M %p UTC")
    except:
        return ts
