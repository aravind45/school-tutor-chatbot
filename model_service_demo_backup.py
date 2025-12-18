"""
Demo Model Service Layer for Tutor Chatbot

This is a demonstration version that provides sample responses
without loading the actual model. Perfect for testing the interface.
"""

import os
import logging
import torch
from typing import Optional
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelService:
    """Demo service for testing the tutor chatbot interface"""
    
    def __init__(self, model_path: str = "tutor_model_lora", max_seq_length: int = 2048):
        """
        Initialize the demo model service.
        
        Args:
            model_path: Path to the model directory (for demo purposes)
            max_seq_length: Maximum sequence length (for demo purposes)
        """
        self.model_path = model_path
        self.max_seq_length = max_seq_length
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing Demo ModelService with device: {self.device}")
        self._initialize_demo()
    
    def _initialize_demo(self):
        """Initialize demo responses"""
        self.demo_responses = {
            # Math responses
            "math": [
                "Great math question! Let me break this down step by step for you.",
                "Mathematics is all about understanding patterns and relationships. Here's how to approach this:",
                "This is a fundamental concept in mathematics. Let me explain it clearly:",
            ],
            # Science responses  
            "science": [
                "Excellent science question! Let me explain the underlying principles:",
                "Science helps us understand how the world works. Here's what's happening:",
                "This is a fascinating topic in science. Let me walk you through it:",
            ],
            # Literature responses
            "literature": [
                "That's a thoughtful question about literature! Let me help you analyze this:",
                "Literature allows us to explore human experiences. Here's my interpretation:",
                "This is an important theme in literature. Let me explain:",
            ],
            # History responses
            "history": [
                "Great historical question! Understanding the context is key:",
                "History helps us learn from the past. Here's what happened:",
                "This is an important event in history. Let me provide some context:",
            ],
            # General responses
            "general": [
                "That's an interesting question! Let me help you understand this topic:",
                "I'm here to help you learn. Here's my explanation:",
                "Great question! Let me break this down for you:",
            ]
        }
        
        logger.info("✅ Demo model service initialized successfully")
        
        if self.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            logger.info(f"GPU: {gpu_name} ({gpu_memory:.1f} GB)")
    
    def format_prompt(self, user_message: str) -> str:
        """
        Format user message (demo version).
        
        Args:
            user_message: The user's question or instruction
            
        Returns:
            Formatted prompt string
        """
        return f"### Instruction:\n{user_message}\n\n### Response:\n"
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate a demo response.
        
        Args:
            prompt: The formatted prompt string
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated demo response
        """
        # Simulate processing time
        time.sleep(random.uniform(1, 3))
        
        # Extract the user message from the prompt
        if "### Instruction:" in prompt:
            user_message = prompt.split("### Instruction:")[1].split("### Response:")[0].strip()
        else:
            user_message = prompt.strip()
        
        # Determine response category based on keywords
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ['math', 'equation', 'solve', 'calculate', 'algebra', 'geometry', 'calculus']):
            category = "math"
        elif any(word in user_lower for word in ['science', 'physics', 'chemistry', 'biology', 'atom', 'cell', 'force']):
            category = "science"
        elif any(word in user_lower for word in ['literature', 'book', 'poem', 'author', 'theme', 'character', 'novel']):
            category = "literature"
        elif any(word in user_lower for word in ['history', 'war', 'ancient', 'civilization', 'empire', 'revolution']):
            category = "history"
        else:
            category = "general"
        
        # Get a random response from the category
        base_response = random.choice(self.demo_responses[category])
        
        # Create a detailed response based on the question
        detailed_response = self._create_detailed_response(user_message, category)
        
        return f"{base_response}\n\n{detailed_response}"
    
    def _create_detailed_response(self, user_message: str, category: str) -> str:
        """Create a detailed demo response based on the category"""
        
        if category == "math":
            return f"""For your question about "{user_message}", here's how I would approach it:

1. **Identify the problem type**: First, let's understand what mathematical concept this involves.

2. **Break it down**: I'll solve this step-by-step to make it clear.

3. **Show the work**: Mathematics is about understanding the process, not just the answer.

4. **Check the result**: Always verify your answer makes sense.

This is a demonstration response. In the full version, I would provide specific calculations and detailed explanations tailored to your exact question."""

        elif category == "science":
            return f"""Regarding your question about "{user_message}", let me explain the scientific principles:

**Key Concepts:**
- The fundamental laws and principles involved
- How these concepts apply to real-world situations
- The relationship between different scientific phenomena

**Explanation:**
Science is about understanding cause and effect. I would explain the underlying mechanisms, provide examples, and help you see how this connects to other scientific concepts you've learned.

This is a demonstration response. The full model would provide detailed scientific explanations with examples and applications."""

        elif category == "literature":
            return f"""For your literature question about "{user_message}", here's my analysis:

**Literary Elements to Consider:**
- Theme and meaning
- Character development
- Symbolism and metaphors
- Historical and cultural context

**Analysis:**
Literature reflects human experiences and emotions. I would help you understand the deeper meanings, analyze the author's techniques, and connect the work to broader themes in literature.

This is a demonstration response. The full model would provide detailed literary analysis and interpretation."""

        elif category == "history":
            return f"""Regarding your history question about "{user_message}", let me provide context:

**Historical Context:**
- The time period and setting
- Key figures and their motivations
- Causes and consequences
- How this event fits into the broader historical narrative

**Analysis:**
History helps us understand how past events shape our present. I would explain the complex factors involved, multiple perspectives, and the lasting impact of these events.

This is a demonstration response. The full model would provide detailed historical analysis and context."""

        else:
            return f"""For your question about "{user_message}", I'm here to help you understand:

**Approach:**
- Breaking down complex topics into manageable parts
- Providing clear explanations with examples
- Connecting new information to what you already know
- Encouraging critical thinking and deeper understanding

**Learning Together:**
Education is about curiosity and discovery. I would guide you through the topic, answer follow-up questions, and help you build confidence in your understanding.

This is a demonstration response. The full model would provide comprehensive explanations tailored to your specific question."""
    
    def cleanup_response(self, raw_output: str) -> str:
        """
        Clean up the response (demo version).
        
        Args:
            raw_output: The raw response
            
        Returns:
            Cleaned response text
        """
        return raw_output.strip()
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """
        Get a demo response for a user message.
        
        Args:
            user_message: The user's question or instruction
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Demo response text
        """
        try:
            # Format the prompt
            prompt = self.format_prompt(user_message)
            
            # Generate the response
            raw_response = self.generate_response(prompt, max_tokens)
            
            # Clean up and return
            return self.cleanup_response(raw_response)
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question about '{user_message}'. Please try again or rephrase your question."
    
    def is_ready(self) -> bool:
        """Check if the demo service is ready"""
        return True
    
    def get_device_info(self) -> dict:
        """Get information about the device being used"""
        info = {
            "device": self.device,
            "model_loaded": True,  # Demo is always "loaded"
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
        
        return info