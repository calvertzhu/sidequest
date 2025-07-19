from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["POST"])
def create_event():
    db = current_app.config["DB"]
    data = request.json
    try:
        event = {
            "name": data["name"],
            "location": data["location"],
            "time": datetime.strptime(data["time"], "%Y-%m-%dT%H:%M"),
            "desc": data.get("desc", ""),
            "users": data.get("users", [])  # Optional list of user IDs
        }
        result = db.events.insert_one(event)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@events_bp.route("/events", methods=["GET"])
def get_events():
    db = current_app.config["DB"]
    location = request.args.get("location")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    query = {}
    if location:
        query["location"] = location
    if from_date and to_date:
        query["time"] = {
            "$gte": datetime.strptime(from_date, "%Y-%m-%d"),
            "$lte": datetime.strptime(to_date, "%Y-%m-%d")
        }

    events = list(db.events.find(query))
    for event in events:
        event["_id"] = str(event["_id"])
        event["time"] = event["time"].strftime("%Y-%m-%dT%H:%M")

    return jsonify(events), 200
