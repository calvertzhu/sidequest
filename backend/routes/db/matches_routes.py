from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from app.models.matches import Match  # adjust import path as needed

matches_bp = Blueprint("matches", __name__)

@matches_bp.route("/matches", methods=["POST"])
def create_match_entry():
    db = current_app.config["DB"]
    data = request.get_json()

    try:
        match_obj = Match(
            user_id=data["user_id"],
            event_id=data["event_id"],
            matches=data.get("matches", [])
        )

        match_doc = match_obj.to_dict()
        result = db.matches.insert_one(match_doc)
        return jsonify({"_id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@matches_bp.route("/generate_matches", methods=["POST"])
def generate_matches():
    db = current_app.config["DB"]
    data = request.get_json()

    return "Success"

@matches_bp.route("/matches", methods=["GET"])
def get_all_matches():
    db = current_app.config["DB"]
    try:
        all_matches = list(db.matches.find({}))
        for m in all_matches:
            m["_id"] = str(m["_id"])
            m["user_id"] = str(m["user_id"])
            m["event_id"] = str(m["event_id"])
            for match in m.get("matches", []):
                match["matched_user_id"] = str(match["matched_user_id"])
        return jsonify(all_matches), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

        
