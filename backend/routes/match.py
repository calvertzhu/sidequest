import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def build_match_prompt(user1, user2):
    """Build a prompt for Gemini to analyze travel compatibility between two users."""
    
    # Format user profiles for the prompt
    user1_profile = f"""
    User 1 Profile:
    - Name: {user1.get('name', 'Unknown')}
    - Interests: {', '.join(user1.get('interests', []))}
    - Location: {user1.get('location', 'Unknown')}
    - Travel Dates: {user1.get('travel_dates', 'Unknown')}
    """
    
    user2_profile = f"""
    User 2 Profile:
    - Name: {user2.get('name', 'Unknown')}
    - Interests: {', '.join(user2.get('interests', []))}
    - Location: {user2.get('location', 'Unknown')}
    - Travel Dates: {user2.get('travel_dates', 'Unknown')}
    """
    
    return f"""
You are a travel compatibility expert. Analyze how well these two travelers would match as travel companions.

{user1_profile}

{user2_profile}

Consider the following factors:
1. **Interest Compatibility**: How well do their interests align?
2. **Travel Style Compatibility**: Based on their interests, what travel style would each prefer?
3. **Schedule Compatibility**: Do their travel dates overlap?
4. **Location Compatibility**: Are they traveling to the same or nearby locations?
5. **Overall Match Score**: Rate their compatibility from 0-100

Return your analysis in **JSON format** like this:
{{
  "interest_compatibility": {{
    "score": 85,
    "explanation": "Both users enjoy outdoor activities and cultural experiences"
  }},
  "travel_style_compatibility": {{
    "score": 90,
    "explanation": "Both prefer active, adventure-based travel"
  }},
  "schedule_compatibility": {{
    "score": 100,
    "explanation": "Travel dates perfectly overlap"
  }},
  "location_compatibility": {{
    "score": 95,
    "explanation": "Both traveling to the same destination"
  }},
  "overall_match_score": 92,
  "recommendation": "Excellent match! These travelers would make great companions.",
  "potential_activities": ["hiking", "museum visits", "local food tours"],
  "potential_conflicts": ["Different budget preferences", "Pace differences"]
}}

Only return the JSON. No extra commentary.
"""

