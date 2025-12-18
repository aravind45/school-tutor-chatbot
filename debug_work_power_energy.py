#!/usr/bin/env python3
"""
Debug the "explain Work power energy" query to see why it's giving incomplete response
"""

from smart_tutor_service import SmartTutorService

def debug_work_power_energy():
    """Debug the work power energy query"""
    
    service = SmartTutorService()
    
    # The exact message from the screenshot
    message = "explain Work power energy"
    
    print("🔍 Debugging Work Power Energy Query")
    print("="*60)
    print(f"👤 User Message: {message}")
    print("="*60)
    
    # Analyze the intent
    intent = service._analyze_intent(message)
    
    print("📊 Intent Analysis Results:")
    print(f"  Type: {intent['type']}")
    print(f"  Subject: {intent['subject']}")
    print(f"  Topic: '{intent['topic']}'")
    print(f"  Level: {intent['level']}")
    print(f"  Specific Request: {intent['specific_request']}")
    print("="*60)
    
    # Test the full response
    print("🧪 Testing Full Response:")
    response = service.get_response(message)
    print(f"📝 Response: {response}")
    print("="*60)
    
    # Check what method is being called
    if intent['type'] == 'explanation_request':
        print("✅ Detected as explanation request")
        if intent['level'] == 'advanced':
            print("⚠️  Using advanced explanation - this might be the template issue!")
        elif intent['level'] == 'middle_school':
            print("✅ Using middle school explanation")
    else:
        print(f"❌ Not detected as explanation request: {intent['type']}")

if __name__ == "__main__":
    debug_work_power_energy()