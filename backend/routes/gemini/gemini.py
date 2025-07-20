import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def build_gemini_prompt(location, interests, activities_response, user_info=None, budget="medium", start_date=None, end_date=None):
    """
    Build Gemini prompt using the complete activity routes response.
    
    Args:
        location: Destination city
        interests: User interests list
        activities_response: Full response from activity routes (includes activities, location, date_range)
        user_info: User profile from database
        budget: Budget level
        start_date: Trip start date
        end_date: Trip end date
    """
    

    # Extract activities from the response

    print("using Gemini to generate itinerary")
    
    activities = activities_response.get('activities', [])
    
    # Format activities for the prompt
    formatted_activities = "\n".join([
        f"- {a['name']} ({', '.join(a.get('tags', []))}): {a.get('address', a.get('url', ''))}"
        for a in activities[:20]
    ])
    
    # Build user context from database info
    user_context = ""
    if user_info:
        user_context = f"""
Traveler Profile: 
- Name: {user_info.get('name', 'Unknown')}
- Age: {user_info.get('age', 'Not specified')}
- Gender: {user_info.get('gender', 'Not specified')}
- Dietary Restrictions: {user_info.get('dietary_restrictions', 'None')}
- Home Location: {user_info.get('location', 'Not specified')}
- Travel Style: Based on interests in {', '.join(interests)}

Please consider the traveler's dietary restrictions when suggesting restaurants and food-related activities.
"""
    
    # Build trip context from activity response
    trip_context = f"""
Trip Information:
- Destination: {activities_response.get('location', location)}
- Date Range: {activities_response.get('date_range', [start_date, end_date])}
- Available Activities: {len(activities)} activities found
- Activity Categories: {', '.join(set([tag for activity in activities for tag in activity.get('tags', [])]))}
"""
    
    return f"""
You're a helpful travel assistant. Create a personalized 2-day itinerary in {location} for a traveler with a budget of {budget}.

{user_context}

{trip_context}

Traveler Interests: {", ".join(interests)}

Available Places and Events:
{formatted_activities}

Instructions:
1. Use the available activities above to create a realistic itinerary
2. Consider the traveler's interests and dietary restrictions
3. Mix different types of activities (cultural, food, entertainment, outdoor)
4. Ensure activities are geographically logical (group nearby locations)
5. Include appropriate timing for each activity and leave 1 hour between activities for travel time

Return the itinerary in **JSON format**. Each activity must include:
- name
- description (1–2 sentences)
- location
- start_time (e.g. "09:00")
- end_time (e.g. "11:00")

The format **must** be:
[
  {{
    "name": "activity name",
    "description": "short description",
    "location": "address or venue",
    "start_time": "HH:MM",
    "end_time": "HH:MM"
  }},
  ...
]

Only return valid JSON. No commentary or markdown.
"""


def generate_itinerary_json(location, interests, activities_response, user_info=None, budget="medium", start_date=None, end_date=None):
    """
    Generate itinerary using Gemini with complete activity routes response.
    
    Args:
        location: Destination city
        interests: User interests list
        activities_response: Full response from activity routes
        user_info: User profile from database
        budget: Budget level
        start_date: Trip start date
        end_date: Trip end date
    """
    try:
        prompt = build_gemini_prompt(location, interests, activities_response, user_info, budget, start_date, end_date)
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
        itinerary_json = json.loads(response_text)
        return itinerary_json
    except Exception as e:
        raise RuntimeError(f"Gemini failed: {str(e)}")



