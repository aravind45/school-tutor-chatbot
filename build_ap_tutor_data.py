#!/usr/bin/env python3
"""
Build AP-Level Tutor Training Data

Creates specialized training data for:
- AP Physics 1, 2, and C (Mechanics & E&M)
- AP Chemistry
- AP Computer Science A and Principles

Based on College Board curriculum and teaching resources.
"""

import json
import os
import random
from typing import List, Dict

def create_ap_physics_mechanics_data() -> List[Dict]:
    """AP Physics C: Mechanics focused examples"""
    return [
        {
            "instruction": "Explain the relationship between force, mass, and acceleration in AP Physics terms.",
            "input": "",
            "output": """In AP Physics, Newton's Second Law (F = ma) is fundamental to understanding mechanics. Let me break this down at the AP level.

**Mathematical Relationship:**
ΣF = ma (vector form)
- ΣF is the net force (sum of all forces)
- m is mass (scalar, always positive)
- a is acceleration (vector, same direction as net force)

**Key AP Physics Concepts:**

**1. Vector Nature:**
- Force and acceleration are vectors
- Must consider components: Fx = max, Fy = may
- Direction matters: positive/negative indicates direction

**2. Free Body Diagrams:**
Essential for AP problems:
- Identify all forces acting on object
- Draw vectors from center of mass
- Choose coordinate system strategically

**3. Common AP Problem Types:**

**Inclined Planes:**
- Weight components: mg sin θ (parallel), mg cos θ (perpendicular)
- Normal force: N = mg cos θ (if no vertical acceleration)
- Net force down plane: mg sin θ - f = ma

**Atwood Machines:**
- Two masses connected by rope over pulley
- Same magnitude acceleration, opposite directions
- Tension is internal force, weight is external

**Circular Motion:**
- Centripetal force: Fc = mv²/r = mω²r
- Always directed toward center
- Can be provided by tension, gravity, normal force, etc.

**Problem-Solving Strategy (AP Method):**
1. **Identify the system** and draw free body diagram
2. **Choose coordinate system** (align with acceleration when possible)
3. **Apply Newton's Second Law** in component form
4. **Solve algebraically** before substituting numbers
5. **Check units and reasonableness**

**Example AP-Style Problem:**
A 2.0 kg block slides down a 30° incline with coefficient of kinetic friction μk = 0.25. Find the acceleration.

**Solution:**
- Forces parallel to incline: mg sin 30° - fk = ma
- Normal force: N = mg cos 30°
- Friction: fk = μkN = μkmg cos 30°
- Net equation: mg sin 30° - μkmg cos 30° = ma
- Divide by m: a = g(sin 30° - μk cos 30°)
- a = 9.8(0.5 - 0.25 × 0.866) = 2.8 m/s²

This approach emphasizes the systematic problem-solving skills essential for AP Physics success."""
        },
        {
            "instruction": "How do I approach rotational motion problems in AP Physics C?",
            "input": "",
            "output": """Rotational motion in AP Physics C requires understanding the parallels between linear and rotational quantities. Here's your comprehensive guide:

**Linear vs. Rotational Analogies:**
- Position (x) ↔ Angle (θ)
- Velocity (v) ↔ Angular velocity (ω)
- Acceleration (a) ↔ Angular acceleration (α)
- Mass (m) ↔ Moment of inertia (I)
- Force (F) ↔ Torque (τ)

**Key Rotational Equations:**

**Kinematic Equations:**
- θ = θ₀ + ω₀t + ½αt²
- ω = ω₀ + αt
- ω² = ω₀² + 2α(θ - θ₀)

**Dynamic Equations:**
- τ = Iα (rotational Newton's second law)
- τ = r × F = rF sin φ (torque definition)
- L = Iω (angular momentum)

**Moment of Inertia (Common Shapes):**
- Point mass: I = mr²
- Solid cylinder: I = ½mr²
- Solid sphere: I = ⅖mr²
- Rod about center: I = 1/12 ml²
- Rod about end: I = ⅓ml²

**Problem-Solving Strategy:**

**1. Identify the Type:**
- Pure rotation about fixed axis
- Rolling motion (rotation + translation)
- Conservation of angular momentum

**2. For Pure Rotation:**
- Draw diagram showing rotation axis
- Identify all torques about that axis
- Apply τnet = Iα
- Use kinematic equations if needed

**3. For Rolling Motion:**
- Constraint: v = ωr (no slipping)
- Energy: KE = ½mv² + ½Iω² = ½mv²(1 + I/mr²)
- Forces: Apply both F = ma and τ = Iα

**Example AP Problem:**
A solid cylinder (mass M, radius R) rolls down an incline of angle θ. Find its acceleration.

**Solution:**
**Forces on cylinder:**
- Weight: Mg (down)
- Normal: N (perpendicular to incline)
- Friction: f (up the incline)

**Linear motion (down incline):**
Mg sin θ - f = Ma

**Rotational motion (about center):**
fR = Iα = ½MR²α

**Rolling constraint:**
a = αR, so α = a/R

**Substitute:**
fR = ½MR²(a/R) = ½MRa
Therefore: f = ½Ma

**Combine equations:**
Mg sin θ - ½Ma = Ma
Mg sin θ = 1.5Ma
a = (2/3)g sin θ

**Key Insight:** Rolling objects accelerate slower than sliding objects because some energy goes into rotation.

**Common AP Mistakes to Avoid:**
- Forgetting the rolling constraint v = ωr
- Using wrong moment of inertia formula
- Not considering all torques about chosen axis
- Mixing up signs in torque calculations

This systematic approach will help you tackle any rotational motion problem on the AP exam!"""
        }
    ]

