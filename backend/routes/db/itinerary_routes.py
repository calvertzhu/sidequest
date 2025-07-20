from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from app.models.itinerary import Itinerary  # adjust path as needed

itins_bp = Blueprint("itineraries", __name__)

def insertItinerary(data):
    db = current_app.config["DB"]
    try:
        itinerary = {
            "user_id": data["user_id"],
            "location": data["location"],
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "event_ids": data.get("event_ids", []),
            "trip_name": data["trip_name"]
        }
        result = db.itineraries.insert_one(itinerary)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@itins_bp.route("/itineraries", methods=["POST"])
def create_itinerary():
    db = current_app.config["DB"]
    data = request.json
    return insertItinerary(db, data)

@itins_bp.route("/itineraries/user/<user_id>", methods=["GET"])
def get_user_itineraries(user_id):
    db = current_app.config["DB"]
    try:
        itineraries = list(db.itineraries.find({"user_id": ObjectId(user_id)}))
        for itin in itineraries:
            itin["_id"] = str(itin["_id"])
            itin["user_id"] = str(itin["user_id"])
            itin["event_ids"] = [str(eid) for eid in itin["event_ids"]]
            itin["trip_name"] = str(itin["trip_name"])
        return jsonify(itineraries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@itins_bp.route("/itineraries/<itinerary_id>/events", methods=["GET"])
def get_itinerary_events(itinerary_id):
    db = current_app.config["DB"]
    try:
        itinerary = db.itineraries.find_one({"_id": ObjectId(itinerary_id)})
        if not itinerary:
            return jsonify({"error": "Itinerary not found"}), 404

        events = list(db.events.find({"_id": {"$in": itinerary["event_ids"]}}))
        events.sort(key=lambda e: e.get("time", None))

        for event in events:
            event["_id"] = str(event["_id"])
            event["time"] = event["time"].strftime("%Y-%m-%dT%H:%M")

        return jsonify(events), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# @itins_bp.route("/itineraries/user/<user_id>/trip", methods=["GET"])
# def get_itinerary_by_user_and_trip(user_id):
#     db = current_app.config["DB"]
#     trip_name = request.args.get("trip_name")

#     if not trip_name:
#         return jsonify({"error": "Missing required query parameter: trip_name"}), 400

#     try:
#         itinerary = db.itineraries.find_one({
#             "user_id": ObjectId(user_id),
#             "trip_name": trip_name
#         })

#         if not itinerary:
#             return jsonify({"error": "Itinerary not found"}), 404

#         itinerary["_id"] = str(itinerary["_id"])
#         itinerary["user_id"] = str(itinerary["user_id"])
#         itinerary["event_ids"] = [str(eid) for eid in itinerary.get("event_ids", [])]

#         return jsonify(itinerary), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
