#!/usr/bin/env python3
"""
Test script to verify Gemini price estimation for activities in itineraries.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.gemini.gemini import generate_itinerary_json, save_activities_to_database

def test_price_estimation():
    """Test that Gemini correctly estimates prices for activities."""
    
    print("💰 Testing Gemini Price Estimation")
    print("=" * 50)
    
    # Mock activities response
    activities_response = {
        "location": "San Francisco",
        "date_range": ["2024-06-01", "2024-06-03"],
        "activities": [
            {
                "name": "Golden Gate Bridge",
                "tags": ["landmark", "tourist_attraction"],
                "address": "Golden Gate Bridge, San Francisco, CA"
            },
            {
                "name": "Fisherman's Wharf",
                "tags": ["tourist_attraction", "restaurant"],
                "address": "Fisherman's Wharf, San Francisco, CA"
            },
            {
                "name": "Alcatraz Island",
                "tags": ["museum", "tourist_attraction"],
                "address": "Alcatraz Island, San Francisco, CA"
            },
            {
                "name": "Chinatown",
                "tags": ["restaurant", "shopping"],
                "address": "Chinatown, San Francisco, CA"
            },
            {
                "name": "Golden Gate Park",
                "tags": ["park", "museum"],
                "address": "Golden Gate Park, San Francisco, CA"
            }
        ]
    }
    
    # Test user info
    user_info = {
        "name": "Test User",
        "age": 28,
        "interests": ["travel", "food", "culture"],
        "budget": "medium"
    }
    
    interests = ["travel", "food", "culture", "history"]
    
    print("🤖 Generating itinerary with price estimation...")
    
    try:
        # Generate itinerary using Gemini
        itinerary_json = generate_itinerary_json(
            location="San Francisco",
            interests=interests,
            activities_response=activities_response,
            user_info=user_info,
            budget="medium",
            start_date="2024-06-01",
            end_date="2024-06-03"
        )
        
        print("✅ Itinerary generated successfully!")
        
        # Analyze price estimations
        print("\n📊 Price Analysis:")
        print("-" * 30)
        
        total_price = 0
        activity_count = 0
        
        for day_key, day_activities in itinerary_json.items():
            print(f"\n{day_key.upper()}:")
            day_price = 0
            
            for period, activities in day_activities.items():
                print(f"  {period.capitalize()}:")
                
                for activity in activities:
                    name = activity.get('name', 'Unknown')
                    price = activity.get('price', 0)
                    description = activity.get('description', 'No description')
                    
                    print(f"    • {name}: ${price}")
                    print(f"      {description}")
                    
                    day_price += price
                    total_price += price
                    activity_count += 1
            
            print(f"  Day Total: ${day_price}")
        
        print(f"\n📈 Summary:")
        print(f"  Total Activities: {activity_count}")
        print(f"  Total Estimated Cost: ${total_price}")
        print(f"  Average Cost per Activity: ${total_price/activity_count if activity_count > 0 else 0:.2f}")
        
        # Check if prices are reasonable
        print(f"\n✅ Price Validation:")
        reasonable_prices = 0
        for day_key, day_activities in itinerary_json.items():
            for period, activities in day_activities.items():
                for activity in activities:
                    price = activity.get('price', 0)
                    if isinstance(price, (int, float)) and 0 <= price <= 200:
                        reasonable_prices += 1
                    else:
                        print(f"  ⚠️  Unusual price for {activity.get('name')}: ${price}")
        
        print(f"  Reasonable prices: {reasonable_prices}/{activity_count}")
        
        # Test database saving (without actually saving)
        print(f"\n💾 Testing database integration...")
        print("  (This would save activities to database with prices)")
        
        # Show what would be saved
        for day_key, day_activities in itinerary_json.items():
            for period, activities in day_activities.items():
                for activity in activities:
                    print(f"  Would save: {activity.get('name')} - ${activity.get('price', 0)}")
        
        return itinerary_json
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_different_activity_types():
    """Test price estimation for different types of activities."""
    
    print(f"\n🎭 Testing Different Activity Types")
    print("=" * 40)
    
    # Test cases with different activity types
    test_cases = [
        {
            "name": "Budget Traveler",
            "interests": ["budget", "free", "parks"],
            "budget": "low",
            "expected_price_range": (0, 50)
        },
        {
            "name": "Luxury Traveler", 
            "interests": ["fine_dining", "luxury", "premium"],
            "budget": "high",
            "expected_price_range": (50, 300)
        },
        {
            "name": "Cultural Explorer",
            "interests": ["museums", "art", "culture"],
            "budget": "medium",
            "expected_price_range": (10, 100)
        }
    ]
    
    activities_response = {
        "location": "New York",
        "date_range": ["2024-07-01", "2024-07-02"],
        "activities": [
            {"name": "Central Park", "tags": ["park"], "address": "Central Park, NY"},
            {"name": "Metropolitan Museum", "tags": ["museum"], "address": "Metropolitan Museum, NY"},
            {"name": "Broadway Show", "tags": ["theater"], "address": "Broadway, NY"},
            {"name": "Fine Dining Restaurant", "tags": ["restaurant"], "address": "Manhattan, NY"}
        ]
    }
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"   Budget: {test_case['budget']}")
        print(f"   Expected price range: ${test_case['expected_price_range'][0]}-${test_case['expected_price_range'][1]}")
        
        try:
            itinerary_json = generate_itinerary_json(
                location="New York",
                interests=test_case["interests"],
                activities_response=activities_response,
                budget=test_case["budget"],
                start_date="2024-07-01",
                end_date="2024-07-02"
            )
            
            # Calculate total price
            total_price = 0
            for day_key, day_activities in itinerary_json.items():
                for period, activities in day_activities.items():
                    for activity in activities:
                        total_price += activity.get('price', 0)
            
            print(f"   ✅ Total estimated cost: ${total_price}")
            
            # Check if within expected range
            min_expected, max_expected = test_case["expected_price_range"]
            if min_expected <= total_price <= max_expected:
                print(f"   ✅ Price within expected range")
            else:
                print(f"   ⚠️  Price outside expected range")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Gemini Price Estimation Test")
    print("Make sure GEMINI_API_KEY is set in .env file")
    print()
    
    # Test basic price estimation
    test_price_estimation()
    
    # Test different activity types
    test_different_activity_types()
    
    print("\n" + "=" * 50)
    print("🎉 Price Estimation Test Completed!") 