#!/usr/bin/env python3
"""
Test script for Gemini-powered activity category parsing.
This demonstrates how Gemini can parse natural language into structured categories.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"

def test_category_parsing():
    """Test the Gemini-powered category parsing with various inputs."""
    
    print("🧠 Testing Gemini-Powered Category Parsing")
    print("=" * 60)
    
    # Test cases with different types of user inputs
    test_cases = [
        {
            "name": "Food & Culture Lover",
            "input": "I want to explore local restaurants and visit museums",
            "expected": "Should parse to restaurant + museum categories"
        },
        {
            "name": "Outdoor Enthusiast", 
            "input": "I love hiking, parks, and outdoor activities",
            "expected": "Should parse to park + outdoor categories"
        },
        {
            "name": "Music & Nightlife",
            "input": "I'm looking for live music venues and nightlife",
            "expected": "Should parse to night_club + music categories"
        },
        {
            "name": "Sports Fan",
            "input": "I want to watch sports games and maybe some concerts",
            "expected": "Should parse to sports + music categories"
        },
        {
            "name": "Art & Entertainment",
            "input": "I'm interested in art galleries, theaters, and cultural events",
            "expected": "Should parse to art_gallery + arts categories"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Input: '{test_case['input']}'")
        print(f"   Expected: {test_case['expected']}")
        
        # Test the activity search with string input
        activity_data = {
            "location": "San Francisco",
            "start_date": "2024-06-15",
            "end_date": "2024-06-17",
            "categories": test_case["input"],  # String input instead of list
            "budget": "medium",
            "trip_name": f"Test Trip - {test_case['name']}"
        }
        
        try:
            response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
            if response.status_code == 200:
                result = response.json()
                
                # Display parsing results
                parsing_info = result.get("parsing_info", {})
                print(f"   ✅ Parsing successful!")
                print(f"      Google Categories: {parsing_info.get('google_categories', [])}")
                print(f"      Ticketmaster Categories: {parsing_info.get('ticketmaster_categories', [])}")
                print(f"      Explanation: {parsing_info.get('explanation', 'No explanation')}")
                print(f"      Activities Found: {len(result.get('activities', []))}")
                
                # Show sample activities
                activities = result.get('activities', [])
                if activities:
                    print(f"      Sample: {activities[0].get('name', 'Unknown')} ({', '.join(activities[0].get('tags', []))})")
                
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Category Parsing Test Completed!")

def test_comparison_with_list_input():
    """Compare string parsing vs direct list input."""
    
    print("\n🔄 Comparing String vs List Input")
    print("=" * 50)
    
    # Test with string input
    string_data = {
        "location": "New York",
        "start_date": "2024-06-01",
        "end_date": "2024-06-03",
        "categories": "I want to visit museums and eat at restaurants",
        "budget": "medium"
    }
    
    # Test with list input
    list_data = {
        "location": "New York", 
        "start_date": "2024-06-01",
        "end_date": "2024-06-03",
        "categories": ["museum", "restaurant"],
        "budget": "medium"
    }
    
    print("Testing string input...")
    try:
        string_response = requests.get(f"{BASE_URL}/activities/search", json=string_data)
        if string_response.status_code == 200:
            string_result = string_response.json()
            string_parsing = string_result.get("parsing_info", {})
            print(f"✅ String input: {len(string_result.get('activities', []))} activities")
            print(f"   Parsed categories: {string_parsing.get('google_categories', [])}")
        else:
            print(f"❌ String input failed: {string_response.text}")
    except Exception as e:
        print(f"❌ String input error: {e}")
    
    print("\nTesting list input...")
    try:
        list_response = requests.get(f"{BASE_URL}/activities/search", json=list_data)
        if list_response.status_code == 200:
            list_result = list_response.json()
            list_parsing = list_result.get("parsing_info", {})
            print(f"✅ List input: {len(list_result.get('activities', []))} activities")
            print(f"   Direct categories: {list_parsing.get('google_categories', [])}")
        else:
            print(f"❌ List input failed: {list_response.text}")
    except Exception as e:
        print(f"❌ List input error: {e}")

def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n🧪 Testing Edge Cases")
    print("=" * 30)
    
    edge_cases = [
        {
            "name": "Empty string",
            "input": "",
            "expected": "Should use fallback categories"
        },
        {
            "name": "Very specific request",
            "input": "I want to visit vegan restaurants, art museums, and attend jazz concerts",
            "expected": "Should parse to restaurant + museum + music"
        },
        {
            "name": "Vague request",
            "input": "I want to have fun",
            "expected": "Should use fallback categories"
        }
    ]
    
    for test_case in edge_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        
        activity_data = {
            "location": "Los Angeles",
            "start_date": "2024-07-01",
            "end_date": "2024-07-03",
            "categories": test_case["input"],
            "budget": "medium"
        }
        
        try:
            response = requests.get(f"{BASE_URL}/activities/search", json=activity_data)
            if response.status_code == 200:
                result = response.json()
                parsing_info = result.get("parsing_info", {})
                print(f"✅ Success: {len(result.get('activities', []))} activities")
                print(f"   Categories: {parsing_info.get('google_categories', [])}")
            else:
                print(f"❌ Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Gemini Category Parsing Test")
    print("Make sure the Flask backend is running on http://localhost:8000")
    print("Make sure GEMINI_API_KEY is set in .env file")
    print()
    
    # Test basic category parsing
    test_category_parsing()
    
    # Test comparison
    test_comparison_with_list_input()
    
    # Test edge cases
    test_edge_cases() 