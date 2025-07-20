import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

activities_bp = Blueprint("activities", __name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")


@activities_bp.route("/activities/search", methods=["GET"])
def search_activities():
    data = request.get_json()
    user_email = data.get("user_email")
    city = data.get("location")
    start_date_str = data.get("start_date")
    end_date_str  = data.get("end_date")
    categories = data.get("categories", [])
    #this logic should be in front end to give a default budget or just say default is 150 per day
    # start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    # end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    # num_days = (end_date - start_date).days
    # default_budget = num_days * 150
    budget = data.get("budget")
    trip_name = data.get("trip_name")

    if not city or not start_date_str or not end_date_str:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    results = []

    # Google Places search
    for category in categories:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{category} in {city}",
            "key": GOOGLE_API_KEY
        }
        res = requests.get(url, params=params).json()
        for place in res.get("results", []):
            results.append({
                "name": place.get("name"),
                # "type": "place",
                "tags": [category],
                "location": city,
                # "source": "Google",
                "address": place.get("formatted_address")
            })

    start_datetime = start_date.isoformat() + "Z"
    end_datetime = end_date.isoformat() + "Z"

    # Build category (classification) filter
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

    if response.status_code != 200:
        return jsonify({"error": "Ticketmaster API error", "details": response.text}), 502

    data = response.json()
    events = data.get("_embedded", {}).get("events", [])

    for e in events:
        # Handle price
        price_info = e.get("priceRanges", [])
        if price_info and isinstance(price_info, list):
            price = {
                "min": price_info[0].get("min"),
                "max": price_info[0].get("max"),
                "currency": price_info[0].get("currency")
            }
        else:
            price = {}

        results.append({
            "name": e.get("name"),
            # "url": e.get("url"),
            "start_date": e.get("dates", {}).get("start", {}).get("localDate"),
            "start_time": e.get("dates", {}).get("start", {}).get("localTime"),
            "address": e.get("_embedded", {}).get("venues", [{}])[0].get("name"),
            "location": e.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
             "price": price
        })

    # # Eventbrite search
    # tm_url = "https://app.ticketmaster.com/discovery/v2/events"
    # headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    # eb_params = {
    #     "location.address": city,
    #     "start_date.range_start": f"{start_date}T00:00:00",
    #     "start_date.range_end": f"{end_date}T23:59:59",
    #     "expand": "venue",
    # }
    # #eb_res = requests.get(eb_url, headers=headers, params=eb_params).json()
    # eb_response = requests.get(eb_url, headers=headers, params=eb_params)
    # print("Status Code:", eb_response.status_code)
    # print("Raw Text:", eb_response.text)
    # eb_res = eb_response.json()
    # for e in eb_res.get("events", []):
    #     results.append({
    #         "name": e.get("name", {}).get("text"),
    #         "type": "event",
    #         "tags": ["event"],
    #         "location": city,
    #         "source": "Eventbrite",
    #         "start": e.get("start", {}).get("local"),
    #         "url": e.get("url")
    #     })

    # Final payload to be sent to Gemini or another API
    response = {
        "location": city,
        "date_range": [start_date_str, end_date_str],
        "activities": results,
        "budget": budget,
        "user_email": user_email
    }

    return jsonify(response), 200
