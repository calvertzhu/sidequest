#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.langchain_match import generate_langchain_match_analysis, get_match_summary

def test_langchain_matching():
    """Test the LangChain-based matching functionality with sample user profiles."""
    
    # Sample user profiles
    user1 = {
        "name": "Alice",
        "interests": ["hiking", "photography", "local cuisine", "museums", "art galleries"],
        "location": "Paris, France",
        "travel_dates": "2024-08-15 to 2024-08-22"
    }
    
    user2 = {
        "name": "Bob",
        "interests": ["hiking", "adventure sports", "street photography", "food tours", "wine tasting"],
        "location": "Paris, France", 
        "travel_dates": "2024-08-16 to 2024-08-23"
    }
    
    print("Testing LangChain-based travel companion matching...")
    print(f"User 1: {user1['name']} - {', '.join(user1['interests'])}")
    print(f"User 2: {user2['name']} - {', '.join(user2['interests'])}")
    print("-" * 60)
    
    try:
        # Generate match analysis using LangChain
        match_analysis = generate_langchain_match_analysis(user1, user2)
        
        # Get summary
        summary = get_match_summary(match_analysis)
        
        print("LANGCHAIN MATCH ANALYSIS RESULTS:")
        print(f"Overall Score: {summary['overall_score']}/100")
        print(f"Match Level: {summary['match_level']}")
        print(f"Analysis Method: {summary['analysis_method']}")
        print(f"Recommendation: {summary['recommendation']}")
        print("\nDETAILED ANALYSIS:")
        
        # Print detailed scores
        print(f"Interest Compatibility: {match_analysis.interest_compatibility.score}/100")
        print(f"  Explanation: {match_analysis.interest_compatibility.explanation}")
        
        print(f"Travel Style Compatibility: {match_analysis.travel_style_compatibility.score}/100")
        print(f"  Explanation: {match_analysis.travel_style_compatibility.explanation}")
        
        print(f"Schedule Compatibility: {match_analysis.schedule_compatibility.score}/100")
        print(f"  Explanation: {match_analysis.schedule_compatibility.explanation}")
        
        print(f"Location Compatibility: {match_analysis.location_compatibility.score}/100")
        print(f"  Explanation: {match_analysis.location_compatibility.explanation}")
        
        print(f"\nPotential Activities: {', '.join(match_analysis.potential_activities)}")
        print(f"Potential Conflicts: {', '.join(match_analysis.potential_conflicts)}")
        
        # Test with different profiles
        print("\n" + "="*60)
        print("Testing with different profiles...")
        
        user3 = {
            "name": "Charlie",
            "interests": ["beach", "spa", "yoga", "meditation", "luxury resorts"],
            "location": "Bali, Indonesia",
            "travel_dates": "2024-09-01 to 2024-09-08"
        }
        
        user4 = {
            "name": "Diana",
            "interests": ["mountain climbing", "extreme sports", "backpacking", "camping"],
            "location": "Bali, Indonesia",
            "travel_dates": "2024-09-02 to 2024-09-09"
        }
        
        print(f"User 3: {user3['name']} - {', '.join(user3['interests'])}")
        print(f"User 4: {user4['name']} - {', '.join(user4['interests'])}")
        print("-" * 60)
        
        match_analysis2 = generate_langchain_match_analysis(user3, user4)
        summary2 = get_match_summary(match_analysis2)
        
        print(f"Overall Score: {summary2['overall_score']}/100")
        print(f"Match Level: {summary2['match_level']}")
        print(f"Analysis Method: {summary2['analysis_method']}")
        print(f"Recommendation: {summary2['recommendation']}")
            
    except Exception as e:
        print(f"Error during matching: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_langchain_matching() 