def create_ap_chemistry_data() -> List[Dict]:
    """AP Chemistry focused examples"""
    return [
        {
            "instruction": "Explain chemical equilibrium and Le Chatelier's principle for AP Chemistry.",
            "input": "",
            "output": """Chemical equilibrium is a central concept in AP Chemistry that connects thermodynamics, kinetics, and molecular behavior. Let me break this down systematically.

**What is Chemical Equilibrium?**
A dynamic state where the forward and reverse reaction rates are equal, resulting in constant concentrations of reactants and products.

**Key Characteristics:**
- **Dynamic:** Reactions continue in both directions
- **Macroscopic:** No observable changes in concentrations
- **Microscopic:** Continuous molecular collisions and reactions

**Equilibrium Expression:**
For reaction: aA + bB ⇌ cC + dD

Keq = [C]^c[D]^d / [A]^a[B]^b

**Important Notes:**
- Only includes aqueous and gaseous species
- Solids and pure liquids have activity = 1
- Temperature dependent
- Unitless (activities, not concentrations)

**Le Chatelier's Principle:**
"When a system at equilibrium is disturbed, it shifts to counteract the disturbance."

**Types of Disturbances:**

**1. Concentration Changes:**
- **Add reactant/remove product:** Shifts right (forward)
- **Remove reactant/add product:** Shifts left (reverse)
- **Example:** N₂ + 3H₂ ⇌ 2NH₃
  - Adding N₂ shifts right to consume excess N₂

**2. Pressure/Volume Changes (gases only):**
- **Increase pressure (decrease volume):** Shifts toward fewer gas molecules
- **Decrease pressure (increase volume):** Shifts toward more gas molecules
- **Example:** N₂ + 3H₂ ⇌ 2NH₃ (4 moles → 2 moles)
  - Increased pressure shifts right

**3. Temperature Changes:**
- **Exothermic reaction (ΔH < 0):**
  - Increase T: Shifts left (endothermic direction)
  - Decrease T: Shifts right (exothermic direction)
- **Endothermic reaction (ΔH > 0):**
  - Increase T: Shifts right (endothermic direction)
  - Decrease T: Shifts left (exothermic direction)

**4. Catalysts:**
- **No effect on equilibrium position**
- Increases both forward and reverse rates equally
- Reaches equilibrium faster

**AP Problem-Solving Strategy:**

**ICE Tables (Initial, Change, Equilibrium):**
```
        N₂  +  3H₂  ⇌  2NH₃
I:      0.5    1.5      0
C:      -x     -3x     +2x
E:    0.5-x   1.5-3x    2x
```

**Example AP Problem:**
At 500°C, Keq = 0.040 for N₂ + 3H₂ ⇌ 2NH₃
Initial: [N₂] = 0.50 M, [H₂] = 1.5 M, [NH₃] = 0 M
Find equilibrium concentrations.

**Solution:**
Keq = [NH₃]² / ([N₂][H₂]³) = 0.040

0.040 = (2x)² / ((0.5-x)(1.5-3x)³)

This requires approximation or numerical methods typical in AP problems.

**Connection to Thermodynamics:**
- ΔG° = -RT ln Keq
- Keq > 1: Products favored (ΔG° < 0)
- Keq < 1: Reactants favored (ΔG° > 0)

**Common AP Applications:**
- Acid-base equilibria (Ka, Kb)
- Solubility equilibria (Ksp)
- Complex ion formation (Kf)
- Gas phase reactions

Understanding equilibrium is crucial for predicting reaction behavior and optimizing industrial processes!"""
        }
    ]

