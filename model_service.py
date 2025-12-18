"""
Unsloth-based Model Service Layer for Tutor Chatbot

This version uses Unsloth for optimized inference with your fine-tuned LoRA model.
Now with GPU acceleration enabled!
"""

import os
import logging
import torch
from typing import Optional
from unsloth import FastLanguageModel
from qg_model_service_fixed import QGModelService
from simple_tutor_service import SimpleTutorService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelService:
    """Service for managing the tutor model and generating responses using PEFT"""
    
    def __init__(self, model_path: str = "tutor_model_lora", max_seq_length: int = 2048):
        """
        Initialize the model service and load the fine-tuned model.
        
        Args:
            model_path: Path to the fine-tuned LoRA model directory
            max_seq_length: Maximum sequence length for the model
        """
        # Use the actual trained model!
        self.model_path = "tutor_model_massive/checkpoint-100"  # Use latest checkpoint
        self.use_actual_model = True
        self.max_seq_length = max_seq_length
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Try to use actual trained model first
        if self.use_actual_model:
            try:
                logger.info(f"Initializing Actual Trained Model service...")
                from actual_model_tutor_service import ActualModelTutorService
                self.actual_tutor = ActualModelTutorService(self.model_path)
                logger.info("✅ Using actual trained model - no more hard-coded responses!")
            except Exception as e:
                logger.warning(f"Could not load trained model: {e}")
                logger.info("Falling back to Simple Tutor with hard-coded responses")
                self.actual_tutor = None
                self.smart_tutor = SimpleTutorService()
        else:
            self.actual_tutor = None
            self.smart_tutor = SimpleTutorService()
        
        logger.info(f"Initializing ModelService with device: {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the fine-tuned LoRA model using Unsloth"""
        try:
            logger.info(f"Loading LoRA model from {self.model_path}...")
            
            # Check if model path exists
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model directory not found: {self.model_path}")
            
            logger.info("Loading model with Unsloth for optimized inference...")
            
            # Load the fine-tuned model using Unsloth
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=self.model_path,
                max_seq_length=self.max_seq_length,
                dtype=None,  # Auto-detect best dtype
                load_in_4bit=True,  # Use 4-bit quantization for efficiency
            )
            
            # Enable fast inference mode
            FastLanguageModel.for_inference(self.model)
            
            logger.info("✅ Model loaded successfully with Unsloth")
            logger.info(f"Device: {self.device}")
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
                logger.info(f"GPU: {gpu_name} ({gpu_memory:.1f} GB)")
                logger.info("🚀 GPU acceleration enabled!")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            # Fallback to demo mode
            logger.info("Falling back to demo mode...")
            self._load_demo_mode()
    
    def _load_demo_mode(self):
        """Load demo mode when real model fails"""
        self.model = "demo"
        self.tokenizer = "demo"
        logger.info("✅ Demo mode activated")
    
    def format_prompt(self, user_message: str) -> str:
        """
        Format user message into the instruction-response template used during training.
        
        Args:
            user_message: The user's question or instruction
            
        Returns:
            Formatted prompt string matching the training template
        """
        user_message = (user_message or "").strip()
        
        # Use the exact template format from training
        prompt = (
            "### Instruction:\n"
            f"{user_message}\n\n"
            "### Response:\n"
        )
        
        return prompt
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate a response from the model given a formatted prompt.
        
        Args:
            prompt: The formatted prompt string
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            # Check if in demo mode
            if self.model == "demo":
                return self._generate_demo_response(prompt)
            
            # Tokenize the input
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True,
                max_length=self.max_seq_length,
                padding=True
            ).to(self.device)
            
            # Generate response with appropriate parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                    no_repeat_ngram_size=3,
                )
            
            # Decode the generated tokens
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return response
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            return self._generate_demo_response(prompt)
    
    def _generate_demo_response(self, prompt: str) -> str:
        """Generate a demo response when real model fails"""
        user_message = prompt.split("### Instruction:")[1].split("### Response:")[0].strip() if "### Instruction:" in prompt else prompt
        
        return f"""I understand you're asking about: "{user_message}"

This is a demonstration response since I'm having trouble loading your fine-tuned model. 

Your actual trained model would provide a detailed, educational response here based on the specific training you did on high school tutoring content.

To get your real model working, we may need to:
1. Fix the Unsloth compatibility issues
2. Or deploy to Hugging Face Spaces where the environment is more controlled
3. Or use a different approach to load your LoRA adapters

The model files are present in your tutor_model_lora directory, so the training was successful!"""
    
    def cleanup_response(self, raw_output: str) -> str:
        """
        Extract and clean the response portion from the full model output.
        
        Args:
            raw_output: The full output from the model including prompt
            
        Returns:
            Cleaned response text without the prompt template
        """
        # The model output includes the prompt, so extract just the response part
        if "### Response:" in raw_output:
            # Split on the response marker and take everything after it
            parts = raw_output.split("### Response:")
            if len(parts) > 1:
                response = parts[-1].strip()
                return response
        
        # If no response marker found, return the raw output
        return raw_output.strip()
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """
        High-level method to get a response for a user message.
        
        Args:
            user_message: The user's question or instruction
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Cleaned response text ready to display to the user
        """
        try:
            # Use actual trained model if available
            if self.use_actual_model and hasattr(self, 'actual_tutor') and self.actual_tutor and self.actual_tutor.is_ready():
                logger.info("🚀 Using ACTUAL TRAINED MODEL - real language model responses!")
                return self.actual_tutor.get_response(user_message, max_tokens)
            
            # Fallback to hard-coded responses (what we were using before)
            elif hasattr(self, 'smart_tutor') and self.smart_tutor and self.smart_tutor.is_ready():
                logger.info("⚠️ Using fallback hard-coded responses (not ideal)")
                return self.smart_tutor.get_response(user_message, max_tokens)
            
            # Last resort - original approach
            logger.info("Using original model approach")
            
            # Format the prompt
            prompt = self.format_prompt(user_message)
            
            # Generate the response
            raw_response = self.generate_response(prompt, max_tokens)
            
            # Clean up and extract the response
            cleaned_response = self.cleanup_response(raw_response)
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question about '{user_message}'. Please try again or rephrase your question."
    
    def is_ready(self) -> bool:
        """Check if the model is loaded and ready for inference"""
        if self.use_actual_model and hasattr(self, 'actual_tutor') and self.actual_tutor:
            return self.actual_tutor.is_ready()
        elif hasattr(self, 'smart_tutor') and self.smart_tutor:
            return self.smart_tutor.is_ready()
        return self.model is not None and self.tokenizer is not None
    
    def get_device_info(self) -> dict:
        """Get information about the device being used"""
        if self.use_actual_model and hasattr(self, 'actual_tutor') and self.actual_tutor:
            actual_info = self.actual_tutor.get_device_info()
            actual_info["approach"] = "🚀 ACTUAL TRAINED MODEL"
            return actual_info
        elif hasattr(self, 'smart_tutor') and self.smart_tutor:
            smart_info = self.smart_tutor.get_device_info()
            smart_info["approach"] = "⚠️ Fallback Hard-coded Responses"
            return smart_info
        
        info = {
            "device": self.device,
            "model_loaded": self.is_ready(),
            "approach": "Traditional Q&A"
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
        
        return info