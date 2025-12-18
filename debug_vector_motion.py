#!/usr/bin/env python3
"""
Debug the "explain Vector addition free fall and projectile motion" query
"""

from smart_tutor_service import SmartTutorService

def debug_vector_motion():
    """Debug the vector motion query"""
    
    service = SmartTutorService()
    
    # The exact message from the screenshot
    message = "explain Vector addition free fall and projectile motion"
    
    print("🔍 Debugging Vector Motion Query")
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
    
    # Test the full response
    print("🧪 Testing Full Response:")
    response = service.get_response(message)
    print(f"📝 Response preview: {response[:200]}...")
    print("="*60)
    
    # Check if it's falling back to generic
    if "important concept that requires careful analysis" in response:
        print("❌ GENERIC FALLBACK - Need to add specific content for this topic!")
    elif "vector" in response.lower() and "projectile" in response.lower():
        print("✅ SPECIFIC CONTENT - Contains vector and projectile information!")
    else:
        print("⚠️  Unknown response type")

if __name__ == "__main__":
    debug_vector_motion()