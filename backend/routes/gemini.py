import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def build_gemini_prompt(location, interests, activities):
    formatted = "\n".join([
        f"- {a['name']} ({', '.join(a.get('tags', []))}): {a.get('address', a.get('url', ''))}"
        for a in activities[:20]
    ])
    return f"""
You're a helpful travel assistant. Create a 2-day itinerary in {location} for a solo traveler who enjoys: {", ".join(interests)}.

Here are recommended places and events:
{formatted}

Return the itinerary in **JSON format** like:
{{
  "day_1": {{
    "morning": ["activity 1", "activity 2"],
    "afternoon": ["..."],
    "evening": ["..."]
  }},
  "day_2": {{
    "morning": ["..."],
    "afternoon": ["..."],
    "evening": ["..."]
  }}
}}

Only return the JSON. No extra commentary.
"""

def generate_itinerary_json(location, interests, activities):
    try:
        prompt = build_gemini_prompt(location, interests, activities)
        response = model.generate_content(prompt)
        itinerary_json = json.loads(response.text)
        return itinerary_json
    except Exception as e:
        raise RuntimeError(f"Gemini failed: {str(e)}")
