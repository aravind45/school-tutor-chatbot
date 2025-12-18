#!/usr/bin/env python3
"""
GPU Check Script

This script checks if your system has a compatible GPU for running the tutor model.
"""

import sys

def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        print("🔍 Checking PyTorch and CUDA...")
        print(f"   PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("✅ CUDA is available!")
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU count: {torch.cuda.device_count()}")
            
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1e9
                print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
            return True
        else:
            print("❌ CUDA is not available")
            print("   Possible reasons:")
            print("   - No NVIDIA GPU installed")
            print("   - CUDA drivers not installed")
            print("   - PyTorch CPU-only version installed")
            return False
            
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def check_unsloth():
    """Check if Unsloth can be imported"""
    try:
        print("\n🔍 Checking Unsloth...")
        from unsloth import FastLanguageModel
        print("✅ Unsloth imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Unsloth import failed: {str(e)}")
        return False

def main():
    print("="*60)
    print("🎓 Tutor Chatbot - GPU Compatibility Check")
    print("="*60 + "\n")
    
    cuda_ok = check_cuda()
    
    if cuda_ok:
        unsloth_ok = check_unsloth()
        
        if unsloth_ok:
            print("\n🎉 Your system is ready to run the tutor chatbot!")
            print("   You can use either:")
            print("   - FastAPI version: python app.py")
            print("   - Gradio version: python app_gradio.py")
        else:
            print("\n⚠️  GPU detected but Unsloth has issues")
            print("   Try reinstalling: pip install --upgrade unsloth")
    else:
        print("\n❌ GPU not available - cannot run the tutor model locally")
        print("\n💡 Alternatives:")
        print("   1. Deploy to Hugging Face Spaces (free GPU)")
        print("   2. Use Google Colab with GPU")
        print("   3. Install CUDA drivers if you have an NVIDIA GPU")
        print("   4. Use a cloud provider with GPU instances")

if __name__ == "__main__":
    main()