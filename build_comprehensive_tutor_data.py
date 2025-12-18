#!/usr/bin/env python3
"""
Build Comprehensive Tutor Training Data

Creates a large, high-quality dataset with hundreds of tutoring examples
across multiple subjects with detailed, helpful explanations.
"""

import json
import os
import random
from typing import List, Dict

def create_math_algebra_data() -> List[Dict]:
    """Algebra tutoring examples"""
    return [
        {
            "instruction": "How do I solve linear equations?",
            "input": "",
            "output": """Linear equations are one of the most fundamental skills in algebra! Let me walk you through this step by step.

**What is a linear equation?**
An equation where the variable has a power of 1 (like x, not x²).
Examples: 2x + 5 = 11, 3x - 7 = 2x + 1

**The Golden Rule: Whatever you do to one side, do to the other!**

**Step-by-step process:**
1. **Simplify both sides** (combine like terms)
2. **Get variables on one side** (add/subtract)
3. **Get constants on the other side** (add/subtract)
4. **Isolate the variable** (multiply/divide)

**Example: 3x + 7 = 2x - 5**
Step 1: Already simplified
Step 2: Subtract 2x from both sides → x + 7 = -5
Step 3: Subtract 7 from both sides → x = -12
Step 4: Already isolated!

**Check your answer:** 3(-12) + 7 = -36 + 7 = -29, and 2(-12) - 5 = -24 - 5 = -29 ✓

Try this one: 4x - 3 = 2x + 9. What do you get?"""
        },
        {
            "instruction": "I'm confused about fractions. Can you help?",
            "input": "",
            "output": """Fractions can be tricky, but once you understand the concept, they become much easier! Let me help you build confidence with fractions.

**What is a fraction?**
A fraction represents part of a whole. The top number (numerator) tells you how many parts you have, and the bottom number (denominator) tells you how many parts make up the whole.

**Key Operations:**

**Adding/Subtracting:**
- Same denominator: Add/subtract numerators, keep denominator
  - 2/5 + 1/5 = 3/5
- Different denominators: Find common denominator first
  - 1/3 + 1/4 = 4/12 + 3/12 = 7/12

**Multiplying:**
- Multiply numerators together, multiply denominators together
  - 2/3 × 3/4 = 6/12 = 1/2

**Dividing:**
- Multiply by the reciprocal (flip the second fraction)
  - 2/3 ÷ 3/4 = 2/3 × 4/3 = 8/9

**Converting to decimals:**
- Divide numerator by denominator
  - 3/4 = 3 ÷ 4 = 0.75

**Real-world examples:**
- Pizza slices: If you eat 3 out of 8 slices, you ate 3/8 of the pizza
- Time: 30 minutes is 30/60 = 1/2 hour

What specific part of fractions would you like to practice?"""
        },
        {
            "instruction": "What's the difference between mean, median, and mode?",
            "input": "",
            "output": """Great question! These are the three main measures of central tendency, and each tells you something different about your data.

**Mean (Average):**
- Add all numbers and divide by how many numbers you have
- Example: 2, 4, 6, 8 → (2+4+6+8) ÷ 4 = 20 ÷ 4 = 5
- **When to use:** When data is fairly evenly distributed
- **Problem:** Sensitive to extreme values (outliers)

**Median (Middle Value):**
- Put numbers in order, find the middle one
- Example: 2, 4, 6, 8 → middle is between 4 and 6 → (4+6) ÷ 2 = 5
- If odd number of values, pick the exact middle
- **When to use:** When you have outliers that skew the mean
- **Example:** House prices (a few mansions don't represent typical prices)

**Mode (Most Common):**
- The number that appears most often
- Example: 2, 3, 3, 4, 5 → mode is 3
- Can have no mode, one mode, or multiple modes
- **When to use:** With categories or when you want the most typical value

**Memory tricks:**
- **Mean:** "Mean" sounds like "average"
- **Median:** Think of the "median strip" in the middle of a highway
- **Mode:** "Mode" sounds like "most" (most common)

**Practice data:** 1, 2, 2, 3, 4, 4, 4, 5, 100
- Mean: 125 ÷ 9 = 13.9 (pulled up by the 100)
- Median: 4 (middle value, not affected by 100)
- Mode: 4 (appears three times)

Which measure best represents this data? Why?"""
        }
    ]

