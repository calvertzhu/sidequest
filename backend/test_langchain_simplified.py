#!/usr/bin/env python3
"""
Test the simplified LangChain match output (user_id and match_score only).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.gemini.langchain_match import (
    get_simplified_match_result,
    get_multiple_matches_simplified,
    generate_langchain_match_analysis,
    get_match_summary
)

def test_simplified_match_output():
    """Test that the simplified match output contains only user_id and match_score."""
    
    print("🧪 Testing Simplified LangChain Match Output")
    print("=" * 50)
    
    # Test user 1
    user1 = {
        "name": "Alice",
        "interests": ["travel", "food", "culture", "museums"],
        "location": "San Francisco",
        "travel_dates": "2024-06-01 to 2024-06-05"
    }
    
    # Test user 2
    user2 = {
        "name": "Bob",
        "interests": ["travel", "food", "music", "nightlife"],
        "location": "San Francisco",
        "travel_dates": "2024-06-02 to 2024-06-06"
    }
    
    # Test user 3 (different location)
    user3 = {
        "name": "Charlie",
        "interests": ["hiking", "outdoors", "adventure"],
        "location": "New York",
        "travel_dates": "2024-06-01 to 2024-06-05"
    }
    
    print("\n1. Testing single match result...")
    try:
        result = get_simplified_match_result(user1, user2, "user_123")
        
        print(f"✅ Simplified result: {result}")
        
        # Verify structure
        expected_keys = {"user_id", "match_score"}
        actual_keys = set(result.keys())
        
        if actual_keys == expected_keys:
            print("✅ Correct structure: only user_id and match_score")
        else:
            print(f"❌ Wrong structure. Expected: {expected_keys}, Got: {actual_keys}")
        
        # Verify data types
        if isinstance(result["user_id"], str):
            print("✅ user_id is string")
        else:
            print(f"❌ user_id is not string: {type(result['user_id'])}")
        
        if isinstance(result["match_score"], int):
            print("✅ match_score is integer")
        else:
            print(f"❌ match_score is not integer: {type(result['match_score'])}")
        
        # Verify score range
        if 0 <= result["match_score"] <= 100:
            print("✅ match_score is in valid range (0-100)")
        else:
            print(f"❌ match_score out of range: {result['match_score']}")
            
    except Exception as e:
        print(f"❌ Single match test failed: {e}")
    
    print("\n2. Testing multiple matches...")
    try:
        potential_matches = [
            {"_id": "user_123", "name": "Bob", "interests": ["travel", "food", "music"], "location": "San Francisco", "travel_dates": "2024-06-02 to 2024-06-06"},
            {"_id": "user_456", "name": "Charlie", "interests": ["hiking", "outdoors"], "location": "New York", "travel_dates": "2024-06-01 to 2024-06-05"},
            {"_id": "user_789", "name": "Diana", "interests": ["travel", "food", "culture"], "location": "San Francisco", "travel_dates": "2024-06-01 to 2024-06-05"}
        ]
        
        results = get_multiple_matches_simplified(user1, potential_matches)
        
        print(f"✅ Multiple matches result: {results}")
        
        # Verify all results have correct structure
        all_correct = True
        for i, result in enumerate(results):
            if set(result.keys()) != {"user_id", "match_score"}:
                print(f"❌ Result {i} has wrong structure: {result}")
                all_correct = False
        
        if all_correct:
            print("✅ All results have correct structure")
        
        # Verify sorting (highest score first)
        scores = [r["match_score"] for r in results]
        if scores == sorted(scores, reverse=True):
            print("✅ Results are sorted by score (highest first)")
        else:
            print(f"❌ Results not sorted correctly: {scores}")
            
    except Exception as e:
        print(f"❌ Multiple matches test failed: {e}")
    
    print("\n3. Testing with None user_id...")
    try:
        result = get_simplified_match_result(user1, user2, None)
        print(f"✅ Result with None user_id: {result}")
        
        if result["user_id"] is None:
            print("✅ Correctly handles None user_id")
        else:
            print(f"❌ Should have None user_id, got: {result['user_id']}")
            
    except Exception as e:
        print(f"❌ None user_id test failed: {e}")
    
    print("\n4. Testing full analysis vs simplified...")
    try:
        # Get full analysis
        full_analysis = generate_langchain_match_analysis(user1, user2)
        
        # Get simplified result
        simplified = get_simplified_match_result(user1, user2, "user_123")
        
        print(f"Full analysis keys: {list(full_analysis.__dict__.keys())}")
        print(f"Simplified keys: {list(simplified.keys())}")
        
        # Verify simplified has much fewer fields
        if len(simplified) < len(full_analysis.__dict__):
            print("✅ Simplified result has fewer fields than full analysis")
        else:
            print("❌ Simplified result should have fewer fields")
            
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")

def test_edge_cases():
    """Test edge cases for simplified match output."""
    
    print(f"\n⚠️ Testing Edge Cases")
    print("=" * 30)
    
    # Test with minimal user data
    minimal_user1 = {"name": "Minimal", "interests": []}
    minimal_user2 = {"name": "Minimal2", "interests": []}
    
    try:
        result = get_simplified_match_result(minimal_user1, minimal_user2, "minimal_user")
        print(f"✅ Minimal data result: {result}")
        
        if result["match_score"] >= 0:
            print("✅ Handles minimal data gracefully")
        else:
            print(f"❌ Negative score with minimal data: {result['match_score']}")
            
    except Exception as e:
        print(f"❌ Minimal data test failed: {e}")
    
    # Test with very different users
    outdoor_user = {
        "name": "Outdoor",
        "interests": ["hiking", "camping", "climbing"],
        "location": "Denver",
        "travel_dates": "2024-07-01 to 2024-07-05"
    }
    
    indoor_user = {
        "name": "Indoor",
        "interests": ["museums", "theater", "spa"],
        "location": "Miami",
        "travel_dates": "2024-08-01 to 2024-08-05"
    }
    
    try:
        result = get_simplified_match_result(outdoor_user, indoor_user, "indoor_user")
        print(f"✅ Very different users result: {result}")
        
        # Should have low match score
        if result["match_score"] < 50:
            print("✅ Correctly identifies low compatibility")
        else:
            print(f"❌ Unexpectedly high score for very different users: {result['match_score']}")
            
    except Exception as e:
        print(f"❌ Different users test failed: {e}")

if __name__ == "__main__":
    print("🧪 Simplified LangChain Match Test")
    print("Make sure GEMINI_API_KEY is set in .env file")
    print()
    
    test_simplified_match_output()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("🎉 Simplified Match Test Completed!") 