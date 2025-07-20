from flask import Blueprint, request, jsonify, current_app
from app.models.message import Message
from bson import ObjectId
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def send_message():
    db = current_app.config["DB"]
    data = request.json
    msg = Message(data["from_user_id"], data["to_user_id"], data["text"])
    db.messages.insert_one(msg.to_dict())
    return jsonify({"message": "Message sent"}), 201

@messages_bp.route('/messages/<user_id>/<other_user_id>', methods=['GET'])
def get_messages(user_id, other_user_id):
    db = current_app.config["DB"]
    # Get all messages between user_id and other_user_id
    messages = list(db.messages.find({
        "$or": [
            {"from_user_id": user_id, "to_user_id": other_user_id},
            {"from_user_id": other_user_id, "to_user_id": user_id}
        ]
    }).sort("created_at", 1))
    for m in messages:
        m["_id"] = str(m["_id"])
        # Convert datetime to ISO string for frontend
        if isinstance(m["created_at"], datetime):
            m["created_at"] = m["created_at"].isoformat()
    return jsonify(messages), 200 