def create_ap_computer_science_data() -> List[Dict]:
    """AP Computer Science A and Principles examples"""
    return [
        {
            "instruction": "Explain object-oriented programming concepts for AP Computer Science A.",
            "input": "",
            "output": """Object-Oriented Programming (OOP) is fundamental to AP Computer Science A and Java programming. Let me explain the core concepts with examples.

**The Four Pillars of OOP:**

**1. Encapsulation:**
Bundling data (attributes) and methods that operate on that data within a single unit (class).

```java
public class BankAccount {
    private double balance;  // Private data
    private String accountNumber;
    
    // Public methods to access private data
    public double getBalance() {
        return balance;
    }
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
    
    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }
}
```

**Benefits:**
- Data protection (private variables)
- Controlled access through methods
- Easier maintenance and debugging

**2. Inheritance:**
Creating new classes based on existing classes, inheriting their properties and methods.

```java
// Parent class
public class Vehicle {
    protected String make;
    protected String model;
    protected int year;
    
    public void start() {
        System.out.println("Vehicle starting...");
    }
}

// Child class
public class Car extends Vehicle {
    private int numDoors;
    
    public Car(String make, String model, int year, int doors) {
        this.make = make;
        this.model = model;
        this.year = year;
        this.numDoors = doors;
    }
    
    @Override
    public void start() {
        System.out.println("Car engine starting...");
    }
    
    public void honk() {
        System.out.println("Beep beep!");
    }
}
```

**Key Concepts:**
- `extends` keyword creates inheritance
- `super` refers to parent class
- `@Override` indicates method overriding
- Child class inherits all public/protected members

**3. Polymorphism:**
Objects of different classes can be treated as objects of a common base class.

```java
public class AnimalDemo {
    public static void main(String[] args) {
        Animal[] animals = {
            new Dog("Buddy"),
            new Cat("Whiskers"),
            new Bird("Tweety")
        };
        
        // Polymorphism in action
        for (Animal animal : animals) {
            animal.makeSound();  // Different sound for each animal
        }
    }
}

abstract class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public abstract void makeSound();  // Must be implemented by subclasses
}

class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }
    
    public void makeSound() {
        System.out.println(name + " says: Woof!");
    }
}
```

**4. Abstraction:**
Hiding complex implementation details while showing only essential features.

```java
// Interface defines what methods must exist
public interface Drawable {
    void draw();
    void resize(double factor);
}

// Abstract class provides partial implementation
public abstract class Shape implements Drawable {
    protected double x, y;
    
    public Shape(double x, double y) {
        this.x = x;
        this.y = y;
    }
    
    public abstract double getArea();  // Must be implemented
    
    public void move(double dx, double dy) {  // Common implementation
        x += dx;
        y += dy;
    }
}

public class Circle extends Shape {
    private double radius;
    
    public Circle(double x, double y, double radius) {
        super(x, y);
        this.radius = radius;
    }
    
    public double getArea() {
        return Math.PI * radius * radius;
    }
    
    public void draw() {
        System.out.println("Drawing circle at (" + x + ", " + y + ")");
    }
    
    public void resize(double factor) {
        radius *= factor;
    }
}
```

**AP Exam Key Points:**

**Class Design:**
- Choose appropriate access modifiers (private, public, protected)
- Use constructors to initialize objects
- Implement toString() and equals() methods when appropriate

**Inheritance Hierarchy:**
- Understand is-a vs has-a relationships
- Know when to use abstract classes vs interfaces
- Understand method overriding vs overloading

**Common AP Patterns:**
- ArrayList of objects
- Interfaces for common behavior
- Abstract classes for shared implementation
- Polymorphic method calls

**Example AP-Style Problem:**
Design a class hierarchy for a school system with Students, Teachers, and Administrators, all inheriting from Person.

This OOP foundation is essential for success in AP Computer Science A and real-world programming!"""
        }
    ]

