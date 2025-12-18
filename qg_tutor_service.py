#!/usr/bin/env python3
"""
Question Generation Tutor Service

This service uses QG models to create an interactive tutoring experience:
1. Generate practice questions from content
2. Create follow-up questions for deeper understanding
3. Generate quiz questions for assessment
4. Support Socratic method teaching
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QGTutorService:
    """Question Generation-based tutoring service"""
    
    def __init__(self, qg_model: str = "valhalla/t5-small-qg-hl"):
        self.qg_model_name = qg_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.qg_model = None
        self.qg_tokenizer = None
        
        logger.info(f"Initializing QG Tutor with {qg_model}")
        self._load_models()
    
    def _load_models(self):
        """Load QG model"""
        try:
            logger.info(f"Loading QG model: {self.qg_model_name}")
            
            self.qg_tokenizer = AutoTokenizer.from_pretrained(self.qg_model_name)
            self.qg_model = AutoModelForSeq2SeqLM.from_pretrained(
                self.qg_model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            if self.device == "cpu":
                self.qg_model = self.qg_model.to(self.device)
            
            logger.info(f"✅ QG model loaded on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load QG model: {str(e)}")
            self.qg_model = None
            self.qg_tokenizer = None
    
    def generate_questions(self, content: str, num_questions: int = 3) -> list:
        """Generate practice questions from content"""
        
        if not self.qg_model or not self.qg_tokenizer:
            return ["Sorry, question generation is not available."]
        
        try:
            # Split content into sentences for better question generation
            sentences = re.split(r'[.!?]+', content)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            questions = []
            
            for sentence in sentences[:num_questions]:
                # Format for question generation
                if "hl" in self.qg_model_name:
                    input_text = f"generate question: {sentence}"
                else:
                    input_text = f"context: {sentence}"
                
                inputs = self.qg_tokenizer(
                    input_text,
                    return_tensors="pt",
                    max_length=512,
                    truncation=True
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = self.qg_model.generate(
                        **inputs,
                        max_length=100,
                        num_beams=4,
                        temperature=0.8,
                        do_sample=True,
                        pad_token_id=self.qg_tokenizer.pad_token_id
                    )
                
                question = self.qg_tokenizer.decode(outputs[0], skip_special_tokens=True)
                if question and len(question) > 5:
                    questions.append(question)
            
            return questions if questions else ["I couldn't generate questions from this content."]
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return ["Error generating questions. Please try again."]
    
    def create_socratic_dialogue(self, topic: str) -> str:
        """Create Socratic method dialogue for deeper learning"""
        
        # Knowledge base for different AP subjects
        knowledge_base = {
            "physics": {
                "newton's laws": "Newton's laws describe the relationship between forces and motion. The first law states that objects at rest stay at rest unless acted upon by a force.",
                "energy": "Energy is the ability to do work. It comes in many forms including kinetic, potential, thermal, and electromagnetic energy.",
                "waves": "Waves transfer energy without transferring matter. They have properties like wavelength, frequency, and amplitude."
            },
            "chemistry": {
                "equilibrium": "Chemical equilibrium occurs when forward and reverse reaction rates are equal, resulting in constant concentrations.",
                "bonding": "Chemical bonds form when atoms share or transfer electrons to achieve stable electron configurations.",
                "thermodynamics": "Thermodynamics deals with energy changes in chemical reactions and the spontaneity of processes."
            },
            "computer science": {
                "oop": "Object-oriented programming organizes code into objects that contain both data and methods that operate on that data.",
                "algorithms": "Algorithms are step-by-step procedures for solving problems efficiently.",
                "data structures": "Data structures organize and store data in ways that enable efficient access and modification."
            }
        }
        
        # Find relevant content
        topic_lower = topic.lower()
        content = ""
        
        for subject, topics in knowledge_base.items():
            for key, value in topics.items():
                if key in topic_lower or any(word in topic_lower for word in key.split()):
                    content = value
                    break
            if content:
                break
        
        if not content:
            content = f"Let's explore the topic of {topic} together."
        
        # Generate guiding questions
        questions = self.generate_questions(content, num_questions=2)
        
        response = f"Let's explore {topic} using the Socratic method. I'll guide you with questions to help you discover the concepts yourself.\n\n"
        response += f"First, let me ask you: {questions[0] if questions else 'What do you already know about this topic?'}\n\n"
        response += f"Think about this, and then I'll ask a follow-up question to deepen your understanding."
        
        return response
    
    def generate_quiz(self, content: str, num_questions: int = 5) -> dict:
        """Generate a quiz from content"""
        
        questions = self.generate_questions(content, num_questions)
        
        quiz = {
            "title": "AP Practice Quiz",
            "questions": [],
            "instructions": "Answer the following questions based on the content provided."
        }
        
        for i, question in enumerate(questions, 1):
            quiz["questions"].append({
                "number": i,
                "question": question,
                "type": "open_ended",
                "points": 1
            })
        
        return quiz
    
    def get_response(self, user_message: str) -> str:
        """Main interface - determine what type of response to give"""
        
        message_lower = user_message.lower()
        
        # Check what the user is asking for
        if any(word in message_lower for word in ["question", "quiz", "test", "practice"]):
            # User wants questions generated
            if "about" in message_lower or "on" in message_lower:
                # Extract topic
                topic = user_message.split("about")[-1].split("on")[-1].strip()
                questions = self.generate_questions(topic, 3)
                
                response = f"Here are some practice questions about {topic}:\n\n"
                for i, q in enumerate(questions, 1):
                    response += f"{i}. {q}\n"
                response += "\nTry answering these and let me know if you need help with any of them!"
                
                return response
            
        elif any(word in message_lower for word in ["explain", "teach", "help me understand"]):
            # Use Socratic method
            topic = user_message.replace("explain", "").replace("teach me", "").replace("help me understand", "").strip()
            return self.create_socratic_dialogue(topic)
        
        else:
            # Generate questions from the user's message content
            questions = self.generate_questions(user_message, 2)
            
            response = "I can help you learn by asking questions! Based on what you've said, here are some questions to think about:\n\n"
            for i, q in enumerate(questions, 1):
                response += f"{i}. {q}\n"
            response += "\nWhat are your thoughts on these questions?"
            
            return response
    
    def is_ready(self) -> bool:
        """Check if models are loaded"""
        return self.qg_model is not None and self.qg_tokenizer is not None
    
    def get_device_info(self) -> dict:
        """Get device information"""
        return {
            "device": self.device,
            "qg_model": self.qg_model_name,
            "model_loaded": self.is_ready()
        }

# Example usage and testing
if __name__ == "__main__":
    print("🎯 Testing QG Tutor Service")
    print("="*40)
    
    service = QGTutorService()
    
    if service.is_ready():
        test_scenarios = [
            "Explain Newton's second law",
            "Generate questions about chemical equilibrium", 
            "Help me understand object-oriented programming",
            "I want to practice physics problems"
        ]
        
        for scenario in test_scenarios:
            print(f"\n👤 User: {scenario}")
            response = service.get_response(scenario)
            print(f"🤖 Tutor: {response}")
            print("-" * 50)
    else:
        print("❌ QG Tutor service not ready")
