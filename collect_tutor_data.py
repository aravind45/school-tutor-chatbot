import json


def collect_real_tutor_data():
    """Template for collecting real tutor data"""

    data_samples = []

    # Example structure for your real data
    sample = {
        "instruction": "How do I solve quadratic equations?",
        "input": "",  # Can be empty or contain specific problem
        "output": """Let's learn quadratic equations step by step...

1. Standard form: ax² + bx + c = 0
2. Three main methods:
   - Factoring (if it factors nicely)
   - Quadratic formula: x = [-b ± √(b² - 4ac)] / 2a
   - Completing the square

Let's practice with x² - 5x + 6 = 0..."""
    }

    # Save data
    with open("tutor_data.jsonl", "w") as f:
        for item in data_samples:
            f.write(json.dumps(item) + "\n")

    print("Data saved to tutor_data.jsonl")