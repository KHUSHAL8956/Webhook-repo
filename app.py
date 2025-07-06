from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    event = request.headers.get('X-GitHub-Event')
    if event == "push":
        author = payload["pusher"]["name"]
        to_branch = payload["ref"].split("/")[-1]
        timestamp = payload["head_commit"]["timestamp"]
        doc = {"type": "push", "author": author, "to_branch": to_branch, "timestamp": timestamp}
    elif event == "pull_request":
        action = payload["action"]
        pr = payload["pull_request"]
        author = pr["user"]["login"]
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]
        if action == "opened":
            timestamp = pr["created_at"]
            doc = {"type": "pull_request", "author": author, "from_branch": from_branch, "to_branch": to_branch, "timestamp": timestamp}
        elif action == "closed" and pr["merged"]:
            timestamp = pr["merged_at"]
            doc = {"type": "merge", "author": author, "from_branch": from_branch, "to_branch": to_branch, "timestamp": timestamp}
        else:
            return "Ignored", 200
    else:
        return "Ignored", 200
    collection.insert_one(doc)
    return "OK", 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(20))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)