import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def match_score(profile1, profile2):
    prompt = f"""
    You are a compatibility engine for travel partners.
    Given two user profiles, rate how good of a match they are on a scale of 0 to 100.
    Higher scores mean more compatible. Consider travel style, interests, and trip overlap.

    Profile 1: {profile1}
    Profile 2: {profile2}

    Only return a number.
    """

    try:
        response = model.generate_content(prompt)
        score_str = response.text.strip()
        return int(score_str.split()[0])  # in case Gemini adds anything extra
    except Exception as e:
        print(f"Error generating match score: {e}")
        return None