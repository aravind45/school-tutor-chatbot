#!/usr/bin/env python3
"""
Create high-quality training data for tutoring model
"""

import json
import os
from typing import List, Dict

class QualityTutoringDataCreator:
    """Creates high-quality tutoring training data"""
    
    def __init__(self):
        self.data = []
        self.output_file = "data_quality/train.jsonl"
        os.makedirs("data_quality", exist_ok=True)
    
    def create_physics_data(self):
        """Create comprehensive physics tutoring data"""
        
        physics_data = [
            {
                "instruction": "Explain vector addition to a high school student",
                "input": "",
                "output": """Vector addition is combining vectors that have both magnitude (size) and direction.

**Key Concept:** You can't just add the numbers - direction matters!

**Two Main Methods:**

**1. Graphical Method (Head-to-Tail):**
- Draw the first vector
- Place the tail of the second vector at the head of the first
- The resultant goes from the tail of the first to the head of the second

**2. Component Method:**
- Break each vector into x and y components
- Add x-components separately: Rx = Ax + Bx
- Add y-components separately: Ry = Ay + By
- Find magnitude: |R| = √(Rx² + Ry²)
- Find direction: θ = tan⁻¹(Ry/Rx)

**Real Example:**
Walk 3 km east, then 4 km north
- You're NOT 7 km from start
- You're 5 km from start (3² + 4² = 5²)
- At an angle of 53° northeast

**Applications:**
- Force analysis in physics
- Navigation and GPS
- Velocity problems in 2D motion""",
                "subject": "Physics",
                "topic": "Vector Addition",
                "level": "High School"
            },
            
            {
                "instruction": "A student asks: 'Give me an analogy to understand vector addition'",
                "input": "",
                "output": """Great question! Here are some helpful analogies:

**The City Walking Analogy:**
Imagine you're in a city with a grid of streets. You walk 3 blocks east, then 4 blocks north. You don't end up 7 blocks away from where you started - you end up 5 blocks away at an angle. That's because you changed direction!

**The Treasure Map Analogy:**
Pirates had maps that said "Walk 30 paces toward the sunrise, then 40 paces toward the North Star." They learned that following these directions didn't put them 70 paces from the starting point, but only 50 paces away at a specific angle.

**The Tug-of-War Analogy:**
If two people pull a rope in different directions, the rope doesn't move in either person's direction - it moves in a direction that combines both pulls. The stronger pull has more influence on the final direction.

**The GPS Analogy:**
When your GPS calculates a route, it's constantly adding up vectors - each turn is a vector with distance and direction. The final destination is the sum of all these vector "steps."

The key insight: Vectors care about BOTH how much AND which way!""",
                "subject": "Physics",
                "topic": "Vector Addition",
                "level": "High School"
            },
            
            {
                "instruction": "Explain Newton's laws of motion with examples",
                "input": "",
                "output": """Newton's Three Laws explain how forces affect motion:

**First Law (Law of Inertia):**
Objects at rest stay at rest, and objects in motion stay in motion at constant velocity, unless acted upon by a net external force.

*Examples:*
- You slide forward when a car brakes suddenly
- A hockey puck glides across ice until friction stops it
- Passengers feel pushed back when a car accelerates

**Second Law (F = ma):**
The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.

*Formula:* F = ma
- More force → more acceleration
- More mass → less acceleration (for same force)

*Examples:*
- Empty shopping cart accelerates easily; full cart needs more force
- Powerful car engines produce more acceleration
- It's harder to stop a moving truck than a bicycle

**Third Law (Action-Reaction):**
For every action, there is an equal and opposite reaction.

*Examples:*
- Walking: you push back on ground, ground pushes you forward
- Swimming: you push water back, water pushes you forward
- Rocket propulsion: hot gases pushed down, rocket pushed up
- Recoil when firing a gun

**Key Insight:** These laws work together to explain ALL motion in the universe!""",
                "subject": "Physics",
                "topic": "Newton's Laws",
                "level": "High School"
            },
            
            {
                "instruction": "Student asks: 'What's the difference between speed and velocity?'",
                "input": "",
                "output": """Excellent question! Speed and velocity are related but different:

**Speed (Scalar Quantity):**
- How fast something is moving
- Only has magnitude (size)
- Always positive
- Units: mph, m/s, km/h
- Example: "The car is going 60 mph"

**Velocity (Vector Quantity):**
- How fast AND in what direction
- Has both magnitude and direction
- Can be positive or negative
- Units: mph north, m/s at 30°, etc.
- Example: "The car is going 60 mph north"

**Key Differences:**

**1. Direction Matters for Velocity:**
- Two cars both going 60 mph have the same speed
- If one goes north and one goes south, they have different velocities

**2. Average Velocity Can Be Zero:**
- Drive in a circle back to your starting point
- Average speed > 0 (you moved)
- Average velocity = 0 (no net displacement)

**3. Velocity Changes When You Turn:**
- Even at constant speed, turning changes your velocity
- Speed stays the same, but direction changes

**Memory Trick:**
- Speed = speedometer reading (just a number)
- Velocity = GPS showing speed AND heading (number + direction)""",
                "subject": "Physics",
                "topic": "Speed vs Velocity",
                "level": "High School"
            }
        ]
        
        self.data.extend(physics_data)
    
    def create_chemistry_data(self):
        """Create chemistry tutoring data"""
        
        chemistry_data = [
            {
                "instruction": "Explain chemical equilibrium to an AP Chemistry student",
                "input": "",
                "output": """Chemical equilibrium occurs when the forward and reverse reaction rates are equal, resulting in constant concentrations of reactants and products.

**Key Characteristics:**
- **Dynamic process:** Reactions continue at molecular level
- **Constant concentrations:** No net change in amounts
- **Reversible reactions:** Can proceed in both directions

**Le Chatelier's Principle:**
When a system at equilibrium is disturbed, it shifts to counteract the disturbance.

**Types of Disturbances:**

**1. Concentration Changes:**
- Add reactant → equilibrium shifts right (toward products)
- Remove product → equilibrium shifts right
- Add product → equilibrium shifts left (toward reactants)

**2. Temperature Changes:**
- **Exothermic reactions:** Heat is a product
  - Increase T → shifts left (endothermic direction)
  - Decrease T → shifts right (exothermic direction)
- **Endothermic reactions:** Heat is a reactant
  - Increase T → shifts right (endothermic direction)
  - Decrease T → shifts left (exothermic direction)

**3. Pressure Changes (gases only):**
- Increase pressure → shifts toward fewer gas molecules
- Decrease pressure → shifts toward more gas molecules

**4. Catalysts:**
- Speed up both forward and reverse reactions equally
- NO effect on equilibrium position
- Help reach equilibrium faster

**Equilibrium Constant (K):**
K = [products]/[reactants] (with proper stoichiometry)
- K >> 1: Products favored
- K << 1: Reactants favored
- K ≈ 1: Neither strongly favored

**Industrial Application:**
Haber Process (NH₃ production) uses high pressure and moderate temperature to optimize ammonia yield while maintaining reasonable reaction rate.""",
                "subject": "Chemistry",
                "topic": "Chemical Equilibrium",
                "level": "AP"
            }
        ]
        
        self.data.extend(chemistry_data)
    
    def create_conversation_data(self):
        """Create conversational tutoring data"""
        
        conversation_data = [
            {
                "instruction": "Student says: 'I don't understand this at all. Can you help me with vectors?'",
                "input": "",
                "output": """Of course! I'm here to help you understand vectors. Let's start from the beginning.

Don't worry - vectors seem confusing at first, but once you get the key idea, they make perfect sense.

**The Big Idea:**
A vector is just a quantity that has TWO pieces of information:
1. **How much** (magnitude/size)
2. **Which direction**

Think of it like giving someone directions:
- "Go 5 miles" ← This is incomplete (speed/scalar)
- "Go 5 miles north" ← This is complete (velocity/vector)

**Let's start simple:**
Can you think of other examples where both amount AND direction matter? 

For instance:
- Force: You need to know how hard to push AND which way
- Wind: Speed matters, but so does direction
- Displacement: How far you moved AND which way you went

What questions do you have about this basic concept? I'll explain anything that's unclear!""",
                "subject": "Physics",
                "topic": "Vectors - Introduction",
                "level": "High School"
            },
            
            {
                "instruction": "Student asks: 'Can you create a story to help me remember vector addition?'",
                "input": "",
                "output": """**The Great Treasure Hunt**

Maya and Alex were treasure hunters who found an ancient map. The map had strange instructions:

"From the old oak tree, walk 30 steps toward the rising sun, then turn and walk 40 steps toward the North Star."

Maya grabbed her calculator. "Easy! 30 + 40 = 70 steps total from the tree!"

But Alex shook his head. "Wait, we're not walking in a straight line. We're making a turn!"

They followed the directions exactly:
- 30 steps east (toward the sunrise)
- Then 40 steps north (toward the North Star)

When they measured their distance from the oak tree, they were amazed - only 50 steps away, not 70!

"It's like that math theorem!" Alex realized. "30² + 40² = 50². We made a right triangle!"

Maya learned something important: when you combine movements in different directions, you can't just add the numbers. You have to consider BOTH the distance AND the direction.

The treasure was buried exactly where the math predicted - 50 steps from the oak tree, at an angle pointing northeast.

**The Lesson:** Vector addition isn't regular addition. When directions change, you need special math to find the true result. That's what makes vectors so powerful - they keep track of both "how much" and "which way"!

**Your Turn:** Next time you walk around your neighborhood, try this: walk one block east, then one block north. Are you really two blocks from home, or something different?""",
                "subject": "Physics",
                "topic": "Vector Addition",
                "level": "High School"
            }
        ]
        
        self.data.extend(conversation_data)
    
    def create_creative_responses(self):
        """Create creative tutoring responses (songs, poems, etc.)"""
        
        creative_data = [
            {
                "instruction": "Student requests: 'Can you make a rap song about Newton's laws?'",
                "input": "",
                "output": """**Newton's Laws Rap** 🎤

*Yo, listen up, I got three laws to share*
*About motion and forces everywhere*
*Newton figured it out way back in the day*
*Now let me break it down in my own way*

**[Verse 1 - First Law]**
*Objects at rest, they wanna stay still*
*Objects in motion keep moving until*
*A force comes along to change their state*
*That's inertia, don't be late!*

*Slide in your car when the brakes hit hard*
*That's your body playing the inertia card*
*Hockey puck glides till friction takes hold*
*First law of motion, never gets old!*

**[Verse 2 - Second Law]**
*F equals m-a, that's the equation*
*Force and mass determine acceleration*
*Push harder, go faster, that's the deal*
*Heavy things need more force to make 'em feel*

*Shopping cart empty, easy to push*
*Load it up heavy, need more whoosh*
*Same force, less speed when the mass is high*
*Second law explains the reason why!*

**[Verse 3 - Third Law]**
*Action-reaction, equal and opposite*
*Push on something, it pushes back, that's it*
*Walk on the ground, it pushes you too*
*That's how you move, physics so true!*

*Rocket shoots gas down toward the ground*
*Newton's third law makes it rocket-bound*
*Swimming in water, push it behind*
*Water pushes you forward, blow your mind!*

**[Outro]**
*Three laws of motion, now you know*
*Newton's the man who made physics flow*
*From cars to rockets to walking around*
*These laws of motion run this town!*

**Drop the mic!** 🎤⬇️""",
                "subject": "Physics",
                "topic": "Newton's Laws",
                "level": "High School"
            }
        ]
        
        self.data.extend(creative_data)
    
    def save_data(self):
        """Save all training data to JSONL file"""
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for item in self.data:
                # Add metadata
                item.update({
                    "id": f"quality_tutor_{len(self.data):03d}",
                    "source": "quality_tutoring_data",
                    "quality": "high",
                    "type": "tutoring"
                })
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"✅ Created {len(self.data)} high-quality training examples")
        print(f"📁 Saved to: {self.output_file}")
        
        # Print statistics
        subjects = {}
        for item in self.data:
            subject = item.get('subject', 'Unknown')
            subjects[subject] = subjects.get(subject, 0) + 1
        
        print("\n📊 Data Statistics:")
        for subject, count in subjects.items():
            print(f"  {subject}: {count} examples")
    
    def create_all_data(self):
        """Create all training data"""
        print("🔄 Creating high-quality tutoring training data...")
        
        self.create_physics_data()
        self.create_chemistry_data()
        self.create_conversation_data()
        self.create_creative_responses()
        
        self.save_data()

if __name__ == "__main__":
    creator = QualityTutoringDataCreator()
    creator.create_all_data()