def create_ap_physics_electricity_data() -> List[Dict]:
    """AP Physics C: Electricity & Magnetism examples"""
    return [
        {
            "instruction": "Explain Gauss's Law and how to apply it in AP Physics C problems.",
            "input": "",
            "output": """Gauss's Law is one of Maxwell's equations and a powerful tool for finding electric fields in AP Physics C. Let me explain both the concept and problem-solving techniques.

**Gauss's Law Statement:**
∮ E⃗ · dA⃗ = Qenc/ε₀

**Physical Meaning:**
The electric flux through any closed surface is proportional to the charge enclosed by that surface.

**Key Components:**
- **E⃗:** Electric field vector
- **dA⃗:** Differential area vector (points outward from surface)
- **Qenc:** Total charge enclosed by the Gaussian surface
- **ε₀:** Permittivity of free space (8.85 × 10⁻¹² C²/N·m²)

**When to Use Gauss's Law:**
Gauss's Law is most useful when the charge distribution has high symmetry:
- **Spherical symmetry:** Point charges, spherical charge distributions
- **Cylindrical symmetry:** Infinite line charges, cylindrical conductors
- **Planar symmetry:** Infinite sheets of charge, parallel plates

**Problem-Solving Strategy:**

**Step 1: Identify Symmetry**
Determine the type of symmetry in the charge distribution.

**Step 2: Choose Gaussian Surface**
Select a surface that matches the symmetry:
- Sphere for spherical symmetry
- Cylinder for cylindrical symmetry
- Pillbox for planar symmetry

**Step 3: Apply Symmetry Arguments**
Use symmetry to determine where E⃗ is constant, zero, or perpendicular to dA⃗.

**Step 4: Evaluate the Flux Integral**
∮ E⃗ · dA⃗ = E∮ dA = EA (when E is constant and parallel to dA⃗)

**Step 5: Find Enclosed Charge**
Calculate Qenc within the Gaussian surface.

**Step 6: Solve for E**
E = Qenc/(ε₀A)

**Example 1: Infinite Line Charge**
Find E⃗ at distance r from an infinite line with charge density λ.

**Solution:**
- **Symmetry:** Cylindrical
- **Gaussian surface:** Cylinder of radius r, length L
- **By symmetry:** E⃗ points radially outward, constant magnitude at fixed r
- **Flux:** ∮ E⃗ · dA⃗ = E(2πrL) (only curved surface contributes)
- **Enclosed charge:** Qenc = λL
- **Apply Gauss's Law:** E(2πrL) = λL/ε₀
- **Result:** E = λ/(2πε₀r)

**Example 2: Spherical Conductor**
A conducting sphere of radius R carries total charge Q. Find E⃗ everywhere.

**Solution:**
**Inside conductor (r < R):**
- **Gaussian surface:** Sphere of radius r < R
- **Key insight:** E⃗ = 0 inside conductor (electrostatic equilibrium)
- **Result:** E = 0

**Outside conductor (r > R):**
- **Gaussian surface:** Sphere of radius r > R
- **By symmetry:** E⃗ radial, constant magnitude at fixed r
- **Flux:** ∮ E⃗ · dA⃗ = E(4πr²)
- **Enclosed charge:** Qenc = Q (all charge on surface)
- **Apply Gauss's Law:** E(4πr²) = Q/ε₀
- **Result:** E = Q/(4πε₀r²) = kQ/r²

**Example 3: Infinite Sheet of Charge**
Find E⃗ near an infinite sheet with surface charge density σ.

**Solution:**
- **Symmetry:** Planar
- **Gaussian surface:** Cylindrical "pillbox" with area A
- **By symmetry:** E⃗ perpendicular to sheet, same magnitude on both sides
- **Flux:** ∮ E⃗ · dA⃗ = 2EA (both flat faces contribute)
- **Enclosed charge:** Qenc = σA
- **Apply Gauss's Law:** 2EA = σA/ε₀
- **Result:** E = σ/(2ε₀)

**Advanced Applications:**
- **Dielectrics:** Replace ε₀ with ε = κε₀
- **Conductors:** Use to find surface charge density
- **Capacitors:** Analyze field between plates

**Common AP Mistakes:**
- Wrong choice of Gaussian surface
- Forgetting that E⃗ = 0 inside conductors
- Not using symmetry arguments properly
- Incorrect calculation of enclosed charge

Mastering Gauss's Law gives you a powerful tool for the AP Physics C: E&M exam!"""
        },
        {
            "instruction": "How do I solve circuit problems with capacitors and resistors in AP Physics?",
            "input": "",
            "output": """Circuit analysis with capacitors and resistors is essential for AP Physics. Let me guide you through both DC steady-state and RC transient analysis.

**Capacitor Fundamentals:**
- **Definition:** C = Q/V (capacitance = charge/voltage)
- **Energy stored:** U = ½CV² = ½QV = Q²/(2C)
- **Current:** I = dQ/dt = C(dV/dt)

**Key Differences: Resistors vs Capacitors**

**Resistors:**
- **Series:** Rtotal = R₁ + R₂ + R₃ + ...
- **Parallel:** 1/Rtotal = 1/R₁ + 1/R₂ + 1/R₃ + ...
- **Voltage division:** V₁ = Vtotal × (R₁/Rtotal)
- **Current division:** I₁ = Itotal × (Rtotal/R₁)

**Capacitors:**
- **Series:** 1/Ctotal = 1/C₁ + 1/C₂ + 1/C₃ + ... (opposite of resistors!)
- **Parallel:** Ctotal = C₁ + C₂ + C₃ + ... (opposite of resistors!)
- **Voltage division (series):** V₁ = Vtotal × (Ctotal/C₁)
- **Charge sharing (parallel):** Q₁ = Qtotal × (C₁/Ctotal)

**DC Steady-State Analysis:**
In steady state (t → ∞), capacitors act like open circuits (I = 0).

**Example:** Find final voltages across capacitors.
```
Battery (12V) → R₁ (100Ω) → [R₂ (200Ω) parallel with C₁ (10μF)] → C₂ (5μF) → Ground
```

**Solution:**
1. **Steady state:** No current through capacitors
2. **No current through R₂** (in parallel with C₁)
3. **No current anywhere** in the circuit
4. **Voltage across C₂:** VC₂ = 12V (no voltage drop across resistors)
5. **Voltage across C₁:** VC₁ = 0V (no voltage drop across R₂)

**RC Transient Analysis:**
When capacitors charge or discharge, we get exponential behavior.

**Charging Capacitor (RC Circuit):**
- **Voltage:** VC(t) = V₀(1 - e^(-t/RC))
- **Current:** I(t) = (V₀/R)e^(-t/RC)
- **Time constant:** τ = RC

**Discharging Capacitor:**
- **Voltage:** VC(t) = V₀e^(-t/RC)
- **Current:** I(t) = -(V₀/R)e^(-t/RC)

**Problem-Solving Strategy:**

**Step 1: Identify Circuit Type**
- Pure resistor network
- Pure capacitor network  
- RC transient
- Mixed DC steady-state

**Step 2: For Steady-State DC**
- Replace capacitors with open circuits
- Analyze remaining resistor network
- Use Kirchhoff's laws if needed

**Step 3: For RC Transients**
- Find initial conditions (t = 0⁺)
- Find final conditions (t = ∞)
- Apply exponential formulas
- Calculate time constant τ = RC

**Example AP Problem:**
A 12V battery, 1000Ω resistor, and 10μF capacitor are connected in series. The capacitor is initially uncharged. Find:
a) Current at t = 0
b) Voltage across capacitor at t = 5ms
c) Time for capacitor to reach 8V

**Solution:**
**Given:** V₀ = 12V, R = 1000Ω, C = 10μF, τ = RC = 0.01s = 10ms

**a) Current at t = 0:**
I(0) = V₀/R = 12V/1000Ω = 12mA

**b) Voltage at t = 5ms:**
VC(5ms) = 12(1 - e^(-5ms/10ms)) = 12(1 - e^(-0.5)) = 12(1 - 0.606) = 4.73V

**c) Time to reach 8V:**
8 = 12(1 - e^(-t/10ms))
8/12 = 1 - e^(-t/10ms)
e^(-t/10ms) = 1 - 2/3 = 1/3
-t/10ms = ln(1/3) = -1.099
t = 10.99ms ≈ 11ms

**Advanced Topics:**
- **Multiple capacitors:** Use equivalent capacitance
- **Kirchhoff's laws:** For complex networks
- **Energy considerations:** Energy stored vs dissipated
- **AC circuits:** Impedance and phasors (AP Physics C)

**Common AP Mistakes:**
- Confusing series/parallel rules for capacitors vs resistors
- Forgetting steady-state behavior of capacitors
- Wrong time constant calculation
- Not considering initial conditions properly

Master these concepts and you'll excel at AP Physics circuit problems!"""
        }
    ]

