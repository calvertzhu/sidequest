#!/usr/bin/env python3
"""
Script to update all test files to use GET with params instead of GET with json for activity routes.
"""

import os
import re

def update_file(filepath):
    """Update a single file to use params instead of json for GET requests to activities/search."""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern to match: requests.get(url, json=data) -> requests.get(url, params=data)
    pattern = r'requests\.get\(([^,]+),\s*json=([^)]+)\)'
    replacement = r'requests.get(\1, params=\2)'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"✅ Updated: {filepath}")
        return True
    else:
        print(f"⏭️  No changes needed: {filepath}")
        return False

def main():
    """Update all test files."""
    
    test_files = [
        "test_gemini_full_integration.py",
        "test_itinerary_integration.py", 
        "test_gemini_with_parsing.py",
        "test_complete_pipeline.py",
        "test_activity_integration.py"
    ]
    
    updated_count = 0
    
    for filename in test_files:
        if os.path.exists(filename):
            if update_file(filename):
                updated_count += 1
        else:
            print(f"❌ File not found: {filename}")
    
    print(f"\n🎉 Updated {updated_count} files")

if __name__ == "__main__":
    main() 