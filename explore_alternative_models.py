#!/usr/bin/env python3
"""
Explore Alternative Models for AP Tutoring

This script explores different model architectures that might work better
for tutoring tasks, including T5, FLAN-T5, and other instruction-tuned models.
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM,
    T5ForConditionalGeneration, T5Tokenizer,
    pipeline
)
import json

def test_t5_models():
    """Test T5-based models for tutoring tasks"""
    
    print("="*60)
    print("🔬 Testing T5-Based Models for AP Tutoring")
    print("="*60)
    
    # T5 models to test
    t5_models = [
        "google/flan-t5-base",      # Instruction-tuned T5
        "google/flan-t5-large",     # Larger instruction-tuned T5
        "lmqg/t5-large-squad-qg",   # Question generation model
        "google/t5-base",           # Base T5 model
    ]
    
    test_prompts = [
        "Explain Newton's second law for AP Physics students",
        "How do I solve quadratic equations step by step?",
        "What is chemical equilibrium in AP Chemistry?",
        "Explain object-oriented programming concepts"
    ]
    
    for model_name in t5_models:
        print(f"\n📚 Testing: {model_name}")
        print("-" * 50)
        
        try:
            # Load model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Test with a sample prompt
            test_prompt = test_prompts[0]
            
            # Format for T5 (instruction format)
            if "flan" in model_name.lower():
                formatted_prompt = f"Answer this question for a high school student: {test_prompt}"
            elif "qg" in model_name.lower():
                formatted_prompt = f"Generate questions about: {test_prompt}"
            else:
                formatted_prompt = f"explain: {test_prompt}"
            
            # Generate response
            inputs = tokenizer(formatted_prompt, return_tensors="pt", max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=200,
                    num_beams=4,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            print(f"✅ Model loaded successfully")
            print(f"📝 Sample response: {response[:150]}...")
            
            # Check model size
            param_count = sum(p.numel() for p in model.parameters())
            print(f"📊 Parameters: {param_count:,}")
            print(f"💾 Memory usage: ~{param_count * 4 / 1e9:.1f} GB")
            
        except Exception as e:
            print(f"❌ Failed to load {model_name}: {str(e)}")
        
        print()

def test_other_instruction_models():
    """Test other instruction-tuned models"""
    
    print("="*60)
    print("🔬 Testing Other Instruction-Tuned Models")
    print("="*60)
    
    # Alternative models that might work better
    alternative_models = [
        "microsoft/DialoGPT-medium",    # Conversational model
        "facebook/blenderbot-400M-distill",  # Conversational AI
        "google/flan-t5-xl",           # Larger FLAN-T5
        "allenai/tk-instruct-base-def-pos",  # Instruction following
    ]
    
    test_prompt = "Explain photosynthesis for AP Biology students"
    
    for model_name in alternative_models:
        print(f"\n📚 Testing: {model_name}")
        print("-" * 50)
        
        try:
            if "dialogpt" in model_name.lower():
                # DialoGPT uses different approach
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                
                inputs = tokenizer.encode(test_prompt + tokenizer.eos_token, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = model.generate(
                        inputs,
                        max_length=150,
                        num_beams=4,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=tokenizer.pad_token_id
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
            elif "blenderbot" in model_name.lower():
                # BlenderBot
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                
                inputs = tokenizer(test_prompt, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = model.generate(**inputs, max_length=200)
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
            else:
                # T5-style models
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                
                inputs = tokenizer(f"Explain for students: {test_prompt}", return_tensors="pt", max_length=512, truncation=True)
                
                with torch.no_grad():
                    outputs = model.generate(**inputs, max_length=200, num_beams=4)
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            print(f"✅ Model loaded successfully")
            print(f"📝 Sample response: {response[:150]}...")
            
            # Check model size
            param_count = sum(p.numel() for p in model.parameters())
            print(f"📊 Parameters: {param_count:,}")
            
        except Exception as e:
            print(f"❌ Failed to load {model_name}: {str(e)}")
        
        print()

def create_t5_tutor_service():
    """Create a T5-based model service for comparison"""
    
    print("="*60)
    print("🛠️  Creating T5-Based Tutor Service")
    print("="*60)
    
    t5_service_code = '''#!/usr/bin/env python3
"""
T5-Based Model Service for AP Tutoring

