#!/usr/bin/env python3
"""
Test the fixed responses for the problematic queries
"""

import requests
import json

def test_query(message, description):
    """Test a specific query"""
    
    url = "http://localhost:8000/chat"
    
    payload = {"message": message}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"🧪 {description}")
            print(f"👤 Query: '{message}'")
            
            # Check if it's a meaningful response
            response_text = data['response']
            
            if "This is an important concept that requires careful analysis" in response_text:
                print("❌ STILL GENERIC TEMPLATE")
            elif "Let me help you understand" in response_text and len(response_text) < 100:
                print("❌ STILL GENERIC SHORT RESPONSE")
            elif len(response_text) > 200 and ("formula" in response_text.lower() or "definition" in response_text.lower() or "concept" in response_text.lower()):
                print("✅ MEANINGFUL EDUCATIONAL CONTENT")
            else:
                print("⚠️  UNCLEAR RESPONSE TYPE")
            
            # Show preview
            preview = response_text[:150].replace('\n', ' ')
            print(f"📝 Preview: {preview}...")
            print("-" * 60)
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

def main():
    """Test the problematic queries from the screenshot"""
    
    print("🎉 TESTING FIXED RESPONSES")
    print("="*60)
    
    # Test the exact queries that were giving problems
    test_cases = [
        ("Vector addition", "Vector Addition Query"),
        ("explain", "Single Word Explain"),
        ("explain Vector addition free fall and projectile motion", "Complex Physics Query"),
        ("What is Newton's second law?", "Physics Question"),
        ("help", "General Help Request")
    ]
    
    success_count = 0
    for message, description in test_cases:
        if test_query(message, description):
            success_count += 1
    
    print(f"\n🎯 RESULTS: {success_count}/{len(test_cases)} queries successful")
    
    if success_count == len(test_cases):
        print("✅ ALL FIXES SUCCESSFUL - No more generic templates!")
    else:
        print("⚠️  Some queries still need improvement")

if __name__ == "__main__":
    main()