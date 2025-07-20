#!/usr/bin/env python3
"""
Test script for the complete itinerary generation integration.
This script demonstrates:
1. Creating a user in the database
2. Fetching activities for a location
3. Generating a personalized itinerary using Gemini with user data
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_complete_itinerary_integration():
    """Test the complete integration workflow."""
    
    print("🚀 Testing Complete Itinerary Integration")
    print("=" * 50)
    
    # Step 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "name": "Alex Johnson",
        "email": "alex.johnson@example.com",
        "birthday": "1995-06-15",
        "gender": "non-binary",
        "interests": ["art", "food", "music", "outdoor activities"],
        "dietary_restrictions": "vegetarian",
        "location": "San Francisco, CA",
        "profile_pic": "https://example.com/alex.jpg"
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
    
    # Step 2: Test activity search
    print("\n2. Testing activity search...")
    activity_data = {
        "location": "New York",
        "start_date": "2024-06-01",
        "end_date": "2024-06-03",
        "categories": ["restaurant", "museum", "music"],
        "budget": "medium",
        "trip_name": "NYC Weekend Trip"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
        if response.status_code == 200:
            activities = response.json()
            print(f"✅ Found {len(activities.get('activities', []))} activities")
        else:
            print(f"❌ Failed to fetch activities: {response.text}")
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
    
    # Step 3: Generate personalized itinerary with user data
    print("\n3. Generating personalized itinerary...")
    itinerary_data = {
        "user_id": user_id,
        "location": "New York",
        "start_date": "2024-06-01",
        "end_date": "2024-06-03",
        "categories": ["restaurant", "museum", "music", "art"],
        "budget": "medium"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-itinerary", json=itinerary_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Personalized itinerary generated successfully!")
            print(f"   User: {result['user_info']['name']}")
            print(f"   Age: {result['user_info']['age']}")
            print(f"   Dietary Restrictions: {result['user_info']['dietary_restrictions']}")
            print(f"   Available Activities: {result['available_activities']}")
            print(f"   Trip Location: {result['trip_info']['location']}")
            
            # Display itinerary structure
            itinerary = result['itinerary']
            print("\n📅 Generated Itinerary Structure:")
            for day_key, day_data in itinerary.items():
                print(f"   {day_key.replace('_', ' ').title()}:")
                for time_slot, activities in day_data.items():
                    print(f"     {time_slot.title()}: {len(activities)} activities")
            
            # Save detailed itinerary to file
            with open('generated_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n💾 Detailed itinerary saved to 'generated_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating itinerary: {e}")
    
    # Step 4: Test quick itinerary (without user in database)
    print("\n4. Testing quick itinerary generation...")
    quick_data = {
        "interests": ["sports", "food", "nightlife"],
        "location": "Los Angeles",
        "start_date": "2024-07-01",
        "end_date": "2024-07-02",
        "categories": ["restaurant", "sports", "entertainment"],
        "budget": "high"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-itinerary/quick", json=quick_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Quick itinerary generated successfully!")
            print(f"   Trip Location: {result['trip_info']['location']}")
            print(f"   Available Activities: {result['available_activities']}")
            
            # Save quick itinerary to file
            with open('quick_itinerary.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Quick itinerary saved to 'quick_itinerary.json'")
            
        else:
            print(f"❌ Failed to generate quick itinerary: {response.text}")
    except Exception as e:
        print(f"❌ Error generating quick itinerary: {e}")
    
    # Step 5: Test health endpoints
    print("\n5. Testing health endpoints...")
    
    try:
        response = requests.get(f"{BASE_URL}/itinerary/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Itinerary service health: {health['status']}")
            print(f"   Features: {', '.join(health['features'])}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Error checking health: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Integration test completed!")
    print("\nGenerated files:")
    print("- generated_itinerary.json: Personalized itinerary with user data")
    print("- quick_itinerary.json: Quick itinerary without user registration")

def test_user_management():
    """Test user management endpoints."""
    print("\n👤 Testing User Management")
    print("-" * 30)
    
    # Test getting all users
    try:
        response = requests.get(f"{BASE_URL}/get_all_users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users in database")
            for user in users:
                print(f"   - {user.get('name', 'Unknown')} ({user.get('email', 'No email')})")
        else:
            print(f"❌ Failed to get users: {response.text}")
    except Exception as e:
        print(f"❌ Error getting users: {e}")

if __name__ == "__main__":
    print("🧪 Sidequest Itinerary Integration Test")
    print("Make sure the Flask backend is running on http://localhost:5000")
    print("Make sure MongoDB is running and accessible")
    print("Make sure all required API keys are set in .env file")
    
    # Test user management
    test_user_management()
    
    # Test complete integration
    test_complete_itinerary_integration() 