Uses FLAN-T5 which is instruction-tuned and should work better
for educational content without additional training.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class T5TutorService:
    """T5-based tutoring service"""
    
    def __init__(self, model_name: str = "google/flan-t5-large"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        
        logger.info(f"Initializing T5TutorService with {model_name}")
        self._load_model()
    
    def _load_model(self):
        """Load T5 model and tokenizer"""
        try:
            logger.info(f"Loading {self.model_name}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            logger.info(f"✅ T5 model loaded successfully on {self.device}")
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"🚀 GPU: {gpu_name}")
            
        except Exception as e:
            logger.error(f"Failed to load T5 model: {str(e)}")
            self.model = None
            self.tokenizer = None
    
    def format_prompt(self, user_message: str) -> str:
        """Format user message for T5 instruction following"""
        
        # Detect subject area for better prompting
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['physics', 'force', 'motion', 'energy', 'wave']):
            subject_context = "for AP Physics students"
        elif any(word in message_lower for word in ['chemistry', 'reaction', 'molecule', 'atom', 'bond']):
            subject_context = "for AP Chemistry students"
        elif any(word in message_lower for word in ['programming', 'code', 'java', 'algorithm', 'class']):
            subject_context = "for AP Computer Science students"
        elif any(word in message_lower for word in ['math', 'equation', 'solve', 'calculate']):
            subject_context = "for high school math students"
        else:
            subject_context = "for high school students"
        
        # Format as instruction for FLAN-T5
        prompt = f"Explain this topic {subject_context} with examples and step-by-step guidance: {user_message}"
        
        return prompt
    
    def generate_response(self, user_message: str, max_tokens: int = 300) -> str:
        """Generate educational response using T5"""
        
        if self.model is None or self.tokenizer is None:
            return "I'm sorry, the tutoring model is not available right now. Please try again later."
        
        try:
            # Format the prompt
            prompt = self.format_prompt(user_message)
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_tokens,
                    num_beams=4,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I encountered an error while processing your question about '{user_message}'. Please try rephrasing your question."
    
    def get_response(self, user_message: str, max_tokens: int = 300) -> str:
        """Main interface for getting responses"""
        return self.generate_response(user_message, max_tokens)
    
    def is_ready(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None
    
    def get_device_info(self) -> dict:
        """Get device information"""
        info = {
            "device": self.device,
            "model_loaded": self.is_ready(),
            "model_name": self.model_name
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
        
        return info

# Example usage
if __name__ == "__main__":
    service = T5TutorService()
    
    test_questions = [
        "What is photosynthesis?",
        "Explain Newton's laws of motion",
        "How do I solve quadratic equations?",
        "What is object-oriented programming?"
    ]
    
    for question in test_questions:
        print(f"\\nQ: {question}")
        response = service.get_response(question)
        print(f"A: {response}")
        print("-" * 50)
'''
    
    # Save the T5 service
    with open("t5_model_service.py", "w", encoding="utf-8") as f:
        f.write(t5_service_code)
    
    print("✅ Created t5_model_service.py")
    print("📝 This service uses FLAN-T5 which is already instruction-tuned")
    print("🎯 No additional training required - should work immediately!")

def compare_model_approaches():
    """Compare different model approaches for tutoring"""
    
    print("="*60)
    print("📊 Model Approach Comparison for AP Tutoring")
    print("="*60)
    
    approaches = {
        "Current Llama + Unsloth": {
            "pros": [
                "Very powerful base model",
                "Optimized training with Unsloth",
                "Good for complex reasoning"
            ],
            "cons": [
                "Training compatibility issues on Windows",
                "Large model size (8B parameters)",
                "Requires fine-tuning for good results"
            ],
            "status": "❌ Training blocked by Triton issues"
        },
        
        "FLAN-T5 Large": {
            "pros": [
                "Already instruction-tuned",
                "No training required",
                "Good at following instructions",
                "Smaller size (780M parameters)",
                "Works well out-of-the-box"
            ],
            "cons": [
                "Smaller than Llama",
                "May need prompting optimization"
            ],
            "status": "✅ Ready to use immediately"
        },
        
        "T5 + Fine-tuning": {
            "pros": [
                "Can be fine-tuned on AP data",
                "Seq2seq architecture good for Q&A",
                "More stable training than Llama"
            ],
            "cons": [
                "Still requires training",
                "May have similar compatibility issues"
            ],
            "status": "⚠️  Needs testing"
        },
        
        "RAG with Knowledge Base": {
            "pros": [
                "Use any base model",
                "Easy to update content",
                "No training required",
                "Can use your AP content directly"
            ],
            "cons": [
                "More complex architecture",
                "Requires vector database setup"
            ],
            "status": "🔄 Alternative approach"
        }
    }
    
    for approach, details in approaches.items():
        print(f"\\n🔍 {approach}")
        print(f"Status: {details['status']}")
        print("Pros:")
        for pro in details['pros']:
            print(f"  ✅ {pro}")
        print("Cons:")
        for con in details['cons']:
            print(f"  ❌ {con}")
        print("-" * 50)

def main():
    """Main function to explore alternatives"""
    
    print("🚀 Exploring Alternative Models for AP Tutoring")
    print("This will help us find the best approach given the training issues\\n")
    
    # Test different model types
    test_t5_models()
    test_other_instruction_models()
    
    # Create T5 service
    create_t5_tutor_service()
    
    # Compare approaches
    compare_model_approaches()
    
    print("\\n" + "="*60)
    print("🎯 RECOMMENDATIONS")
    print("="*60)
    
    print("\\n1. **Immediate Solution: FLAN-T5**")
    print("   - Use google/flan-t5-large")
    print("   - Already instruction-tuned")
    print("   - No training required")
    print("   - Should give much better responses than current MMLU model")
    
    print("\\n2. **Test the T5 Service:**")
    print("   - Run: python t5_model_service.py")
    print("   - Compare responses with current model")
    print("   - If good, integrate into your app")
    
    print("\\n3. **Future Improvements:**")
    print("   - Fine-tune T5 on your AP data (more stable than Llama)")
    print("   - Implement RAG with your AP content")
    print("   - Try cloud training for Llama model")
    
    print("\\n💡 **Quick Win:** FLAN-T5 will likely give much better responses")
    print("than your current MMLU-trained model without any training!")

if __name__ == "__main__":
    main()