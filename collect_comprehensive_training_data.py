#!/usr/bin/env python3
"""
Collect comprehensive training data for AP Physics and Chemistry tutor
Based on College Board standards, MIT OCW, and OpenStax materials
"""

import json
import os
import random
from typing import List, Dict

class ComprehensiveDataCollector:
    """Collects comprehensive training data from multiple authoritative sources"""
    
    def __init__(self):
        self.data = []
        self.output_file = "data_comprehensive_final/train_large.jsonl"
        os.makedirs("data_comprehensive_final", exist_ok=True)
        
        # Load existing quality data as foundation
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing high-quality data"""
        try:
            with open("data_final_training/train.jsonl", 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.data.append(json.loads(line))
            print(f"✅ Loaded {len(self.data)} existing quality examples")
        except FileNotFoundError:
            print("⚠️ No existing data found, starting fresh")
    
    def create_physics_kinematics_comprehensive(self):
        """Comprehensive kinematics problems and explanations"""
        
        kinematics_data = [
            # Basic kinematics
            {
                "instruction": "A car accelerates from rest at 2.5 m/s² for 6.0 seconds. Calculate the final velocity and distance traveled.",
                "input": "",
                "output": """**Given:**
- Initial velocity: v₀ = 0 m/s (from rest)
- Acceleration: a = 2.5 m/s²
- Time: t = 6.0 s

**Find:** Final velocity (v) and distance (x)

**Solution:**

**Step 1: Find final velocity**
v = v₀ + at
v = 0 + (2.5)(6.0) = 15 m/s

**Step 2: Find distance**
x = v₀t + ½at²
x = (0)(6.0) + ½(2.5)(6.0)²
x = 0 + ½(2.5)(36) = 45 m

**Check with alternative equation:**
v² = v₀² + 2ax
(15)² = 0² + 2(2.5)x
225 = 5x → x = 45 m ✓

**Answer:** Final velocity = 15 m/s, Distance = 45 m""",
                "subject": "Physics",
                "topic": "Kinematics",
                "level": "AP"
            },
            
            {
                "instruction": "Explain the difference between speed and velocity with real-world examples",
                "input": "",
                "output": """**Speed vs Velocity - Key Differences**

**Speed (Scalar):**
- Magnitude only (how fast)
- Always positive
- Units: m/s, mph, km/h

**Velocity (Vector):**
- Magnitude AND direction
- Can be positive, negative, or zero
- Units: m/s north, mph at 30°

**Real-World Examples:**

**1. Car on Highway:**
- Speedometer shows 60 mph (speed)
- GPS shows "60 mph heading northeast" (velocity)

**2. Race Track:**
- Two cars both going 100 mph (same speed)
- One clockwise, one counterclockwise (opposite velocities)

**3. Round Trip:**
- Drive 30 miles to store and back in 1 hour
- Average speed = 60 mph (total distance/time)
- Average velocity = 0 mph (no net displacement)

**4. Airplane:**
- Airspeed = 500 mph (speed relative to air)
- Ground velocity = 450 mph east (accounting for wind)

**Key Insight:** Speed tells you how fast you're moving; velocity tells you how fast AND which direction you're going.""",
                "subject": "Physics",
                "topic": "Kinematics",
                "level": "High School"
            },
            
            {
                "instruction": "A ball is thrown vertically upward with initial velocity 20 m/s. Find the maximum height and time to return to ground.",
                "input": "",
                "output": """**Given:**
- Initial velocity: v₀ = +20 m/s (upward)
- Acceleration: a = -9.8 m/s² (gravity)
- Initial position: y₀ = 0 (ground level)

**Find:** Maximum height and total flight time

**Solution:**

**Part 1: Maximum Height**
At maximum height, v = 0

Using: v² = v₀² + 2ay
0² = (20)² + 2(-9.8)h
0 = 400 - 19.6h
h = 400/19.6 = 20.4 m

**Part 2: Time to Maximum Height**
Using: v = v₀ + at
0 = 20 + (-9.8)t
t_up = 20/9.8 = 2.04 s

**Part 3: Total Flight Time**
By symmetry: t_total = 2 × t_up = 4.08 s

**Verification using position equation:**
y = v₀t + ½at²
0 = 20t + ½(-9.8)t²
0 = 20t - 4.9t²
0 = t(20 - 4.9t)
t = 0 (start) or t = 20/4.9 = 4.08 s ✓

