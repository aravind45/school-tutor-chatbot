import os
import glob


def find_llama_models():
    """Search for Llama model files"""

    possible_extensions = ['.bin', '.gguf', '.safetensors', '.pth', '.pt']
    found_models = []

    # Search in common locations
    search_paths = [
        os.path.expanduser("~"),  # Home directory
        os.path.expanduser("~/.cache/huggingface/hub"),
        os.path.expanduser("~/.ollama/models"),
        "/opt",  # Linux only
        "C:\\",  # Windows only
    ]

    print("🔍 Searching for Llama models...")

    for search_path in search_paths:
        if os.path.exists(search_path):
            print(f"\nChecking: {search_path}")

            # Search for model files
            for ext in possible_extensions:
                pattern = os.path.join(search_path, f"**/*{ext}")
                try:
                    for file in glob.glob(pattern, recursive=True):
                        # Check if it looks like a model file (larger than 1MB)
                        if os.path.getsize(file) > 1024 * 1024:
                            print(f"  Found: {file}")
                            found_models.append(file)
                except:
                    pass

    return found_models


if __name__ == "__main__":
    models = find_llama_models()

    if models:
        print("\n✅ Found models:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
    else:
        print("\n❌ No models found. Try downloading one first.")