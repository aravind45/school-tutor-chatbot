#!/usr/bin/env python3
"""
Expand training data with comprehensive tutoring examples
"""

import json
import os
from typing import List, Dict

class ComprehensiveDataExpander:
    """Expands training data with comprehensive examples"""
    
    def __init__(self):
        self.data = []
        self.output_file = "data_comprehensive_final/train.jsonl"
        os.makedirs("data_comprehensive_final", exist_ok=True)
    
    def add_physics_mechanics(self):
        """Add comprehensive physics mechanics data"""
        
        mechanics_data = [
            # Kinematics
            {
                "instruction": "Explain the kinematic equations for uniformly accelerated motion",
                "input": "",
                "output": """The kinematic equations describe motion with constant acceleration. Here are the four key equations:

**The Big Four Kinematic Equations:**

**1. v = v₀ + at**
- Final velocity = initial velocity + acceleration × time
- Use when you don't need to know displacement

**2. x = x₀ + v₀t + ½at²**
- Position equation with time
- Use when you know time and need position

**3. v² = v₀² + 2a(x - x₀)**
- Velocity-position relationship (no time)
- Use when you don't know time

**4. x = x₀ + ½(v₀ + v)t**
- Average velocity equation
- Use when you know both initial and final velocities

**Problem-Solving Strategy:**
1. **List what you know** (given values)
2. **Identify what you need** (unknown)
3. **Choose the equation** that connects known and unknown
4. **Substitute and solve**
5. **Check units and reasonableness**

**Example Problem:**
A car accelerates from rest at 2 m/s² for 5 seconds. How far does it travel?

*Given:* v₀ = 0, a = 2 m/s², t = 5 s
*Find:* x (displacement)
*Equation:* x = v₀t + ½at² = 0 + ½(2)(5)² = 25 m

**Key Insight:** These equations only work for constant acceleration!""",
                "subject": "Physics",
                "topic": "Kinematics",
                "level": "High School"
            },
            
            # Projectile Motion
            {
                "instruction": "Explain projectile motion step by step",
                "input": "",
                "output": """Projectile motion combines horizontal uniform motion with vertical free fall motion.

**Key Principle:** Horizontal and vertical motions are INDEPENDENT.

**Horizontal Motion:**
- No acceleration (ignoring air resistance)
- Constant velocity: vₓ = v₀ cos(θ)
- Position: x = v₀ cos(θ) × t

**Vertical Motion:**
- Constant acceleration due to gravity: a = -g = -9.8 m/s²
- Initial velocity: v₀ᵧ = v₀ sin(θ)
- Velocity: vᵧ = v₀ sin(θ) - gt
- Position: y = v₀ sin(θ) × t - ½gt²

**Key Formulas:**

**Range (horizontal distance):**
R = (v₀² sin(2θ))/g

**Maximum height:**
H = (v₀² sin²(θ))/(2g)

**Time of flight:**
T = (2v₀ sin(θ))/g

**Trajectory equation:**
y = x tan(θ) - (gx²)/(2v₀² cos²(θ))

**Problem-Solving Steps:**
1. **Break initial velocity into components**
2. **Analyze horizontal and vertical motions separately**
3. **Use kinematic equations for each direction**
4. **Combine results as needed**

**Example:**
A ball is launched at 20 m/s at 30° above horizontal.

*Horizontal:* vₓ = 20 cos(30°) = 17.3 m/s
*Vertical:* vᵧ = 20 sin(30°) = 10 m/s

*Time to peak:* t = vᵧ/g = 10/9.8 = 1.02 s
*Maximum height:* H = vᵧ²/(2g) = 100/19.6 = 5.1 m
*Range:* R = v₀² sin(60°)/g = 400(0.866)/9.8 = 35.3 m

**Real Applications:** Sports (basketball, soccer), military ballistics, water fountains""",
                "subject": "Physics",
                "topic": "Projectile Motion",
                "level": "High School"
            },
            
            # Forces and Dynamics
            {
                "instruction": "How do you solve force problems using free body diagrams?",
                "input": "",
                "output": """Free body diagrams are essential for solving force problems systematically.

**Step-by-Step Process:**

**1. Isolate the Object**
- Draw the object as a simple shape (box, dot)
- Remove everything else from the picture

**2. Identify All Forces**
- **Weight:** Always points downward (mg)
- **Normal forces:** Perpendicular to surfaces
- **Friction:** Parallel to surfaces, opposes motion
- **Tension:** Along ropes/strings, always pulls
- **Applied forces:** As given in problem

**3. Draw Force Vectors**
- Start from the object's center
- Draw arrows in correct directions
- Label with force names and magnitudes

**4. Choose Coordinate System**
- Usually: x-axis along motion, y-axis perpendicular
- For inclines: x-axis along the slope

**5. Apply Newton's Second Law**
- ΣFₓ = maₓ (sum of x-components)
- ΣFᵧ = maᵧ (sum of y-components)

**Example Problem:**
A 10 kg box slides down a 30° incline with friction coefficient μ = 0.2.

**Free Body Diagram:**
- Weight: mg = 98 N (downward)
- Normal: N (perpendicular to incline)
- Friction: f = μN (up the incline)

**Component Analysis:**
- mg∥ = mg sin(30°) = 49 N (down incline)
- mg⊥ = mg cos(30°) = 85 N (into incline)

**Equations:**
- Perpendicular: N = mg cos(30°) = 85 N
- Parallel: mg sin(30°) - μN = ma
- 49 - 0.2(85) = 10a
- 49 - 17 = 10a
- a = 3.2 m/s² (down the incline)

**Common Mistakes to Avoid:**
- Forgetting to break weight into components on inclines
- Drawing forces on the wrong object
- Not choosing consistent coordinate system""",
                "subject": "Physics",
                "topic": "Forces and Free Body Diagrams",
                "level": "High School"
            }
        ]
        
        self.data.extend(mechanics_data)
    
    def add_chemistry_comprehensive(self):
        """Add comprehensive chemistry data"""
        
        chemistry_data = [
            {
                "instruction": "Explain acid-base chemistry and pH calculations",
                "input": "",
                "output": """Acid-base chemistry involves the transfer of protons (H⁺ ions) between substances.

**Definitions:**

**Arrhenius Theory:**
- **Acid:** Produces H⁺ ions in water
- **Base:** Produces OH⁻ ions in water

**Brønsted-Lowry Theory:**
- **Acid:** Proton (H⁺) donor
- **Base:** Proton (H⁺) acceptor

**Lewis Theory:**
- **Acid:** Electron pair acceptor
- **Base:** Electron pair donor

**pH Scale:**
pH = -log[H⁺]
- **Range:** 0 to 14
- **pH < 7:** Acidic
- **pH = 7:** Neutral
- **pH > 7:** Basic

**Key Relationships:**
- **Water autoionization:** H₂O ⇌ H⁺ + OH⁻
- **Kw = [H⁺][OH⁻] = 1.0 × 10⁻¹⁴** (at 25°C)
- **pH + pOH = 14**
- **pOH = -log[OH⁻]**

**Strong Acids (complete ionization):**
HCl, HBr, HI, HNO₃, H₂SO₄, HClO₄, HClO₃

**Strong Bases (complete ionization):**
Group 1 hydroxides: LiOH, NaOH, KOH, RbOH, CsOH
Group 2 hydroxides: Ca(OH)₂, Sr(OH)₂, Ba(OH)₂

**pH Calculations:**

**Strong Acid Example:**
0.01 M HCl
[H⁺] = 0.01 M = 1.0 × 10⁻² M
pH = -log(1.0 × 10⁻²) = 2.0

**Strong Base Example:**
0.005 M NaOH
[OH⁻] = 0.005 M = 5.0 × 10⁻³ M
pOH = -log(5.0 × 10⁻³) = 2.3
pH = 14 - 2.3 = 11.7

**Weak Acid Calculations:**
Use Ka expression and ICE table
HA ⇌ H⁺ + A⁻
Ka = [H⁺][A⁻]/[HA]

**Buffer Systems:**
- Resist pH changes
- Contain weak acid + conjugate base
- Henderson-Hasselbalch equation: pH = pKa + log([A⁻]/[HA])

**Titration Curves:**
- **Equivalence point:** Moles acid = moles base
- **Endpoint:** Indicator color change
- **Buffer region:** Gradual pH change""",
                "subject": "Chemistry",
                "topic": "Acid-Base Chemistry",
                "level": "AP"
            },
            
            {
                "instruction": "Explain chemical bonding: ionic, covalent, and metallic",
                "input": "",
                "output": """Chemical bonding explains how atoms combine to form compounds through electron interactions.

**Three Main Types of Bonding:**

**1. Ionic Bonding**
- **Mechanism:** Complete electron transfer
- **Participants:** Metal + nonmetal
- **Driving force:** Large electronegativity difference (>1.7)
- **Result:** Cations (+) and anions (-)

**Properties of Ionic Compounds:**
- High melting/boiling points
- Conduct electricity when molten or dissolved
- Brittle (shatter when stressed)
- Often soluble in polar solvents

**Example:** NaCl
Na → Na⁺ + e⁻ (loses electron)
Cl + e⁻ → Cl⁻ (gains electron)
Electrostatic attraction holds ions together

**2. Covalent Bonding**
- **Mechanism:** Electron sharing
- **Participants:** Nonmetal + nonmetal
- **Driving force:** Similar electronegativity (<1.7)
- **Result:** Shared electron pairs

**Types of Covalent Bonds:**
- **Nonpolar covalent:** Equal sharing (ΔEN < 0.4)
- **Polar covalent:** Unequal sharing (0.4 < ΔEN < 1.7)

**Properties of Covalent Compounds:**
- Lower melting/boiling points (molecular)
- Poor electrical conductors
- Can be gases, liquids, or solids at room temperature

**Example:** H₂O
Oxygen shares electrons with two hydrogens
Bent molecular geometry due to lone pairs

**3. Metallic Bonding**
- **Mechanism:** "Sea of electrons"
- **Participants:** Metal atoms
- **Model:** Delocalized electrons move freely
- **Result:** Positive metal cations in electron sea

**Properties of Metals:**
- **Conductivity:** Mobile electrons carry current
- **Malleability:** Layers can slide past each other
- **Ductility:** Can be drawn into wires
- **Luster:** Electrons interact with light

**VSEPR Theory (Molecular Geometry):**
Electron pairs repel and arrange to minimize repulsion

**Common Geometries:**
- **Linear:** 2 electron pairs (180°)
- **Trigonal planar:** 3 electron pairs (120°)
- **Tetrahedral:** 4 electron pairs (109.5°)
- **Trigonal bipyramidal:** 5 electron pairs
- **Octahedral:** 6 electron pairs (90°)

**Intermolecular Forces:**
- **London dispersion:** All molecules (weakest)
- **Dipole-dipole:** Polar molecules
- **Hydrogen bonding:** H bonded to N, O, or F (strongest)

**Bond Strength Order:**
Ionic ≈ Covalent > Metallic > Intermolecular forces""",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "level": "AP"
            }
        ]
        
        self.data.extend(chemistry_data)
    
    def add_conversational_tutoring(self):
        """Add conversational and creative tutoring examples"""
        
        conversational_data = [
            {
                "instruction": "Student says: 'I'm really struggling with chemistry. Everything seems so abstract and hard to visualize.'",
                "input": "",
                "output": """I completely understand! Chemistry can feel abstract at first, but I promise it gets much clearer once you start thinking about it the right way.

**Here's the secret:** Chemistry is actually happening all around you, all the time. Let me help you see it!

**Start with what you know:**
- **Cooking:** When you bake cookies, proteins denature, sugars caramelize, and Maillard reactions create flavors
- **Breathing:** You're doing gas exchange - O₂ in, CO₂ out
- **Digestion:** Enzymes are breaking down food molecules
- **Cleaning:** Soap molecules have hydrophilic and hydrophobic ends

**Visualization strategies:**

**1. Use analogies:**
- Atoms are like LEGO blocks - they connect in specific ways
- Electrons are like people at a dance - they pair up and move around
- Chemical reactions are like trading cards - atoms swap partners

**2. Draw everything:**
- Molecular structures (even simple ones)
- Electron dot diagrams
- Reaction mechanisms with arrows

**3. Use models:**
- Ball-and-stick models for molecules
- Your hands for orbital shapes
- Colored pens for different elements

**Let's start simple:** What specific chemistry topic is giving you the most trouble right now? I'll help you visualize it step by step.

Remember: Every chemistry expert started exactly where you are. The key is connecting abstract concepts to concrete things you can see and touch!""",
                "subject": "Chemistry",
                "topic": "Study Strategies",
                "level": "High School"
            },
            
            {
                "instruction": "Create a memorable story about electron configuration",
                "input": "",
                "output": """**The Electron Apartment Building**

Imagine atoms as apartment buildings where electrons live. Each building (atom) has strict rules about where electrons can live.

**The Building Rules:**

**Ground Floor (1s):** Only 2 apartments, always filled first
**Second Floor (2s):** 2 apartments, filled after ground floor is full
**Second Floor Penthouse (2p):** 6 luxury apartments with great views
**Third Floor (3s):** 2 apartments
**Third Floor Penthouse (3p):** 6 apartments
...and so on

**The Aufbau Principle - "The Filling Order":**
Electrons are like apartment hunters - they always choose the cheapest rent (lowest energy) first!

**Hund's Rule - "The Roommate Rule":**
In the penthouse suites (p, d, f orbitals), electrons prefer their own apartment before sharing. They're antisocial until they have to double up!

**Pauli Exclusion - "The Spin Rule":**
If two electrons share an apartment, they must have opposite "personalities" (spins). No two identical electrons allowed!

**Example - Carbon's Story:**
Carbon has 6 electrons looking for homes:
- 2 electrons move into 1s (ground floor full)
- 2 electrons move into 2s (second floor full)  
- 2 electrons move into 2p (each gets their own penthouse apartment)

**Configuration:** 1s² 2s² 2p²

**The Noble Gas Shortcut:**
Instead of describing every floor, you can say "like the previous fully-occupied building, plus..."
Carbon: [He] 2s² 2p²

**Why This Matters:**
Electron configuration determines:
- How atoms bond
- What compounds they form
- Their chemical properties
- Their position on the periodic table

The electrons in the highest floor (valence electrons) are the ones that interact with other atoms - they're the social butterflies of the atomic world!""",
                "subject": "Chemistry",
                "topic": "Electron Configuration",
                "level": "High School"
            }
        ]
        
        self.data.extend(conversational_data)
    
    def save_comprehensive_data(self):
        """Save all comprehensive training data"""
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for i, item in enumerate(self.data):
                item.update({
                    "id": f"comprehensive_tutor_{i+1:03d}",
                    "source": "comprehensive_tutoring_data",
                    "quality": "high",
                    "type": "tutoring"
                })
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"✅ Created {len(self.data)} comprehensive training examples")
        print(f"📁 Saved to: {self.output_file}")
        
        # Statistics
        subjects = {}
        topics = {}
        for item in self.data:
            subject = item.get('subject', 'Unknown')
            topic = item.get('topic', 'Unknown')
            subjects[subject] = subjects.get(subject, 0) + 1
            topics[topic] = topics.get(topic, 0) + 1
        
        print("\n📊 Data Statistics:")
        print("By Subject:")
        for subject, count in subjects.items():
            print(f"  {subject}: {count} examples")
        
        print("\nBy Topic:")
        for topic, count in topics.items():
            print(f"  {topic}: {count} examples")
    
    def create_all_comprehensive_data(self):
        """Create all comprehensive training data"""
        print("🔄 Creating comprehensive tutoring training data...")
        
        self.add_physics_mechanics()
        self.add_chemistry_comprehensive()
        self.add_conversational_tutoring()
        
        self.save_comprehensive_data()

if __name__ == "__main__":
    expander = ComprehensiveDataExpander()
    expander.create_all_comprehensive_data()