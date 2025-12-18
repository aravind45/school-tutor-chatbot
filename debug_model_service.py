#!/usr/bin/env python3
"""
Debug the model service to see which service is being used
"""

from model_service import ModelService
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)

def test_model_service():
    """Test which service is being used"""
    
    print("🔍 Testing Model Service Initialization")
    print("="*50)
    
    # Initialize model service
    service = ModelService()
    
    print(f"✅ Service initialized")
    print(f"📊 Device info: {service.get_device_info()}")
    print(f"🔧 Ready: {service.is_ready()}")
    
    # Check which service is being used
    if hasattr(service, 'use_smart_tutor') and service.use_smart_tutor:
        print("🧠 Using Smart Tutor Service")
        if hasattr(service, 'smart_tutor') and service.smart_tutor:
            print("✅ Smart Tutor instance exists")
        else:
            print("❌ Smart Tutor instance missing")
    else:
        print("❌ Not using Smart Tutor Service")
    
    # Test a response
    print("\n🧪 Testing Response:")
    message = "I want some analogy for a middle schooler to understand Newton's laws"
    response = service.get_response(message)
    
    print(f"👤 User: {message}")
    print(f"🎓 Response: {response[:200]}...")
    
    # Check if it's the Smart Tutor response
    if "video game" in response.lower() or "lazy rule" in response.lower():
        print("✅ SMART TUTOR RESPONSE DETECTED!")
    else:
        print("❌ OLD SERVICE RESPONSE")

if __name__ == "__main__":
    test_model_service()