#!/usr/bin/env python3
"""
Debug script to test Gemini API directly.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini_direct():
    """Test Gemini API directly."""
    
    print("🔍 Debugging Gemini API")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        print("✅ Gemini model configured")
        
        # Test with a simple prompt
        simple_prompt = "Hello, can you respond with just 'Hello World'?"
        
        print("🚀 Testing simple prompt...")
        response = model.generate_content(simple_prompt)
        
        print(f"✅ Response received: {response.text}")
        
        # Test with JSON prompt
        json_prompt = """
        Return only valid JSON in this format:
        {
          "message": "Hello World",
          "status": "success"
        }
        """
        
        print("🚀 Testing JSON prompt...")
        response = model.generate_content(json_prompt)
        
        print(f"✅ JSON Response: {response.text}")
        
        # Try to parse as JSON
        import json
        try:
            parsed = json.loads(response.text)
            print(f"✅ JSON parsed successfully: {parsed}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response: {repr(response.text)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_gemini_direct() 