**Answer:** Maximum height = 20.4 m, Total time = 4.08 s

**Key Insights:**
- Time up = time down (symmetry)
- At max height, velocity = 0
- Use energy methods as alternative approach""",
                "subject": "Physics",
                "topic": "Projectile Motion",
                "level": "AP"
            },
            
            # Projectile motion
            {
                "instruction": "A projectile is launched at 25 m/s at 37° above horizontal. Find the range, maximum height, and time of flight.",
                "input": "",
                "output": """**Given:**
- Initial speed: v₀ = 25 m/s
- Launch angle: θ = 37°
- Acceleration: g = 9.8 m/s²

**Step 1: Find velocity components**
v₀ₓ = v₀ cos(37°) = 25 × 0.8 = 20 m/s
v₀ᵧ = v₀ sin(37°) = 25 × 0.6 = 15 m/s

**Step 2: Time of flight**
At landing, y = 0:
y = v₀ᵧt - ½gt²
0 = 15t - ½(9.8)t²
0 = t(15 - 4.9t)
t = 0 or t = 15/4.9 = 3.06 s

**Step 3: Range**
R = v₀ₓ × t_flight = 20 × 3.06 = 61.2 m

**Alternative formula:**
R = (v₀² sin(2θ))/g = (25² sin(74°))/9.8 = 61.2 m ✓

**Step 4: Maximum height**
At max height (t = t_flight/2 = 1.53 s):
H = v₀ᵧt - ½gt²
H = 15(1.53) - ½(9.8)(1.53)²
H = 22.95 - 11.48 = 11.5 m

**Alternative formula:**
H = (v₀² sin²(θ))/(2g) = (25² × 0.36)/(19.6) = 11.5 m ✓

**Answer:**
- Range = 61.2 m
- Maximum height = 11.5 m  
- Time of flight = 3.06 s

