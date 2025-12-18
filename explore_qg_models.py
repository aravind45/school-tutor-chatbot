#!/usr/bin/env python3
"""
Explore Question Generation (QG) Models for AP Tutoring

This script explores QG models that can:
1. Generate practice questions from content
2. Create follow-up questions for deeper learning
3. Generate quiz questions for assessment
4. Support interactive tutoring dialogue
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM,
    T5ForConditionalGeneration, T5Tokenizer,
    pipeline
)
import json

def explore_qg_models():
    """Explore different Question Generation models"""
    
    print("="*70)
    print("🎯 Exploring Question Generation Models for AP Tutoring")
    print("="*70)
    
    # QG models to test (smaller ones due to disk space)
    qg_models = [
        {
            "name": "valhalla/t5-small-qg-hl",
            "description": "T5-small fine-tuned for question generation with highlight",
            "size": "Small (~60MB)",
            "use_case": "Generate questions from highlighted text"
        },
        {
            "name": "valhalla/t5-base-qg-hl", 
            "description": "T5-base fine-tuned for question generation",
            "size": "Medium (~220MB)",
            "use_case": "Better quality question generation"
        },
        {
            "name": "mrm8488/t5-base-finetuned-question-generation-ap",
            "description": "T5 fine-tuned specifically for question generation",
            "size": "Medium (~220MB)", 
            "use_case": "General question generation"
        },
        {
            "name": "potsawee/t5-large-generation-squad-QuestionAnswer",
            "description": "T5-large for question-answer generation",
            "size": "Large (~3GB)",
            "use_case": "High-quality Q&A generation"
        }
    ]
    
    # Test content for AP subjects
    test_content = {
        "physics": "Newton's second law states that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. This can be expressed as F = ma, where F is force, m is mass, and a is acceleration.",
        
        "chemistry": "Chemical equilibrium occurs when the forward and reverse reaction rates are equal. At equilibrium, the concentrations of reactants and products remain constant over time, though the reactions continue to occur at the molecular level.",
        
        "computer_science": "Object-oriented programming is based on four main principles: encapsulation, inheritance, polymorphism, and abstraction. These principles help organize code into reusable and maintainable structures."
    }
    
    for model_info in qg_models:
        model_name = model_info["name"]
        print(f"\n🔍 Testing: {model_name}")
        print(f"📝 Description: {model_info['description']}")
        print(f"📊 Size: {model_info['size']}")
        print(f"🎯 Use case: {model_info['use_case']}")
        print("-" * 60)
        
        try:
            # Load model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            print("✅ Model loaded successfully")
            
            # Test question generation for each subject
            for subject, content in test_content.items():
                print(f"\n📚 Testing {subject.upper()} content:")
                
                # Format input for question generation
                if "hl" in model_name:  # Highlight-based models
                    # These models expect <hl> tags around the part to generate questions about
                    input_text = f"generate question: {content}"
                else:
                    input_text = f"context: {content}"
                
                # Generate question
                inputs = tokenizer(
                    input_text,
                    return_tensors="pt",
                    max_length=512,
                    truncation=True
                )
                
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_length=100,
                        num_beams=4,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=tokenizer.pad_token_id
                    )
                
                question = tokenizer.decode(outputs[0], skip_special_tokens=True)
                print(f"   Generated question: {question}")
            
            # Check model parameters
            param_count = sum(p.numel() for p in model.parameters())
            print(f"\n📊 Model stats:")
            print(f"   Parameters: {param_count:,}")
            print(f"   Memory: ~{param_count * 4 / 1e6:.0f} MB")
            
        except Exception as e:
            print(f"❌ Failed to load {model_name}: {str(e)}")
        
        print("\n" + "="*60)

def create_qg_tutor_service():
    """Create a Question Generation-based tutor service"""
    
    print("\n🛠️  Creating QG-Based Tutor Service")
    print("="*50)
    
    qg_service_code = '''#!/usr/bin/env python3
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
        
        response = f"Let's explore {topic} using the Socratic method. I'll guide you with questions to help you discover the concepts yourself.\\n\\n"
        response += f"First, let me ask you: {questions[0] if questions else 'What do you already know about this topic?'}\\n\\n"
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
                
                response = f"Here are some practice questions about {topic}:\\n\\n"
                for i, q in enumerate(questions, 1):
                    response += f"{i}. {q}\\n"
                response += "\\nTry answering these and let me know if you need help with any of them!"
                
                return response
            
        elif any(word in message_lower for word in ["explain", "teach", "help me understand"]):
            # Use Socratic method
            topic = user_message.replace("explain", "").replace("teach me", "").replace("help me understand", "").strip()
            return self.create_socratic_dialogue(topic)
        
        else:
            # Generate questions from the user's message content
            questions = self.generate_questions(user_message, 2)
            
            response = "I can help you learn by asking questions! Based on what you've said, here are some questions to think about:\\n\\n"
            for i, q in enumerate(questions, 1):
                response += f"{i}. {q}\\n"
            response += "\\nWhat are your thoughts on these questions?"
            
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
            print(f"\\n👤 User: {scenario}")
            response = service.get_response(scenario)
            print(f"🤖 Tutor: {response}")
            print("-" * 50)
    else:
        print("❌ QG Tutor service not ready")
'''
    
    # Save the QG service
    with open("qg_tutor_service.py", "w", encoding="utf-8") as f:
        f.write(qg_service_code)
    
    print("✅ Created qg_tutor_service.py")
    print("🎯 This service uses Question Generation for interactive tutoring")

def compare_tutoring_approaches():
    """Compare different tutoring approaches"""
    
    print("\n" + "="*70)
    print("📊 Tutoring Approach Comparison")
    print("="*70)
    
    approaches = {
        "Traditional Q&A (Current)": {
            "description": "Direct answers to questions",
            "pros": ["Simple", "Direct answers", "Fast responses"],
            "cons": ["Passive learning", "No engagement", "Limited retention"],
            "example": "Q: What is F=ma? A: Newton's second law..."
        },
        
        "Question Generation Tutoring": {
            "description": "Generate questions to guide learning",
            "pros": ["Active learning", "Socratic method", "Better retention", "Engaging"],
            "cons": ["More complex", "Requires good QG model"],
            "example": "Instead of explaining F=ma, ask: 'What happens to acceleration if you double the force?'"
        },
        
        "Hybrid Approach": {
            "description": "Combine explanations with generated questions",
            "pros": ["Best of both worlds", "Flexible", "Comprehensive"],
            "cons": ["More complex to implement"],
            "example": "Explain concept, then generate follow-up questions for practice"
        }
    }
    
    for approach, details in approaches.items():
        print(f"\n🎓 {approach}")
        print(f"📝 {details['description']}")
        print("Pros:")
        for pro in details['pros']:
            print(f"  ✅ {pro}")
        print("Cons:")
        for con in details['cons']:
            print(f"  ❌ {con}")
        print(f"💡 Example: {details['example']}")
        print("-" * 60)

def create_hybrid_tutor_service():
    """Create a hybrid service combining explanations and question generation"""
    
    print("\n🔧 Creating Hybrid Tutor Service")
    print("="*40)
    
    hybrid_code = '''#!/usr/bin/env python3
"""
Hybrid Tutor Service

