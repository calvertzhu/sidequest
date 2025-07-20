import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def build_category_parsing_prompt(user_input):
    """
    Build a prompt for Gemini to parse user input into structured categories.
    
    Args:
        user_input: String input from user describing desired activities
    """
    
    return f"""
You are an activity category parser for a travel planning system. Parse the user's input and return structured categories for two APIs:

1. Google Places API - for restaurants, attractions, museums, parks, etc.
2. Ticketmaster API - for live events, concerts, sports, etc.

User Input: "{user_input}"

Return ONLY valid JSON in this exact format:
{{
  "google_places_categories": [
    "category1",
    "category2"
  ],
  "ticketmaster_categories": [
    "category1", 
    "category2"
  ],
  "explanation": "Brief explanation of why these categories were chosen"
}}

Google Places Categories (choose from):
- restaurant, cafe, bar, museum, art_gallery, park, aquarium, zoo, amusement_park, 
- shopping_mall, movie_theater, theater, library, tourist_attraction, landmark,
- night_club, gym, spa, yoga, hiking, beach, mountain, lake, river

Ticketmaster Categories (choose from):
- music, sports, arts, film, comedy, family, theater, opera, dance, 
- festival, conference, workshop, lecture, exhibition

Rules:
1. Choose 2-5 categories for each API
2. Focus on the most relevant categories based on user input
3. If user mentions food/dining, include "restaurant"
4. If user mentions entertainment/nightlife, include relevant categories
5. If user mentions outdoor activities, include parks/nature categories
6. If user mentions culture/arts, include museum/art categories
7. If user mentions sports, include sports category
8. If user mentions music, include music category

Only return valid JSON. No markdown, no commentary.
"""

def parse_activities_with_gemini(user_input):
    """
    Use Gemini to parse user input into structured activity categories.
    
    Args:
        user_input: String describing desired activities
        
    Returns:
        dict: Parsed categories for Google Places and Ticketmaster APIs
    """
    try:
        # Build the prompt
        prompt = build_category_parsing_prompt(user_input)
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Clean the response text to handle markdown code blocks
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        
        response_text = response_text.strip()
        
        # Parse the JSON
        parsed_categories = json.loads(response_text)
        
        return parsed_categories
        
    except Exception as e:
        # Fallback to default categories if Gemini fails
        print(f"Gemini parsing failed: {e}. Using fallback categories.")
        return {
            "google_places_categories": ["restaurant", "tourist_attraction"],
            "ticketmaster_categories": ["music"],
            "explanation": "Fallback categories due to parsing error"
        }

def get_fallback_categories(user_input):
    """
    Fallback function to provide basic category mapping without Gemini.
    
    Args:
        user_input: String describing desired activities
        
    Returns:
        dict: Basic category mapping
    """
    user_input_lower = user_input.lower()
    
    google_categories = []
    ticketmaster_categories = []
    
    # Food-related keywords
    if any(word in user_input_lower for word in ['food', 'eat', 'dining', 'restaurant', 'cafe', 'bar']):
        google_categories.append('restaurant')
    
    # Culture/arts keywords
    if any(word in user_input_lower for word in ['art', 'museum', 'culture', 'gallery', 'exhibit']):
        google_categories.append('museum')
        google_categories.append('art_gallery')
    
    # Outdoor/nature keywords
    if any(word in user_input_lower for word in ['park', 'outdoor', 'nature', 'hiking', 'beach']):
        google_categories.append('park')
    
    # Entertainment keywords
    if any(word in user_input_lower for word in ['music', 'concert', 'live', 'band']):
        ticketmaster_categories.append('music')
    
    # Sports keywords
    if any(word in user_input_lower for word in ['sports', 'game', 'match', 'athletic']):
        ticketmaster_categories.append('sports')
    
    # Default categories if none found
    if not google_categories:
        google_categories = ['restaurant', 'tourist_attraction']
    if not ticketmaster_categories:
        ticketmaster_categories = ['music']
    
    return {
        "google_places_categories": google_categories,
        "ticketmaster_categories": ticketmaster_categories,
        "explanation": "Fallback categories based on keyword matching"
    }

def parse_activities_smart(user_input, use_gemini=True):
    """
    Smart activity parsing that tries Gemini first, falls back to keyword matching.
    
    Args:
        user_input: String describing desired activities
        use_gemini: Whether to try Gemini first (default: True)
        
    Returns:
        dict: Parsed categories for both APIs
    """
    if use_gemini and os.getenv("GEMINI_API_KEY"):
        try:
            return parse_activities_with_gemini(user_input)
        except Exception as e:
            print(f"Gemini parsing failed, using fallback: {e}")
            return get_fallback_categories(user_input)
    else:
        return get_fallback_categories(user_input)