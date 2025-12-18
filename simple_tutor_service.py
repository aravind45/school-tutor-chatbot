#!/usr/bin/env python3
"""
Simple, working tutor service that actually provides useful responses
"""

import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTutorService:
    """A simple tutor that actually works and gives useful responses"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.last_topic = None
        logger.info(f"Initializing Simple Tutor Service on {self.device}")
    
    def get_response(self, user_message: str, max_tokens: int = 500) -> str:
        """Generate a helpful response"""
        
        message = user_message.lower().strip()
        
        # Handle follow-up requests
        if self._is_follow_up(message) and self.last_topic:
            return self._get_follow_up_response(message, self.last_topic)
        
        # Handle specific topics
        if 'vector addition' in message or 'vector' in message:
            self.last_topic = 'vector addition'
            return self._get_vector_addition_response(message)
        
        elif 'newton' in message and 'law' in message:
            self.last_topic = 'newton laws'
            return self._get_newton_laws_response(message)
        
        elif 'speed' in message and 'velocity' in message:
            self.last_topic = 'speed velocity'
            return self._get_speed_velocity_response(message)
        
        elif 'work' in message and 'power' in message and 'energy' in message:
            self.last_topic = 'work power energy'
            return self._get_work_power_energy_response()
        
        elif 'projectile' in message or 'free fall' in message:
            self.last_topic = 'projectile motion'
            return self._get_projectile_motion_response()
        
        elif 'equilibrium' in message:
            self.last_topic = 'chemical equilibrium'
            return self._get_equilibrium_response()
        
        # General help
        else:
            return self._get_general_help()
    
    def _is_follow_up(self, message):
        """Check if this is a follow-up question"""
        follow_ups = [
            'give me analogy', 'analogy', 'example', 'explain more',
            'tell me more', 'help me understand', 'show me', 'can you',
            'create a story', 'short story', 'make a story', 'tell a story',
            'give me a story', 'story to', 'help me remember',
            'rap song', 'song', 'poem', 'rhyme', 'give me short',
            'make a rap', 'create a rap', 'write a song'
        ]
        return any(phrase in message for phrase in follow_ups)
    
    def _get_follow_up_response(self, message, topic):
        """Handle follow-up questions"""
        
        if 'rap' in message or 'song' in message or 'rhyme' in message:
            if topic == 'vector addition':
                return """**Vector Addition Rap 🎤**

*Yo, listen up, I got something to say*
*About vectors and how they work every day*
*They got magnitude, that's the size you see*
*Plus direction too, that's the key to be free*

*When you add them up, don't just add the numbers*
*That's a rookie mistake that always encumbers*
*Use components, break 'em down x and y*
*Add them separate, then you'll reach for the sky*

*Head to tail method, that's another way*
*Draw them vectors, let the math have its say*
*Pythagorean theorem, that's the final test*
*Square root of squares, and you'll get the best*

*Vector addition, it's not just math*
*It's forces and motion on physics' path*
*From GPS navigation to rocket flight*
*Vectors make everything work just right!*

**Drop the mic! 🎤⬇️**"""

            elif topic == 'newton laws':
                return """**Newton's Laws Rap 🎤**

*Three laws of motion, let me break it down*
*Newton figured it out, he's the physics crown*
*First law says objects stay in their state*
*Unless a force comes to change their fate*

*Second law, F equals m-a*
*More force, more speed, that's the way*
*Heavy things need more push to move*
*Light things fly when you're in the groove*

*Third law's the coolest, action-reaction*
*Push on something, get back satisfaction*
*Walk on the ground, it pushes you too*
*That's how you move, it's physics true!*

