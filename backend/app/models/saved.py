from bson import ObjectId

class Saved:
    def __init__(self, user_id, saved_user_id):
        self.user_id = ObjectId(user_id)
        self.saved_user_id = ObjectId(saved_user_id)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "saved_user_id": self.saved_user_id
        }
