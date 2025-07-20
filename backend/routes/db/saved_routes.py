from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime

saved_bp = Blueprint("saved", __name__)

# POST /api/saved - Save another user's profile
@saved_bp.route("/saved", methods=["POST"])
def save_user():
    db = current_app.config["DB"]
    data = request.get_json()
    user_id = data.get("user_id")
    saved_user_id = data.get("saved_user_id")

    if not user_id or not saved_user_id:
        return jsonify({"error": "Missing user_id or saved_user_id"}), 400

    try:
        connection = SavedConnection(user_id, saved_user_id)
        db.saved.insert_one(connection.to_dict())
        return jsonify({"message": "User saved successfully"}), 201

    except Exception as e:
        if "duplicate key" in str(e).lower():
            return jsonify({"message": "User already saved"}), 200
        return jsonify({"error": str(e)}), 400


# GET /api/saved/<user_id> - Get all saved profiles for a user
@saved_bp.route("/saved/<user_id>", methods=["GET"])
def get_saved_users(user_id):
    db = current_app.config["DB"]
    try:
        saved = list(db.saved.find({"user_id": ObjectId(user_id)}))
        for s in saved:
            s["_id"] = str(s["_id"])
            s["user_id"] = str(s["user_id"])
            s["saved_user_id"] = str(s["saved_user_id"])

        return jsonify(saved), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# GET /api/saved/check - Check if a user is already saved
@saved_bp.route("/saved/check", methods=["GET"])
def check_saved():
    db = current_app.config["DB"]
    user_id = request.args.get("user_id")
    saved_user_id = request.args.get("saved_user_id")

    if not user_id or not saved_user_id:
        return jsonify({"error": "Missing user_id or saved_user_id"}), 400

    try:
        exists = db.saved.find_one({
            "user_id": ObjectId(user_id),
            "saved_user_id": ObjectId(saved_user_id)
        })
        return jsonify({"saved": bool(exists)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