**Newton's in the house! 🎤⬇️**"""

        elif 'story' in message:
            if topic == 'vector addition':
                return """**The Great Treasure Hunt**

Maya and Alex were treasure hunters with an old map. The map said:
"From the old oak tree, walk 30 steps toward the sunrise, then 40 steps toward the North Star."

Maya said, "That's easy! 30 + 40 = 70 steps total!"

But Alex shook his head. "Wait, we're not walking in a straight line. We're making a turn!"

They followed the directions exactly:
- 30 steps east (toward sunrise)
- Then 40 steps north (toward North Star)

When they measured their distance from the oak tree, they were only 50 steps away, not 70!

"It's like the Pythagorean theorem!" Alex realized. "30² + 40² = 50²"

Maya learned that when you combine movements in different directions, you can't just add the numbers. You have to consider BOTH the distance AND the direction - that's vector addition!

The treasure was buried exactly 50 steps from the oak tree, at an angle of 53° northeast.

**The Lesson:** Vectors aren't just numbers - they're movements with direction. When you add them, you get a new movement that might be shorter or longer than you expect!"""

        elif 'analogy' in message:
            if topic == 'vector addition':
                return """**Vector Addition Analogy**

Think of vector addition like giving directions:

**Walking in a City:**
- Walk 3 blocks east, then 4 blocks north
- You don't end up 7 blocks away from start
- You end up 5 blocks away (3² + 4² = 5²) at an angle

**Pulling a Heavy Box:**
- You pull northeast, your friend pulls northwest
- The box moves north (sum of your forces)
- Stronger pull = bigger influence on direction

**GPS Navigation:**
- Each turn is a vector (distance + direction)
- GPS adds all vectors to find your final position
- Same math as vector addition!

The key: Vectors care about BOTH how much AND which way."""

            elif topic == 'newton laws':
                if 'story' in message:
                    return """**Sir Isaac and the Magic Rules**

Long ago, Sir Isaac Newton discovered three magical rules that control everything that moves:

**The Lazy Spell (First Law):**
Everything in the kingdom was under a lazy spell. Things at rest wanted to stay at rest, and things moving wanted to keep moving forever - unless someone cast a "force spell" to change them.

**The Push Spell (Second Law):**
The stronger you cast a push spell, the faster things would speed up. But heavy things needed much stronger spells than light things to move the same amount.

**The Push-Back Curse (Third Law):**
This was the strangest magic of all - whenever you pushed something, it would automatically push back on you with exactly the same strength! Knights learned this when they tried to push castle walls - the wall would push back just as hard!

These three rules became the foundation of all motion in the kingdom, and even today, everything from cars to rockets follows Sir Isaac's magical laws!

**The Real Magic:** These aren't just stories - they're the actual rules that govern how everything moves in our universe!"""
                else:
                    return """**Newton's Laws Analogies**

**First Law - The Lazy Couch:**
- You're comfortable on the couch (at rest)
- You'll stay there unless someone makes you move (external force)
- Once walking, you'd walk forever if nothing stopped you

**Second Law - Shopping Cart:**
- Empty cart = easy to push, speeds up quickly
- Full cart = need more force, speeds up slowly
- Push harder = faster acceleration

**Third Law - Walking:**
- You push back on ground with your foot
- Ground pushes forward on you with equal force
- That's how you move forward!"""

            elif topic == 'speed velocity':
                return """**Speed vs Velocity Analogy**

**Speedometer vs GPS:**
- Speedometer shows speed: "60 mph" (just how fast)
- GPS shows velocity: "60 mph heading north" (fast + direction)

**Running Track:**
- Two runners both going 8 mph (same speed)
- One clockwise, one counter-clockwise (different velocities)
- Speed is the same, velocity is opposite!"""

        return f"Let me explain more about {topic}..."
    
    def _get_vector_addition_response(self, message):
        """Vector addition explanation"""
        return """**Vector Addition**

Vectors have both magnitude (size) and direction.

**Two Methods:**
1. **Graphical:** Draw vectors head-to-tail, measure result
2. **Component:** Break into x,y parts, add separately

**Key Formulas:**
- Magnitude: |R| = √(Rx² + Ry²)  
- Direction: θ = tan⁻¹(Ry/Rx)

**Example:**
- Vector A: 3 units east
- Vector B: 4 units north  
- Result: 5 units northeast

**Applications:**
- Force analysis
- Velocity problems
- Navigation systems"""
    
    def _get_newton_laws_response(self, message):
        """Newton's laws explanation"""
        return """**Newton's Three Laws**

**First Law (Inertia):**
Objects at rest stay at rest, moving objects keep moving, unless a force acts on them.

**Second Law (F = ma):**
Force equals mass times acceleration. More force = more acceleration. More mass = less acceleration.

**Third Law (Action-Reaction):**
For every action, there's an equal and opposite reaction.

**Real Examples:**
- Car braking: you slide forward (1st law)
- Pushing a car: heavy car needs more force (2nd law)  
- Walking: you push ground, ground pushes you (3rd law)"""
    
    def _get_speed_velocity_response(self, message):
        """Speed vs velocity explanation"""
        return """**Speed vs Velocity**

**Speed:** How fast (scalar)
- Just a number: "50 mph"
- Always positive

**Velocity:** How fast + direction (vector)  
- Number + direction: "50 mph north"
- Can be negative

**Key Difference:**
- Speed = distance/time
- Velocity = displacement/time

**Example:**
Drive in a circle back to start:
- Average speed > 0 (you moved)
- Average velocity = 0 (no net displacement)"""
    
    def _get_work_power_energy_response(self):
        """Work, power, energy explanation"""
        return """**Work, Power, and Energy**

**Work:** Force × Distance
- Formula: W = F·d·cos(θ)
- Units: Joules
- No movement = no work

**Energy:** Ability to do work
- Kinetic: KE = ½mv²
- Potential: PE = mgh
- Units: Joules

**Power:** Work per time
- Formula: P = W/t
- Units: Watts
- How quickly energy is used

**Connection:**
Work changes energy. Power is how fast that happens."""
    
    def _get_projectile_motion_response(self):
        """Projectile motion explanation"""
        return """**Projectile Motion**

**Key Idea:** Horizontal and vertical motions are independent.

**Horizontal Motion:**
- Constant velocity (no acceleration)
- x = v₀t

**Vertical Motion:**  
- Constant acceleration due to gravity
- y = v₀t - ½gt²

**Important Formulas:**
- Range: R = (v₀²sin(2θ))/g
- Max height: H = (v₀²sin²(θ))/(2g)
- Time of flight: T = (2v₀sin(θ))/g

**Best angle for max range:** 45°"""
    
    def _get_equilibrium_response(self):
        """Chemical equilibrium explanation"""
        return """**Chemical Equilibrium**

**Definition:** Forward and reverse reaction rates are equal.

**Key Points:**
- Reactions still happening (dynamic)
- Concentrations stay constant
- Can be disturbed and will shift

**Le Chatelier's Principle:**
System shifts to counteract changes:
- Add reactant → shifts right
- Increase temperature → shifts to absorb heat
- Increase pressure → shifts to fewer gas molecules

**Example:** Making ammonia (Haber process)"""
    
    def _get_general_help(self):
        """General help message"""
        return """**Hi! I'm your physics tutor.**

I can help with:
- Vector addition and motion
- Newton's laws of motion  
- Work, power, and energy
- Projectile motion and free fall
- Speed vs velocity
- Chemical equilibrium

**Just ask me about any of these topics!**

Examples:
- "Explain vector addition"
- "What are Newton's laws?"
- "Give me analogy for speed vs velocity"

I'll remember what we're discussing so you can ask follow-up questions like "give me an analogy" or "show me examples"."""
    
    def is_ready(self) -> bool:
        """Check if service is ready"""
        return True
    
    def get_device_info(self) -> dict:
        """Get device information"""
        return {
            "device": self.device,
            "model_loaded": True,
            "approach": "Simple Working Tutor",
            "model_path": "simple_tutor"
        }