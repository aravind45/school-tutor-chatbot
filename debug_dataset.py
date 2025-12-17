"""
Debug script to inspect the MMLU dataset structure
"""
from datasets import load_dataset

DATASET_NAME = "brucewlee1/mmlu-high-school-physics"


def main():
    print(f"Loading dataset: {DATASET_NAME}")
    ds = load_dataset(DATASET_NAME)

    print(f"\n📊 Available splits: {list(ds.keys())}")

    for split in ds.keys():
        print(f"\n{'=' * 60}")
        print(f"Split: {split}")
        print(f"Number of examples: {len(ds[split])}")

        if len(ds[split]) > 0:
            first_example = ds[split][0]
            print(f"\n🔍 First example keys: {list(first_example.keys())}")
            print(f"\n📝 First example content:")
            for key, value in first_example.items():
                print(f"  {key}: {value}")
                print(f"    Type: {type(value)}")

            # Show a few more examples to see patterns
            print(f"\n📋 First 3 examples (abbreviated):")
            for i in range(min(3, len(ds[split]))):
                ex = ds[split][i]
                print(f"\n  Example {i}:")
                # Handle both dict and direct access
                if hasattr(ex, 'get'):
                    print(f"    question: {ex.get('question', ex.get('centerpiece', 'N/A'))}")
                    print(f"    answer: {ex.get('answer', ex.get('correct_options', 'N/A'))}")
                else:
                    print(f"    centerpiece: {ex['centerpiece'] if 'centerpiece' in first_example else 'N/A'}")
                    print(f"    options: {ex['options'] if 'options' in first_example else 'N/A'}")
                    print(
                        f"    correct_options: {ex['correct_options'] if 'correct_options' in first_example else 'N/A'}")


if __name__ == "__main__":
    main()