def create_ap_chemistry_advanced_data() -> List[Dict]:
    """Advanced AP Chemistry topics"""
    return [
        {
            "instruction": "Explain electrochemistry and galvanic cells for AP Chemistry.",
            "input": "",
            "output": """Electrochemistry is a major topic in AP Chemistry that connects thermodynamics, kinetics, and atomic structure. Let me break down galvanic cells systematically.

**Fundamental Concepts:**

**Oxidation-Reduction (Redox):**
- **Oxidation:** Loss of electrons (increase in oxidation state)
- **Reduction:** Gain of electrons (decrease in oxidation state)
- **Memory device:** "OIL RIG" (Oxidation Is Loss, Reduction Is Gain)

**Galvanic (Voltaic) Cells:**
Spontaneous redox reactions that produce electrical energy.

**Cell Components:**
- **Anode:** Where oxidation occurs (electrons produced)
- **Cathode:** Where reduction occurs (electrons consumed)
- **Salt bridge:** Maintains electrical neutrality
- **External circuit:** Path for electron flow

**Standard Cell Notation:**
Anode | Anode solution || Cathode solution | Cathode

Example: Zn(s) | Zn²⁺(1M) || Cu²⁺(1M) | Cu(s)

**Cell Potential Calculations:**

**Standard Reduction Potentials (E°):**
Measured under standard conditions (25°C, 1M, 1 atm)

**Cell Potential Formula:**
E°cell = E°cathode - E°anode

**Example: Zinc-Copper Cell**
- **Anode reaction:** Zn(s) → Zn²⁺(aq) + 2e⁻  [E° = -0.76 V]
- **Cathode reaction:** Cu²⁺(aq) + 2e⁻ → Cu(s)  [E° = +0.34 V]
- **Overall:** Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)
- **E°cell = 0.34 - (-0.76) = 1.10 V**

**Thermodynamic Relationships:**

**Gibbs Free Energy:**
ΔG° = -nFE°cell
- n = moles of electrons transferred
- F = Faraday constant (96,485 C/mol)
- Spontaneous when E°cell > 0 (ΔG° < 0)

**Equilibrium Constant:**
E°cell = (RT/nF) ln K = (0.0257 V/n) ln K (at 25°C)

**Nernst Equation:**
For non-standard conditions:
Ecell = E°cell - (RT/nF) ln Q = E°cell - (0.0257/n) ln Q

**Example Calculation:**
Zn | Zn²⁺(0.10 M) || Cu²⁺(2.0 M) | Cu

E°cell = 1.10 V (from above)
Q = [Zn²⁺]/[Cu²⁺] = 0.10/2.0 = 0.050
n = 2 electrons

Ecell = 1.10 - (0.0257/2) ln(0.050)
Ecell = 1.10 - 0.01285(-2.996)
Ecell = 1.10 + 0.0385 = 1.14 V

**Types of Electrochemical Cells:**

**1. Galvanic Cells:**
- Spontaneous reactions (E°cell > 0)
- Convert chemical energy to electrical energy
- Examples: Batteries, fuel cells

**2. Electrolytic Cells:**
- Non-spontaneous reactions (E°cell < 0)
- Require external electrical energy
- Examples: Electrolysis, electroplating

**Common AP Applications:**

**Battery Analysis:**
- **Lead-acid battery:** Pb/PbSO₄/H₂SO₄/PbO₂
- **Alkaline battery:** Zn/KOH/MnO₂
- Calculate theoretical voltage and energy

**Corrosion:**
- Iron rusting: Fe → Fe²⁺ + 2e⁻
- Cathodic protection using sacrificial anodes

**Electrolysis:**
- **Water:** 2H₂O → 2H₂ + O₂ (E°cell = -1.23 V)
- **Molten NaCl:** 2NaCl → 2Na + Cl₂
- Calculate minimum voltage required

**Problem-Solving Strategy:**

**1. Identify half-reactions**
- Determine what's being oxidized and reduced
- Balance electrons in each half-reaction

**2. Look up standard potentials**
- Use reduction potential table
- Remember: higher E° means stronger oxidizing agent

**3. Calculate cell potential**
- E°cell = E°cathode - E°anode
- Check if reaction is spontaneous (E°cell > 0)

**4. Apply Nernst equation if needed**
- For non-standard concentrations
- Consider temperature effects

**5. Connect to thermodynamics**
- Calculate ΔG° and K if required
- Relate to spontaneity and equilibrium

**Example AP Problem:**
Design a galvanic cell using Ag⁺/Ag (E° = 0.80 V) and Ni²⁺/Ni (E° = -0.25 V).
a) Write cell notation
b) Calculate E°cell
c) Determine if spontaneous
d) Calculate K at 25°C

**Solution:**
a) Ni(s) | Ni²⁺(1M) || Ag⁺(1M) | Ag(s)
b) E°cell = 0.80 - (-0.25) = 1.05 V
c) E°cell > 0, so spontaneous
d) ln K = nFE°/(RT) = (2)(1.05)/0.0257 = 81.7, so K = 1.3 × 10³⁵

This systematic approach will help you master electrochemistry for the AP exam!"""
        }
    ]