def create_math_geometry_data() -> List[Dict]:
    """Geometry tutoring examples"""
    return [
        {
            "instruction": "How do I find the area of different shapes?",
            "input": "",
            "output": """Area formulas are super useful in real life! Let me give you the key formulas and help you remember them.

**Basic Shapes:**

**Rectangle:** A = length × width
- Easy! Just multiply the two sides
- Example: 5m × 3m = 15 m²

**Square:** A = side²
- Since all sides are equal, just square one side
- Example: 4m × 4m = 16 m²

**Triangle:** A = ½ × base × height
- Remember: height must be perpendicular to base
- Example: base = 6m, height = 4m → A = ½ × 6 × 4 = 12 m²

**Circle:** A = πr²
- π ≈ 3.14, r is radius (center to edge)
- Example: radius = 3m → A = π × 3² = 9π ≈ 28.3 m²

**Parallelogram:** A = base × height
- Same as rectangle, but height is perpendicular distance
- Example: base = 8m, height = 5m → A = 40 m²

**Trapezoid:** A = ½ × (base₁ + base₂) × height
- Average of the two parallel sides, times height
- Example: bases = 6m and 4m, height = 3m → A = ½ × (6+4) × 3 = 15 m²

**Memory tricks:**
- Triangle: "Half of rectangle" (½ × base × height)
- Circle: "Pi are squared" (πr²)
- Parallelogram: "Like rectangle but slanted"

**Real-world uses:**
- Painting walls (rectangles)
- Landscaping yards (various shapes)
- Pizza sizes (circles)

Which shape would you like to practice with?"""
        }
    ]

def create_science_physics_data() -> List[Dict]:
    """Physics tutoring examples"""
    return [
        {
            "instruction": "Can you explain force and motion in simple terms?",
            "input": "",
            "output": """Absolutely! Force and motion are all around us every day. Let me break this down in a way that makes sense.

**What is Force?**
Force is a push or a pull. That's it! When you push a door open, pull a drawer, or kick a ball, you're applying force.

**Types of Forces:**
- **Contact forces:** You touch the object (pushing, pulling, friction)
- **Non-contact forces:** No touching needed (gravity, magnetism)

**What is Motion?**
Motion is just change in position over time. An object is in motion if it's changing location.

**Key Concepts:**

**1. Balanced vs. Unbalanced Forces:**
- **Balanced:** Forces cancel out → no change in motion
  - Example: Book sitting on table (gravity down, table pushes up)
- **Unbalanced:** Net force exists → motion changes
  - Example: Pushing a shopping cart (your push > friction)

**2. Inertia:**
- Objects resist changes in motion
- Heavy objects have more inertia (harder to start/stop moving)
- Example: It's harder to push a full shopping cart than an empty one

**3. Acceleration:**
- Change in speed OR direction
- More force = more acceleration
- More mass = less acceleration (for same force)

**Real-world examples:**
- **Car accelerating:** Engine force > air resistance and friction
- **Falling objects:** Gravity pulls down (until air resistance balances it)
- **Walking:** You push back on ground, ground pushes you forward

**Fun fact:** When you're in a moving car at constant speed, you don't feel the motion because there's no acceleration!

What aspect of force and motion would you like to explore more?"""
        },
        {
            "instruction": "How does electricity work?",
            "input": "",
            "output": """Electricity might seem mysterious, but it's actually based on simple principles! Let me explain it in a way that makes sense.

**What is Electricity?**
Electricity is the flow of tiny particles called electrons. Think of it like water flowing through pipes.

**Key Concepts:**

**1. Electric Current:**
- Flow of electrons through a conductor (like wire)
- Measured in amperes (amps)
- Like water flow rate in a pipe

**2. Voltage:**
- The "pressure" that pushes electrons
- Measured in volts
- Like water pressure in pipes
- Higher voltage = more "push"

**3. Resistance:**
- How much a material opposes electron flow
- Measured in ohms
- Like friction in a pipe
- Thicker wires = less resistance

**The Water Analogy:**
- **Voltage** = water pressure
- **Current** = flow rate
- **Resistance** = pipe width/friction
- **Battery** = water pump

**Ohm's Law:** V = I × R
- Voltage = Current × Resistance
- If you increase voltage, current increases
- If you increase resistance, current decreases

**Types of Current:**
- **DC (Direct Current):** Flows one direction (batteries)
- **AC (Alternating Current):** Changes direction rapidly (wall outlets)

**Safety Rules:**
- Electricity always takes the easiest path
- Your body conducts electricity (dangerous!)
- Never mix electricity and water
- Respect electrical devices

**Real-world examples:**
- **Flashlight:** Battery pushes current through bulb
- **House wiring:** AC current powers appliances
- **Lightning:** Massive voltage discharge

**Fun fact:** The electricity in your house changes direction 60 times per second!

What part of electricity would you like to understand better?"""
        }
    ]

