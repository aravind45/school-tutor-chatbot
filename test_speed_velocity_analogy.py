#!/usr/bin/env python3
"""
Test the speed vs velocity analogy request that was shown in the screenshot
"""

import requests
import json

def test_speed_velocity_analogy():
    """Test the speed vs velocity analogy request"""
    
    url = "http://localhost:8000/chat"
    
    # This is the exact request from the screenshot
    message = "speed vs velocity ? explain using analogy"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 SPEED VS VELOCITY ANALOGY TEST")
            print("="*60)
            print(f"👤 User Request: {message}")
            print("="*60)
            print("🎓 Smart Tutor Response:")
            print(data['response'])
            print("="*60)
            
            # Check if this is a good analogy response
            response_text = data['response'].lower()
            
            if "analogy" in response_text and ("speedometer" in response_text or "gps" in response_text or "navigation" in response_text):
                print("✅ SUCCESS! Contains good analogies for speed vs velocity!")
            elif "think of it like" in response_text and "analogy would be customized" in response_text:
                print("❌ TEMPLATE RESPONSE DETECTED - This is the generic fallback!")
            else:
                print("⚠️  Response type unclear")
                
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_speed_velocity_analogy()