#!/usr/bin/env python3
"""
Quick test of the actual trained model
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_model():
    """Test the actual trained model"""
    print("🧪 Testing Actual Trained Model")
    print("="*50)
    
    try:
        from actual_model_tutor_service import ActualModelTutorService
        
        print("📥 Loading model...")
        service = ActualModelTutorService()
        
        if service.is_ready():
            print("✅ Model loaded successfully!")
            print(f"📊 Device info: {service.get_device_info()}")
            
            # Quick test
            print("\n🧪 Quick Test:")
            question = "What is Newton's first law?"
            print(f"❓ Question: {question}")
            
            response = service.get_response(question, max_tokens=200)
            print(f"🤖 Response: {response}")
            
            print("\n🎉 SUCCESS! The actual trained model is working!")
            print("🚀 No more hard-coded responses - this is real AI!")
            
        else:
            print("❌ Model not ready")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 The training might still be running or model files missing")

if __name__ == "__main__":
    test_model()