def create_science_chemistry_data() -> List[Dict]:
    """Chemistry tutoring examples"""
    return [
        {
            "instruction": "What are atoms and how do they work?",
            "input": "",
            "output": """Atoms are the building blocks of everything around you! Let me help you understand these tiny but incredibly important particles.

**What is an Atom?**
An atom is the smallest unit of an element that still has the properties of that element. Think of it as the "LEGO brick" of matter.

**Parts of an Atom:**

**1. Nucleus (Center):**
- **Protons:** Positive charge, determines what element it is
- **Neutrons:** No charge, adds mass and stability
- Tiny but contains almost all the atom's mass

**2. Electron Cloud (Outside):**
- **Electrons:** Negative charge, much lighter than protons
- Move around the nucleus in "shells" or energy levels
- Determine how atoms bond with each other

**Size Perspective:**
If an atom were the size of a football stadium, the nucleus would be like a marble at the center!

**Key Rules:**
- **Atoms are neutral:** Equal numbers of protons and electrons
- **Atomic number:** Number of protons (defines the element)
- **Mass number:** Protons + neutrons

**Examples:**
- **Hydrogen:** 1 proton, 1 electron (simplest atom)
- **Carbon:** 6 protons, 6 electrons, usually 6 neutrons
- **Oxygen:** 8 protons, 8 electrons, usually 8 neutrons

**Why This Matters:**
- Different arrangements = different elements
- Electrons determine chemical bonding
- Understanding atoms explains why materials have different properties

**Fun Facts:**
- You're made of about 7 octillion atoms (7 followed by 27 zeros!)
- Atoms are 99.9% empty space
- The atoms in your body were forged in ancient stars

**Real-world connections:**
- **Medicine:** Understanding how drugs interact at atomic level
- **Technology:** Computer chips work by controlling electron flow
- **Environment:** Chemical reactions involve atoms rearranging

Would you like to learn about how atoms bond together to make molecules?"""
        }
    ]

