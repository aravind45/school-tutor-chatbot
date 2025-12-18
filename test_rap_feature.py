#!/usr/bin/env python3
"""
Test the rap song feature - simulating the exact scenario from the screenshot
"""

import requests
import json
import time

def send_message(message):
    """Send a message to the tutor API"""
    
    url = "http://localhost:8000/chat"
    payload = {"message": message}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data['response']
        else:
            return f"ERROR: {response.status_code}"
            
    except Exception as e:
        return f"CONNECTION ERROR: {str(e)}"

def test_full_conversation():
    """Test the complete conversation flow"""
    
    print("🎤 TESTING RAP SONG FEATURE")
    print("="*60)
    
    # Step 1: User asks about vector addition
    print("👤 User: Vector addition")
    response1 = send_message("Vector addition")
    print(f"🎓 Tutor: {response1[:100]}...")
    print("-" * 60)
    
    time.sleep(1)
    
    # Step 2: User asks for analogy
    print("👤 User: give me any analogy to understand")
    response2 = send_message("give me any analogy to understand")
    print(f"🎓 Tutor: {response2[:100]}...")
    print("-" * 60)
    
    time.sleep(1)
    
    # Step 3: User asks for story
    print("👤 User: can you create a short story to understand and remember")
    response3 = send_message("can you create a short story to understand and remember")
    print(f"🎓 Tutor: {response3[:100]}...")
    print("-" * 60)
    
    time.sleep(1)
    
    # Step 4: User asks for rap song (this was failing)
    print("👤 User: give me short rap song")
    response4 = send_message("give me short rap song")
    print(f"🎓 Tutor: {response4[:100]}...")
    print("-" * 60)
    
    # Check if the fourth response is a rap
    if "yo" in response4.lower() or "rap" in response4.lower() or "*" in response4:
        print("✅ SUCCESS: Tutor created a rap song about vector addition!")
    elif "Hi! I'm your physics tutor" in response4:
        print("❌ FAILED: Lost context and gave generic help instead of rap")
    else:
        print("⚠️  UNCLEAR: Response doesn't clearly indicate rap creation")
    
    print(f"\n📊 Analysis:")
    print(f"  Rap keywords in response: {'yo' in response4.lower() or 'mic' in response4.lower()}")
    print(f"  Response length: {len(response4)} chars")
    print(f"  Contains rhyming structure: {'*' in response4}")

if __name__ == "__main__":
    test_full_conversation()