#!/usr/bin/env python3
"""
Debug the Smart Tutor intent analysis to see why it's not detecting Newton's laws properly
"""

from smart_tutor_service import SmartTutorService

def debug_intent_analysis():
    """Debug the intent analysis for the problematic message"""
    
    service = SmartTutorService()
    
    # The exact message that's causing issues
    message = "I want some analogy for a middle schooler to understand Newton's laws"
    
    print("🔍 Debugging Smart Tutor Intent Analysis")
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
    
    # Check if Newton's laws would be detected
    topic_lower = topic_extracted.lower()
    print(f"🔍 Topic (lowercase): '{topic_lower}'")
    print(f"🧪 Contains 'newton': {'newton' in topic_lower}")
    print(f"🧪 Contains 'force': {'force' in topic_lower}")
    
    # Test the analogy creation
    print("\n🧪 Testing Analogy Creation:")
    if intent['type'] == 'analogy_request':
        print("✅ Detected as analogy request")
        response = service._create_analogy_response(intent)
        print(f"📝 Response preview: {response[:100]}...")
        
        if "video game" in response.lower():
            print("✅ Contains video game analogy - SUCCESS!")
        else:
            print("❌ Missing video game analogy - PROBLEM!")
    else:
        print(f"❌ Not detected as analogy request, detected as: {intent['type']}")

if __name__ == "__main__":
    debug_intent_analysis()