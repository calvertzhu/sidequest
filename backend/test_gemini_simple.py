#!/usr/bin/env python3
"""
Simple test script for Gemini functionality without external API dependencies.
This tests the core Gemini integration with mock data.
"""

import os
import json
from dotenv import load_dotenv
import sys
sys.path.append('.')

# Import the Gemini functions
from routes.gemini.gemini import generate_itinerary_json, build_gemini_prompt

load_dotenv()

def test_gemini_with_mock_data():
    """Test Gemini with mock user and activity data."""
    
    print("🧠 Testing Gemini AI Integration")
    print("=" * 50)
    
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in .env file")
        print("Please set your Gemini API key in the .env file")
        return
    
    # Mock user data (simulating database user)
    mock_user = {
        "name": "Alex Johnson",
        "age": 29,
        "gender": "non-binary",
        "interests": ["art", "food", "music", "outdoor activities"],
        "dietary_restrictions": "vegetarian",
        "location": "San Francisco, CA"
    }
    
    # Mock activity data (simulating API response)
    mock_activities_response = {
        "location": "New York",
        "date_range": ["2024-06-01", "2024-06-03"],
        "activities": [
            {
                "name": "MoMA - Museum of Modern Art",
                "tags": ["museum", "art"],
                "address": "11 W 53rd St, New York, NY 10019"
            },
            {
                "name": "Central Park",
                "tags": ["park", "outdoor"],
                "address": "Central Park, New York, NY"
            },
            {
                "name": "Gramercy Tavern",
                "tags": ["restaurant", "food"],
                "address": "42 E 20th St, New York, NY 10003"
            },
            {
                "name": "Blue Note Jazz Club",
                "tags": ["music", "nightlife"],
                "address": "131 W 3rd St, New York, NY 10012"
            },
            {
                "name": "High Line Park",
                "tags": ["park", "outdoor"],
                "address": "High Line, New York, NY"
            },
            {
                "name": "Chelsea Market",
                "tags": ["food", "shopping"],
                "address": "75 9th Ave, New York, NY 10011"
            }
        ]
    }
    
    # Test parameters
    location = "New York"
    interests = mock_user["interests"]
    budget = "medium"
    start_date = "2024-06-01"
    end_date = "2024-06-03"
    
    print(f"📍 Location: {location}")
    print(f"👤 User: {mock_user['name']} (Age: {mock_user['age']})")
    print(f"🎯 Interests: {', '.join(interests)}")
    print(f"🥗 Dietary Restrictions: {mock_user['dietary_restrictions']}")
    print(f"💰 Budget: {budget}")
    print(f"📅 Dates: {start_date} to {end_date}")
    print(f"🎪 Available Activities: {len(mock_activities_response['activities'])}")
    
    print("\n📋 Available Activities:")
    for i, activity in enumerate(mock_activities_response['activities'], 1):
        print(f"   {i}. {activity['name']} ({', '.join(activity['tags'])})")
    
    print("\n🚀 Generating itinerary with Gemini...")
    
    try:
        # Generate itinerary using Gemini
        itinerary = generate_itinerary_json(
            location=location,
            interests=interests,
            activities_response=mock_activities_response,
            user_info=mock_user,
            budget=budget,
            start_date=start_date,
            end_date=end_date
        )
        
        print("✅ Gemini itinerary generated successfully!")
        
        # Display the generated itinerary
        print("\n📅 Generated Itinerary:")
        print("=" * 50)
        
        for day_key, day_data in itinerary.items():
            print(f"\n{day_key.replace('_', ' ').title()}:")
            print("-" * 30)
            
            for time_slot, activities in day_data.items():
                print(f"\n{time_slot.title()}:")
                for i, activity in enumerate(activities, 1):
                    print(f"  {i}. {activity.get('name', 'Unknown Activity')}")
                    print(f"     📍 {activity.get('location', 'No location')}")
                    print(f"     ⏰ {activity.get('start_time', 'TBD')} - {activity.get('end_time', 'TBD')}")
                    print(f"     📝 {activity.get('description', 'No description')}")
                    print()
        
        # Save to file
        result = {
            "success": True,
            "user_info": mock_user,
            "trip_info": {
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "budget": budget
            },
            "available_activities": len(mock_activities_response['activities']),
            "itinerary": itinerary
        }
        
        with open('gemini_test_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print("💾 Full result saved to 'gemini_test_result.json'")
        
    except Exception as e:
        print(f"❌ Error generating itinerary: {e}")
        print("\nThis could be due to:")
        print("- Invalid Gemini API key")
        print("- Network connectivity issues")
        print("- Gemini API rate limits")
        print("- Malformed prompt or response")

def test_gemini_prompt_building():
    """Test the prompt building function without making API calls."""
    
    print("\n🔧 Testing Gemini Prompt Building")
    print("=" * 40)
    
    # Mock data
    mock_user = {
        "name": "Test User",
        "age": 25,
        "gender": "female",
        "interests": ["art", "food"],
        "dietary_restrictions": "vegan"
    }
    
    mock_activities = {
        "location": "San Francisco",
        "date_range": ["2024-06-01", "2024-06-03"],
        "activities": [
            {"name": "Test Museum", "tags": ["museum"], "address": "123 Test St"}
        ]
    }
    
    try:
        prompt = build_gemini_prompt(
            location="San Francisco",
            interests=["art", "food"],
            activities_response=mock_activities,
            user_info=mock_user,
            budget="medium",
            start_date="2024-06-01",
            end_date="2024-06-03"
        )
        
        print("✅ Prompt built successfully!")
        print(f"📏 Prompt length: {len(prompt)} characters")
        
        # Show a preview of the prompt
        print("\n📝 Prompt Preview (first 500 chars):")
        print("-" * 40)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        
        # Save prompt to file
        with open('gemini_prompt_example.txt', 'w') as f:
            f.write(prompt)
        
        print("\n💾 Full prompt saved to 'gemini_prompt_example.txt'")
        
    except Exception as e:
        print(f"❌ Error building prompt: {e}")

if __name__ == "__main__":
    print("🧪 Simple Gemini Test")
    print("This test uses mock data to avoid external API dependencies")
    print()
    
    # Test prompt building first
    test_gemini_prompt_building()
    
    # Test full Gemini integration
    test_gemini_with_mock_data() 