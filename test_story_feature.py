#!/usr/bin/env python3
"""
Test the story feature - simulating the exact scenario from the screenshot
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

def test_story_conversation():
    """Test the exact conversation flow from the screenshot"""
    
    print("📚 TESTING STORY FEATURE")
    print("="*60)
    
    # Step 1: User asks about vector addition
    print("👤 User: Vector addition")
    response1 = send_message("Vector addition")
    print(f"🎓 Tutor: {response1[:100]}...")
    print("-" * 60)
    
    # Small delay to simulate real conversation
    time.sleep(1)
    
    # Step 2: User asks for analogy (this worked before)
    print("👤 User: give me any analogy to understand")
    response2 = send_message("give me any analogy to understand")
    print(f"🎓 Tutor: {response2[:100]}...")
    print("-" * 60)
    
    # Small delay
    time.sleep(1)
    
    # Step 3: User asks for story (this was failing)
    print("👤 User: can you create a short story to understand and remember")
    response3 = send_message("can you create a short story to understand and remember")
    print(f"🎓 Tutor: {response3[:100]}...")
    print("-" * 60)
    
    # Check if the third response is a story
    if "treasure" in response3.lower() or "maya" in response3.lower() or "story" in response3.lower():
        print("✅ SUCCESS: Tutor created a story about vector addition!")
    elif "Let me explain more about" in response3:
        print("❌ FAILED: Still giving generic response instead of story")
    else:
        print("⚠️  UNCLEAR: Response doesn't clearly indicate story creation")
    
    print(f"\n📊 Analysis:")
    print(f"  Story keywords in response: {'treasure' in response3.lower() or 'maya' in response3.lower()}")
    print(f"  Response length: {len(response3)} chars")

if __name__ == "__main__":
    test_story_conversation()