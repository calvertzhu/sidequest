from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    db = current_app.config["DB"]
    data = request.json

    # Parse and sanitize input
    try:
        user_obj = User(
            name=data["name"],
            email=data["email"],
            birthday=data["birthday"],  # still as string "YYYY-MM-DD"
            gender=data["gender"],
            interests=data.get("interests", []),
            profile_pic=data.get("profile_pic", ""),
            dietary_restrictions=data.get("dietary_restrictions", []),
            location=data.get("location", ""),
            travel_dates=data.get("travel_dates", {})  # optional or required, depending on use
        )

        user = user_obj.to_dict()
        user["birthday"] = datetime.strptime(user["birthday"], "%Y-%m-%d") if user["birthday"] else "" # convert before DB insert
        result = db.users.insert_one(user)
        return jsonify({"_id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route("/users/<email>", methods=["PUT"])
def update_user_by_email(email):
    db = current_app.config["DB"]
    data = request.json

    try:
        # Check if user exists
        existing_user = db.users.find_one({"email": email})
        if not existing_user:
            return jsonify({"error": "User not found"}), 404

        # Prepare update data
        update_data = {
            "name": data.get("name", existing_user.get("name", "")),
            "birthday": datetime.strptime(data["birthday"], "%Y-%m-%d") if data.get("birthday") else existing_user.get("birthday"),
            "gender": data.get("gender", existing_user.get("gender", "")),
            "interests": data.get("interests", existing_user.get("interests", [])),
            "profile_pic": data.get("profile_pic", existing_user.get("profile_pic", "")),
            "dietary_restrictions": data.get("dietary_restrictions", existing_user.get("dietary_restrictions", "")),
            "location": data.get("location", existing_user.get("location", "")),
            "travel_dates": data.get("travel_dates", existing_user.get("travel_dates", {}))
        }

        # Update user in database
        result = db.users.update_one(
            {"email": email},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"message": "No changes made"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route("/get_all_users", methods=["GET"])
def get_all_users():
    db = current_app.config["DB"]
    users = list(db.users.find({}))
    for user in users:
        user["_id"] = str(user["_id"])
        if "birthday" in user:
            user["birthday"] = user["birthday"].strftime("%Y-%m-%d")
    return jsonify(users), 200

@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    db = current_app.config["DB"]

    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        user["_id"] = str(user["_id"])
        user["interests"] = user.get("interests", [])
        user["gender"] = user.get("gender")
        user["profile_pic"] = user.get("profile_pic")
        if "birthday" in user:
            user["birthday"] = user["birthday"].strftime("%Y-%m-%d")

        return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def getUserByEmail(db, email):
    if not email:
        return jsonify({"error": "Missing required query parameter: email"}), 400

    try:
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"exists": False}), 200

        user["_id"] = str(user["_id"])
        user["interests"] = user.get("interests", [])
        user["gender"] = user.get("gender")
        user["dietary_restrictions"] = user.get("dietary_restrictions", [])
        if "birthday" in user and isinstance(user["birthday"], datetime):
            user["birthday"] = user["birthday"].strftime("%Y-%m-%d")

        return jsonify({"exists": True, "user": user}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route("/users/search", methods=["GET"])
def get_user_by_email():
    db = current_app.config["DB"]
    email = request.args.get("email")

    return getUserByEmail(db, email)
    