import os
import requests
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

activities_bp = Blueprint("activities", __name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")


@activities_bp.route("/activities/search", methods=["POST"])
def search_activities():
    data = request.get_json()
    db = current_app.config["DB"]

    city = data.get("location")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    categories = data.get("categories", [])

    if not city or not start_date or not end_date:
        return jsonify({"error": "Missing required fields"}), 400

    results = []

    # Google Places search per category
    for category in categories:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{category} in {city}",
            "key": GOOGLE_API_KEY
        }
        response = requests.get(url, params=params).json()
        for place in response.get("results", []):
            results.append({
                "name": place.get("name"),
                "type": "place",
                "tags": [category],
                "location": city,
                "source": "Google",
                "address": place.get("formatted_address")
            })

    # Eventbrite search
    eb_url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    eb_params = {
        "location.address": city,
        "start_date.range_start": f"{start_date}T00:00:00",
        "start_date.range_end": f"{end_date}T23:59:59"
    }

    eb_response = requests.get(eb_url, headers=headers, params=eb_params).json()
    for event in eb_response.get("events", []):
        results.append({
            "name": event.get("name", {}).get("text"),
            "type": "event",
            "tags": ["event"],
            "location": city,
            "source": "Eventbrite",
            "start": event.get("start", {}).get("local"),
            "url": event.get("url")
        })

    return jsonify(results), 200
