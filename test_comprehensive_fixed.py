#!/usr/bin/env python3
"""
Comprehensive test of the fixed Smart Tutor service
"""

import requests
import json

def test_tutor_response(message: str, description: str):
    """Test a message with the tutor API"""
    
    url = "http://localhost:8000/chat"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"🧪 {description}")
            print(f"👤 User: {message}")
            print(f"🎓 Response: {data['response'][:200]}...")
            
            # Check if it's a template response
            if "analogy would be customized" in data['response'].lower():
                print("❌ TEMPLATE RESPONSE")
            else:
                print("✅ RICH CONTENT")
            
            print("="*80)
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

def main():
    """Test various scenarios with the fixed Smart Tutor"""
    
    print("🧠 Testing Fixed Smart Tutor Service")
    print("="*80)
    
    # Test cases that were problematic
    test_cases = [
        ("I want some analogy for a middle schooler to understand Newton's laws", "Newton's Laws Middle School"),
        ("speed vs velocity ? explain using analogy", "Speed vs Velocity Analogy"),
        ("Explain the difference between speed and velocity for middle school", "Speed vs Velocity Middle School"),
        ("Can you give me an analogy for chemical equilibrium for middle schoolers?", "Chemical Equilibrium Middle School"),
        ("What is Newton's second law?", "Newton's Second Law"),
        ("Help me understand object-oriented programming", "Object-Oriented Programming")
    ]
    
    for message, description in test_cases:
        success = test_tutor_response(message, description)
        if not success:
            print("Failed to get response, stopping tests.")
            break

if __name__ == "__main__":
    main()