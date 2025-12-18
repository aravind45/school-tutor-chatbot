#!/usr/bin/env python3
"""
Comprehensive test of the Smart Tutor service with various scenarios
"""

import requests
import json

def test_tutor_response(message: str, expected_keywords: list = None):
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
            print(f"🎓 Tutor: {data['response'][:300]}...")
            
            # Check for expected keywords
            if expected_keywords:
                found_keywords = []
                response_lower = data['response'].lower()
                for keyword in expected_keywords:
                    if keyword.lower() in response_lower:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    print(f"✅ FOUND KEYWORDS: {', '.join(found_keywords)}")
                else:
                    print(f"❌ MISSING KEYWORDS: {', '.join(expected_keywords)}")
            
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
    """Test various scenarios with the Smart Tutor"""
    
    print("🧠 Comprehensive Smart Tutor Testing")
    print("="*80)
    
    # Test cases with expected keywords to verify Smart Tutor responses
    test_cases = [
        {
            "message": "I want some analogy for a middle schooler to understand Newton's laws",
            "keywords": ["video game", "lazy rule", "middle school"]
        },
        {
            "message": "Explain the difference between speed and velocity for middle school",
            "keywords": ["middle school", "speedometer", "GPS", "direction"]
        },
        {
            "message": "Can you give me an analogy for chemical equilibrium for middle schoolers?",
            "keywords": ["restaurant", "middle school", "equilibrium"]
        },
        {
            "message": "What is Newton's second law?",
            "keywords": ["F = ma", "acceleration", "force"]
        },
        {
            "message": "Help me understand object-oriented programming",
            "keywords": ["encapsulation", "inheritance", "polymorphism"]
        },
        {
            "message": "Explain speed and velocity with analogies",
            "keywords": ["analogy", "speed", "velocity"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}:")
        response = test_tutor_response(
            test_case["message"], 
            test_case.get("keywords", [])
        )
        if response is None:
            print("Failed to get response, stopping tests.")
            break

if __name__ == "__main__":
    main()