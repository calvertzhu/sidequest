#!/usr/bin/env python3
"""
Test script demonstrating the complete flow:
String input -> Gemini parsing -> Activity search -> Itinerary generation
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_complete_flow():
    """Test the complete flow from string input to itinerary generation."""
    
    print("🔄 Testing Complete Flow: String → Parsing → Activities → Itinerary")
    print("=" * 70)
    
    # Step 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "name": "Gemini Parsing Test User",
        "email": f"parsing.test.{int(datetime.now().timestamp())}@example.com",
        "birthday": "1988-12-10",
        "gender": "male",
        "interests": ["food", "art", "music", "outdoor activities"],
        "dietary_restrictions": "none",
        "location": "Austin, TX",
        "profile_pic": "https://example.com/parsing-test.jpg"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        if response.status_code == 201:
            user_id = response.json()["_id"]
            print(f"✅ User created successfully with ID: {user_id}")
        else:
            print(f"❌ Failed to create user: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return
    
    # Step 2: Test activity search with string input (Gemini parsing)
    print("\n2. Testing activity search with Gemini parsing...")
    natural_language_input = "I want to explore art museums, try local restaurants, and maybe catch some live music"
    
    activity_data = {
        "location": "San Francisco",
        "start_date": "2024-06-20",
        "end_date": "2024-06-22",
        "categories": natural_language_input,  # String input for Gemini parsing
        "budget": "medium",
        "trip_name": "SF Art & Food Adventure"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
        if response.status_code == 200:
            activities_response = response.json()
            parsing_info = activities_response.get("parsing_info", {})
            
            print("✅ Activity search with Gemini parsing successful!")
            print(f"   Original Input: '{parsing_info.get('original_input', '')}'")
            print(f"   Google Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Ticketmaster Categories: {parsing_info.get('ticketmaster_categories', [])}")
            print(f"   Explanation: {parsing_info.get('explanation', '')}")
            print(f"   Activities Found: {len(activities_response.get('activities', []))}")
            
            # Show sample activities
            activities = activities_response.get('activities', [])
            if activities:
                print("\n📋 Sample Activities Found:")
                for i, activity in enumerate(activities[:3]):
                    print(f"   {i+1}. {activity.get('name', 'Unknown')}")
                    print(f"      Tags: {', '.join(activity.get('tags', []))}")
                    print(f"      Address: {activity.get('address', 'No address')}")
                    print()
            
        else:
            print(f"❌ Failed to fetch activities: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
        return
    
    # Step 3: Generate itinerary using the parsed activities
    print("\n3. Generating itinerary with parsed activities...")
    itinerary_data = {
        "user_id": user_id,
        "location": "San Francisco",
        "start_date": "2024-06-20",
        "end_date": "2024-06-22",
        "categories": natural_language_input,  # Use the same string input
        "budget": "medium"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-itinerary", json=itinerary_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Itinerary generated successfully!")
            print(f"   User: {result['user_info']['name']} (Age: {result['user_info']['age']})")
            print(f"   Trip Location: {result['trip_info']['location']}")
            print(f"   Available Activities: {result['available_activities']}")
            
            # Display itinerary structure
            itinerary = result['itinerary']
            print("\n📅 Generated Itinerary Structure:")
            for day_key, day_data in itinerary.items():
                print(f"   {day_key.replace('_', ' ').title()}:")
                for time_slot, activities in day_data.items():
                    print(f"     {time_slot.title()}: {len(activities)} activities")
                    # Show first activity as example
                    if activities:
                        first_activity = activities[0]
                        print(f"       Example: {first_activity.get('name', 'Unknown')} at {first_activity.get('start_time', 'TBD')}")
            
            # Save the complete result
            with open('complete_flow_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n💾 Complete flow result saved to 'complete_flow_result.json'")
            
        else:
            print(f"❌ Failed to generate itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating itinerary: {e}")

def test_different_inputs():
    """Test different types of natural language inputs."""
    
    print("\n🧪 Testing Different Natural Language Inputs")
    print("=" * 50)
    
    test_inputs = [
        {
            "name": "Foodie Request",
            "input": "I'm a foodie and want to try the best restaurants in the city"
        },
        {
            "name": "Culture Seeker",
            "input": "I love visiting museums, art galleries, and cultural landmarks"
        },
        {
            "name": "Nightlife Enthusiast",
            "input": "I want to experience the nightlife, bars, and live music scene"
        },
        {
            "name": "Outdoor Lover",
            "input": "I enjoy hiking, parks, and outdoor activities"
        },
        {
            "name": "Mixed Interests",
            "input": "I want a mix of good food, some culture, and maybe a concert"
        }
    ]
    
    for test_case in test_inputs:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        
        activity_data = {
            "location": "Los Angeles",
            "start_date": "2024-07-10",
            "end_date": "2024-07-12",
            "categories": test_case["input"],
            "budget": "high"
        }
        
        try:
            response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
            if response.status_code == 200:
                result = response.json()
                parsing_info = result.get("parsing_info", {})
                print(f"✅ Success: {len(result.get('activities', []))} activities")
                print(f"   Google: {parsing_info.get('google_categories', [])}")
                print(f"   Ticketmaster: {parsing_info.get('ticketmaster_categories', [])}")
            else:
                print(f"❌ Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Complete Gemini Flow Test")
    print("Make sure the Flask backend is running on http://localhost:8000")
    print("Make sure GEMINI_API_KEY is set in .env file")
    print()
    
    # Test the complete flow
    test_complete_flow()
    
    # Test different inputs
    test_different_inputs() 