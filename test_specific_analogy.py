#!/usr/bin/env python3
"""
Test the specific analogy request that should trigger Smart Tutor
"""

import requests
import json

def test_analogy_request():
    """Test the specific analogy request for middle schoolers"""
    
    url = "http://localhost:8000/chat"
    
    # This should trigger the Smart Tutor's analogy response
    message = "I want some analogy for a middle schooler to understand Newton's laws"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            print(f"👤 User: {message}")
            print(f"🎓 Tutor Response:")
            print(data['response'])
            print("="*80)
            
            # Check if this is the Smart Tutor response (should have middle school analogies)
            if "video game" in data['response'].lower() or "lazy rule" in data['response'].lower():
                print("✅ SMART TUTOR DETECTED - Contains middle school analogies!")
            else:
                print("❌ OLD SERVICE - Still using QG service responses")
                
            return data['response']
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return None

if __name__ == "__main__":
    test_analogy_request()