#!/usr/bin/env python3
"""
Quick start script for running the tutor chatbot locally.

This script checks prerequisites and starts the server.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.10 or higher"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_cuda():
    """Check if CUDA is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            return True
        else:
            print("⚠️  CUDA not available - will use CPU (slower)")
            return True
    except ImportError:
        print("⚠️  PyTorch not installed - will install dependencies")
        return True

def check_model_files():
    """Check if model files exist"""
    model_path = "tutor_model_lora"
    required_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "tokenizer.json"
    ]
    
    if not os.path.exists(model_path):
        print(f"❌ Model directory not found: {model_path}")
        return False
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(model_path, file)):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing model files: {', '.join(missing_files)}")
        return False
    
    print(f"✅ Model files found in {model_path}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "torch",
        "transformers"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    print("✅ All dependencies installed")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n" + "="*60)
    print("🚀 Starting Tutor Chatbot Server")
    print("="*60)
    print("\nServer will be available at: http://localhost:7860")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")

def main():
    """Main function"""
    print("="*60)
    print("🎓 Tutor Chatbot - Startup Check")
    print("="*60 + "\n")
    
    # Run checks
    checks = [
        ("Python Version", check_python_version),
        ("CUDA/GPU", check_cuda),
        ("Model Files", check_model_files),
        ("Dependencies", check_dependencies)
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
            break
        print()
    
    if not all_passed:
        print("\n❌ Startup checks failed. Please fix the issues above.")
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
