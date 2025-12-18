#!/usr/bin/env python3
"""
Debug why "speed vs velocity ? explain using analogy" gives template response
"""

from smart_tutor_service import SmartTutorService

def debug_speed_velocity_intent():
    """Debug the intent analysis for the speed vs velocity query"""
    
    service = SmartTutorService()
    
    # The exact message that's causing the template response
    message = "speed vs velocity ? explain using analogy"
    
    print("🔍 Debugging Speed vs Velocity Intent Analysis")
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
    
    # Check topic extraction specifically
    topic_extracted = service._extract_topic(message)
    print(f"🎯 Topic Extraction: '{topic_extracted}'")
    
    # Check if speed/velocity would be detected
    topic_lower = topic_extracted.lower()
    print(f"🔍 Topic (lowercase): '{topic_lower}'")
    print(f"🧪 Contains 'speed': {'speed' in topic_lower}")
    print(f"🧪 Contains 'velocity': {'velocity' in topic_lower}")
    
    # Test the analogy creation
    print("\n🧪 Testing Analogy Creation:")
    if intent['type'] == 'analogy_request':
        print("✅ Detected as analogy request")
        response = service._create_analogy_response(intent)
        print(f"📝 Response preview: {response[:200]}...")
        
        if "speedometer" in response.lower() or "gps" in response.lower():
            print("✅ Contains good speed/velocity analogy - SUCCESS!")
        elif "analogy would be customized" in response:
            print("❌ Generic template response - PROBLEM!")
        else:
            print("⚠️  Unknown response type")
    else:
        print(f"❌ Not detected as analogy request, detected as: {intent['type']}")

if __name__ == "__main__":
    debug_speed_velocity_intent()