import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def build_gemini_prompt(location, interests, activities, budget="medium"):
    formatted = "\n".join([
        f"- {a['name']} ({', '.join(a.get('tags', []))}): {a.get('address', a.get('url', ''))}"
        for a in activities[:20]
    ])
    
    return f"""
You're a helpful travel assistant. Create a 2-day itinerary in {location} for a solo traveler who enjoys: {", ".join(interests)} with a budget of {budget}.

Here are recommended places and events:
{formatted}

Return the itinerary in **JSON format**. Each activity must include:
- name
- description (1–2 sentences)
- location
- start_time (e.g. "09:00")
- end_time (e.g. "11:00")

The format must be:

{{
  "day_1": {{
    "morning": [
      {{
        "name": "activity name",
        "description": "short description",
        "location": "address or venue",
        "start_time": "HH:MM",
        "end_time": "HH:MM"
      }},
      ...
    ],
    "afternoon": [ ... ],
    "evening": [ ... ]
  }},
  "day_2": {{
    ...
  }}
}}

Only return valid JSON. No commentary or markdown.
"""


def generate_itinerary_json(location, interests, activities):
    try:
        prompt = build_gemini_prompt(location, interests, activities)
        response = model.generate_content(prompt)
        itinerary_json = json.loads(response.text)
        return itinerary_json
    except Exception as e:
        raise RuntimeError(f"Gemini failed: {str(e)}")
