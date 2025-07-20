from datetime import datetime
from bson import ObjectId

class Match:
    def __init__(self, user_id, event_id, matches=None):
        self.user_id = user_id  # string, expected to be a valid ObjectId
        self.event_id = event_id  # string, expected to be a valid ObjectId
        self.matches = matches or []  # list of dicts: {matched_user_id, score}
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": ObjectId(self.user_id),
            "event_id": ObjectId(self.event_id),
            "matches": [
                {
                    "matched_user_id": ObjectId(match["matched_user_id"]),
                    "score": float(match["score"])
                }
                for match in self.matches
            ],
        }
