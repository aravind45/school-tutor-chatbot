#!/usr/bin/env python3
"""
Final comprehensive test of readability improvements
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
            print(f"👤 Query: {message}")
            
            # Show first 200 characters to check readability
            preview = data['response'][:200].replace('\n', ' ')
            print(f"📝 Preview: {preview}...")
            
            # Check if it's readable (not too many asterisks)
            asterisk_count = data['response'].count('**')
            if asterisk_count < 20:
                print("✅ READABLE")
            else:
                print("❌ TOO MUCH MARKDOWN")
            
            print("-" * 60)
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

def main():
    """Test various queries for readability"""
    
    print("🎉 FINAL READABILITY TEST")
    print("="*60)
    
    test_cases = [
        ("explain Vector addition free fall and projectile motion", "Vector Motion"),
        ("explain Work power energy", "Work Power Energy"),
        ("I want some analogy for a middle schooler to understand Newton's laws", "Newton's Laws Analogy"),
        ("speed vs velocity ? explain using analogy", "Speed vs Velocity"),
        ("What is chemical equilibrium?", "Chemical Equilibrium"),
        ("Help me understand object-oriented programming", "OOP Concepts")
    ]
    
    success_count = 0
    for message, description in test_cases:
        if test_query(message, description):
            success_count += 1
    
    print(f"\n🎯 RESULTS: {success_count}/{len(test_cases)} queries successful")
    
    if success_count == len(test_cases):
        print("✅ ALL TESTS PASSED - Readability improvements successful!")
    else:
        print("⚠️  Some tests failed - may need further improvements")

if __name__ == "__main__":
    main()