Combines explanations with question generation for optimal learning:
1. Provides clear explanations when asked
2. Generates follow-up questions for practice
3. Uses Socratic method for deeper understanding
4. Creates quizzes and assessments
"""

from qg_tutor_service import QGTutorService
import re

class HybridTutorService:
    """Hybrid tutoring service combining explanations and QG"""
    
    def __init__(self):
        self.qg_service = QGTutorService()
        
        # Knowledge base for explanations
        self.knowledge_base = {
            "newton's second law": {
                "explanation": """Newton's Second Law states that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.

**Mathematical Form:** F = ma
- F = Net force (Newtons)
- m = Mass (kg) 
- a = Acceleration (m/s²)

**Key Insights:**
- More force → More acceleration
- More mass → Less acceleration (for same force)
- Force and acceleration are in the same direction

**Real-world Examples:**
- Pushing a shopping cart: harder to accelerate when full (more mass)
- Car acceleration: more powerful engine (more force) = faster acceleration""",
                
                "follow_up_questions": [
                    "If you double the force on an object, what happens to its acceleration?",
                    "Why is it harder to push a full shopping cart than an empty one?",
                    "How would the acceleration change if you used the same force on a bowling ball vs a tennis ball?"
                ]
            },
            
            "chemical equilibrium": {
                "explanation": """Chemical equilibrium occurs when the forward and reverse reaction rates become equal, resulting in constant concentrations of reactants and products.

**Key Characteristics:**
- Dynamic process (reactions still occurring)
- Constant concentrations (no net change)
- Can be disturbed by changing conditions

**Le Chatelier's Principle:**
When a system at equilibrium is disturbed, it shifts to counteract the disturbance.

