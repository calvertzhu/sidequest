# from flask import Blueprint, request, jsonify, current_app
# from datetime import datetime

# users_bp = Blueprint('users', __name__)

# @users_bp.route('/users', methods=['POST'])
# def create_user():
#     db = current_app.config["DB"]
#     data = request.json

#     # Parse and sanitize input
#     try:
#         user = {
#             "name": data["name"],
#             "birthday": datetime.strptime(data["birthday"], "%Y-%m-%d"),
#             "gender": data["gender"],
#             "interests": data.get("interests", []),
#             "profile_pic": data.get("profile_pic", ""),
#             "dietary_restrictions": data.get("dietary_restrictions", "")
#         }

#         result = db.users.insert_one(user)
#         return jsonify({"_id": str(result.inserted_id)}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


# @users_bp.route("/get_all_users", methods=["GET"])
# def get_all_users():
#     db = current_app.config["DB"]
#     users = list(db.users.find({}))
#     for user in users:
#         user["_id"] = str(user["_id"])
#         if "birthday" in user:
#             user["birthday"] = user["birthday"].strftime("%Y-%m-%d")
#     return jsonify(users), 200
