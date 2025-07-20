from bson import ObjectId

class Itinerary:
    def __init__(self, user_id, location, date_from, date_to, event_ids=None):
        self.user_id = ObjectId(user_id)
        self.location = location
        self.date_range = {
            "from": date_from,  # expected as string "YYYY-MM-DD"
            "to": date_to       # expected as string "YYYY-MM-DD"
        }
        self.event_ids = [ObjectId(eid) for eid in (event_ids or [])]
        self.trip_name

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "location": self.location,
            "date_range": self.date_range,
            "event_ids": self.event_ids,
            "trip_name": self.trip_name
        }
