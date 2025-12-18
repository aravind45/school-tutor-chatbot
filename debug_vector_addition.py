#!/usr/bin/env python3
"""
Debug why "Vector addition" is giving generic template responses
"""

from smart_tutor_service import SmartTutorService

def debug_vector_addition():
    """Debug the vector addition query"""
    
    service = SmartTutorService()
    
    # Test both queries from the screenshot
    messages = [
        "Vector addition",
        "explain"
    ]
    
    for message in messages:
        print(f"🔍 Debugging: '{message}'")
        print("="*50)
        
        # Analyze the intent
        intent = service._analyze_intent(message)
        
        print("📊 Intent Analysis:")
        print(f"  Type: {intent['type']}")
        print(f"  Subject: {intent['subject']}")
        print(f"  Topic: '{intent['topic']}'")
        print(f"  Level: {intent['level']}")
        print(f"  Specific Request: {intent['specific_request']}")
        
        # Check topic extraction
        topic = service._extract_topic(message)
        print(f"🎯 Topic Extraction: '{topic}'")
        
        # Test the full response
        response = service.get_response(message)
        print(f"📝 Response: {response[:100]}...")
        
        print("="*50)
        print()

if __name__ == "__main__":
    debug_vector_addition()