def create_ap_computer_science_algorithms_data() -> List[Dict]:
    """AP Computer Science algorithms and data structures"""
    return [
        {
            "instruction": "Explain searching and sorting algorithms for AP Computer Science A.",
            "input": "",
            "output": """Searching and sorting algorithms are fundamental to AP Computer Science A. Understanding their implementation, efficiency, and appropriate use cases is crucial for the exam.

**Searching Algorithms:**

**1. Linear Search:**
Examines each element sequentially until target is found or end is reached.

```java
public static int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;  // Return index if found
        }
    }
    return -1;  // Return -1 if not found
}
```

**Characteristics:**
- **Time Complexity:** O(n) - worst case checks every element
- **Space Complexity:** O(1) - uses constant extra space
- **Works on:** Sorted or unsorted arrays
- **Best case:** O(1) if target is first element
- **Average case:** O(n/2)

**2. Binary Search:**
Repeatedly divides sorted array in half, comparing target with middle element.

```java
public static int binarySearch(int[] arr, int target) {
    int left = 0;
    int right = arr.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;  // Avoid overflow
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;  // Search right half
        } else {
            right = mid - 1;  // Search left half
        }
    }
    return -1;  // Not found
}
```

**Characteristics:**
- **Time Complexity:** O(log n) - much faster for large arrays
- **Space Complexity:** O(1) for iterative version
- **Prerequisite:** Array must be sorted
- **Key insight:** Eliminates half the possibilities each iteration

**Sorting Algorithms:**

**1. Selection Sort:**
Finds minimum element and swaps it with first position, then repeats for remaining elements.

```java
public static void selectionSort(int[] arr) {
    for (int i = 0; i < arr.length - 1; i++) {
        int minIndex = i;
        
        // Find minimum element in remaining array
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        
        // Swap minimum with current position
        int temp = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = temp;
    }
}
```

**Characteristics:**
- **Time Complexity:** O(n²) - always, regardless of input
- **Space Complexity:** O(1) - sorts in place
- **Swaps:** Exactly n-1 swaps (minimum possible)
- **Stability:** Not stable (doesn't preserve relative order of equal elements)

**2. Insertion Sort:**
Builds sorted array one element at a time by inserting each element in correct position.

```java
public static void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        
        // Move elements greater than key one position ahead
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        
        arr[j + 1] = key;  // Insert key in correct position
    }
}
```

**Characteristics:**
- **Time Complexity:** 
  - Best case: O(n) - already sorted
  - Average/Worst case: O(n²)
- **Space Complexity:** O(1)
- **Stability:** Stable
- **Adaptive:** Performs well on nearly sorted data

**3. Merge Sort:**
Divide-and-conquer algorithm that recursively divides array and merges sorted halves.

```java
public static void mergeSort(int[] arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        // Recursively sort both halves
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        
        // Merge the sorted halves
        merge(arr, left, mid, right);
    }
}

private static void merge(int[] arr, int left, int mid, int right) {
    // Create temporary arrays for left and right subarrays
    int[] leftArr = new int[mid - left + 1];
    int[] rightArr = new int[right - mid];
    
    // Copy data to temporary arrays
    for (int i = 0; i < leftArr.length; i++) {
        leftArr[i] = arr[left + i];
    }
    for (int j = 0; j < rightArr.length; j++) {
        rightArr[j] = arr[mid + 1 + j];
    }
    
    // Merge the temporary arrays back into arr[left..right]
    int i = 0, j = 0, k = left;
    
    while (i < leftArr.length && j < rightArr.length) {
        if (leftArr[i] <= rightArr[j]) {
            arr[k] = leftArr[i];
            i++;
        } else {
            arr[k] = rightArr[j];
            j++;
        }
        k++;
    }
    
    // Copy remaining elements
    while (i < leftArr.length) {
        arr[k] = leftArr[i];
        i++;
        k++;
    }
    while (j < rightArr.length) {
        arr[k] = rightArr[j];
        j++;
        k++;
    }
}
```

**Characteristics:**
- **Time Complexity:** O(n log n) - always, best guaranteed performance
- **Space Complexity:** O(n) - requires additional memory
- **Stability:** Stable
- **Divide and Conquer:** Classic example of this paradigm

**Algorithm Comparison:**

| Algorithm | Best Case | Average Case | Worst Case | Space | Stable |
|-----------|-----------|--------------|------------|-------|--------|
| Linear Search | O(1) | O(n) | O(n) | O(1) | N/A |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) | N/A |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

**AP Exam Tips:**

**1. Know when to use each algorithm:**
- **Small arrays:** Insertion sort often fastest in practice
- **Large arrays:** Merge sort for guaranteed performance
- **Memory constrained:** Selection sort uses least swaps
- **Nearly sorted data:** Insertion sort is adaptive

**2. Understand trade-offs:**
- Time vs. space complexity
- Stability requirements
- Best/average/worst case scenarios

**3. Be able to trace through algorithms:**
- Show step-by-step execution
- Count comparisons and swaps
- Identify when algorithm terminates

**4. Recursive thinking:**
- Understand how merge sort divides problem
- Base cases and recursive cases
- Stack space considerations

**Practice Problems:**
1. Modify binary search to find insertion point for new element
2. Implement binary search recursively
3. Count number of comparisons in each sorting algorithm
4. Determine which sorting algorithm was used based on trace

Mastering these algorithms provides the foundation for more advanced data structures and algorithmic thinking in computer science!"""
        }
    ]