def fallback_match_analysis(user1, user2):
    """Fallback matching algorithm when Gemini API is unavailable."""
    
    # Interest compatibility scoring
    interests1 = set(user1.get('interests', []))
    interests2 = set(user2.get('interests', []))
    
    if interests1 and interests2:
        common_interests = interests1.intersection(interests2)
        interest_score = min(100, len(common_interests) * 25)
    else:
        interest_score = 0
    
    # Location compatibility
    location1 = user1.get('location', '').lower()
    location2 = user2.get('location', '').lower()
    
    if location1 == location2:
        location_score = 100
    elif location1 in location2 or location2 in location1:
        location_score = 80
    else:
        location_score = 20
    
    # Schedule compatibility (simple date overlap check)
    dates1 = user1.get('travel_dates', '')
    dates2 = user2.get('travel_dates', '')
    
    # Extract dates using regex
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates1_list = re.findall(date_pattern, dates1)
    dates2_list = re.findall(date_pattern, dates2)
    
    if dates1_list and dates2_list:
        try:
            start1 = datetime.strptime(dates1_list[0], '%Y-%m-%d')
            end1 = datetime.strptime(dates1_list[-1], '%Y-%m-%d')
            start2 = datetime.strptime(dates2_list[0], '%Y-%m-%d')
            end2 = datetime.strptime(dates2_list[-1], '%Y-%m-%d')
            
            # Check for overlap
            if (start1 <= end2 and start2 <= end1):
                schedule_score = 100
            else:
                schedule_score = 0
        except:
            schedule_score = 50  # Default if date parsing fails
    else:
        schedule_score = 50
    
    # Travel style compatibility (based on interest categories)
    outdoor_keywords = ['hiking', 'camping', 'adventure', 'sports', 'climbing', 'biking']
    cultural_keywords = ['museums', 'art', 'history', 'culture', 'architecture']
    food_keywords = ['cuisine', 'food', 'restaurants', 'cooking', 'wine']
    relaxation_keywords = ['spa', 'beach', 'yoga', 'meditation', 'wellness']
    
    def categorize_interests(interests):
        categories = {'outdoor': 0, 'cultural': 0, 'food': 0, 'relaxation': 0}
        for interest in interests:
            interest_lower = interest.lower()
            if any(keyword in interest_lower for keyword in outdoor_keywords):
                categories['outdoor'] += 1
            if any(keyword in interest_lower for keyword in cultural_keywords):
                categories['cultural'] += 1
            if any(keyword in interest_lower for keyword in food_keywords):
                categories['food'] += 1
            if any(keyword in interest_lower for keyword in relaxation_keywords):
                categories['relaxation'] += 1
        return categories
    
    style1 = categorize_interests(interests1)
    style2 = categorize_interests(interests2)
    
    # Calculate style similarity
    style_score = 0
    for category in style1:
        diff = abs(style1[category] - style2[category])
        if diff == 0:
            style_score += 25
        elif diff == 1:
            style_score += 15
        elif diff == 2:
            style_score += 5
    
    # Overall score calculation
    overall_score = (interest_score * 0.3 + location_score * 0.25 + 
                    schedule_score * 0.25 + style_score * 0.2)
    
    # Generate recommendations
    if overall_score >= 80:
        recommendation = "Excellent match! These travelers would make great companions."
    elif overall_score >= 60:
        recommendation = "Good match! They have compatible interests and schedules."
    elif overall_score >= 40:
        recommendation = "Fair match. Some compatibility but may have different preferences."
    else:
        recommendation = "Poor match. Limited compatibility in interests or schedules."
    
    # Generate potential activities
    potential_activities = list(common_interests)[:3] if common_interests else ["exploring local attractions"]
    
    # Generate potential conflicts
    conflicts = []
    if location_score < 50:
        conflicts.append("Different travel destinations")
    if schedule_score < 50:
        conflicts.append("Non-overlapping travel dates")
    if len(conflicts) == 0:
        conflicts.append("Different travel pace preferences")
    
    return {
        "interest_compatibility": {
            "score": int(interest_score),
            "explanation": f"Found {len(common_interests)} common interests: {', '.join(common_interests) if common_interests else 'None'}"
        },
        "travel_style_compatibility": {
            "score": int(style_score),
            "explanation": f"Style compatibility based on interest categories"
        },
        "schedule_compatibility": {
            "score": int(schedule_score),
            "explanation": f"Travel date overlap analysis"
        },
        "location_compatibility": {
            "score": int(location_score),
            "explanation": f"Destination compatibility: {location1} vs {location2}"
        },
        "overall_match_score": int(overall_score),
        "recommendation": recommendation,
        "potential_activities": potential_activities,
        "potential_conflicts": conflicts,
        "analysis_method": "fallback_algorithm"
    }

def generate_match_analysis(user1, user2):
    """Generate a compatibility analysis between two user profiles using Gemini."""
    try:
        prompt = build_match_prompt(user1, user2)
        response = model.generate_content(prompt)
        match_analysis = json.loads(response.text)
        match_analysis["analysis_method"] = "gemini_ai"
        return match_analysis
    except Exception as e:
        print(f"Gemini API failed: {str(e)}. Using fallback algorithm...")
        return fallback_match_analysis(user1, user2)

def get_match_summary(match_analysis):
    """Extract a simple summary from the match analysis."""
    overall_score = match_analysis.get('overall_match_score', 0)
    recommendation = match_analysis.get('recommendation', 'No recommendation available.')
    
    if overall_score >= 80:
        match_level = "Excellent Match"
    elif overall_score >= 60:
        match_level = "Good Match"
    elif overall_score >= 40:
        match_level = "Fair Match"
    else:
        match_level = "Poor Match"
    
    return {
        "match_level": match_level,
        "overall_score": overall_score,
        "recommendation": recommendation,
        "analysis_method": match_analysis.get("analysis_method", "unknown")
    } 