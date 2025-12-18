#!/usr/bin/env python3
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
            
            response = explanation + "\n\n"
            response += "**Practice Questions:**\n"
            for i, question in enumerate(follow_ups, 1):
                response += f"{i}. {question}\n"
            response += "\nTry answering these questions to test your understanding!"
            
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
            
            response = explanation + "\n\n"
            response += "**Think about this:**\n"
            for i, question in enumerate(questions, 1):
                response += f"{i}. {question}\n"
            
            return response
    
    def _extract_topic(self, message: str) -> str:
        """Extract the main topic from user message"""
        # Remove common question words
        topic = re.sub(r'\b(explain|what is|define|describe|help me understand|tell me about)\b', '', message, flags=re.IGNORECASE)
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
            print(f"\n👤 Student: {test}")
            response = service.get_response(test)
            print(f"🎓 Tutor: {response[:200]}...")
            print("-" * 50)
    else:
        print("❌ Hybrid service not ready")
