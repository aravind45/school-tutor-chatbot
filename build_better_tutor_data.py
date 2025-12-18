#!/usr/bin/env python3
"""
Build Better Tutor Training Data

This script creates high-quality tutoring data with:
- Detailed explanations
- Step-by-step solutions
- Multiple subjects
- Conversational tone
- Encouraging responses
"""

import json
import os
import random
from typing import List, Dict

def create_math_data() -> List[Dict]:
    """Create math tutoring examples"""
    return [
        {
            "instruction": "Can you help me understand how to solve quadratic equations?",
            "input": "",
            "output": """I'd be happy to help you with quadratic equations! Let's break this down step by step.

A quadratic equation has the form: ax² + bx + c = 0, where a ≠ 0.

There are three main methods to solve them:

**1. Factoring (when possible)**
Example: x² - 5x + 6 = 0
- Look for two numbers that multiply to 6 and add to -5
- Those numbers are -2 and -3
- So: (x - 2)(x - 3) = 0
- Therefore: x = 2 or x = 3

**2. Quadratic Formula (always works)**
For ax² + bx + c = 0: x = [-b ± √(b² - 4ac)] / (2a)

**3. Completing the Square**
Useful for understanding the vertex form.

Would you like me to work through a specific example with you?"""
        },
        {
            "instruction": "I'm struggling with the Pythagorean theorem. Can you explain it?",
            "input": "",
            "output": """Absolutely! The Pythagorean theorem is one of the most useful tools in mathematics.

**The Theorem:** In a right triangle, a² + b² = c²
- a and b are the lengths of the two shorter sides (legs)
- c is the length of the longest side (hypotenuse)

**Why does this work?**
Think of it as the relationship between the areas of squares built on each side of a right triangle.

**Example:**
If you have a right triangle with legs of 3 and 4:
- 3² + 4² = c²
- 9 + 16 = c²
- 25 = c²
- c = 5

**Real-world uses:**
- Finding distances on maps
- Construction and carpentry
- Computer graphics
- Navigation

Try this: If a ladder is 10 feet long and the base is 6 feet from a wall, how high up the wall does it reach?"""
        },
        {
            "instruction": "What's the difference between speed and velocity?",
            "input": "",
            "output": """Great question! This is a common source of confusion, but the difference is important in physics.

**Speed** is a scalar quantity:
- Only tells you HOW FAST something is moving
- Always positive
- Units: m/s, mph, km/h
- Example: "The car is going 60 mph"

**Velocity** is a vector quantity:
- Tells you HOW FAST AND IN WHAT DIRECTION
- Can be positive or negative (depending on direction)
- Units: same as speed, but with direction
- Example: "The car is going 60 mph north"

**Key differences:**
1. **Direction matters for velocity:** A car going 60 mph east has different velocity than one going 60 mph west
2. **Average velocity can be zero:** If you drive in a circle and return to start, your average velocity is zero, but your average speed isn't
3. **Velocity changes when direction changes:** Even at constant speed, turning changes velocity

Think of it this way: Speed is like the speedometer reading, velocity is like GPS navigation showing speed AND direction!

Does this help clarify the difference?"""
        }
    ]

def create_science_data() -> List[Dict]:
    """Create science tutoring examples"""
    return [
        {
            "instruction": "Can you explain photosynthesis in a way that's easy to understand?",
            "input": "",
            "output": """Of course! Let me explain photosynthesis in a way that makes sense.

**What is photosynthesis?**
It's how plants make their own food using sunlight, water, and carbon dioxide.

**The Simple Equation:**
6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂
(Carbon dioxide + Water + Light → Sugar + Oxygen)

**Think of it like a kitchen:**
- **Ingredients:** CO₂ from air, H₂O from roots
- **Energy source:** Sunlight (captured by chlorophyll)
- **Kitchen:** Chloroplasts in leaves
- **Recipe result:** Glucose (sugar) for plant food
- **Bonus:** Oxygen released for us to breathe!

**Two main stages:**
1. **Light reactions:** Capture sunlight energy
2. **Calvin cycle:** Use that energy to make sugar

**Why should you care?**
- Plants feed the entire food chain
- They produce the oxygen we breathe
- They remove CO₂ from the atmosphere

**Fun fact:** One large tree produces enough oxygen for two people per day!

Would you like me to explain any part in more detail?"""
        },
        {
            "instruction": "I don't understand Newton's laws of motion. Help?",
            "input": "",
            "output": """Newton's laws can seem tricky, but they're actually describing things you experience every day! Let me break them down:

**First Law (Law of Inertia):**
"An object at rest stays at rest, and an object in motion stays in motion, unless acted upon by a force."

*Real life:* When a bus suddenly stops, you keep moving forward. When you're sitting still, you stay still until you decide to get up.

**Second Law (F = ma):**
"The force on an object equals its mass times its acceleration."

*Real life:* It takes more force to push a heavy box than a light one. The harder you push, the faster it accelerates.

**Third Law (Action-Reaction):**
"For every action, there is an equal and opposite reaction."

*Real life:* When you walk, you push back on the ground, and the ground pushes forward on you. When you sit in a chair, you push down on it, and it pushes up on you.

**Memory tricks:**
- First law: "Lazy objects stay lazy, moving objects keep moving"
- Second law: "More force = more acceleration"
- Third law: "Forces always come in pairs"

**Practice question:** Why do you feel pushed back into your seat when a car accelerates forward?

Which law would you like me to explain more?"""
        }
    ]

