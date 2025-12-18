#!/usr/bin/env python3
"""
Test the improved readable format
"""

import requests
import json

def test_readable_format():
    """Test the more readable format"""
    
    url = "http://localhost:8000/chat"
    
    # Test the vector motion query
    message = "explain Vector addition free fall and projectile motion"
    
    payload = {
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 READABLE FORMAT TEST")
            print("="*60)
            print(f"👤 User Request: {message}")
            print("="*60)
            print("🎓 Smart Tutor Response:")
            print(data['response'])
            print("="*60)
            
            # Check readability
            response_text = data['response']
            
            # Count formatting issues
            asterisk_count = response_text.count('**')
            line_breaks = response_text.count('\n')
            
            print(f"📊 Readability Analysis:")
            print(f"  - Asterisks (markdown): {asterisk_count}")
            print(f"  - Line breaks: {line_breaks}")
            print(f"  - Length: {len(response_text)} characters")
            
            if asterisk_count < 10 and line_breaks > 5:
                print("✅ IMPROVED READABILITY - Less markdown, better structure!")
            else:
                print("⚠️  Still needs formatting improvements")
                
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_readable_format()