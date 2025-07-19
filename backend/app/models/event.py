from datetime import datetime

class Event:
    def __init__(self, name, location, time, desc="", users=None):
        self.name = name
        self.location = location
        self.time = time  # expected as string: "YYYY-MM-DDTHH:MM"
        self.desc = desc
        self.users = users or []

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "time": datetime.strptime(self.time, "%Y-%m-%dT%H:%M"),
            "desc": self.desc,
            "users": self.users
        }
