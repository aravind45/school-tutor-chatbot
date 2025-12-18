#!/usr/bin/env python3
"""
Test script for the Tutor Chatbot API

This script tests the health endpoint and chat functionality.
"""

import requests
import json
import time

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check Passed")
            print(f"   Status: {data['status']}")
            print(f"   Model Loaded: {data['model_loaded']}")
            print(f"   Device: {data['device']}")
            if 'gpu_name' in data:
                print(f"   GPU: {data['gpu_name']} ({data['gpu_memory_gb']} GB)")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_chat(message):
    """Test the chat endpoint"""
    try:
        payload = {"message": message}
        response = requests.post(
            "http://localhost:8000/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat Response Received")
            print(f"   Question: {message}")
            print(f"   Response: {data['response'][:200]}...")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return False

def main():
    print("="*60)
    print("🎓 Tutor Chatbot API Test")
    print("="*60)
    print()
    
    # Test health endpoint
    print("1. Testing Health Endpoint...")
    if not test_health():
        print("\n❌ Server is not running or not healthy")
        print("   Start the server with: python app.py")
        return
    
    print("\n2. Testing Chat Functionality...")
    
    # Test questions
    test_questions = [
        "What is photosynthesis?",
        "Explain Newton's first law of motion",
        "What is the Pythagorean theorem?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Test {i}: {question}")
        if test_chat(question):
            time.sleep(1)  # Brief pause between requests
        else:
            break
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("Your tutor chatbot is ready to use at: http://localhost:8000")

if __name__ == "__main__":
    main()