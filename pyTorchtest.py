import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")

# Test if unsloth can import
try:
    from unsloth import FastLanguageModel
    print("✓ Unsloth imported successfully!")
except Exception as e:
    print(f"✗ Unsloth import failed: {e}")