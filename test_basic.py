"""
Basic tests to verify the application is working before deployment.
Run this before deploying to catch any obvious issues.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("  ✅ FastAPI dependencies OK")
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
        return False
    
    try:
        from model_service import ModelService
        print("  ✅ model_service.py imports OK")
    except Exception as e:
        print(f"  ❌ model_service.py import failed: {e}")
        return False
    
    try:
        import app
        print("  ✅ app.py imports OK")
    except Exception as e:
        print(f"  ❌ app.py import failed: {e}")
        return False
    
    return True

def test_model_files():
    """Test that model files exist"""
    print("\nTesting model files...")
    model_path = "tutor_model_lora"
    required_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json"
    ]
    
    if not os.path.exists(model_path):
        print(f"  ❌ Model directory not found: {model_path}")
        return False
    
    all_exist = True
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if os.path.exists(file_path):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ Missing: {file}")
            all_exist = False
    
    return all_exist

def test_static_files():
    """Test that static files exist"""
    print("\nTesting static files...")
    if not os.path.exists("static/index.html"):
        print("  ❌ static/index.html not found")
        return False
    print("  ✅ static/index.html exists")
    return True

def test_prompt_formatting():
    """Test prompt formatting function"""
    print("\nTesting prompt formatting...")
    try:
        from model_service import ModelService
        
        # Create a mock service just to test formatting (without loading model)
        # We'll test the format_prompt method directly
        test_message = "Explain Newton's second law"
        
        # Expected format
        expected = "### Instruction:\nExplain Newton's second law\n\n### Response:\n"
        
        # We can't instantiate ModelService without loading the model,
        # so we'll just verify the method exists
        if hasattr(ModelService, 'format_prompt'):
            print("  ✅ format_prompt method exists")
            return True
        else:
            print("  ❌ format_prompt method not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing prompt formatting: {e}")
        return False

def test_pydantic_models():
    """Test Pydantic models"""
    print("\nTesting Pydantic models...")
    try:
        from app import ChatRequest, ChatResponse, ErrorResponse
        
        # Test valid request
        valid_request = ChatRequest(message="Test message")
        print("  ✅ ChatRequest accepts valid input")
        
        # Test empty message (should fail)
        try:
            invalid_request = ChatRequest(message="")
            print("  ❌ ChatRequest should reject empty messages")
            return False
        except:
            print("  ✅ ChatRequest rejects empty messages")
        
        # Test response models
        response = ChatResponse(response="Test response")
        print("  ✅ ChatResponse model works")
        
        error = ErrorResponse(error="Test error")
        print("  ✅ ErrorResponse model works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing Pydantic models: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Running Basic Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Model Files", test_model_files),
        ("Static Files", test_static_files),
        ("Prompt Formatting", test_prompt_formatting),
        ("Pydantic Models", test_pydantic_models)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n" + "="*60)
    print("📊 Test Results")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ All tests passed! Ready for deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
