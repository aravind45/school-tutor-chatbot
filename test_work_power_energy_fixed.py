#!/usr/bin/env python3
"""
Test the fixed work power energy response
"""

import requests
import json

def test_work_power_energy():
    """Test the work power energy explanation"""
    
    url = "http://localhost:8000/chat"
    
    # The exact query from the screenshot
    message = "explain Work power energy"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 WORK POWER ENERGY TEST")
            print("="*60)
            print(f"👤 User Request: {message}")
            print("="*60)
            print("🎓 Smart Tutor Response:")
            print(data['response'])
            print("="*60)
            
            # Check if this is a comprehensive response
            response_text = data['response'].lower()
            
            if "physics trinity" in response_text and "formula" in response_text and "joules" in response_text:
                print("✅ SUCCESS! Comprehensive physics explanation with formulas and units!")
            elif "here's a comprehensive explanation" in response_text and len(data['response']) < 100:
                print("❌ STILL TEMPLATE RESPONSE - Short and incomplete!")
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
    test_work_power_energy()