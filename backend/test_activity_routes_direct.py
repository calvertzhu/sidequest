#!/usr/bin/env python3
"""
Direct test of activity routes functionality.
Tests both string parsing and direct category lists.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_activity_routes_direct():
    """Test activity routes directly with various inputs."""
    
    print("🔗 Direct Activity Routes Test")
    print("=" * 50)
    
    # Test 1: String input with Gemini parsing
    print("\n1. Testing string input with Gemini parsing...")
    string_data = {
        "location": "New York",
        "start_date": "2024-06-01",
        "end_date": "2024-06-03",
        "categories": "I want to visit museums and eat at restaurants",
        "budget": "medium"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=string_data)
        if response.status_code == 200:
            result = response.json()
            parsing_info = result.get("parsing_info", {})
            print("✅ String input successful!")
            print(f"   Original: '{parsing_info.get('original_input', '')}'")
            print(f"   Google Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Ticketmaster Categories: {parsing_info.get('ticketmaster_categories', [])}")
            print(f"   Activities Found: {len(result.get('activities', []))}")
            print(f"   Explanation: {parsing_info.get('explanation', '')}")
        else:
            print(f"❌ String input failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ String input error: {e}")
    
    # Test 2: Direct list input
    print("\n2. Testing direct list input...")
    list_data = {
        "location": "Los Angeles",
        "start_date": "2024-07-01",
        "end_date": "2024-07-03",
        "categories": ["restaurant", "museum", "park"],
        "budget": "high"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=list_data)
        if response.status_code == 200:
            result = response.json()
            parsing_info = result.get("parsing_info", {})
            print("✅ List input successful!")
            print(f"   Direct Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Activities Found: {len(result.get('activities', []))}")
        else:
            print(f"❌ List input failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ List input error: {e}")
    
    # Test 3: Complex string input
    print("\n3. Testing complex string input...")
    complex_data = {
        "location": "San Francisco",
        "start_date": "2024-08-01",
        "end_date": "2024-08-03",
        "categories": "I want to experience the nightlife, visit art galleries, and maybe catch a concert",
        "budget": "medium"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=complex_data)
        if response.status_code == 200:
            result = response.json()
            parsing_info = result.get("parsing_info", {})
            print("✅ Complex input successful!")
            print(f"   Original: '{parsing_info.get('original_input', '')}'")
            print(f"   Google Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Ticketmaster Categories: {parsing_info.get('ticketmaster_categories', [])}")
            print(f"   Activities Found: {len(result.get('activities', []))}")
            
            # Show sample activities
            activities = result.get('activities', [])
            if activities:
                print("   Sample Activities:")
                for i, activity in enumerate(activities[:3]):
                    print(f"     {i+1}. {activity.get('name', 'Unknown')} ({', '.join(activity.get('tags', []))})")
        else:
            print(f"❌ Complex input failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Complex input error: {e}")
    
    # Test 4: Edge case - empty categories
    print("\n4. Testing edge case - empty categories...")
    empty_data = {
        "location": "Chicago",
        "start_date": "2024-09-01",
        "end_date": "2024-09-03",
        "categories": "",
        "budget": "low"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=empty_data)
        if response.status_code == 200:
            result = response.json()
            parsing_info = result.get("parsing_info", {})
            print("✅ Empty input handled!")
            print(f"   Google Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Activities Found: {len(result.get('activities', []))}")
        else:
            print(f"❌ Empty input failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Empty input error: {e}")
    
    # Test 5: Sports-focused input
    print("\n5. Testing sports-focused input...")
    sports_data = {
        "location": "Boston",
        "start_date": "2024-10-01",
        "end_date": "2024-10-03",
        "categories": "I want to watch sports games and attend live events",
        "budget": "high"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=sports_data)
        if response.status_code == 200:
            result = response.json()
            parsing_info = result.get("parsing_info", {})
            print("✅ Sports input successful!")
            print(f"   Google Categories: {parsing_info.get('google_categories', [])}")
            print(f"   Ticketmaster Categories: {parsing_info.get('ticketmaster_categories', [])}")
            print(f"   Activities Found: {len(result.get('activities', []))}")
        else:
            print(f"❌ Sports input failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Sports input error: {e}")

def test_response_structure():
    """Test the response structure and data format."""
    
    print("\n📋 Testing Response Structure")
    print("=" * 40)
    
    test_data = {
        "location": "Miami",
        "start_date": "2024-11-01",
        "end_date": "2024-11-03",
        "categories": "I want to visit beaches and try local restaurants",
        "budget": "medium"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=test_data)
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Response structure test successful!")
            print(f"   Location: {result.get('location')}")
            print(f"   Date Range: {result.get('date_range')}")
            print(f"   Total Activities: {len(result.get('activities', []))}")
            
            # Check parsing info
            parsing_info = result.get("parsing_info", {})
            print(f"   Has Parsing Info: {'✅' if parsing_info else '❌'}")
            if parsing_info:
                print(f"   Original Input: {parsing_info.get('original_input')}")
                print(f"   Google Categories: {parsing_info.get('google_categories')}")
                print(f"   Ticketmaster Categories: {parsing_info.get('ticketmaster_categories')}")
                print(f"   Explanation: {parsing_info.get('explanation')}")
            
            # Check activity structure
            activities = result.get('activities', [])
            if activities:
                first_activity = activities[0]
                print(f"   Activity Structure: {'✅' if 'name' in first_activity else '❌'}")
                print(f"   Sample Activity: {first_activity.get('name')} ({', '.join(first_activity.get('tags', []))})")
                print(f"   Has Address: {'✅' if 'address' in first_activity else '❌'}")
            
        else:
            print(f"❌ Response structure test failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Response structure test error: {e}")

def test_error_handling():
    """Test error handling for invalid inputs."""
    
    print("\n⚠️ Testing Error Handling")
    print("=" * 30)
    
    # Test missing required fields
    print("\n1. Testing missing required fields...")
    invalid_data = {
        "location": "Seattle",
        # Missing start_date and end_date
        "categories": "restaurants"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=invalid_data)
        if response.status_code == 400:
            print("✅ Properly handled missing fields")
        else:
            print(f"❌ Unexpected response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test invalid date format
    print("\n2. Testing invalid date format...")
    invalid_date_data = {
        "location": "Portland",
        "start_date": "2024/06/01",  # Wrong format
        "end_date": "2024/06/03",    # Wrong format
        "categories": "museums"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/activities/search", json=invalid_date_data)
        if response.status_code == 400:
            print("✅ Properly handled invalid date format")
        else:
            print(f"❌ Unexpected response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Date format test failed: {e}")

if __name__ == "__main__":
    print("🧪 Direct Activity Routes Test")
    print("Make sure the Flask backend is running on http://localhost:8000")
    print("Make sure GEMINI_API_KEY is set in .env file")
    print()
    
    # Test basic functionality
    test_activity_routes_direct()
    
    # Test response structure
    test_response_structure()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎉 Activity Routes Test Completed!") 