#!/usr/bin/env python3
"""
Test script for the matching functionality.
Run this to test how well two user profiles match as travel companions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.match import generate_match_analysis, get_match_summary

def test_matching():
    """Test the matching functionality with sample user profiles."""
    
    # Sample user profiles
    user1 = {
        "name": "Alice",
        "interests": ["hiking", "photography", "local cuisine", "museums"],
        "location": "Paris, France",
        "travel_dates": "2024-08-15 to 2024-08-22"
    }
    
    user2 = {
        "name": "Bob",
        "interests": ["hiking", "adventure sports", "street photography", "food tours"],
        "location": "Paris, France", 
        "travel_dates": "2024-08-16 to 2024-08-23"
    }
    
    print("Testing travel companion matching...")
    print(f"User 1: {user1['name']} - {', '.join(user1['interests'])}")
    print(f"User 2: {user2['name']} - {', '.join(user2['interests'])}")
    print("-" * 50)
    
    try:
        # Generate match analysis
        match_analysis = generate_match_analysis(user1, user2)
        
        # Get summary
        summary = get_match_summary(match_analysis)
        
        print("MATCH ANALYSIS RESULTS:")
        print(f"Overall Score: {summary['overall_score']}/100")
        print(f"Match Level: {summary['match_level']}")
        print(f"Recommendation: {summary['recommendation']}")
        print("\nDETAILED ANALYSIS:")
        
        # Print detailed scores
        for category, data in match_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                print(f"{category.replace('_', ' ').title()}: {data['score']}/100")
                print(f"  Explanation: {data['explanation']}")
        
        if 'potential_activities' in match_analysis:
            print(f"\nPotential Activities: {', '.join(match_analysis['potential_activities'])}")
        
        if 'potential_conflicts' in match_analysis:
            print(f"Potential Conflicts: {', '.join(match_analysis['potential_conflicts'])}")
            
    except Exception as e:
        print(f"Error during matching: {e}")

if __name__ == "__main__":
    test_matching() 