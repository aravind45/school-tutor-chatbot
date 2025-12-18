#!/usr/bin/env python3
"""
Test the fixed vector motion response
"""

import requests
import json

def test_vector_motion():
    """Test the vector motion explanation"""
    
    url = "http://localhost:8000/chat"
    
    # The exact query from the screenshot
    message = "explain Vector addition free fall and projectile motion"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 VECTOR MOTION TEST")
            print("="*60)
            print(f"👤 User Request: {message}")
            print("="*60)
            print("🎓 Smart Tutor Response:")
            print(data['response'])
            print("="*60)
            
            # Check if this is a comprehensive response
            response_text = data['response'].lower()
            
            if ("vector addition" in response_text and 
                "projectile motion" in response_text and 
                "free fall" in response_text and
                "formula" in response_text):
                print("✅ SUCCESS! Comprehensive physics explanation with all three topics!")
            elif "important concept that requires careful analysis" in response_text:
                print("❌ STILL GENERIC TEMPLATE - Need to debug further!")
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
    test_vector_motion()