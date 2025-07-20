from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from .gemini.gemini import generate_itinerary_json

load_dotenv()

itinerary_bp = Blueprint('itinerary', __name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

def get_user_from_db(user_id):
    """Fetch user data from MongoDB database."""
    db = current_app.config["DB"]
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        
        # Convert ObjectId to string and format birthday
        user["_id"] = str(user["_id"])
        if "birthday" in user and isinstance(user["birthday"], datetime):
            user["birthday"] = user["birthday"].strftime("%Y-%m-%d")
            # Calculate age from birthday
            try:
                birth_date = datetime.strptime(user["birthday"], "%Y-%m-%d")
                today = datetime.now()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                user["age"] = age
            except:
                user["age"] = "Unknown"
        
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def get_activities_for_location(city, start_date_str, end_date_str, categories=None):
    """Fetch activities from Google Places and Ticketmaster APIs."""
    if categories is None:
        categories = ["restaurant", "museum", "park", "shopping"]
    
    results = []
    
    # Google Places search
    for category in categories:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{category} in {city}",
            "key": GOOGLE_API_KEY
        }
        try:
            res = requests.get(url, params=params).json()
            for place in res.get("results", []):
                results.append({
                    "name": place.get("name"),
                    "tags": [category],
                    "location": city,
                    "address": place.get("formatted_address")
                })
        except Exception as e:
            print(f"Error fetching Google Places data: {e}")
    
    # Ticketmaster events search
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        start_datetime = start_date.isoformat() + "Z"
        end_datetime = end_date.isoformat() + "Z"
        
        # Build category filter
        segment_ids = {
            "music": "KZFzniwnSyZfZ7v7nJ",
            "sports": "KZFzniwnSyZfZ7v7nE",
            "arts": "KZFzniwnSyZfZ7v7na",
            "film": "KZFzniwnSyZfZ7v7nn",
            "misc": "KZFzniwnSyZfZ7v7n1"
        }
        
        classification_filter = ','.join([segment_ids.get(cat.lower(), '') for cat in categories if cat.lower() in segment_ids])
        
        params = {
            "apikey": TICKETMASTER_API_KEY,
            "city": city,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "size": 20,
            "sort": "date,asc"
        }
        
        if classification_filter:
            params["segmentId"] = classification_filter
        
        response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("_embedded", {}).get("events", [])
            
            for e in events:
                results.append({
                    "name": e.get("name"),
                    "tags": ["event"],
                    "start_date": e.get("dates", {}).get("start", {}).get("localDate"),
                    "start_time": e.get("dates", {}).get("start", {}).get("localTime"),
                    "address": e.get("_embedded", {}).get("venues", [{}])[0].get("name"),
                    "location": e.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name")
                })
    except Exception as e:
        print(f"Error fetching Ticketmaster data: {e}")
    
    # Return in the same format as activity routes
    return {
        "location": city,
        "date_range": [start_date_str, end_date_str],
        "activities": results
    }

@itinerary_bp.route('/generate-itinerary', methods=['POST'])
def generate_personalized_itinerary():
    """Generate a personalized itinerary using user data from database and activities."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'location', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: user_id, location, start_date, end_date'}), 400
    
    user_id = data['user_id']
    location = data['location']
    start_date = data['start_date']
    end_date = data['end_date']
    categories = data.get('categories', [])
    budget = data.get('budget', 'medium')
    
    try:
        # 1. Fetch user data from database
        user = get_user_from_db(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 2. Get user interests
        user_interests = user.get('interests', [])
        if not user_interests:
            return jsonify({'error': 'User has no interests defined'}), 400
        
        # 3. Fetch activities for the location and date range using activity routes
        activities_response = get_activities_for_location(location, start_date, end_date, categories)
        
        if not activities_response.get('activities'):
            return jsonify({'error': 'No activities found for the specified location and dates'}), 404
        
        # 4. Generate itinerary using Gemini with user information and complete activity response
        itinerary = generate_itinerary_json(location, user_interests, activities_response, user, budget, start_date, end_date)
        
        # 5. Return the complete response
        response = {
            'success': True,
            'user_info': {
                'name': user.get('name'),
                'age': user.get('age'),
                'gender': user.get('gender'),
                'interests': user_interests,
                'dietary_restrictions': user.get('dietary_restrictions', ''),
                'location': user.get('location', '')
            },
            'trip_info': {
                'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'budget': budget
            },
            'available_activities': len(activities_response.get('activities', [])),
            'itinerary': itinerary
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate itinerary: {str(e)}'
        }), 500

@itinerary_bp.route('/generate-itinerary/quick', methods=['POST'])
def generate_quick_itinerary():
    """Generate a quick itinerary without requiring user to be in database."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['interests', 'location', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: interests, location, start_date, end_date'}), 400
    
    interests = data['interests']
    location = data['location']
    start_date = data['start_date']
    end_date = data['end_date']
    categories = data.get('categories', [])
    budget = data.get('budget', 'medium')
    
    try:
        # Fetch activities for the location and date range using activity routes
        activities_response = get_activities_for_location(location, start_date, end_date, categories)
        
        if not activities_response.get('activities'):
            return jsonify({'error': 'No activities found for the specified location and dates'}), 404
        
        # Generate itinerary using Gemini with complete activity response
        itinerary = generate_itinerary_json(location, interests, activities_response, None, budget, start_date, end_date)
        
        # Return the response
        response = {
            'success': True,
            'trip_info': {
                'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'budget': budget,
                'interests': interests
            },
            'available_activities': len(activities_response.get('activities', [])),
            'itinerary': itinerary
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate itinerary: {str(e)}'
        }), 500

@itinerary_bp.route('/itinerary/health', methods=['GET'])
def itinerary_health():
    """Health check endpoint for the itinerary service."""
    return jsonify({
        'status': 'healthy',
        'service': 'personalized_itinerary_generator',
        'version': '1.0.0',
        'features': [
            'database_integration',
            'activity_fetching',
            'gemini_ai_integration',
            'personalized_recommendations',
            'user_profile_integration'
        ]
    }), 200 