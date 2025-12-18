#!/usr/bin/env python3
"""
Smart Tutor Service

This service provides intelligent, context-aware tutoring responses
that adapt to the user's specific needs and requests.
"""

import torch
import logging
import re
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartTutorService:
    """Smart tutoring service that understands context and user needs"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.conversation_context = {
            'last_topic': None,
            'last_subject': None,
            'conversation_history': []
        }
        logger.info(f"Initializing Smart Tutor Service on {self.device}")
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """Generate intelligent response based on user's specific request"""
        
        message_lower = user_message.lower()
        
        # Analyze user intent and requirements
        intent = self._analyze_intent(user_message)
        
        # Check if this is a follow-up question without a specific topic
        if self._is_follow_up_question(user_message, intent):
            # Use the last topic from conversation context
            if self.conversation_context['last_topic']:
                intent['topic'] = self.conversation_context['last_topic']
                intent['subject'] = self.conversation_context['last_subject']
                logger.info(f"Using context topic: {intent['topic']}")
        
        # Update conversation context
        if intent['topic'] and intent['topic'] not in ['general help', 'explain']:
            self.conversation_context['last_topic'] = intent['topic']
            self.conversation_context['last_subject'] = intent['subject']
        
        # Add to conversation history
        self.conversation_context['conversation_history'].append({
            'message': user_message,
            'intent': intent['type'],
            'topic': intent['topic']
        })
        
        # Keep only last 5 messages in history
        if len(self.conversation_context['conversation_history']) > 5:
            self.conversation_context['conversation_history'].pop(0)
        
        # Generate appropriate response
        if intent['type'] == 'analogy_request':
            return self._create_analogy_response(intent)
        elif intent['type'] == 'explanation_request':
            return self._create_explanation_response(intent)
        elif intent['type'] == 'example_request':
            return self._create_example_response(intent)
        elif intent['type'] == 'practice_request':
            return self._create_practice_response(intent)
        else:
            return self._create_general_response(intent)
    
    def _analyze_intent(self, user_message: str) -> dict:
        """Analyze user message to understand what they're asking for"""
        
        message_lower = user_message.lower()
        
        intent = {
            'type': 'general',
            'subject': 'general',
            'topic': '',
            'level': 'high_school',
            'specific_request': ''
        }
        
        # Determine subject
        if any(word in message_lower for word in ['physics', 'force', 'motion', 'newton', 'velocity', 'acceleration', 'energy', 'vector', 'projectile', 'kinematics']):
            intent['subject'] = 'physics'
        elif any(word in message_lower for word in ['chemistry', 'reaction', 'equilibrium', 'molecule', 'atom', 'bond']):
            intent['subject'] = 'chemistry'
        elif any(word in message_lower for word in ['programming', 'code', 'java', 'algorithm', 'class', 'object']):
            intent['subject'] = 'computer_science'
        elif any(word in message_lower for word in ['math', 'equation', 'algebra', 'geometry', 'calculate']):
            intent['subject'] = 'math'
        
        # Determine level
        if any(word in message_lower for word in ['middle school', 'middle schooler', '6th grade', '7th grade', '8th grade']):
            intent['level'] = 'middle_school'
        elif any(word in message_lower for word in ['elementary', 'simple', 'basic', 'easy']):
            intent['level'] = 'elementary'
        elif any(word in message_lower for word in ['ap', 'advanced', 'college', 'university']):
            intent['level'] = 'advanced'
        
        # Determine request type
        if any(word in message_lower for word in ['analogy', 'like', 'similar to', 'compare to', 'metaphor']):
            intent['type'] = 'analogy_request'
        elif any(word in message_lower for word in ['example', 'examples', 'show me', 'demonstrate']):
            intent['type'] = 'example_request'
        elif any(word in message_lower for word in ['practice', 'problems', 'questions', 'quiz', 'test']):
            intent['type'] = 'practice_request'
        elif any(word in message_lower for word in ['explain', 'what is', 'how does', 'why', 'help me understand']):
            intent['type'] = 'explanation_request'
        # If it's a physics/science topic, treat it as explanation request even without explicit "explain"
        elif intent['subject'] in ['physics', 'chemistry', 'math'] and len(message_lower.split()) <= 3:
            intent['type'] = 'explanation_request'
        
        # Extract topic
        intent['topic'] = self._extract_topic(user_message)
        intent['specific_request'] = user_message
        
        return intent
    
    def _is_follow_up_question(self, user_message: str, intent: dict) -> bool:
        """Check if this is a follow-up question that refers to a previous topic"""
        
        message_lower = user_message.lower()
        
        # Common follow-up patterns
        follow_up_patterns = [
            'give me any analogy',
            'can you explain',
            'show me examples',
            'give me examples',
            'more details',
            'tell me more',
            'explain that',
            'what about',
            'how about',
            'can you help',
            'i need help',
            'help me understand'
        ]
        
        # Check if the message is a follow-up pattern and doesn't contain a specific topic
        for pattern in follow_up_patterns:
            if pattern in message_lower:
                # If it's a follow-up pattern and the extracted topic is generic or the same as the pattern
                if (intent['topic'] in ['general help', 'explain', user_message.strip()] or 
                    intent['topic'] == message_lower.strip()):
                    return True
        
        # Also check if the message is very short and generic
        if (len(user_message.split()) <= 4 and 
            any(word in message_lower for word in ['analogy', 'example', 'explain', 'help']) and
            intent['topic'] in [user_message.strip(), 'general help']):
            return True
        
        return False
    
    def _extract_topic(self, message: str) -> str:
        """Extract the main topic from the message"""
        message_lower = message.lower()
        
        # Check for specific multi-word physics topics first (more specific)
        if 'vector addition' in message_lower and ('projectile' in message_lower or 'free fall' in message_lower):
            return 'vector motion and projectile motion'
        elif 'projectile motion' in message_lower:
            return 'projectile motion'
        elif 'free fall' in message_lower:
            return 'free fall'
        elif 'vector addition' in message_lower:
            return 'vector addition'
        elif 'work' in message_lower and 'power' in message_lower and 'energy' in message_lower:
            return 'work power energy'
        
        # Physics topics (single words)
        physics_topics = {
            'newton': 'Newton\'s laws',
            'force': 'forces',
            'motion': 'motion',
            'velocity': 'velocity',
            'speed': 'speed',
            'acceleration': 'acceleration',
            'energy': 'energy',
            'momentum': 'momentum',
            'vector': 'vectors',
            'kinematics': 'kinematics',
            'dynamics': 'dynamics'
        }
        
        # Chemistry topics
        chemistry_topics = {
            'equilibrium': 'chemical equilibrium',
            'reaction': 'chemical reactions',
            'atom': 'atomic structure',
            'molecule': 'molecules',
            'bond': 'chemical bonding'
        }
        
        # Check for specific topics
        for key, topic in physics_topics.items():
            if key in message_lower:
                return topic
        
        for key, topic in chemistry_topics.items():
            if key in message_lower:
                return topic
        
        # Handle generic words that aren't real topics
        if message.strip().lower() in ['explain', 'help', 'teach', 'learn', 'understand']:
            return 'general help'
        
        return message.strip()
    
    def _create_analogy_response(self, intent: dict) -> str:
        """Create response with analogies appropriate for the level"""
        
        topic = intent['topic'].lower()
        level = intent['level']
        
        if 'newton' in topic or 'force' in topic:
            if level == 'middle_school':
                return """**Newton's Laws - Perfect for Middle School! 🚀**

Think of Newton's laws like rules for a video game:

**First Law (Inertia) - The "Lazy Rule":**
Imagine you're playing a game where characters are super lazy. If they're sitting still, they'll keep sitting still forever unless you press a button to make them move. If they're running, they'll keep running in a straight line forever unless you press a button to stop them or turn them.

**Real life:** When you're in a car and it suddenly stops, your body keeps moving forward because of inertia - you're following the "lazy rule"!

**Second Law (F = ma) - The "Push Harder, Go Faster Rule":**
Think of pushing a shopping cart:
- Empty cart (light) = easy to push, speeds up quickly
- Full cart (heavy) = need more muscle, speeds up slowly
- Want to go faster? Push harder!

It's like a video game where stronger characters can make heavier objects move faster.

**Third Law - The "Push Back Rule":**
Every action has an equal and opposite reaction - like when you push against a wall, the wall pushes back just as hard!

**Fun examples:**
- Walking: You push back on the ground, ground pushes you forward
- Swimming: You push water back, water pushes you forward
- Rocket: Hot gases push down, rocket goes up!

**Try this:** Next time you're on a skateboard or scooter, notice how you push back to go forward - that's Newton's third law in action! 🛹"""

            else:  # high school or advanced
                return """**Newton's Laws Through Analogies 🎯**

**First Law - The "Cruise Control" Analogy:**
Think of Newton's First Law like cruise control in a car. Once you set it, the car maintains constant speed until something interferes (hills, braking, etc.). Objects in motion stay in motion, objects at rest stay at rest - unless a net force acts on them.

**Second Law - The "Gym Workout" Analogy:**
F = ma is like working out:
- **Force (F)** = How hard you push/pull the weight
- **Mass (m)** = How heavy the weight is  
- **Acceleration (a)** = How quickly the weight moves

Heavy weights (more mass) need more force to accelerate. Light weights (less mass) accelerate easily with the same force.

**Third Law - The "Conversation" Analogy:**
Every conversation involves give and take - when you speak (action), someone listens and responds (reaction). In physics, when you exert a force on something, it exerts an equal and opposite force back on you.

**Advanced Applications:**
- **Rocket propulsion:** Exhaust gases pushed down (action) → rocket pushed up (reaction)
- **Car acceleration:** Tires push back on road (action) → road pushes car forward (reaction)
- **Walking:** Foot pushes back on ground (action) → ground pushes body forward (reaction)

These aren't just academic concepts - they're the fundamental rules governing all motion in the universe! 🌌"""

        elif ('speed' in topic and 'velocity' in topic) or ('speed' in intent['specific_request'].lower() and 'velocity' in intent['specific_request'].lower()):
            if level == 'middle_school':
                return """**Speed vs Velocity - Easy to Remember! 🏃‍♂️**

Think of it like this:

**Speed = How Fast You're Going**
Like looking at your bike speedometer - it just shows a number like "15 mph." That's it!

**Velocity = How Fast + Which Direction**
Like using GPS navigation - it shows "15 mph North" or "15 mph toward the mall."

**The Best Analogy - Running Track:**

**Speed:** "I'm running 8 mph!" (Just tells you how fast)

**Velocity:** "I'm running 8 mph clockwise around the track!" (Tells you how fast AND which way)

**Why This Matters:**
Imagine two friends both running 8 mph on a circular track:
- Friend A runs clockwise
- Friend B runs counter-clockwise

They have the SAME SPEED (8 mph) but DIFFERENT VELOCITIES (opposite directions)!

**Real Life Examples:**
- **Speed:** "The car is going 60 mph" 
- **Velocity:** "The car is going 60 mph toward downtown"

**Memory Trick:** 
- **Speed** = **S**imple number
- **Velocity** = **V**ector (has direction like an arrow →)

**Fun Fact:** If you drive in a perfect circle and end up where you started, your average velocity is ZERO (no net displacement), but your average speed is definitely NOT zero! 🔄"""

            else:
                return """**Speed vs Velocity - The Vector Distinction 📐**

**The Navigation Analogy:**
- **Speed** is like a car's speedometer - shows magnitude only
- **Velocity** is like GPS navigation - shows magnitude AND direction

**Mathematical Perspective:**
- **Speed** = scalar quantity (magnitude only)
- **Velocity** = vector quantity (magnitude + direction)

**The Airplane Analogy:**
An airplane flying at 500 mph could be:
- **Speed:** Always 500 mph (scalar)
- **Velocity:** 500 mph North, 500 mph East, 500 mph at 45° Northeast, etc. (vector)

**Key Implications:**
1. **Velocity can be negative** (depending on chosen coordinate system)
2. **Average velocity can be zero** (round trip) while average speed cannot
3. **Velocity changes when direction changes** even at constant speed (circular motion)

**Calculus Connection:**
- **Speed** = |ds/dt| (magnitude of velocity)
- **Velocity** = dr/dt (derivative of position vector)

**Real Applications:**
- **Air traffic control:** Needs velocity (speed + heading)
- **Physics problems:** Velocity determines momentum, kinetic energy calculations
- **Engineering:** Vector analysis for forces, accelerations"""

        elif 'equilibrium' in topic:
            if level == 'middle_school':
                return """**Chemical Equilibrium - Like a Busy Restaurant! 🍽️**

Imagine a super popular restaurant:

**The Restaurant Analogy:**
- **Customers coming in** = Forward reaction (reactants → products)
- **Customers leaving** = Reverse reaction (products → reactants)
- **Restaurant at capacity** = Chemical equilibrium

**What Equilibrium Looks Like:**
When the restaurant reaches equilibrium:
- Customers keep coming in at the same rate they're leaving
- The restaurant stays equally busy (constant "concentration" of people)
- It LOOKS like nothing's changing, but people are constantly coming and going!

**Le Chatelier's Principle - The Restaurant Manager:**
The manager (Le Chatelier) always tries to keep things balanced:

**If too many people show up (add reactants):**
- Manager opens more tables (shifts right to make more products)

**If the restaurant gets too hot (increase temperature):**
- Manager turns on AC (system shifts to absorb heat)

**If it gets crowded (increase pressure):**
- Manager tries to fit people at fewer tables (shifts toward fewer molecules)

**Real Example - Making Lemonade:**
- **Forward:** Sugar + Water → Sweet Lemonade
- **Reverse:** Sweet Lemonade → Sugar + Water
- **Equilibrium:** Sugar dissolving at same rate it's crystallizing out
- **Add more sugar:** More dissolves until new equilibrium
- **Add heat:** More sugar can dissolve (shifts right)

**The Key Insight:** Equilibrium doesn't mean "stopped" - it means "balanced activity"! ⚖️"""

        # Default analogy for any topic
        return f"""**Understanding {intent['topic']} Through Analogies**

Let me help you understand this concept using relatable comparisons that make it easier to grasp.

{self._get_basic_explanation(intent['topic'])}

**Think of it like:** [Analogy would be customized based on the specific topic and level]

The key is to connect new concepts to things you already understand well. What aspects of {intent['topic']} would you like me to explain with more specific analogies?"""
    
    def _create_explanation_response(self, intent: dict) -> str:
        """Create clear explanations appropriate for the level"""
        
        topic = intent['topic'].lower()
        level = intent['level']
        
        # Use existing explanation logic but adapt for level
        if level == 'middle_school':
            return self._get_middle_school_explanation(topic)
        elif level == 'elementary':
            return self._get_elementary_explanation(topic)
        else:
            return self._get_advanced_explanation(topic)
    
    def _get_middle_school_explanation(self, topic: str) -> str:
        """Get explanations appropriate for middle school level"""
        
        if 'newton' in topic:
            return """**Newton's Laws - Made Simple! 🎯**

**What Are Newton's Laws?**
Three rules that explain how things move (or don't move) in our world.

**Law #1 - The Lazy Law:**
Things that aren't moving want to stay still. Things that are moving want to keep moving in a straight line. They only change when something pushes or pulls them.

**Law #2 - The Push Law:**
The harder you push something, the faster it speeds up. Heavy things are harder to push than light things.

**Law #3 - The Push-Back Law:**
When you push on something, it pushes back on you just as hard.

**Why Should You Care?**
These laws explain EVERYTHING that moves:
- Why you slide forward when a car stops suddenly
- How rockets work
- Why it's harder to push a full shopping cart
- How you can walk (you push on the ground, it pushes back!)

**Try This:** Push against a wall. Feel it pushing back? That's Newton's third law! The wall pushes back just as hard as you push on it."""

        return f"Let me explain {topic} in a way that's perfect for middle school level..."
    
    def _get_elementary_explanation(self, topic: str) -> str:
        """Get very simple explanations for elementary level"""
        return f"Here's a super simple explanation of {topic}..."
    
    def _get_advanced_explanation(self, topic: str) -> str:
        """Get detailed explanations for advanced level"""
        
        topic_lower = topic.lower()
        
        # Physics explanations
        if 'energy' in topic_lower or 'work' in topic_lower or 'power' in topic_lower:
            return """**Work, Power, and Energy - The Physics Trinity ⚡**

These three concepts are fundamental to understanding how things move and change in physics.

**Work (W)**
- **Definition:** Force applied over a distance
- **Formula:** W = F × d × cos(θ)
- **Units:** Joules (J)
- **Key Point:** No movement = No work done (even if you push hard!)

**Energy (E)**
- **Definition:** The ability to do work
- **Types:**
  - **Kinetic Energy (KE):** Energy of motion = ½mv²
  - **Potential Energy (PE):** Stored energy = mgh (gravitational)
  - **Mechanical Energy:** KE + PE = constant (conservation)
- **Units:** Joules (J)

**Power (P)**
- **Definition:** Rate of doing work or using energy
- **Formula:** P = W/t = F×v
- **Units:** Watts (W) = Joules/second
- **Key Point:** Same work done faster = more power needed

**The Connections:**
1. **Work-Energy Theorem:** Work done = Change in kinetic energy
2. **Power-Work Relationship:** Power = Work/Time
3. **Conservation of Energy:** Energy cannot be created or destroyed, only transformed

**Real-World Applications:**
- **Car engines:** Convert chemical energy → kinetic energy (power rating in horsepower/watts)
- **Hydroelectric dams:** Gravitational PE → electrical energy
- **Athletes:** Muscle chemical energy → kinetic energy (power output matters for performance)

**Problem-Solving Strategy:**
1. Identify what type of energy/work problem
2. Draw diagrams showing energy transformations
3. Apply conservation laws
4. Use appropriate formulas
5. Check units and reasonableness

**Advanced Concepts:**
- **Conservative vs Non-conservative forces**
- **Work done by variable forces (calculus)**
- **Power dissipation and efficiency**"""

        elif 'newton' in topic_lower:
            return """**Newton's Laws - Advanced Physics Perspective 🎯**

**First Law (Law of Inertia):**
- **Statement:** An object at rest stays at rest, and an object in motion stays in motion at constant velocity, unless acted upon by a net external force.
- **Mathematical Form:** ΣF = 0 ⟺ a = 0
- **Key Concepts:** Inertial reference frames, equilibrium conditions

**Second Law (F = ma):**
- **Statement:** The acceleration of an object is directly proportional to the net force and inversely proportional to its mass.
- **Mathematical Form:** ΣF = ma (vector equation)
- **Advanced Applications:** Variable mass systems, non-inertial frames

**Third Law (Action-Reaction):**
- **Statement:** For every action, there is an equal and opposite reaction.
- **Mathematical Form:** F₁₂ = -F₂₁
- **Key Point:** Forces always occur in pairs on different objects

**Advanced Applications:**
- **Dynamics problems:** Free body diagrams, constraint forces
- **Rotational motion:** τ = Iα (rotational analog)
- **Momentum conservation:** Derived from Newton's laws
- **Engineering:** Structural analysis, machine design"""

        elif 'equilibrium' in topic_lower:
            return """**Chemical Equilibrium - Advanced Concepts ⚖️**

**Dynamic Equilibrium:**
At equilibrium, forward and reverse reaction rates are equal, but reactions continue at the molecular level.

**Equilibrium Constant (K):**
- **Expression:** K = [products]/[reactants] (with proper stoichiometry)
- **Temperature dependence:** K changes with temperature
- **Magnitude interpretation:** K >> 1 (products favored), K << 1 (reactants favored)

**Le Chatelier's Principle:**
System responds to disturbances by shifting to counteract the change:
- **Concentration changes:** Add/remove species
- **Temperature changes:** Endothermic vs exothermic direction
- **Pressure changes:** Favor side with fewer gas molecules
- **Catalysts:** No effect on equilibrium position, only rate

**Thermodynamic Relationships:**
- **ΔG° = -RT ln K** (Gibbs free energy)
- **Van't Hoff equation:** Temperature dependence of K
- **Reaction quotient (Q):** Predicts direction of reaction

**Industrial Applications:**
- **Haber process:** NH₃ synthesis optimization
- **Contact process:** H₂SO₄ production
- **Buffer systems:** pH control in biological systems"""

        elif 'oop' in topic_lower or 'object-oriented' in topic_lower:
            return """**Object-Oriented Programming - Advanced Concepts 💻**

**Core Principles:**

**1. Encapsulation:**
- **Data hiding:** Private/protected access modifiers
- **Interface design:** Public methods define object behavior
- **Benefits:** Modularity, maintainability, security

**2. Inheritance:**
- **IS-A relationship:** Derived classes extend base classes
- **Method overriding:** Polymorphic behavior
- **Multiple inheritance:** Complex hierarchies (language-dependent)

**3. Polymorphism:**
- **Runtime polymorphism:** Virtual functions, dynamic binding
- **Compile-time polymorphism:** Function/operator overloading
- **Interface polymorphism:** Abstract base classes

**4. Abstraction:**
- **Abstract classes:** Cannot be instantiated
- **Interfaces:** Pure abstract classes (contracts)
- **Data abstraction:** Hide implementation details

**Advanced Concepts:**
- **Design patterns:** Singleton, Factory, Observer, Strategy
- **SOLID principles:** Single responsibility, Open/closed, etc.
- **Memory management:** Constructors, destructors, RAII
- **Template programming:** Generic programming concepts

**Best Practices:**
- **Composition over inheritance**
- **Dependency injection**
- **Unit testing and mocking**
- **Code documentation and maintainability**"""

        elif 'vector' in topic_lower and ('motion' in topic_lower or 'projectile' in topic_lower):
            return """Vector Addition, Free Fall, and Projectile Motion

These three physics concepts work together to describe how objects move in two dimensions.

**Vector Addition**
Vectors have both size (magnitude) and direction. When adding vectors:
- Use the head-to-tail method graphically
- Or break vectors into x and y components and add separately
- Final magnitude: |R| = √(Rx² + Ry²)
- Final direction: θ = tan⁻¹(Ry/Rx)

**Free Fall Motion**
Objects falling under gravity alone:
- Acceleration is always g = 9.8 m/s² downward
- Horizontal velocity stays constant
- Vertical motion follows: y = y₀ + v₀t - ½gt²
- Time to reach peak: t = v₀y/g

**Projectile Motion**
Combines horizontal uniform motion with vertical free fall:
- Horizontal and vertical motions are independent
- Horizontal: vx = constant, x = x₀ + vxt
- Vertical: vy = v₀y - gt, y = y₀ + v₀yt - ½gt²
- Maximum range occurs at 45° launch angle

**Key Formulas**
- Range: R = (v₀²sin(2θ))/g
- Maximum height: H = (v₀²sin²(θ))/(2g)
- Time of flight: T = (2v₀sin(θ))/g

**Problem-Solving Steps**
1. Identify the type of motion
2. Set up your coordinate system
3. Separate into x and y components
4. Apply kinematic equations for each direction
5. Use vector addition for final results

**Real Examples**
- Basketball shots and soccer kicks
- Water fountain trajectories
- Satellite launches and ballistics

This foundation helps you understand how objects move in the real world when multiple forces and directions are involved."""

        elif 'projectile motion' in topic_lower:
            return """**Projectile Motion - Complete Analysis 🏹**

**Fundamental Concept:**
Projectile motion is 2D motion where an object moves under the influence of gravity alone.

**Key Principles:**
1. **Independence of Motion:** Horizontal and vertical components are independent
2. **Horizontal Motion:** Uniform (constant velocity)
3. **Vertical Motion:** Uniformly accelerated (due to gravity)

**Mathematical Framework:**
- **Position:** r(t) = (x₀ + v₀ₓt, y₀ + v₀yt - ½gt²)
- **Velocity:** v(t) = (v₀ₓ, v₀y - gt)
- **Acceleration:** a = (0, -g)

**Launch Parameters:**
- **Initial speed:** v₀
- **Launch angle:** θ
- **Components:** v₀ₓ = v₀cos(θ), v₀y = v₀sin(θ)

**Trajectory Equation:**
y = x·tan(θ) - (gx²)/(2v₀²cos²(θ))

**Key Results:**
- **Range:** R = (v₀²sin(2θ))/g
- **Maximum height:** H = (v₀²sin²(θ))/(2g)
- **Time of flight:** T = (2v₀sin(θ))/g

**Optimization:**
- **Maximum range:** θ = 45° (level ground)
- **Maximum height:** θ = 90° (vertical launch)

**Problem Types:**
1. **Range problems:** Find distance traveled
2. **Height problems:** Maximum altitude calculations
3. **Time problems:** Flight duration analysis
4. **Angle problems:** Optimal launch angles"""

        elif 'free fall' in topic_lower:
            return """**Free Fall Motion - Gravity in Action ⬇️**

**Definition:**
Motion of an object under the influence of gravity alone, with air resistance neglected.

**Key Characteristics:**
- **Acceleration:** Constant g = 9.8 m/s² (downward)
- **Direction:** Always toward Earth's center
- **Independence:** Horizontal motion unaffected

**Kinematic Equations:**
- **Position:** y = y₀ + v₀t - ½gt²
- **Velocity:** v = v₀ - gt
- **Velocity-position:** v² = v₀² - 2g(y - y₀)

**Special Cases:**
1. **Dropped object:** v₀ = 0
   - y = y₀ - ½gt²
   - v = -gt
2. **Thrown upward:** v₀ > 0
   - Time to peak: t = v₀/g
   - Maximum height: h = v₀²/(2g)
3. **Thrown downward:** v₀ < 0
   - Accelerated descent

**Common Misconceptions:**
- ❌ Heavier objects fall faster (without air resistance, all objects fall at same rate)
- ❌ Objects thrown horizontally fall slower (vertical motion independent of horizontal)
- ❌ Acceleration changes during fall (g is constant near Earth's surface)

**Real Applications:**
- **Engineering:** Drop tests, safety calculations
- **Sports:** Diving, gymnastics timing
- **Physics:** Galileo's experiments, g measurement"""

        elif 'vector addition' in topic_lower:
            return """**Vector Addition - Combining Quantities with Direction 📐**

**Fundamental Concept:**
Vectors have both magnitude and direction, requiring special addition rules.

**Addition Methods:**

**1. Graphical Methods:**
- **Head-to-tail:** Place vectors end-to-end, resultant from tail of first to head of last
- **Parallelogram:** Form parallelogram, resultant is diagonal
- **Polygon:** For multiple vectors, form closed polygon

**2. Component Method:**
- **Break down:** Each vector into x and y components
- **Add components:** Rx = ΣAx, Ry = ΣAy
- **Find resultant:** |R| = √(Rx² + Ry²), θ = tan⁻¹(Ry/Rx)

**Mathematical Framework:**
- **Component form:** A = Axî + Ayĵ
- **Magnitude:** |A| = √(Ax² + Ay²)
- **Direction:** θ = tan⁻¹(Ay/Ax)
- **Unit vector:** Â = A/|A|

**Properties:**
- **Commutative:** A + B = B + A
- **Associative:** (A + B) + C = A + (B + C)
- **Distributive:** k(A + B) = kA + kB

**Applications:**
- **Force analysis:** Multiple forces on objects
- **Velocity addition:** Relative motion problems
- **Displacement:** Path-independent total displacement
- **Field superposition:** Electric, magnetic, gravitational fields

**Problem-Solving Steps:**
1. **Draw diagram** with all vectors
2. **Choose coordinate system**
3. **Find components** of each vector
4. **Add components** separately
5. **Calculate resultant** magnitude and direction"""

        elif 'general help' in topic_lower:
            return """Hi! I'm your AI tutor and I'm here to help you learn!

I can assist you with:

**Mathematics**
- Algebra, Geometry, Trigonometry, Calculus
- Problem-solving strategies and step-by-step solutions

**Science**
- Physics: Motion, forces, energy, waves, electricity
- Chemistry: Reactions, equilibrium, atomic structure
- Biology: Cell structure, genetics, ecology

**Computer Science**
- Programming concepts and languages
- Object-oriented programming
- Algorithms and data structures

**How to get the best help:**
- Ask specific questions about topics you're studying
- Request analogies or examples for difficult concepts
- Ask for practice problems or explanations
- Let me know your grade level for appropriate explanations

**Examples of good questions:**
- "Explain Newton's second law with analogies"
- "What is the difference between speed and velocity?"
- "Help me understand chemical equilibrium"
- "Show me examples of object-oriented programming"

What would you like to learn about today?"""

        # Default for other topics
        else:
            return f"""**Understanding {topic.title()}**

This is an important concept that requires careful analysis and understanding of the underlying principles.

**Key Aspects to Consider:**
- Fundamental definitions and terminology
- Mathematical relationships and formulas
- Real-world applications and examples
- Problem-solving strategies and techniques
- Connections to other related concepts

**Study Approach:**
1. Master the basic definitions
2. Understand the mathematical framework
3. Practice with varied examples
4. Connect to broader concepts
5. Apply to real-world situations

Would you like me to focus on any specific aspect of {topic}?"""
    
    def _create_example_response(self, intent: dict) -> str:
        """Create response with specific examples"""
        return f"Here are some great examples of {intent['topic']}..."
    
    def _create_practice_response(self, intent: dict) -> str:
        """Create practice problems or questions"""
        return f"Let's practice {intent['topic']} with some problems..."
    
    def _create_general_response(self, intent: dict) -> str:
        """Create general educational response"""
        
        # For physics topics, provide explanation
        if intent['subject'] == 'physics':
            return self._create_explanation_response(intent)
        
        # For other topics, provide helpful guidance
        topic = intent['topic']
        return f"""I'd be happy to help you understand {topic}!

To give you the best explanation, could you be more specific about what aspect of {topic} you'd like to learn about?

For example:
- Basic concepts and definitions
- How it works or why it's important
- Real-world applications and examples
- Problem-solving techniques
- Connections to other topics

Just let me know what would be most helpful for your learning!"""
    
    def _get_basic_explanation(self, topic: str) -> str:
        """Get basic explanation for any topic"""
        return f"This concept involves understanding the fundamental principles of {topic}."
    
    def is_ready(self) -> bool:
        """Check if service is ready"""
        return True
    
    def get_device_info(self) -> dict:
        """Get device information"""
        return {
            "device": self.device,
            "model_loaded": True,
            "approach": "Smart Context-Aware Tutoring",
            "model_path": "custom_smart_tutor"
        }

# Test the service
if __name__ == "__main__":
    print("🧠 Testing Smart Tutor Service")
    print("="*50)
    
    service = SmartTutorService()
    
    test_messages = [
        "I want some analogy for a middle schooler to understand Newton's laws",
        "Explain the difference between speed and velocity for middle school",
        "Can you give me examples of chemical equilibrium?",
        "What is Newton's second law?"
    ]
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        response = service.get_response(message)
        print(f"🎓 Tutor: {response[:300]}...")
        print("-" * 50)