def create_english_data() -> List[Dict]:
    """Create English/writing tutoring examples"""
    return [
        {
            "instruction": "How do I write a good thesis statement?",
            "input": "",
            "output": """A strong thesis statement is the backbone of any good essay! Let me help you craft one.

**What makes a good thesis statement:**
1. **Takes a clear position** - Not just a fact, but an argument
2. **Is specific** - Focused, not too broad
3. **Is debatable** - Someone could reasonably disagree
4. **Previews your main points** - Gives a roadmap

**Formula that works:**
"[Topic] [your position] because [reason 1], [reason 2], and [reason 3]."

**Examples:**

**Weak:** "Social media is popular."
(This is just a fact, not arguable)

**Better:** "Social media has negative effects on teenagers."
(Takes a position, but still vague)

**Strong:** "Social media negatively impacts teenagers by increasing anxiety, reducing face-to-face social skills, and promoting unrealistic body image standards."
(Specific position + three clear reasons)

**Steps to write yours:**
1. Start with your topic
2. Ask: "What's my main argument about this topic?"
3. Ask: "What are my 2-3 strongest reasons?"
4. Combine them into one sentence

**Pro tip:** Your thesis usually goes at the end of your introduction paragraph.

What topic are you writing about? I can help you develop a specific thesis!"""
        }
    ]

def create_history_data() -> List[Dict]:
    """Create history tutoring examples"""
    return [
        {
            "instruction": "Why did World War I start?",
            "input": "",
            "output": """World War I didn't start from just one cause - it was like a perfect storm of tensions that had been building up. Let me explain the main factors:

**The "Powder Keg" of Europe:**
By 1914, Europe was full of tensions ready to explode.

**Main Causes (Remember: MAIN)**

**M - Militarism:**
- Countries were building up huge armies and navies
- Arms race, especially between Britain and Germany
- Military leaders had too much influence

**A - Alliances:**
- Europe divided into two camps:
  - Triple Alliance: Germany, Austria-Hungary, Italy
  - Triple Entente: France, Russia, Britain
- "If you attack my friend, you attack me"

**I - Imperialism:**
- European powers competing for colonies
- Created tensions, especially in Africa and Asia
- Germany felt left out of the colonial game

**N - Nationalism:**
- Ethnic groups wanted their own countries
- Especially explosive in the Balkans
- Slavic peoples wanted independence from Austria-Hungary

**The Spark: Assassination of Archduke Franz Ferdinand**
- June 28, 1914, in Sarajevo
- Killed by a Serbian nationalist
- Austria-Hungary blamed Serbia
- Alliance system kicked in like dominoes falling

**Think of it like:** A room full of gunpowder (tensions) + a lit match (assassination) = explosion (war)

Would you like me to explain how the alliance system turned a regional conflict into a world war?"""
        }
    ]

def create_study_skills_data() -> List[Dict]:
    """Create study skills and learning strategy examples"""
    return [
        {
            "instruction": "I have trouble remembering what I study. Any tips?",
            "input": "",
            "output": """I totally understand! Memory can be tricky, but there are proven strategies that really work. Let me share some of the best ones:

**Active Learning Techniques:**

**1. The Feynman Technique:**
- Explain the concept in simple terms (like to a 5-year-old)
- If you can't explain it simply, you don't understand it yet
- Find the gaps and go back to study those parts

**2. Spaced Repetition:**
- Review material at increasing intervals
- Day 1: Learn it
- Day 2: Review
- Day 4: Review again
- Day 7: Review again
- This fights the "forgetting curve"

**3. Active Recall:**
- Close your book and try to remember what you just read
- Use flashcards or practice tests
- Much better than just re-reading

**4. Connect to What You Know:**
- Link new information to things you already understand
- Create analogies and examples
- Build a "web" of knowledge

**5. Use Multiple Senses:**
- Read it, write it, say it out loud
- Draw diagrams or mind maps
- Use colors and visual organization

**6. Teach Someone Else:**
- Explain concepts to friends, family, or even your pet!
- Teaching forces you to really understand

**Quick Memory Tricks:**
- Acronyms (like ROYGBIV for rainbow colors)
- Rhymes and songs
- Visual associations
- Story method (create a story linking facts)

What subject are you studying? I can suggest specific techniques that work best for that type of material!"""
        }
    ]

def main():
    """Generate comprehensive tutoring dataset"""
    
    # Collect all data
    all_data = []
    all_data.extend(create_math_data())
    all_data.extend(create_science_data())
    all_data.extend(create_english_data())
    all_data.extend(create_history_data())
    all_data.extend(create_study_skills_data())
    
    # Add metadata
    for i, item in enumerate(all_data):
        item['id'] = f"tutor_{i+1:03d}"
        item['source'] = "custom_tutor_data"
        item['quality'] = "high"
    
    # Shuffle the data
    random.seed(42)
    random.shuffle(all_data)
    
    # Split into train/eval (90/10)
    split_idx = int(len(all_data) * 0.9)
    train_data = all_data[:split_idx]
    eval_data = all_data[split_idx:]
    
    # Create data directory
    os.makedirs("data_improved", exist_ok=True)
    
    # Save training data
    with open("data_improved/train.jsonl", "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    # Save evaluation data
    with open("data_improved/eval.jsonl", "w", encoding="utf-8") as f:
        for item in eval_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Created improved tutoring dataset:")
    print(f"   Training samples: {len(train_data)}")
    print(f"   Evaluation samples: {len(eval_data)}")
    print(f"   Total samples: {len(all_data)}")
    print(f"   Saved to: data_improved/")
    
    # Show sample
    print(f"\n📝 Sample training example:")
    print(f"Instruction: {train_data[0]['instruction']}")
    print(f"Output: {train_data[0]['output'][:200]}...")

if __name__ == "__main__":
    main()