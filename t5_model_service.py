#!/usr/bin/env python3
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
        print(f"\nQ: {question}")
        response = service.get_response(question)
        print(f"A: {response}")
        print("-" * 50)
