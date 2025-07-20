#!/usr/bin/env python3
"""
Comprehensive test script for Gemini integration with full API system.
This tests the complete flow: user creation -> activity search -> Gemini itinerary generation.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_full_gemini_integration():
    """Test the complete Gemini integration with APIs."""
    
    print("🧠 Testing Full Gemini Integration with APIs")
    print("=" * 60)
    
    # Step 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "name": "Gemini Test User",
        "email": f"gemini.test.{int(time.time())}@example.com",
        "birthday": "1990-08-15",
        "gender": "female",
        "interests": ["art", "food", "music", "outdoor activities"],
        "dietary_restrictions": "vegan",
        "location": "Seattle, WA",
        "profile_pic": "https://example.com/gemini-test.jpg"
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
    
    # Step 2: Test activity search (this will use Google Places API)
    print("\n2. Testing activity search with Google Places API...")
    activity_data = {
        "location": "San Francisco",
        "start_date": "2024-06-15",
        "end_date": "2024-06-17",
        "categories": ["restaurant", "museum", "park"],
        "budget": "medium",
        "trip_name": "SF Gemini Test Trip"
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
                print("\n📋 Sample Activities Found:")
                for i, activity in enumerate(activities[:5]):
                    print(f"   {i+1}. {activity.get('name', 'Unknown')}")
                    print(f"      Tags: {', '.join(activity.get('tags', []))}")
                    print(f"      Address: {activity.get('address', 'No address')}")
                    print()
            
            # Save activity response for inspection
            with open('api_activities_response.json', 'w') as f:
                json.dump(activities_response, f, indent=2)
            print("💾 Activity response saved to 'api_activities_response.json'")
            
        else:
            print(f"❌ Failed to fetch activities: {response.text}")
            print("This might be due to missing API keys (Google Places, Ticketmaster)")
            return
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
        return
    
    # Step 3: Test Gemini-powered personalized itinerary generation
    print("\n3. Testing Gemini-powered itinerary generation...")
    itinerary_data = {
        "user_id": user_id,
        "location": "San Francisco",
        "start_date": "2024-06-15",
        "end_date": "2024-06-17",
        "categories": ["restaurant", "museum", "park"],
        "budget": "medium"
    }
    
    try:
        print("🚀 Sending request to Gemini-powered itinerary endpoint...")
        response = requests.post(f"{BASE_URL}/generate-itinerary", json=itinerary_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Gemini-powered itinerary generated successfully!")
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
            with open('gemini_api_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n💾 Full Gemini API itinerary saved to 'gemini_api_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate itinerary: {response.text}")
            print("This might be due to:")
            print("- Missing Gemini API key")
            print("- Gemini API rate limits")
            print("- Invalid user data")
            
    except Exception as e:
        print(f"❌ Error generating itinerary: {e}")
    
    # Step 4: Test quick itinerary generation (without user in database)
    print("\n4. Testing quick itinerary generation...")
    quick_data = {
        "interests": ["sports", "nightlife", "food"],
        "location": "Los Angeles",
        "start_date": "2024-07-20",
        "end_date": "2024-07-22",
        "categories": ["restaurant", "sports"],
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
            with open('gemini_quick_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Quick itinerary saved to 'gemini_quick_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate quick itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating quick itinerary: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Full Gemini Integration Test Completed!")
    print("\nGenerated files:")
    print("- api_activities_response.json: Raw activity data from APIs")
    print("- gemini_api_itinerary.json: Personalized itinerary with user data")
    print("- gemini_quick_itinerary.json: Quick itinerary without user registration")

def test_gemini_health():
    """Test the Gemini service health endpoint."""
    print("\n🏥 Testing Gemini Service Health")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/itinerary/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Itinerary service health: {health['status']}")
            print(f"   Service: {health['service']}")
            print(f"   Version: {health['version']}")
            print(f"   Features: {', '.join(health['features'])}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Error checking health: {e}")

def test_api_endpoints():
    """Test basic API endpoint availability."""
    print("\n🔗 Testing API Endpoints")
    print("-" * 30)
    
    endpoints = [
        ("/", "Home"),
        ("/health", "Health"),
        ("/api/users", "Users"),
        ("/api/activities/search", "Activities"),
        ("/api/generate-itinerary", "Itinerary"),
        ("/api/generate-itinerary/quick", "Quick Itinerary")
    ]
    
    for endpoint, name in endpoints:
        try:
            if endpoint in ["/api/users", "/api/activities/search", "/api/generate-itinerary", "/api/generate-itinerary/quick"]:
                # These are POST/GET endpoints that need data, just check if they're reachable
                response = requests.get(f"http://localhost:8000{endpoint}")
                status = "✅ Available" if response.status_code in [200, 405] else f"❌ Error {response.status_code}"
            else:
                response = requests.get(f"http://localhost:8000{endpoint}")
                status = "✅ Available" if response.status_code == 200 else f"❌ Error {response.status_code}"
            
            print(f"   {name}: {status}")
        except Exception as e:
            print(f"   {name}: ❌ Connection Error")

if __name__ == "__main__":
    print("🧪 Full Gemini Integration Test")
    print("Make sure the Flask backend is running on http://localhost:8000")
    print("Make sure MongoDB is running and accessible")
    print("Make sure all required API keys are set in .env file:")
    print("- GEMINI_API_KEY")
    print("- GOOGLE_API_KEY") 
    print("- TICKETMASTER_API_KEY")
    print()
    
    # Test basic endpoints first
    test_api_endpoints()
    
    # Test health endpoints
    test_gemini_health()
    
    # Test full integration
    test_full_gemini_integration() 