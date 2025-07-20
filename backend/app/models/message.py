from datetime import datetime
from bson import ObjectId

class Message:
    def __init__(self, from_user_id, to_user_id, text, created_at=None):
        self.from_user_id = str(from_user_id)
        self.to_user_id = str(to_user_id)
        self.text = text
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "text": self.text,
            "created_at": self.created_at,
        } 