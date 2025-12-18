"""
Simple Model Service Layer for Tutor Chatbot (without Unsloth)

This is a fallback version that uses standard transformers library
when Unsloth is not available or compatible.
"""

import os
import logging
import torch
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelService:
    """Service for managing the tutor model and generating responses"""
    
    def __init__(self, model_path: str = "tutor_model_lora", max_seq_length: int = 2048):
        """
        Initialize the model service and load the fine-tuned model.
        
        Args:
            model_path: Path to the fine-tuned model directory
            max_seq_length: Maximum sequence length for the model
        """
        self.model_path = model_path
        self.max_seq_length = max_seq_length
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing ModelService with device: {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the fine-tuned model with standard transformers"""
        try:
            logger.info(f"Loading model from {self.model_path}...")
            
            # Check if model path exists
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model directory not found: {self.model_path}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            # Add pad token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with appropriate settings
            if self.device == "cuda":
                # Load with GPU optimizations
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True
                )
            else:
                # Load for CPU
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                )
                self.model = self.model.to(self.device)
            
            # Set to evaluation mode
            self.model.eval()
            
            logger.info("✅ Model loaded successfully")
            logger.info(f"Device: {self.device}")
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
                logger.info(f"GPU: {gpu_name} ({gpu_memory:.1f} GB)")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            # Try loading base model as fallback
            logger.info("Attempting to load base model as fallback...")
            try:
                self._load_base_model()
            except Exception as e2:
                logger.error(f"Failed to load base model: {str(e2)}")
                raise
    
    def _load_base_model(self):
        """Load base Llama model as fallback"""
        base_model_name = "microsoft/DialoGPT-medium"  # Smaller fallback model
        
        logger.info(f"Loading fallback model: {base_model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        )
        self.model = self.model.to(self.device)
        self.model.eval()
        
        logger.info("✅ Fallback model loaded successfully")
    
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
            raise
    
    def cleanup_response(self, raw_output: str) -> str:
        """
        Extract and clean the response portion from the full model output.
        
        The model output includes the prompt, so we need to extract just the response.
        
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
        # (this shouldn't happen with properly formatted prompts)
        return raw_output.strip()
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """
        High-level method to get a response for a user message.
        
        This combines formatting, generation, and cleanup into one call.
        
        Args:
            user_message: The user's question or instruction
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Cleaned response text ready to display to the user
        """
        try:
            # Format the prompt
            prompt = self.format_prompt(user_message)
            
            # Generate the response
            raw_response = self.generate_response(prompt, max_tokens)
            
            # Clean up and extract the response
            cleaned_response = self.cleanup_response(raw_response)
            
            # If response is empty or too short, provide a fallback
            if not cleaned_response or len(cleaned_response.strip()) < 10:
                cleaned_response = f"I understand you're asking about: {user_message}. Let me help you with that. This is a demonstration response since the full model isn't loaded yet."
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question about '{user_message}'. Please try again or rephrase your question."
    
    def is_ready(self) -> bool:
        """Check if the model is loaded and ready for inference"""
        return self.model is not None and self.tokenizer is not None
    
    def get_device_info(self) -> dict:
        """Get information about the device being used"""
        info = {
            "device": self.device,
            "model_loaded": self.is_ready(),
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
        
        return info