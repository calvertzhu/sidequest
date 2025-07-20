from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
from app.models.event import Event

events_bp = Blueprint("events", __name__)

def insertEvent(db, data):
    try:
        event_obj = Event(
            name=data["name"],
            location=data["location"],
            time=data["time"], #datetime.strptime(data["time"], "%Y-%m-%dT%H:%M"),
            # price=data["price"],
            # link=data["link"],
            desc=data.get("desc", ""),
            users=data.get("users", [])
        )

        event = event_obj.to_dict()
        result = db.events.insert_one(event)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@events_bp.route("/events", methods=["POST"])
def create_event():
    db = current_app.config["DB"]
    data = request.json
    return insertEvent(db, data)

def updateEventWithUser(db, data):
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id in request body"}), 400

    try:
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        user_obj_id = ObjectId(user_id)

        # Prevent duplicate entries
        if user_obj_id in event.get("users", []):
            return jsonify({"message": "User already added"}), 200

        db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$addToSet": {"users": user_obj_id}}
        )

        return jsonify({"message": "User added to event"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@events_bp.route("/events/<event_id>/add-user", methods=["POST"])
def add_user_to_event(event_id):
    db = current_app.config["DB"]
    data = request.get_json()
    return updateEventWithUser(db, data)


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

        user_ids = event.get("users", [])
        if user_ids:
            users = list(db.users.find({"_id": {"$in": user_ids}}))
            for user in users:
                user["_id"] = str(user["_id"])
            event["users"] = users

    return jsonify(events), 200

def getEventByDetails(db, name, location, time_str):
    if not name or not location or not time_str:
        return jsonify({"error": "Missing required query parameters: name, location, time"}), 400

    try:
        event_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        event = db.events.find_one({
            "name": name,
            "location": location,
            "time": event_time
        })

        if not event:
            return jsonify({"exists": False}), 200

        event["_id"] = str(event["_id"])
        event["time"] = event["time"].strftime("%Y-%m-%dT%H:%M")
        return jsonify({"exists": True, "event": event}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@events_bp.route("/events/search", methods=["GET"])
def search_event_by_details():
    db = current_app.config["DB"]
    name = request.args.get("name")
    location = request.args.get("location")
    time_str = request.args.get("time")  # expects ISO format: "YYYY-MM-DDTHH:MM"

    return getEventByDetails(db, name, location, time_str)


