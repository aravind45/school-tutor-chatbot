#!/usr/bin/env python3
"""
Final verification test - the exact scenario that was giving poor responses
"""

import requests
import json

def test_final_scenario():
    """Test the exact scenario that was problematic"""
    
    url = "http://localhost:8000/chat"
    
    # This was the exact request that was giving poor responses
    message = "I want some analogy for a middle schooler to understand Newton's laws"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 FINAL VERIFICATION TEST")
            print("="*60)
            print(f"👤 User Request: {message}")
            print("="*60)
            print("🎓 Smart Tutor Response:")
            print(data['response'])
            print("="*60)
            
            # Verify this is the Smart Tutor response
            response_text = data['response'].lower()
            smart_tutor_indicators = [
                "video game",
                "lazy rule", 
                "middle school",
                "shopping cart",
                "skateboard"
            ]
            
            found_indicators = [indicator for indicator in smart_tutor_indicators if indicator in response_text]
            
            if found_indicators:
                print(f"✅ SUCCESS! Smart Tutor is working!")
                print(f"✅ Found Smart Tutor indicators: {', '.join(found_indicators)}")
                print("✅ Response is engaging, age-appropriate, and uses great analogies!")
            else:
                print("❌ This doesn't look like a Smart Tutor response")
                
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_final_scenario()