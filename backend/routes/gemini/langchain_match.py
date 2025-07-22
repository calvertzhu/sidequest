import os
from typing import List, Dict, Any
from datetime import datetime
import re
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

# Initialize LangChain with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_tokens=2048
)

# Pydantic models for structured output
class CompatibilityScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Compatibility score from 0-100")
    explanation: str = Field(..., description="Detailed explanation of the compatibility score")

class MatchAnalysis(BaseModel):
    interest_compatibility: CompatibilityScore = Field(..., description="Interest alignment analysis")
    travel_style_compatibility: CompatibilityScore = Field(..., description="Travel style compatibility")
    schedule_compatibility: CompatibilityScore = Field(..., description="Travel date overlap analysis")
    location_compatibility: CompatibilityScore = Field(..., description="Destination compatibility")
    overall_match_score: int = Field(..., ge=0, le=100, description="Overall compatibility score")
    recommendation: str = Field(..., description="Overall recommendation for the match")
    potential_activities: List[str] = Field(..., description="Suggested activities for the pair")
    potential_conflicts: List[str] = Field(..., description="Potential areas of conflict")
    analysis_method: str = Field(default="langchain_gemini", description="Method used for analysis")

class UserProfile(BaseModel):
    name: str = Field(..., description="User's name")
    interests: List[str] = Field(..., description="List of user interests")
    location: str = Field(..., description="Travel destination")
    travel_dates: str = Field(..., description="Travel date range")

def create_match_prompt_template() -> ChatPromptTemplate:
    """Create a structured prompt template for travel compatibility analysis."""
    
    template = """You are an expert travel compatibility analyst. Your job is to analyze how well two travelers would match as travel companions.

User 1 Profile:
- Name: {user.get('user_id', 'Unknown')}
- Interests: {user.get('interests', [])}
- Location: {user.get('location', 'Unknown')}
- Travel Dates: {user.get('travel_dates', 'Unknown')}

User 2 Profile:
- Name: {user.get('matched_user_id', 'Unknown')}
- Interests: {user.get('interests', [])}
- Location: {user.get('location', 'Unknown')}
- Travel Dates: {user.get('travel_dates', 'Unknown')}

Analyze their compatibility based on:

1. **Interest Compatibility**: How well do their interests align? Consider shared interests, complementary interests, and potential conflicts.

2. **Travel Style Compatibility**: Based on their interests, what travel style would each prefer? Consider adventure vs. relaxation, budget vs. luxury, group vs. solo preferences.

3. **Schedule Compatibility**: Do their travel dates overlap? Consider exact matches, partial overlaps, and timing preferences.

4. **Location Compatibility**: Are they traveling to the same or nearby locations? Consider exact matches, nearby destinations, and travel logistics.

5. **Overall Assessment**: Provide a comprehensive recommendation and identify potential activities they could enjoy together and potential conflicts to be aware of.

{format_instructions}

Provide your analysis in the exact JSON format specified above. Be thorough but concise in your explanations."""

    return ChatPromptTemplate.from_template(template)

def fallback_match_analysis(user1: Dict[str, Any], user2: Dict[str, Any]) -> MatchAnalysis:
    """Fallback matching algorithm when LangChain/Gemini is unavailable."""
    
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
    
    # Schedule compatibility
    dates1 = user1.get('travel_dates', '')
    dates2 = user2.get('travel_dates', '')
    
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates1_list = re.findall(date_pattern, dates1)
    dates2_list = re.findall(date_pattern, dates2)
    
    if dates1_list and dates2_list:
        try:
            start1 = datetime.strptime(dates1_list[0], '%Y-%m-%d')
            end1 = datetime.strptime(dates1_list[-1], '%Y-%m-%d')
            start2 = datetime.strptime(dates2_list[0], '%Y-%m-%d')
            end2 = datetime.strptime(dates2_list[-1], '%Y-%m-%d')
            
            if (start1 <= end2 and start2 <= end1):
                schedule_score = 100
            else:
                schedule_score = 0
        except:
            schedule_score = 50
    else:
        schedule_score = 50
    
    # Travel style compatibility
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
    
    potential_activities = list(common_interests)[:3] if common_interests else ["exploring local attractions"]
    
    conflicts = []
    if location_score < 50:
        conflicts.append("Different travel destinations")
    if schedule_score < 50:
        conflicts.append("Non-overlapping travel dates")
    if len(conflicts) == 0:
        conflicts.append("Different travel pace preferences")
    
    return MatchAnalysis(
        interest_compatibility=CompatibilityScore(
            score=int(interest_score),
            explanation=f"Found {len(common_interests)} common interests: {', '.join(common_interests) if common_interests else 'None'}"
        ),
        travel_style_compatibility=CompatibilityScore(
            score=int(style_score),
            explanation="Style compatibility based on interest categories"
        ),
        schedule_compatibility=CompatibilityScore(
            score=int(schedule_score),
            explanation="Travel date overlap analysis"
        ),
        location_compatibility=CompatibilityScore(
            score=int(location_score),
            explanation=f"Destination compatibility: {location1} vs {location2}"
        ),
        overall_match_score=int(overall_score),
        recommendation=recommendation,
        potential_activities=potential_activities,
        potential_conflicts=conflicts,
        analysis_method="fallback_algorithm"
    )