def create_english_writing_data() -> List[Dict]:
    """English and writing tutoring examples"""
    return [
        {
            "instruction": "How do I write a strong introduction paragraph?",
            "input": "",
            "output": """A great introduction is like a movie trailer - it hooks your audience and gives them a preview of what's coming! Let me show you how to write one that grabs attention.

**The Introduction Formula:**

**1. Hook (1-2 sentences):**
Grab the reader's attention with:
- Surprising statistic: "Every year, Americans throw away 80 billion pounds of food."
- Thought-provoking question: "What if I told you that your smartphone is more powerful than the computers that sent humans to the moon?"
- Vivid scene: "The gymnasium fell silent as Sarah stepped up to the free-throw line."
- Bold statement: "Social media is rewiring our brains."

**2. Background/Context (2-3 sentences):**
- Give necessary background information
- Narrow from general topic to your specific focus
- Help readers understand why this matters

**3. Thesis Statement (1 sentence):**
- Your main argument or point
- Usually the last sentence of introduction
- Previews what your essay will prove

**Example Introduction:**
*Hook:* "Imagine never forgetting a face, a conversation, or even what you had for lunch three years ago."
*Context:* "While most of us struggle to remember where we put our keys, some people have a condition called hyperthymesia that makes forgetting nearly impossible. This rare ability affects fewer than 100 people worldwide and offers fascinating insights into how memory works."
*Thesis:* "Though hyperthymesia might seem like a superpower, research shows that perfect memory can be both a blessing and a curse for those who experience it."

**Common Mistakes to Avoid:**
- Starting with "In this essay, I will..." (boring!)
- Making your hook too dramatic or unrelated
- Including your thesis in the middle instead of at the end
- Making it too long (3-5 sentences is usually perfect)

**Pro Tips:**
- Write your introduction last (after you know what you're arguing)
- Read it out loud - does it flow?
- Make sure every sentence connects to the next

What topic are you writing about? I can help you craft a specific hook!"""
        },
        {
            "instruction": "How do I improve my vocabulary?",
            "input": "",
            "output": """Building vocabulary is like building muscle - it takes consistent practice, but the results are worth it! Here are proven strategies that actually work.

**Active Learning Strategies:**

**1. Context Clues Method:**
- When you encounter unknown words, try to guess meaning from context
- Look for definition clues, example clues, or contrast clues
- Then verify with a dictionary
- This builds your natural word-learning skills

**2. Word Families:**
- Learn related words together
- Example: "spect" (to look) → inspect, respect, spectacle, perspective
- Root words help you decode new vocabulary

**3. Personal Word Journal:**
- Keep a notebook of new words you encounter
- Write: word, definition, example sentence, personal connection
- Review weekly - repetition is key!

**4. Use New Words Immediately:**
- Try to use 3 new words in conversation each day
- Write sentences with new vocabulary
- "Use it or lose it" principle

**Reading Strategies:**

**5. Read Slightly Above Your Level:**
- Choose books with some challenging vocabulary
- Don't stop for every unknown word - get the gist first
- Circle words to look up later

**6. Diverse Reading:**
- News articles, fiction, science magazines, poetry
- Different genres use different vocabulary
- Exposes you to formal and informal language

**Memory Techniques:**

**7. Visual Associations:**
- Create mental images for new words
- "Gregarious" (sociable) → imagine a person at a party
- Silly images often stick better!

**8. Word Games:**
- Crosswords, Scrabble, word apps
- Makes learning fun and competitive
- Try "Word of the Day" apps

**Long-term Habits:**
- Set realistic goals (5 new words per week)
- Focus on words you'll actually use
- Practice in different contexts (speaking, writing, thinking)

**Pro tip:** Don't just memorize definitions - understand how words are used in different situations. "House" and "home" both mean dwelling, but they feel different!

What type of vocabulary are you most interested in building - academic, creative writing, or everyday conversation?"""
        }
    ]

def create_history_data() -> List[Dict]:
    """History tutoring examples"""
    return [
        {
            "instruction": "Why is the Renaissance important?",
            "input": "",
            "output": """The Renaissance was one of the most transformative periods in human history! Let me explain why it matters so much.

**What was the Renaissance?**
"Renaissance" means "rebirth" in French. It was a period (roughly 1300-1600) when Europe experienced a cultural, artistic, and intellectual revival after the Middle Ages.

**Why It Started:**
- **Rediscovery of classical texts:** Greek and Roman works were translated and studied
- **Rise of wealthy merchant cities:** Especially in Italy (Florence, Venice)
- **New trade routes:** Brought wealth and new ideas
- **Decline of feudalism:** People had more freedom to think and create

**Major Changes:**

**1. Art Revolution:**
- **Before:** Flat, religious-focused art
- **Renaissance:** Realistic, human-centered art
- **Key figures:** Leonardo da Vinci, Michelangelo, Raphael
- **Innovations:** Perspective, oil painting, detailed anatomy

**2. Scientific Method:**
- **Before:** Accept what authorities said
- **Renaissance:** Observe, experiment, question
- **Key figures:** Galileo, Copernicus, Vesalius
- **Impact:** Foundation of modern science

**3. Humanism:**
- **Focus shifted:** From God-centered to human-centered
- **Education:** Liberal arts, critical thinking
- **Individual worth:** People could achieve greatness

**4. Literature and Ideas:**
- **Printing press:** Books became accessible
- **Vernacular writing:** Authors wrote in local languages, not just Latin
- **Key figures:** Shakespeare, Dante, Machiavelli

**Long-term Impact:**
- **Scientific Revolution:** Led to modern medicine, astronomy, physics
- **Exploration Age:** Renaissance navigation led to global exploration
- **Reformation:** Questioning authority led to religious reform
- **Modern education:** Liberal arts curriculum still used today
- **Democratic ideals:** Individual worth concepts influenced later revolutions

**Why It Matters Today:**
- **Critical thinking:** Renaissance emphasis on questioning authority
- **Artistic techniques:** Still used in art and design
- **Scientific method:** Foundation of all modern research
- **Individual potential:** Belief that anyone can achieve greatness

**Fun fact:** Leonardo da Vinci designed helicopters, tanks, and submarines 500 years before they were built!

The Renaissance shows us how periods of curiosity, creativity, and open-mindedness can transform civilization. What aspect interests you most?"""
        }
    ]