**Factors affecting equilibrium:**
- Concentration changes
- Temperature changes  
- Pressure changes (for gases)
- Catalysts (affect rate, not position)""",
                
                "follow_up_questions": [
                    "What happens to equilibrium if you add more reactants?",
                    "How does temperature affect the equilibrium position?",
                    "Why don't catalysts change the equilibrium position?"
                ]
            }
        }
    
    def get_explanation(self, topic: str) -> str:
        """Get detailed explanation of a topic"""
        topic_lower = topic.lower()
        
        for key, content in self.knowledge_base.items():
            if key in topic_lower or any(word in topic_lower for word in key.split()):
                return content["explanation"]
        
        # Fallback for topics not in knowledge base
        return f"I'd be happy to help you understand {topic}. Let me guide you through it with some questions to help you discover the concepts yourself."
    
    def get_follow_up_questions(self, topic: str) -> list:
        """Get follow-up questions for a topic"""
        topic_lower = topic.lower()
        
        for key, content in self.knowledge_base.items():
            if key in topic_lower or any(word in topic_lower for word in key.split()):
                return content["follow_up_questions"]
        
        # Generate questions using QG model
        return self.qg_service.generate_questions(topic, 3)
    
    def get_response(self, user_message: str) -> str:
        """Main response method - hybrid approach"""
        
        message_lower = user_message.lower()
        
        # Determine user intent
        if any(word in message_lower for word in ["explain", "what is", "define", "describe"]):
            # User wants explanation
            topic = self._extract_topic(user_message)
            explanation = self.get_explanation(topic)
            follow_ups = self.get_follow_up_questions(topic)
            
            response = explanation + "\\n\\n"
            response += "**Practice Questions:**\\n"
            for i, question in enumerate(follow_ups, 1):
                response += f"{i}. {question}\\n"
            response += "\\nTry answering these questions to test your understanding!"
            
            return response
            
        elif any(word in message_lower for word in ["question", "quiz", "practice", "test"]):
            # User wants questions/practice
            return self.qg_service.get_response(user_message)
            
        elif any(word in message_lower for word in ["help", "understand", "confused"]):
            # Use Socratic method
            topic = self._extract_topic(user_message)
            return self.qg_service.create_socratic_dialogue(topic)
            
        else:
            # Default: provide explanation with questions
            explanation = self.get_explanation(user_message)
            questions = self.qg_service.generate_questions(user_message, 2)
            
            response = explanation + "\\n\\n"
            response += "**Think about this:**\\n"
            for i, question in enumerate(questions, 1):
                response += f"{i}. {question}\\n"
            
            return response
    
    def _extract_topic(self, message: str) -> str:
        """Extract the main topic from user message"""
        # Remove common question words
        topic = re.sub(r'\\b(explain|what is|define|describe|help me understand|tell me about)\\b', '', message, flags=re.IGNORECASE)
        return topic.strip()
    
    def is_ready(self) -> bool:
        """Check if service is ready"""
        return self.qg_service.is_ready()

# Test the hybrid service
if __name__ == "__main__":
    print("🔬 Testing Hybrid Tutor Service")
    print("="*40)
    
    service = HybridTutorService()
    
    if service.is_ready():
        test_cases = [
            "Explain Newton's second law",
            "What is chemical equilibrium?", 
            "I'm confused about object-oriented programming",
            "Generate practice questions about physics"
        ]
        
        for test in test_cases:
            print(f"\\n👤 Student: {test}")
            response = service.get_response(test)
            print(f"🎓 Tutor: {response[:200]}...")
            print("-" * 50)
    else:
        print("❌ Hybrid service not ready")
'''
    
    with open("hybrid_tutor_service.py", "w", encoding="utf-8") as f:
        f.write(hybrid_code)
    
    print("✅ Created hybrid_tutor_service.py")
    print("🎯 Combines explanations with question generation")

def main():
    """Main function"""
    
    print("🎯 Exploring Question Generation Models for AP Tutoring")
    print("This approach focuses on active learning through questions\\n")
    
    # Explore QG models
    explore_qg_models()
    
    # Create services
    create_qg_tutor_service()
    create_hybrid_tutor_service()
    
    # Compare approaches
    compare_tutoring_approaches()
    
    print("\\n" + "="*70)
    print("🎯 RECOMMENDATIONS FOR QG-BASED TUTORING")
    print("="*70)
    
    print("\\n1. **Start with QG Tutor Service:**")
    print("   - Run: python qg_tutor_service.py")
    print("   - Uses small, fast QG models")
    print("   - Focuses on active learning through questions")
    
    print("\\n2. **Upgrade to Hybrid Service:**")
    print("   - Combines explanations with question generation")
    print("   - Best of both worlds approach")
    print("   - More comprehensive tutoring experience")
    
    print("\\n3. **Benefits of QG Approach:**")
    print("   - ✅ Active learning (better retention)")
    print("   - ✅ Socratic method teaching")
    print("   - ✅ Engaging and interactive")
    print("   - ✅ Generates unlimited practice questions")
    print("   - ✅ No training required")
    
    print("\\n4. **Integration with Current System:**")
    print("   - Replace model_service.py with qg_tutor_service.py")
    print("   - Update app.py to use new service")
    print("   - Test with AP-level content")
    
    print("\\n💡 **QG models could be the perfect solution!**")
    print("They provide interactive, engaging tutoring without training issues.")

if __name__ == "__main__":
    main()