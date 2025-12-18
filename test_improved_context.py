#!/usr/bin/env python3
"""
Test improved conversation context functionality
"""

import requests
import json
import time

def test_improved_context():
    """Test that the model maintains conversation context better"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing IMPROVED Conversation Context")
    print("="*60)
    
    try:
        session_id = None
        
        # Test 1: Ask about vector addition
        print("\n1️⃣ First question: Explain vector addition")
        response1 = requests.post(f"{base_url}/chat", 
                                json={"message": "Explain vector addition"})
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"✅ Response: {data1['response'][:150]}...")
            session_id = data1.get('session_id')
            print(f"📝 Session ID: {session_id}")
        else:
            print(f"❌ Error: {response1.status_code}")
            return
        
        time.sleep(2)  # Brief pause
        
        # Test 2: Ask for rap (the failing case)
        print("\n2️⃣ Follow-up: any rap to remember")
        response2 = requests.post(f"{base_url}/chat", 
                                json={"message": "any rap to remember", "session_id": session_id})
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Response: {data2['response'][:300]}...")
            
            # Check if response mentions vector addition or related concepts
            response_text = data2['response'].lower()
            vector_indicators = ['vector', 'addition', 'direction', 'magnitude', 'component', 'head', 'tail']
            
            found_indicators = [ind for ind in vector_indicators if ind in response_text]
            
            if found_indicators:
                print(f"🎉 SUCCESS: Model remembered vector context! Found: {found_indicators}")
            else:
                print("⚠️ FAILURE: Model did not use vector context properly")
                print(f"Response was about: {response_text[:100]}...")
        else:
            print(f"❌ Error: {response2.status_code}")
            return
        
        time.sleep(2)  # Brief pause
        
        # Test 3: Another follow-up to test persistence
        print("\n3️⃣ Follow-up: give me an analogy")
        response3 = requests.post(f"{base_url}/chat", 
                                json={"message": "give me an analogy", "session_id": session_id})
        
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"✅ Response: {data3['response'][:300]}...")
            
            response_text = data3['response'].lower()
            if any(indicator in response_text for indicator in vector_indicators):
                print("🎉 SUCCESS: Context persisted across multiple exchanges!")
            else:
                print("⚠️ Context may have been lost")
        else:
            print(f"❌ Error: {response3.status_code}")
        
        # Test 4: New topic to test topic switching
        print("\n4️⃣ New topic: What are Newton's laws?")
        response4 = requests.post(f"{base_url}/chat", 
                                json={"message": "What are Newton's laws?", "session_id": session_id})
        
        if response4.status_code == 200:
            data4 = response4.json()
            print(f"✅ Response: {data4['response'][:150]}...")
        
        time.sleep(2)
        
        # Test 5: Follow-up on new topic
        print("\n5️⃣ Follow-up on Newton: create a rap")
        response5 = requests.post(f"{base_url}/chat", 
                                json={"message": "create a rap", "session_id": session_id})
        
        if response5.status_code == 200:
            data5 = response5.json()
            print(f"✅ Response: {data5['response'][:300]}...")
            
            response_text = data5['response'].lower()
            newton_indicators = ['newton', 'law', 'force', 'motion', 'inertia', 'acceleration']
            
            found_newton = [ind for ind in newton_indicators if ind in response_text]
            
            if found_newton:
                print(f"🎉 SUCCESS: Model switched to Newton context! Found: {found_newton}")
            else:
                print("⚠️ Model may not have switched context properly")
        
        print("\n🏁 Improved context test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure app.py is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_improved_context()