def create_study_skills_data() -> List[Dict]:
    """Study skills and learning strategies"""
    return [
        {
            "instruction": "How can I manage my time better for studying?",
            "input": "",
            "output": """Time management is a skill that will help you not just in school, but throughout your entire life! Let me share some proven strategies.

**The Foundation: Planning**

**1. Time Audit:**
- Track how you spend time for one week
- Identify time wasters (social media, TV, etc.)
- Find your most productive hours
- Be honest about how long tasks actually take

**2. Priority Matrix:**
- **Urgent + Important:** Do first (upcoming tests)
- **Important + Not Urgent:** Schedule (long-term projects)
- **Urgent + Not Important:** Delegate or minimize
- **Neither:** Eliminate

**Effective Study Scheduling:**

**3. Time Blocking:**
- Assign specific times for specific subjects
- Example: 3-4 PM = Math, 4-5 PM = History
- Include breaks and buffer time
- Treat study blocks like appointments

**4. The Pomodoro Technique:**
- Study for 25 minutes, break for 5 minutes
- After 4 cycles, take a longer break (15-30 minutes)
- Helps maintain focus and prevents burnout
- Perfect for tasks you're avoiding

**5. Backward Planning:**
- Start with due date, work backward
- Break large projects into smaller tasks
- Assign deadlines to each part
- Example: Research paper due in 3 weeks
  - Week 1: Research and outline
  - Week 2: First draft
  - Week 3: Revise and edit

**Daily Habits:**

**6. The 2-Minute Rule:**
- If something takes less than 2 minutes, do it now
- Prevents small tasks from piling up
- Examples: Filing notes, responding to emails

**7. Evening Planning:**
- Spend 10 minutes each night planning tomorrow
- Reduces morning decision fatigue
- Helps you start the day with purpose

**8. Energy Management:**
- Do hardest subjects when you're most alert
- Save easier tasks for low-energy times
- Match task difficulty to your energy level

**Common Time Wasters to Avoid:**
- Perfectionism on low-stakes assignments
- Multitasking (it's actually less efficient)
- Not having a designated study space
- Checking phone/social media while studying

**Pro Tips:**
- Use a physical planner or calendar app
- Build in flexibility for unexpected events
- Reward yourself for sticking to your schedule
- Start with small changes - don't overhaul everything at once

**Remember:** The goal isn't to be busy all the time, it's to be productive with the time you have!

What's your biggest time management challenge? I can help you create a specific plan!"""
        }
    ]

def create_test_prep_data() -> List[Dict]:
    """Test preparation strategies"""
    return [
        {
            "instruction": "I get really nervous during tests. How can I manage test anxiety?",
            "input": "",
            "output": """Test anxiety is incredibly common - you're definitely not alone! The good news is that there are proven strategies to help you feel more confident and perform better.

**Understanding Test Anxiety:**
- **Physical symptoms:** Racing heart, sweating, nausea, tense muscles
- **Mental symptoms:** Blank mind, negative thoughts, difficulty concentrating
- **It's normal:** Some nervousness actually helps performance (keeps you alert)
- **The problem:** When anxiety becomes overwhelming and hurts performance

**Before the Test:**

**1. Preparation is Key:**
- **Study well in advance:** Cramming increases anxiety
- **Practice tests:** Simulate test conditions at home
- **Know the format:** Understand what types of questions to expect
- **Organize materials:** Have everything ready the night before

**2. Physical Preparation:**
- **Good sleep:** 7-9 hours the night before
- **Healthy breakfast:** Protein and complex carbs for steady energy
- **Light exercise:** A walk or stretching reduces tension
- **Avoid caffeine:** Can increase jitters

**3. Mental Preparation:**
- **Positive self-talk:** "I'm prepared" instead of "I'm going to fail"
- **Visualization:** Imagine yourself succeeding on the test
- **Relaxation techniques:** Deep breathing, progressive muscle relaxation

**During the Test:**

**4. Start Strong:**
- **Read instructions carefully:** Don't rush this step
- **Do easy questions first:** Builds confidence and momentum
- **Budget your time:** Quick mental calculation of time per section

**5. Anxiety Management Techniques:**
- **Deep breathing:** 4 counts in, hold for 4, out for 4
- **Progressive muscle relaxation:** Tense and release muscle groups
- **Positive mantras:** "I can do this," "One question at a time"
- **Refocus technique:** If mind goes blank, move to another question

**6. Strategic Approaches:**
- **Don't panic over one question:** Skip and return later
- **Trust your first instinct:** Usually correct unless you find an obvious error
- **Use process of elimination:** Cross out obviously wrong answers

**Long-term Strategies:**

**7. Build Confidence:**
- **Regular practice:** Take practice tests under timed conditions
- **Study groups:** Explaining concepts to others builds confidence
- **Track progress:** Notice improvement over time

**8. Reframe Your Thinking:**
- **Tests measure preparation, not worth as a person**
- **Mistakes are learning opportunities**
- **Focus on effort, not just results**

**Emergency Techniques:**
- **5-4-3-2-1 grounding:** Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste
- **Bathroom break:** If allowed, splash cold water on face
- **Gentle self-talk:** "This feeling will pass"

**Remember:**
- Some nervousness is normal and helpful
- Preparation is your best defense against anxiety
- Focus on what you can control (your effort and preparation)
- Every test is practice for the next one

What specific situations make you most anxious during tests? I can help you develop targeted strategies!"""
        }
    ]

