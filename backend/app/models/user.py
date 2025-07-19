class User:
    def __init__(self, name, email, interests, location, travel_dates):
        self.name = name
        self.email = email
        self.interests = interests
        self.location = location
        self.travel_dates = travel_dates

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'interests': self.interests,
            'location': self.location,
            'travel_dates': self.travel_dates
        } 
        