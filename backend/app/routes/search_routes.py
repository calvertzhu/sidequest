import os
from flask import Blueprint, request, jsonify
import requests

search_bp = Blueprint('search', __name__)

GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')

@search_bp.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    interests = request.args.get('interests')
    travel_dates = request.args.get('travel_dates')
    if not city or not interests or not travel_dates:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Google Places API
    places_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={interests}+in+{city}&key={GOOGLE_PLACES_API_KEY}'
    try:
        places_resp = requests.get(places_url)
        places_resp.raise_for_status()
        places_results = places_resp.json().get('results', [])
    except Exception as e:
        places_results = []

    # Eventbrite API
    eventbrite_url = f'https://www.eventbriteapi.com/v3/events/search/?location.address={city}&q={interests}&start_date.range_start={travel_dates}&token={EVENTBRITE_API_KEY}'
    try:
        eventbrite_resp = requests.get(eventbrite_url)
        eventbrite_resp.raise_for_status()
        eventbrite_results = eventbrite_resp.json().get('events', [])
    except Exception as e:
        eventbrite_results = []

    return jsonify({
        'attractions': places_results,
        'events': eventbrite_results
    }) 