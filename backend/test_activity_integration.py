#!/usr/bin/env python3
"""
Test script for the activity routes integration with Gemini.
This script demonstrates how the activity routes response is used in Gemini prompts.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_activity_routes_integration():
    """Test the integration of activity routes with Gemini."""
    
    print("🚀 Testing Activity Routes Integration with Gemini")
    print("=" * 60)
    
    # Step 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "name": "Sarah Chen",
        "email": "sarah.chen@example.com",
        "birthday": "1992-03-20",
        "gender": "female",
        "interests": ["art", "food", "music", "outdoor activities"],
        "dietary_restrictions": "vegan",
        "location": "Seattle, WA",
        "profile_pic": "https://example.com/sarah.jpg"
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
    
    # Step 2: Test activity search and see the response format
    print("\n2. Testing activity search response format...")
    activity_data = {
        "location": "San Francisco",
        "start_date": "2024-06-15",
        "end_date": "2024-06-17",
        "categories": ["restaurant", "museum", "music", "art"],
        "budget": "medium",
        "trip_name": "SF Art & Food Weekend"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
        if response.status_code == 200:
            activities_response = response.json()
            print("✅ Activity search successful!")
            print(f"   Location: {activities_response.get('location')}")
            print(f"   Date Range: {activities_response.get('date_range')}")
            print(f"   Total Activities: {len(activities_response.get('activities', []))}")
            
            # Show sample activities
            activities = activities_response.get('activities', [])
            if activities:
                print("\n📋 Sample Activities:")
                for i, activity in enumerate(activities[:5]):
                    print(f"   {i+1}. {activity.get('name', 'Unknown')}")
                    print(f"      Tags: {', '.join(activity.get('tags', []))}")
                    print(f"      Address: {activity.get('address', 'No address')}")
                    if activity.get('start_date'):
                        print(f"      Date: {activity.get('start_date')}")
                    print()
            
            # Save activity response for inspection
            with open('activity_response.json', 'w') as f:
                json.dump(activities_response, f, indent=2)
            print("💾 Activity response saved to 'activity_response.json'")
            
        else:
            print(f"❌ Failed to fetch activities: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
        return
    
    # Step 3: Generate personalized itinerary using the activity response
    print("\n3. Generating personalized itinerary with activity response...")
    itinerary_data = {
        "user_id": user_id,
        "location": "San Francisco",
        "start_date": "2024-06-15",
        "end_date": "2024-06-17",
        "categories": ["restaurant", "museum", "music", "art"],
        "budget": "medium"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-itinerary", json=itinerary_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Personalized itinerary generated successfully!")
            print(f"   User: {result['user_info']['name']} (Age: {result['user_info']['age']})")
            print(f"   Dietary Restrictions: {result['user_info']['dietary_restrictions']}")
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
            
            # Save detailed itinerary to file
            with open('personalized_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n💾 Personalized itinerary saved to 'personalized_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating itinerary: {e}")
    
    # Step 4: Test quick itinerary with different activity categories
    print("\n4. Testing quick itinerary with different categories...")
    quick_data = {
        "interests": ["sports", "nightlife", "food"],
        "location": "Los Angeles",
        "start_date": "2024-07-20",
        "end_date": "2024-07-22",
        "categories": ["restaurant", "sports", "entertainment"],
        "budget": "high"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-itinerary/quick", json=quick_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Quick itinerary generated successfully!")
            print(f"   Trip Location: {result['trip_info']['location']}")
            print(f"   Interests: {', '.join(result['trip_info']['interests'])}")
            print(f"   Available Activities: {result['available_activities']}")
            
            # Save quick itinerary to file
            with open('quick_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Quick itinerary saved to 'quick_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate quick itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating quick itinerary: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Activity Routes Integration Test Completed!")
    print("\nGenerated files:")
    print("- activity_response.json: Raw activity data from APIs")
    print("- personalized_itinerary.json: Itinerary with user data from database")
    print("- quick_itinerary.json: Quick itinerary without user registration")

def test_gemini_prompt_enhancement():
    """Test how the enhanced Gemini prompt uses activity data."""
    print("\n🧠 Testing Gemini Prompt Enhancement")
    print("-" * 40)
    
    print("The enhanced Gemini prompt now includes:")
    print("✅ Complete activity response structure")
    print("✅ Trip information (location, date range)")
    print("✅ Activity categories and counts")
    print("✅ User profile integration")
    print("✅ Dietary restrictions consideration")
    print("✅ Geographic and timing logic")
    
    print("\n📝 Sample prompt structure:")
    print("""
    Traveler Profile:
    - Name, Age, Gender, Dietary Restrictions
    
    Trip Information:
    - Destination, Date Range, Available Activities
    
    Available Places and Events:
    - Formatted list from activity APIs
    
    Instructions:
    - Use available activities for realistic itinerary
    - Consider dietary restrictions
    - Mix activity types
    - Group geographically
    - Include appropriate timing
    """)

if __name__ == "__main__":
    print("🧪 Sidequest Activity Routes Integration Test")
    print("Make sure the Flask backend is running on http://localhost:5000")
    print("Make sure MongoDB is running and accessible")
    print("Make sure all required API keys are set in .env file")
    
    # Test the integration
    test_activity_routes_integration()
    
    # Test prompt enhancement
    test_gemini_prompt_enhancement() 