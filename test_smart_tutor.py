#!/usr/bin/env python3
"""
Test the Smart Tutor integration to verify improved responses
"""

import requests
import json

def test_tutor_response(message: str):
    """Test a message with the tutor API"""
    
    url = "http://localhost:8000/chat"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            print(f"👤 User: {message}")
            print(f"🎓 Tutor: {data['response']}")
            print("="*80)
            return data['response']
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return None

def main():
    """Test various scenarios that were problematic before"""
    
    print("🧠 Testing Smart Tutor Integration")
    print("="*80)
    
    # Test cases that were giving poor responses before
    test_cases = [
        "I want some analogy for a middle schooler to understand Newton's laws",
        "Explain the difference between speed and velocity for middle school",
        "Can you give me examples of chemical equilibrium?",
        "What is Newton's second law?",
        "Help me understand object-oriented programming",
        "Explain chemical equilibrium using analogies"
    ]
    
    for message in test_cases:
        response = test_tutor_response(message)
        if response is None:
            print("Failed to get response, stopping tests.")
            break
        print()  # Add spacing between tests

if __name__ == "__main__":
    main()