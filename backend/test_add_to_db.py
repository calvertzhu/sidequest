from routes.gemini.add_to_db import process_gemini_itinerary_to_database

def main():
    # Dummy Gemini-style itinerary JSON
    itinerary_json = {
        "day_1": {
            "morning": [
                {
                    "name": "Golden Gate Bridge",
                    "description": "Walk across the iconic bridge.",
                    "location": "Golden Gate Bridge, San Francisco, CA",
                    "start_time": "09:00",
                    "end_time": "10:30",
                    "price": 0
                }
            ],
            "afternoon": [
                {
                    "name": "Fisherman's Wharf",
                    "description": "Enjoy seafood and street performers.",
                    "location": "Fisherman's Wharf, San Francisco, CA",
                    "start_time": "12:00",
                    "end_time": "13:30",
                    "price": 25
                }
            ],
            "evening": [
                {
                    "name": "Alcatraz Island Tour",
                    "description": "Tour the historic prison island.",
                    "location": "Alcatraz Island, San Francisco, CA",
                    "start_time": "18:00",
                    "end_time": "20:00",
                    "price": 45
                }
            ]
        },
        "day_2": {
            "morning": [
                {
                    "name": "Golden Gate Park",
                    "description": "Relax in the park and visit museums.",
                    "location": "Golden Gate Park, San Francisco, CA",
                    "start_time": "09:30",
                    "end_time": "11:30",
                    "price": 0
                }
            ],
            "afternoon": [
                {
                    "name": "Chinatown Lunch",
                    "description": "Sample dim sum in Chinatown.",
                    "location": "Chinatown, San Francisco, CA",
                    "start_time": "12:30",
                    "end_time": "14:00",
                    "price": 20
                }
            ],
            "evening": [
                {
                    "name": "Cable Car Ride",
                    "description": "Ride the famous San Francisco cable cars.",
                    "location": "Powell St, San Francisco, CA",
                    "start_time": "19:00",
                    "end_time": "20:00",
                    "price": 8
                }
            ]
        }
    }

    # Dummy user/trip info
    user_id = "dummyuserid1234567890123456"  # Use a valid ObjectId string if your DB enforces it
    location = "San Francisco"
    start_date = "2024-06-01"
    end_date = "2024-06-02"
    trip_name = "Test Gemini Trip"

    # Run the process
    result = process_gemini_itinerary_to_database(
        itinerary_json=itinerary_json,
        user_id=user_id,
        location=location,
        start_date=start_date,
        end_date=end_date,
        trip_name=trip_name,
        use_api=True,  # Set to False if you want to test direct DB access and have the helpers
        base_url="http://localhost:8000/api"
    )

    print("\n=== Test Result ===")
    print(result)

if __name__ == "__main__":
    main() 