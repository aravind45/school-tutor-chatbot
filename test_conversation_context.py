#!/usr/bin/env python3
"""
Test conversation context functionality
"""

import requests
import json

def test_conversation_context():
    """Test that the model maintains conversation context"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Conversation Context")
    print("="*50)
    
    try:
        # Test 1: Ask about vector addition
        print("\n1️⃣ First question: Explain vector addition")
        response1 = requests.post(f"{base_url}/chat", 
                                json={"message": "Explain vector addition"})
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"✅ Response: {data1['response'][:100]}...")
            session_id = data1.get('session_id')
            print(f"📝 Session ID: {session_id}")
        else:
            print(f"❌ Error: {response1.status_code}")
            return
        
        # Test 2: Ask for analogy (should remember vector addition context)
        print("\n2️⃣ Follow-up: Give me an analogy")
        response2 = requests.post(f"{base_url}/chat", 
                                json={"message": "Give me an analogy", "session_id": session_id})
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Response: {data2['response'][:200]}...")
            
            # Check if response mentions vector addition or related concepts
            response_text = data2['response'].lower()
            context_indicators = ['vector', 'addition', 'direction', 'magnitude', 'component']
            
            if any(indicator in response_text for indicator in context_indicators):
                print("🎉 SUCCESS: Model remembered vector addition context!")
            else:
                print("⚠️ WARNING: Model may not have used context properly")
        else:
            print(f"❌ Error: {response2.status_code}")
            return
        
        # Test 3: Ask for story (should still remember context)
        print("\n3️⃣ Follow-up: Create a story")
        response3 = requests.post(f"{base_url}/chat", 
                                json={"message": "Create a story about this", "session_id": session_id})
        
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"✅ Response: {data3['response'][:200]}...")
            
            response_text = data3['response'].lower()
            if any(indicator in response_text for indicator in ['vector', 'addition', 'story']):
                print("🎉 SUCCESS: Model maintained context across multiple exchanges!")
            else:
                print("⚠️ Model response may not be using full context")
        else:
            print(f"❌ Error: {response3.status_code}")
        
        print("\n🏁 Context test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure app.py is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_conversation_context()