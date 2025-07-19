class User:
    def __init__(self, name, email, birthday, gender, interests, profile_pic, dietary_restrictions, location, travel_dates):
        self.name = name
        self.email = email
        self.birthday = birthday  # expected as string "YYYY-MM-DD"
        self.gender = gender
        self.interests = interests
        self.profile_pic = profile_pic
        self.dietary_restrictions = dietary_restrictions
        self.location = location
        self.travel_dates = travel_dates

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'birthday': self.birthday,
            'gender': self.gender,
            'interests': self.interests,
            'profile_pic': self.profile_pic,
            'dietary_restrictions': self.dietary_restrictions,
            'location': self.location
        }
