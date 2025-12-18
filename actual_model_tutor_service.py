#!/usr/bin/env python3
"""
Actual Model Tutor Service - Uses the trained model instead of hard-coded responses
This is what we should have been using all along!
"""

import torch
import logging
from typing import Optional
from unsloth import FastLanguageModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActualModelTutorService:
    """Uses the actual trained model for tutoring responses with conversation context"""
    
    def __init__(self, model_path: str = "tutor_model_massive/checkpoint-100"):
        """Initialize with the trained model"""
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_seq_length = 2048
        
        # Conversation context tracking
        self.conversation_history = []
        self.current_topic = None
        self.last_response = None
        
        logger.info(f"Initializing Actual Model Tutor Service on {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the trained model"""
        try:
            logger.info(f"Loading trained model from {self.model_path}...")
            
            # Load the fine-tuned model using Unsloth
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=self.model_path,
                max_seq_length=self.max_seq_length,
                dtype=None,  # Auto-detect
                load_in_4bit=True,
            )
            
            # Enable fast inference mode
            FastLanguageModel.for_inference(self.model)
            
            logger.info("✅ Trained model loaded successfully!")
            logger.info(f"Device: {self.device}")
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
                logger.info(f"GPU: {gpu_name} ({gpu_memory:.1f} GB)")
            
        except Exception as e:
            logger.error(f"Failed to load trained model: {str(e)}")
            logger.error("This means the training didn't complete or model files are missing")
            raise e
    
    def format_prompt(self, user_message: str) -> str:
        """Format user message with conversation context"""
        user_message = (user_message or "").strip()
        
        # Check if this is a follow-up question
        if self._is_follow_up(user_message) and self.conversation_history:
            # Include recent conversation context with explicit topic
            context = self._build_context()
            current_topic = self.current_topic or "the previous topic"
            
            prompt = (
                "### Instruction:\n"
                f"You are continuing a conversation about {current_topic}. "
                f"The user is asking for a follow-up response related to this topic.\n\n"
                f"Recent conversation:\n{context}\n\n"
                f"User's follow-up request: {user_message}\n\n"
                f"Please provide a response about {current_topic} that addresses their request.\n\n"
                "### Response:\n"
            )
        else:
            # Regular question without context
            prompt = (
                "### Instruction:\n"
                f"{user_message}\n\n"
                "### Response:\n"
            )
        
        return prompt
    
    def _is_follow_up(self, message: str) -> bool:
        """Check if this is a follow-up question"""
        follow_up_indicators = [
            # Explicit follow-up requests
            'give me analogy', 'analogy', 'example', 'explain more',
            'tell me more', 'help me understand', 'show me', 'can you',
            
            # Creative content requests
            'create a story', 'short story', 'make a story', 'tell a story',
            'give me a story', 'story to', 'help me remember',
            'rap song', 'song', 'poem', 'rhyme', 'give me short',
            'make a rap', 'create a rap', 'write a song', 'any rap',
            
            # Continuation indicators
            'what about', 'how about', 'also', 'and', 'but what if', 'what if',
            'follow up', 'continue', 'more details', 'elaborate',
            
            # Short requests that likely refer to previous context
            'any', 'some', 'another', 'different', 'more'
        ]
        message_lower = message.lower().strip()
        
        # Check for exact matches and partial matches
        for indicator in follow_up_indicators:
            if indicator in message_lower:
                return True
        
        # Special case: very short messages are likely follow-ups
        if len(message_lower.split()) <= 3 and any(word in message_lower for word in ['rap', 'song', 'story', 'analogy', 'example']):
            return True
            
        return False
    
    def _build_context(self) -> str:
        """Build conversation context from recent history"""
        if not self.conversation_history:
            return ""
        
        # Get last 2 exchanges for context (more focused)
        recent_history = self.conversation_history[-2:]
        context_parts = []
        
        for exchange in recent_history:
            # Include more context but focus on key information
            user_msg = exchange['user']
            assistant_msg = exchange['assistant']
            
            # Keep more of the assistant response for better context
            if len(assistant_msg) > 400:
                assistant_msg = assistant_msg[:400] + "..."
            
            context_parts.append(f"User asked: {user_msg}")
            context_parts.append(f"Assistant explained: {assistant_msg}")
        
        return "\n".join(context_parts)
    
    def _extract_topic(self, user_message: str) -> str:
        """Extract the main topic from user message"""
        message_lower = user_message.lower()
        
        # Physics topics
        if any(word in message_lower for word in ['vector', 'addition', 'component']):
            return 'vector addition'
        elif any(word in message_lower for word in ['newton', 'law', 'force', 'motion']):
            return 'newton laws'
        elif any(word in message_lower for word in ['energy', 'work', 'power', 'kinetic', 'potential']):
            return 'energy'
        elif any(word in message_lower for word in ['projectile', 'motion', 'trajectory']):
            return 'projectile motion'
        elif any(word in message_lower for word in ['speed', 'velocity', 'acceleration']):
            return 'kinematics'
        
        # Chemistry topics
        elif any(word in message_lower for word in ['ph', 'acid', 'base', 'hydrogen']):
            return 'acids and bases'
        elif any(word in message_lower for word in ['molarity', 'concentration', 'solution']):
            return 'solutions'
        elif any(word in message_lower for word in ['bond', 'ionic', 'covalent', 'electron']):
            return 'chemical bonding'
        
        return 'general'
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response using the trained model"""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_seq_length,
                padding=True
            ).to(self.device)
            
            # Generate response
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
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the response part (after "### Response:")
            if "### Response:" in response:
                response = response.split("### Response:")[-1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            return f"I apologize, but I encountered an error processing your question: '{prompt}'. Please try rephrasing your question."
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """Main method to get tutoring response with conversation context"""
        try:
            # Extract topic for context tracking
            topic = self._extract_topic(user_message)
            if topic != 'general':
                self.current_topic = topic
            
            # Check if this is a follow-up
            is_followup = self._is_follow_up(user_message)
            
            # Debug logging
            logger.info(f"User message: '{user_message}'")
            logger.info(f"Detected topic: {topic}")
            logger.info(f"Current topic: {self.current_topic}")
            logger.info(f"Is follow-up: {is_followup}")
            logger.info(f"Conversation history length: {len(self.conversation_history)}")
            
            # Format the prompt with context
            prompt = self.format_prompt(user_message)
            
            # Log the prompt being sent to model (truncated)
            logger.info(f"Prompt preview: {prompt[:200]}...")
            
            # Generate response using trained model
            response = self.generate_response(prompt, max_tokens)
            
            # Clean up response
            response = response.strip()
            
            # If response is too short or seems incomplete, add helpful note
            if len(response) < 50:
                response += "\n\nWould you like me to explain this topic in more detail or provide additional examples?"
            
            # Store in conversation history
            self.conversation_history.append({
                'user': user_message,
                'assistant': response,
                'topic': self.current_topic or topic
            })
            
            # Keep only last 5 exchanges to manage memory
            if len(self.conversation_history) > 5:
                self.conversation_history = self.conversation_history[-5:]
            
            self.last_response = response
            
            return response
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question about '{user_message}'. Please try again or rephrase your question."
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.current_topic = None
        self.last_response = None
        logger.info("Conversation history cleared")
    
    def is_ready(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None
    
    def get_device_info(self) -> dict:
        """Get device information"""
        info = {
            "device": self.device,
            "model_loaded": self.is_ready(),
            "approach": "Actual Trained Model",
            "model_path": self.model_path
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
        
        return info

# Test the service
if __name__ == "__main__":
    print("🧪 Testing Actual Model Tutor Service")
    print("="*50)
    
    try:
        # Initialize service
        service = ActualModelTutorService()
        
        if service.is_ready():
            print("✅ Model loaded successfully!")
            print(f"📊 Device info: {service.get_device_info()}")
            
            # Test questions
            test_questions = [
                "Explain vector addition",
                "What are Newton's laws?",
                "Give me an analogy for electric current",
                "A car accelerates from rest at 2 m/s² for 5 seconds. Find the distance traveled."
            ]
            
            for question in test_questions:
                print(f"\n❓ Question: {question}")
                print("🤖 Response:")
                response = service.get_response(question)
                print(response)
                print("-" * 50)
        
        else:
            print("❌ Model failed to load")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the training completed and model files exist")