def main():
    """Generate AP-focused tutoring dataset"""
    
    # Collect all AP data
    all_data = []
    
    # AP Physics
    all_data.extend(create_ap_physics_mechanics_data())
    all_data.extend(create_ap_physics_electricity_data())
    
    # AP Chemistry
    all_data.extend(create_ap_chemistry_data())
    all_data.extend(create_ap_chemistry_advanced_data())
    
    # AP Computer Science
    all_data.extend(create_ap_computer_science_data())
    all_data.extend(create_ap_computer_science_algorithms_data())
    
    # Add metadata
    for i, item in enumerate(all_data):
        item['id'] = f"ap_tutor_{i+1:03d}"
        item['source'] = "ap_curriculum_data"
        item['quality'] = "high"
        item['level'] = "AP"
        item['type'] = "tutoring"
    
    # Shuffle for better training
    random.seed(42)
    random.shuffle(all_data)
    
    # Split into train/eval (90/10)
    split_idx = int(len(all_data) * 0.9)
    train_data = all_data[:split_idx]
    eval_data = all_data[split_idx:]
    
    # Create output directory
    os.makedirs("data_ap", exist_ok=True)
    
    # Save training data
    with open("data_ap/train.jsonl", "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    # Save evaluation data
    with open("data_ap/eval.jsonl", "w", encoding="utf-8") as f:
        for item in eval_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Created AP-focused tutoring dataset:")
    print(f"   Training samples: {len(train_data)}")
    print(f"   Evaluation samples: {len(eval_data)}")
    print(f"   Total samples: {len(all_data)}")
    print(f"   Subjects: AP Physics C, AP Chemistry, AP Computer Science A")
    print(f"   Saved to: data_ap/")
    
    # Show sample
    print(f"\n📝 Sample AP training example:")
    sample = train_data[0]
    print(f"Subject: {sample['instruction'][:50]}...")
    print(f"Content preview: {sample['output'][:200]}...")
    
    # Subject breakdown
    subjects = {'Physics': 0, 'Chemistry': 0, 'Computer Science': 0}
    for item in all_data:
        instruction = item['instruction'].lower()
        if any(word in instruction for word in ['physics', 'force', 'motion', 'electric', 'gauss', 'circuit']):
            subjects['Physics'] += 1
        elif any(word in instruction for word in ['chemistry', 'equilibrium', 'electrochemistry', 'reaction']):
            subjects['Chemistry'] += 1
        elif any(word in instruction for word in ['computer', 'programming', 'algorithm', 'java', 'object']):
            subjects['Computer Science'] += 1
    
    print(f"\n📊 AP Subject distribution:")
    for subject, count in subjects.items():
        print(f"   AP {subject}: {count} examples")
    
    print(f"\n🎯 Next steps:")
    print(f"1. Run: python retrain_with_better_data.py")
    print(f"2. Update model path to use AP-trained model")
    print(f"3. Test with AP-level questions!")

if __name__ == "__main__":
    main()