def generate_langchain_match_analysis(user1: Dict[str, Any], user2: Dict[str, Any]) -> MatchAnalysis:
    """Generate compatibility analysis using LangChain and structured outputs."""
    
    try:
        # Create parser for structured output
        parser = PydanticOutputParser(pydantic_object=MatchAnalysis)
        
        # Create prompt template
        prompt_template = create_match_prompt_template()
        
        # Format the prompt with user data
        formatted_prompt = prompt_template.format_messages(
            user1_name=user1.get('name', 'Unknown'),
            user1_interests=', '.join(user1.get('interests', [])),
            user1_location=user1.get('location', 'Unknown'),
            user1_dates=user1.get('travel_dates', 'Unknown'),
            user2_name=user2.get('name', 'Unknown'),
            user2_interests=', '.join(user2.get('interests', [])),
            user2_location=user2.get('location', 'Unknown'),
            user2_dates=user2.get('travel_dates', 'Unknown'),
            format_instructions=parser.get_format_instructions()
        )
        
        # Generate response using LangChain
        response = llm.invoke(formatted_prompt)
        
        # Parse the structured output
        match_analysis = parser.parse(response.content)
        
        return match_analysis
        
    except Exception as e:
        print(f"LangChain analysis failed: {str(e)}. Using fallback algorithm...")
        return fallback_match_analysis(user1, user2)

def get_match_summary(match_analysis: MatchAnalysis, user_id: str = None, matched_user_id: str = None) -> Dict[str, Any]:
    """Extract user_id, match_user_id, and match score from the match analysis."""
    overall_score = match_analysis.overall_match_score
    return {
        "user_id": user_id,
        "matched_user_id": matched_user_id,
        "match_score": overall_score
    }  


def save_langchain_match_to_db(db, user1: dict, user2: dict, event_id: str):
    """Run LangChain match analysis and save match summary to DB."""
    try:
        # Run LangChain or fallback analysis
        match_analysis = generate_langchain_match_analysis(user1, user2)
        summary = get_match_summary(
            match_analysis,
            user_id=str(user1.get('_id')),
            matched_user_id=str(user2.get('_id'))
        )

        # Structure to upsert or append into existing match doc
        user_id = str(user1.get('_id'))
        match_entry = {
            "matched_user_id": summary["matched_user_id"],
            "match_score": summary["match_score"],
            "analysis": match_analysis.dict()
        }

        # Check if a match doc for this user + event already exists
        existing = db.matches.find_one({
            "user_id": user_id,
            "event_id": event_id
        })

        if existing:
            # Update: append to matches array
            db.matches.update_one(
                {"_id": existing["_id"]},
                {"$addToSet": {"matches": match_entry}}  # prevent duplicates
            )
            print(f"Match updated for user {user_id} in event {event_id}")
        else:
            # Create new match doc
            match_doc = {
                "user_id": ObjectId(user_id),
                "event_id": ObjectId(event_id),
                "matches": [match_entry]
            }
            db.matches.insert_one(match_doc)
            print(f"Match document created for user {user_id} in event {event_id}")

    except Exception as e:
        print("Error saving match:", str(e))


