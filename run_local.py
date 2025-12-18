#!/usr/bin/env python3
"""
Local Development Runner for Tutor Chatbot

This script helps you run the chatbot locally with your desktop GPU.
Choose between FastAPI (web interface) or Gradio (simple interface).
"""

import os
import sys
import subprocess
import argparse

def check_gpu():
    """Check if CUDA GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✅ GPU detected: {gpu_name}")
            print(f"   Memory: {gpu_memory:.1f} GB")
            return True
        else:
            print("⚠️  No CUDA GPU detected - will use CPU (much slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_fastapi():
    """Run the FastAPI version (web interface)"""
    print("\n🚀 Starting FastAPI server...")
    print("📱 Web interface will be available at: http://localhost:8000")
    print("🎯 API docs available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Set environment variables for local development
        os.environ["HOST"] = "127.0.0.1"
        os.environ["PORT"] = "8000"
        os.environ["MODEL_PATH"] = "tutor_model_lora"
        
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n✅ Server stopped")

def run_gradio():
    """Run the Gradio version (simple interface)"""
    print("\n🚀 Starting Gradio interface...")
    print("📱 Interface will be available at: http://localhost:7860")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Set environment variables for local development
        os.environ["MODEL_PATH"] = "tutor_model_lora"
        
        subprocess.run([sys.executable, "app_gradio.py"])
    except KeyboardInterrupt:
        print("\n✅ Server stopped")

def main():
    parser = argparse.ArgumentParser(description="Run Tutor Chatbot locally")
    parser.add_argument(
        "--interface", 
        choices=["fastapi", "gradio"], 
        default="fastapi",
        help="Choose interface type (default: fastapi)"
    )
    parser.add_argument(
        "--skip-install", 
        action="store_true",
        help="Skip dependency installation"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("🎓 Tutor Chatbot - Local Development")
    print("="*60 + "\n")
    
    # Check GPU
    has_gpu = check_gpu()
    print()
    
    # Install dependencies if needed
    if not args.skip_install:
        if not install_dependencies():
            sys.exit(1)
        print()
    
    # Run the selected interface
    if args.interface == "fastapi":
        print("🌐 Running FastAPI version (full web interface)")
        run_fastapi()
    else:
        print("🎨 Running Gradio version (simple interface)")
        run_gradio()

if __name__ == "__main__":
    main()