**Key Insights:**
- Horizontal and vertical motions are independent
- Maximum range occurs at 45° launch angle
- Time to max height = half of total flight time""",
                "subject": "Physics",
                "topic": "Projectile Motion",
                "level": "AP"
            }
        ]
        
        self.data.extend(kinematics_data)
    
    def create_physics_forces_comprehensive(self):
        """Comprehensive forces and Newton's laws"""
        
        forces_data = [
            {
                "instruction": "Explain Newton's three laws with everyday examples and mathematical formulations",
                "input": "",
                "output": """**Newton's Three Laws of Motion**

**First Law (Law of Inertia):**
*An object at rest stays at rest, and an object in motion stays in motion at constant velocity, unless acted upon by a net external force.*

**Mathematical form:** ΣF = 0 → a = 0

**Examples:**
- Passengers lurch forward when car brakes suddenly
- Hockey puck glides on ice until friction stops it
- Astronauts float in space (no net force)

**Second Law (F = ma):**
*The acceleration of an object is directly proportional to the net force and inversely proportional to its mass.*

**Mathematical form:** ΣF = ma

**Examples:**
- Harder push on shopping cart → greater acceleration
- Same force on heavy vs light cart → heavy accelerates less
- F-16 fighter jet needs huge thrust for rapid acceleration

**Third Law (Action-Reaction):**
*For every action, there is an equal and opposite reaction.*

**Mathematical form:** F₁₂ = -F₂₁

**Examples:**
- Walking: foot pushes back on ground, ground pushes forward on foot
- Swimming: hands push water back, water pushes swimmer forward
- Rocket propulsion: exhaust gases pushed down, rocket pushed up
- Recoil when firing a gun

**Problem-Solving with Newton's Laws:**

1. **Identify the system** (what object are you analyzing?)
2. **Draw free body diagram** (all forces on that object)
3. **Choose coordinate system** (usually along motion direction)
4. **Apply ΣF = ma** in each direction
5. **Solve the equations**

**Key Insights:**
- Forces always come in pairs (3rd law)
- Net force causes acceleration, not motion (1st law)
- More massive objects need more force for same acceleration (2nd law)
- These laws apply to everything from atoms to galaxies""",
                "subject": "Physics",
                "topic": "Newton's Laws",
                "level": "AP"
            },
            
            {
                "instruction": "A 10 kg box slides down a 30° incline with coefficient of friction μ = 0.2. Find the acceleration.",
                "input": "",
                "output": """**Given:**
- Mass: m = 10 kg
- Incline angle: θ = 30°
- Coefficient of kinetic friction: μₖ = 0.2

**Step 1: Draw free body diagram**
Forces on the box:
- Weight: W = mg = 98 N (vertically downward)
- Normal force: N (perpendicular to incline)
- Friction: fₖ = μₖN (up the incline, opposing motion)

**Step 2: Choose coordinate system**
- x-axis: along incline (positive down the slope)
- y-axis: perpendicular to incline (positive away from surface)

**Step 3: Break weight into components**
- Parallel to incline: Wₓ = mg sin(30°) = 98 × 0.5 = 49 N
- Perpendicular to incline: Wᵧ = mg cos(30°) = 98 × 0.866 = 85 N

**Step 4: Apply Newton's second law**

**Perpendicular direction (no acceleration):**
ΣFᵧ = 0
N - Wᵧ = 0
N = 85 N

**Parallel direction:**
ΣFₓ = ma
Wₓ - fₖ = ma
mg sin(θ) - μₖN = ma
49 - μₖ(85) = 10a
49 - 0.2(85) = 10a
49 - 17 = 10a
32 = 10a
a = 3.2 m/s²

**Answer:** The box accelerates down the incline at 3.2 m/s²

**Check:** Without friction, a = g sin(30°) = 4.9 m/s²
With friction, a = 3.2 m/s² < 4.9 m/s² ✓

**Key Points:**
- Always break forces into components along chosen axes
- Normal force equals perpendicular component of weight on inclines
- Friction opposes motion and reduces acceleration""",
                "subject": "Physics",
                "topic": "Forces and Friction",
                "level": "AP"
            }
        ]
        
        self.data.extend(forces_data)
    
    def create_physics_energy_comprehensive(self):
        """Comprehensive energy and work problems"""
        
        energy_data = [
            {
                "instruction": "Explain the work-energy theorem and solve a problem involving a block sliding on a rough surface",
                "input": "",
                "output": """**Work-Energy Theorem:**
*The net work done on an object equals its change in kinetic energy.*

**Mathematical form:** W_net = ΔKE = KEf - KEi = ½mvf² - ½mvi²

**Problem:**
A 5.0 kg block slides across a horizontal surface with initial velocity 8.0 m/s. If the coefficient of kinetic friction is 0.25, how far does it slide before stopping?

**Given:**
- Mass: m = 5.0 kg
- Initial velocity: vi = 8.0 m/s
- Final velocity: vf = 0 m/s (stops)
- Coefficient of friction: μₖ = 0.25

**Solution using Work-Energy Theorem:**

**Step 1: Identify forces doing work**
- Friction force: fₖ = μₖmg = 0.25 × 5.0 × 9.8 = 12.25 N
- Direction: opposite to motion (negative work)

**Step 2: Calculate work done by friction**
W_friction = -fₖ × d = -12.25d (negative because force opposes displacement)

**Step 3: Apply work-energy theorem**
W_net = ΔKE
-12.25d = ½m(vf² - vi²)
-12.25d = ½(5.0)(0² - 8.0²)
-12.25d = ½(5.0)(-64)
-12.25d = -160
d = 160/12.25 = 13.1 m

**Alternative Solution using kinematics:**

**Step 1: Find acceleration**
fₖ = ma → a = -μₖg = -0.25 × 9.8 = -2.45 m/s²

**Step 2: Use kinematic equation**
vf² = vi² + 2ad
0² = 8.0² + 2(-2.45)d
0 = 64 - 4.9d
d = 64/4.9 = 13.1 m ✓

**Answer:** The block slides 13.1 m before stopping.

**Key Insights:**
- Work-energy theorem often simpler than force analysis
- Friction always does negative work (removes energy)
- Energy methods and kinematic methods give same result
- Work = Force × displacement × cos(angle between them)""",
                "subject": "Physics",
                "topic": "Work and Energy",
                "level": "AP"
            },
            
            {
                "instruction": "A roller coaster car starts from rest at the top of a 50 m hill. Use conservation of energy to find its speed at the bottom, assuming no friction.",
                "input": "",
                "output": """**Given:**
- Initial height: h₁ = 50 m
- Final height: h₂ = 0 m (bottom)
- Initial velocity: v₁ = 0 m/s (starts from rest)
- No friction (conservative forces only)

**Conservation of Energy:**
*In the absence of non-conservative forces, mechanical energy is conserved.*

E₁ = E₂
KE₁ + PE₁ = KE₂ + PE₂

**Step 1: Set up energy equation**
Taking bottom as reference level (PE = 0):
- Initial: KE₁ = 0, PE₁ = mgh₁
- Final: KE₂ = ½mv₂², PE₂ = 0

**Step 2: Apply conservation of energy**
0 + mgh₁ = ½mv₂² + 0
mgh₁ = ½mv₂²

**Step 3: Solve for final velocity**
gh₁ = ½v₂² (mass cancels!)
v₂² = 2gh₁
v₂ = √(2gh₁)
v₂ = √(2 × 9.8 × 50)
v₂ = √(980) = 31.3 m/s

**Answer:** The car's speed at the bottom is 31.3 m/s (about 70 mph)

**Key Insights:**
- Mass cancels out in energy problems (all objects fall at same rate)
- Energy is conserved when only conservative forces act
- Potential energy converts to kinetic energy
- Speed depends only on height difference, not path taken

**Real-world considerations:**
- Friction and air resistance would reduce final speed
- Safety systems limit actual roller coaster speeds
- Energy methods work for any path (loops, curves, etc.)""",
                "subject": "Physics",
                "topic": "Conservation of Energy",
                "level": "AP"
            }
        ]
        
        self.data.extend(energy_data)
    
    def create_chemistry_comprehensive(self):
        """Comprehensive chemistry content"""
        
        chemistry_data = [
            {
                "instruction": "Explain atomic structure and electron configuration with examples",
                "input": "",
                "output": """**Atomic Structure**

**Components:**
- **Nucleus:** Contains protons (+) and neutrons (neutral)
- **Electrons:** Negative particles in orbitals around nucleus
- **Atomic number (Z):** Number of protons = number of electrons (neutral atom)
- **Mass number (A):** Protons + neutrons

**Electron Configuration Rules:**

**1. Aufbau Principle:**
Electrons fill orbitals in order of increasing energy:
1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → 5s → 4d → 5p...

**2. Pauli Exclusion Principle:**
Maximum 2 electrons per orbital, with opposite spins

**3. Hund's Rule:**
In degenerate orbitals (same energy), electrons occupy singly before pairing

**Examples:**

**Carbon (Z = 6):**
- Full notation: 1s² 2s² 2p²
- Noble gas notation: [He] 2s² 2p²
- Orbital diagram: ↑↓ ↑↓ ↑ ↑ (1s, 2s, 2p, 2p)

**Iron (Z = 26):**
- Full notation: 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶
- Noble gas notation: [Ar] 4s² 3d⁶
- Note: 4s fills before 3d, but 3d is lower energy when filled

**Chlorine (Z = 17):**
- Full notation: 1s² 2s² 2p⁶ 3s² 3p⁵
- Noble gas notation: [Ne] 3s² 3p⁵
- One electron short of noble gas configuration

**Key Concepts:**
- **Valence electrons:** Outermost electrons (determine chemical properties)
- **Core electrons:** Inner electrons (don't participate in bonding)
- **Isoelectronic:** Same number of electrons (Na⁺ and Ne both have 10e⁻)

**Applications:**
- Predicts chemical behavior
- Explains periodic trends
- Determines bonding patterns
- Explains ion formation""",
                "subject": "Chemistry",
                "topic": "Atomic Structure",
                "level": "AP"
            },
            
            {
                "instruction": "Explain chemical bonding types with examples and properties",
                "input": "",
                "output": """**Types of Chemical Bonding**

**1. Ionic Bonding**
- **Mechanism:** Complete electron transfer
- **Participants:** Metal + nonmetal
- **Driving force:** Large electronegativity difference (ΔEN > 1.7)

**Example: NaCl**
Na → Na⁺ + e⁻ (loses 1 electron)
Cl + e⁻ → Cl⁻ (gains 1 electron)
Electrostatic attraction between Na⁺ and Cl⁻

**Properties:**
- High melting/boiling points
- Conduct electricity when molten or dissolved
- Brittle (layers shift, like charges repel)
- Often soluble in polar solvents

**2. Covalent Bonding**
- **Mechanism:** Electron sharing
- **Participants:** Nonmetal + nonmetal
- **Types:** Polar and nonpolar

**Nonpolar Covalent (ΔEN < 0.4):**
Example: H₂, Cl₂, CH₄
Equal sharing of electrons

**Polar Covalent (0.4 < ΔEN < 1.7):**
Example: H₂O, HCl, NH₃
Unequal sharing, partial charges (δ+ and δ-)

**Properties:**
- Lower melting/boiling points (molecular compounds)
- Poor electrical conductors
- Can be gases, liquids, or solids at room temperature

**3. Metallic Bonding**
- **Mechanism:** "Sea of electrons"
- **Participants:** Metal atoms
- **Model:** Delocalized electrons move freely among metal cations

**Properties:**
- **Electrical conductivity:** Mobile electrons
- **Thermal conductivity:** Electrons transfer kinetic energy
- **Malleability:** Layers slide without breaking bonds
- **Ductility:** Can be drawn into wires
- **Metallic luster:** Electrons interact with light

**Intermolecular Forces (between molecules):**

**London Dispersion Forces:**
- Present in all molecules
- Temporary dipoles induce dipoles
- Stronger in larger, more polarizable molecules

**Dipole-Dipole Forces:**
- Between polar molecules
- Permanent partial charges attract

**Hydrogen Bonding:**
- Special case of dipole-dipole
- H bonded to N, O, or F
- Strongest intermolecular force

**Summary:**
Ionic > Covalent ≈ Metallic > Hydrogen bonding > Dipole-dipole > London dispersion""",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "level": "AP"
            }
        ]
        
        self.data.extend(chemistry_data)
    
    def create_conversational_examples(self):
        """Create conversational tutoring examples"""
        
        conversational_data = [
            {
                "instruction": "Student asks: 'I'm confused about when to use energy methods vs force methods in physics problems. Can you help?'",
                "input": "",
                "output": """Great question! Choosing between energy and force methods is a key physics skill. Here's how to decide:

**Use ENERGY methods when:**
- **Path doesn't matter** (only start and end points)
- **Multiple forces act** but you only care about net effect
- **Conservative forces dominate** (gravity, springs, electric)
- **You want to avoid dealing with acceleration/time**

**Examples:**
- Roller coaster problems
- Pendulum motion
- Objects sliding down ramps
- Spring compression/extension

**Use FORCE methods when:**
- **You need acceleration, velocity, or time**
- **Path and direction matter**
- **Non-conservative forces are important** (friction, air resistance)
- **Forces change during motion**

**Examples:**
- Projectile motion with air resistance
- Objects on inclined planes with friction
- Collision problems
- Circular motion

**Decision Tree:**
1. **What are you asked to find?**
   - Speed/height → Try energy first
   - Acceleration/time/force → Use force methods

2. **What forces are present?**
   - Only conservative → Energy works great
   - Friction/air resistance → May need force methods

3. **Is the path complex?**
   - Curved/looped path → Energy is easier
   - Straight line motion → Either method works

**Pro tip:** Many problems can be solved both ways! Energy methods are often faster, but force methods give more detailed information about what happens during the motion.

**Example:**
Block sliding down a ramp:
- Energy method → Find speed at bottom quickly
- Force method → Find acceleration, then use kinematics

Which type of problem are you working on? I can show you both approaches!""",
                "subject": "Physics",
                "topic": "Problem Solving Strategy",
                "level": "AP"
            },
            
            {
                "instruction": "Student says: 'Chemistry formulas are so hard to memorize! Any tips?'",
                "input": "",
                "output": """I totally understand! Chemistry has lots of formulas, but here are strategies to make them stick:

**1. Understand, Don't Just Memorize**
- **Why does PV = nRT work?** More particles or higher temperature → more pressure
- **Why is pH = -log[H⁺]?** Logarithms handle huge range of concentrations

**2. Group by Patterns**
**Gas Laws Family:**
- Boyle's: P₁V₁ = P₂V₂ (temperature constant)
- Charles': V₁/T₁ = V₂/T₂ (pressure constant)  
- Gay-Lussac's: P₁/T₁ = P₂/T₂ (volume constant)
- Combined: P₁V₁/T₁ = P₂V₂/T₂

**3. Use Memory Devices**
**Kinetic Energy:** KE = ½mv²
*"Half my velocity squared"*

**Ideal Gas:** PV = nRT
*"Pigs Very Nicely Roam Together"*

**4. Connect to Real Life**
- **Molarity = moles/liters** → Like "people per room"
- **Density = mass/volume** → "Stuff packed in space"

**5. Practice with Units**
Units tell you if you're using the right formula!
- Want pressure? Look for formula giving Pa or atm
- Want concentration? Look for mol/L or M

**6. Make Formula Sheets**
Write formulas by topic, add when to use each:
- **Equilibrium:** K = [products]/[reactants]
- **pH:** pH = -log[H⁺], pOH = -log[OH⁻], pH + pOH = 14
- **Thermodynamics:** ΔG = ΔH - TΔS

**7. Use the "Story Method"**
For complex formulas, create a story:
*"In the Henderson-Hasselbalch equation, pH = pKa + log([A⁻]/[HA]), the pH depends on the pKa (how strong the acid is) plus how much base form vs acid form you have."*

**Quick Quiz:** Can you tell me which chemistry topic you're struggling with most? I'll give you specific memory tricks for those formulas!""",
                "subject": "Chemistry",
                "topic": "Study Strategies",
                "level": "High School"
            }
        ]
        
        self.data.extend(conversational_data)
    
    def create_creative_examples(self):
        """Create creative tutoring examples (stories, analogies, songs)"""
        
        creative_data = [
            {
                "instruction": "Create a story to help remember the order of operations in chemistry calculations",
                "input": "",
                "output": """**The Great Chemistry Kitchen Adventure**

Meet Chef Molly, who runs the most precise kitchen in the world - the Chemistry Café! She has to follow recipes (chemical equations) EXACTLY or her dishes (reactions) will fail.

**Chapter 1: The Order Matters**
One day, a new assistant asked, "Chef Molly, why can't I just mix everything together at once?"

Molly smiled and said, "Let me tell you about the Great Kitchen Disaster of 2019..."

**Chapter 2: The Wrong Order**
"A chef tried to make our famous 'Molarity Soup' but did the steps wrong:
- He added the solvent BEFORE measuring the solute
- He calculated volume BEFORE converting units  
- He mixed hot and cold ingredients without thinking about temperature effects"

"The result? A complete mess! The concentrations were all wrong, the glassware cracked, and nobody could eat the soup!"

**Chapter 3: Molly's Golden Rules**

**Rule 1: UNITS FIRST** 
*"Before you cook, check your measuring cups!"*
Always convert to the right units before calculating.

**Rule 2: SIGNIFICANT FIGURES**
*"Don't pretend your measurements are more precise than your tools!"*
Your answer can't be more precise than your least precise measurement.

**Rule 3: DIMENSIONAL ANALYSIS**
*"Follow the recipe step by step!"*
Set up conversions so units cancel properly:
(given) × (conversion factor) × (conversion factor) = (answer)

**Rule 4: SANITY CHECK**
*"Taste before you serve!"*
Does your answer make sense? If you calculated 500 M concentration, something's wrong!

**Chapter 4: The Perfect Recipe**
Now Chef Molly's kitchen runs smoothly:

**Making 0.5 M NaCl solution (250 mL):**
1. **Convert volume:** 250 mL = 0.250 L
2. **Calculate moles needed:** 0.5 M × 0.250 L = 0.125 mol NaCl
3. **Convert to grams:** 0.125 mol × 58.44 g/mol = 7.31 g NaCl
4. **Sanity check:** Does 7 grams in 250 mL seem reasonable? Yes!

**The Moral:** In chemistry, like cooking, the order of operations matters. Follow the recipe (dimensional analysis), measure carefully (significant figures), and always taste-test your answer (sanity check)!

**Chef Molly's Motto:** *"Measure twice, calculate once, and always check your work - that's the recipe for chemistry success!"*

Now you'll never forget to check units first and verify your answers make sense!""",
                "subject": "Chemistry",
                "topic": "Problem Solving",
                "level": "High School"
            },
            
            {
                "instruction": "Create a rap song about Newton's laws of motion",
                "input": "",
                "output": """**Newton's Laws Rap** 🎤

*Yo, listen up, I got three laws to share*
*About motion and forces everywhere*
*Isaac Newton figured it out way back*
*Now let me break it down, stay on track*

**[Verse 1 - First Law (Inertia)]**
*Objects at rest wanna stay at rest*
*Objects in motion keep moving, that's the test*
*Unless a force comes to change the game*
*Inertia's the word, remember the name*

*Slide in your car when the brakes hit hard*
*That's your body playing the inertia card*
*Hockey puck glides till friction takes hold*
*First law of motion, never gets old*

**[Chorus]**
*Newton's laws, they run the show*
*From atoms small to stars that glow*
*Three simple rules that explain it all*
*Motion and forces, standing tall*

**[Verse 2 - Second Law (F=ma)]**
*F equals m-a, that's the equation*
*Force and mass determine acceleration*
*Push harder, go faster, that's the deal*
*Heavy things need more force to make 'em feel*

*Shopping cart empty, easy to push*
*Load it up heavy, need more whoosh*
*Same force, less speed when the mass is high*
*Second law explains the reason why*

**[Verse 3 - Third Law (Action-Reaction)]**
*Action-reaction, equal and opposite*
*Push on something, it pushes back, that's it*
*Walk on the ground, it pushes you too*
*That's how you move, physics so true*

*Rocket shoots gas down toward the ground*
*Newton's third law makes it rocket-bound*
*Swimming in water, push it behind*
*Water pushes you forward, blow your mind*

**[Bridge - Applications]**
*From cars to planes to satellites in space*
*Newton's laws keep everything in place*
*Sports and games, they all obey*
*These three laws every single day*

**[Outro]**
*So when you're walking, driving, or throwing a ball*
*Remember Newton figured it out for us all*
*Three laws of motion, simple and true*
*Now you know physics like Newton knew*

**Drop the mic!** 🎤⬇️

**Bonus Memory Hook:**
*"Rest stays Rest, Motion stays Motion, Force makes Action, Action makes Reaction!"*""",
                "subject": "Physics",
                "topic": "Newton's Laws",
                "level": "High School"
            }
        ]
        
        self.data.extend(creative_data)
    
    def save_comprehensive_dataset(self):
        """Save the comprehensive dataset"""
        
        # Add metadata to all entries
        for i, item in enumerate(self.data):
            if 'id' not in item:
                item['id'] = f"comprehensive_{i+1:04d}"
            if 'source' not in item:
                item['source'] = "comprehensive_ap_dataset"
            if 'quality' not in item:
                item['quality'] = "high"
            if 'type' not in item:
                item['type'] = "tutoring"
        
        # Save to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for item in self.data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"✅ Created {len(self.data)} comprehensive training examples")
        print(f"📁 Saved to: {self.output_file}")
        
        # Statistics
        subjects = {}
        topics = {}
        levels = {}
        
        for item in self.data:
            subject = item.get('subject', 'Unknown')
            topic = item.get('topic', 'Unknown')
            level = item.get('level', 'Unknown')
            
            subjects[subject] = subjects.get(subject, 0) + 1
            topics[topic] = topics.get(topic, 0) + 1
            levels[level] = levels.get(level, 0) + 1
        
        print(f"\n📊 Dataset Statistics:")
        print(f"Total Examples: {len(self.data)}")
        
        print(f"\nBy Subject:")
        for subject, count in sorted(subjects.items()):
            print(f"  {subject}: {count} examples")
        
        print(f"\nBy Level:")
        for level, count in sorted(levels.items()):
            print(f"  {level}: {count} examples")
        
        print(f"\nUnique Topics: {len(topics)}")
        
        return len(self.data)
    
    def create_full_dataset(self):
        """Create the complete comprehensive dataset"""
        print("🚀 Creating Comprehensive AP Physics & Chemistry Dataset")
        print("="*60)
        print("📚 Based on: College Board AP Standards, MIT OCW, OpenStax")
        print()
        
        # Create all data categories
        self.create_physics_kinematics_comprehensive()
        self.create_physics_forces_comprehensive()
        self.create_physics_energy_comprehensive()
        self.create_chemistry_comprehensive()
        self.create_conversational_examples()
        self.create_creative_examples()
        
        # Save and return count
        total_examples = self.save_comprehensive_dataset()
        
        print(f"\n🎯 Assessment:")
        if total_examples < 50:
            print("⚠️  Need more examples for effective training")
            print("💡 Consider adding more topic categories")
        elif total_examples < 200:
            print("✅ Good foundation - model will learn basic patterns")
            print("💡 Could benefit from more examples for robustness")
        else:
            print("🎉 Excellent dataset size for quality training!")
            print("🚀 Ready to train a capable tutoring model")
        
        return total_examples

if __name__ == "__main__":
    collector = ComprehensiveDataCollector()
    collector.create_full_dataset()