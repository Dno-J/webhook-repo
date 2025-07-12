# 📡 GitHub Webhook Dashboard

A Flask-based project was developed as part of a technical assignment for TechStax. It showcases the ability to build a backend service using Flask that receives and processes GitHub webhook events, stores them in MongoDB, and presents them through a clean, responsive UI.
---

## 🛠️ Tech Stack

- **Flask** – Lightweight Python web framework  
- **Flask-PyMongo** – MongoDB integration  
- **MongoDB** – NoSQL database for storing webhook events  
- **HTML/CSS** – Responsive UI with animations  
- **GitHub Webhooks** – Event source  
- **ngrok** – Public tunnel for local development

---

## 📁 Project Structure

```
webhook-repo/
│
├── app/
│   ├── __init__.py              # App factory
│   ├── extensions.py            # MongoDB setup
│   └── webhook/
│       ├── __init__.py
│       └── routes.py            # Webhook logic and routes
│
├── static/
│   └── styles.css               # UI styling for dashboard
│
├── templates/
│   └── webhook.html             # Dashboard UI
│
├── run.py                       # Entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignore cache/env files
└── README.md                    # Project documentation
```

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB locally  
Make sure MongoDB is running on `localhost:27017`.

### 5. Run the app

```bash
python run.py
```

---

## 🌐 Expose Locally with ngrok

GitHub webhooks require a public URL. Use [ngrok](https://ngrok.com/) to expose your local Flask server.

### 1. Install ngrok (if not already)

```bash
# On macOS
brew install ngrok

# On Windows/Linux
Download from https://ngrok.com/download
```

### 2. Run ngrok to expose port 5000

```bash
ngrok http 5000
```

### 3. Copy the HTTPS URL from ngrok

It will look like:

```
https://abc123.ngrok.io
```

Use this in your GitHub webhook settings:

- **Payload URL**: `https://abc123.ngrok.io/webhook/receiver`

---

## 📡 Webhook Setup

In your GitHub repository:

1. Go to **Settings → Webhooks**
2. Add a new webhook:
   - **Payload URL**: `https://your-ngrok-url/webhook/receiver`
   - **Content type**: `application/json`
   - **Events**: `push`, `pull_request`

---

## 🗄️ MongoDB Integration

This project uses **Flask-PyMongo** to connect and interact with MongoDB.

### 🔌 Configuration

MongoDB is configured in `create_app()` inside `app/__init__.py`:

```python
app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
mongo.init_app(app)
```

- `github_events` is the database name  
- MongoDB must be running locally on port `27017`

### 🧩 Initialization

The `mongo` object is created in `app/extensions.py`:

```python
from flask_pymongo import PyMongo
mongo = PyMongo()
```

This is imported and used across the app.

### 📥 Storing Events

Webhook data is stored using:

```python
mongo.db.events.insert_one(event_data)
```

Each event is saved in the `events` collection inside the `github_events` database.

### 📤 Retrieving Events

To display or return recent events:

```python
events = mongo.db.events.find().sort("timestamp", -1).limit(10)
```

This is used in both the dashboard UI and the JSON API.

---

## 🌐 Endpoints

| Route                | Description                        |
|---------------------|------------------------------------|
| `/webhook/receiver` | Receives GitHub webhook payloads   |
| `/webhook/`         | Displays recent events in UI       |
| `/webhook/events`   | Returns raw JSON of recent events  |

---

## 🎯 Features

- ✅ Stores push and pull request events  
- ✅ Detects and labels merge actions  
- ✅ Displays events with hover animations  
- ✅ Clean separation of API and UI  
- ✅ MongoDB-backed persistence  
- ✅ ngrok-compatible for local testing

---

## 📬 Example JSON Output

```json
{
  "author": "Dino",
  "action": "PUSH",
  "from_branch": "main",
  "to_branch": "main",
  "timestamp": "2025-07-12T02:00:00Z",
  "request_id": "abc123"
}
```

---

## 🙌 Credits

Developed by Dino as part of a technical interview assignment for TechStax, highlighting backend integration, data handling, and UI design skills.