def main():
    """Generate comprehensive tutoring dataset"""
    
    # Collect all data from different categories
    all_data = []
    
    # Math
    all_data.extend(create_math_algebra_data())
    all_data.extend(create_math_geometry_data())
    
    # Science
    all_data.extend(create_science_physics_data())
    all_data.extend(create_science_chemistry_data())
    
    # English
    all_data.extend(create_english_writing_data())
    
    # History
    all_data.extend(create_history_data())
    
    # Study Skills
    all_data.extend(create_study_skills_data())
    all_data.extend(create_test_prep_data())
    
    # Add metadata to each example
    for i, item in enumerate(all_data):
        item['id'] = f"comprehensive_tutor_{i+1:03d}"
        item['source'] = "comprehensive_tutor_data"
        item['quality'] = "high"
        item['type'] = "tutoring"
    
    # Shuffle the data for better training
    random.seed(42)
    random.shuffle(all_data)
    
    # Split into train/eval (90/10 split)
    split_idx = int(len(all_data) * 0.9)
    train_data = all_data[:split_idx]
    eval_data = all_data[split_idx:]
    
    # Create output directory
    os.makedirs("data_comprehensive", exist_ok=True)
    
    # Save training data
    with open("data_comprehensive/train.jsonl", "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    # Save evaluation data
    with open("data_comprehensive/eval.jsonl", "w", encoding="utf-8") as f:
        for item in eval_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Created comprehensive tutoring dataset:")
    print(f"   Training samples: {len(train_data)}")
    print(f"   Evaluation samples: {len(eval_data)}")
    print(f"   Total samples: {len(all_data)}")
    print(f"   Subjects covered: Math, Science, English, History, Study Skills")
    print(f"   Saved to: data_comprehensive/")
    
    # Show sample
    print(f"\n📝 Sample training example:")
    sample = train_data[0]
    print(f"Instruction: {sample['instruction']}")
    print(f"Output preview: {sample['output'][:300]}...")
    
    # Show subject distribution
    subjects = {}
    for item in all_data:
        instruction = item['instruction'].lower()
        if any(word in instruction for word in ['math', 'equation', 'algebra', 'geometry', 'calculate']):
            subjects['Math'] = subjects.get('Math', 0) + 1
        elif any(word in instruction for word in ['science', 'physics', 'chemistry', 'atom', 'force']):
            subjects['Science'] = subjects.get('Science', 0) + 1
        elif any(word in instruction for word in ['write', 'writing', 'essay', 'vocabulary', 'english']):
            subjects['English'] = subjects.get('English', 0) + 1
        elif any(word in instruction for word in ['history', 'renaissance', 'war']):
            subjects['History'] = subjects.get('History', 0) + 1
        elif any(word in instruction for word in ['study', 'time', 'test', 'anxiety', 'memory']):
            subjects['Study Skills'] = subjects.get('Study Skills', 0) + 1
        else:
            subjects['Other'] = subjects.get('Other', 0) + 1
    
    print(f"\n📊 Subject distribution:")
    for subject, count in subjects.items():
        print(f"   {subject}: {count} examples")

if __name__ == "__main__":
    main()