import os
import json
import random
from datasets import load_dataset

DATASET_NAME = "brucewlee1/mmlu-high-school-physics"
OUT_TRAIN = "data/train.jsonl"
OUT_EVAL = "data/eval.jsonl"
EVAL_RATIO = 0.10
SEED = 42


def _clean(x) -> str:
    return ("" if x is None else str(x)).strip()


def _get_choices(example: dict):
    """
    Extract choices from the dataset.
    This dataset uses 'options' field.
    """
    # First try 'options' which this dataset uses
    if 'options' in example:
        v = example['options']
        if isinstance(v, (list, tuple)) and len(v) > 0:
            return list(v)

    # Fallback to other common variants
    for k in ["choices", "answer_choices", "endings"]:
        v = example.get(k)
        if isinstance(v, (list, tuple)) and len(v) > 0:
            return list(v)
    return []


def _parse_answer(answer, choices):
    """
    Returns (correct_letter, correct_text) or (None, None) if can't parse.

    This dataset's 'correct_options' field contains a list like ['B']
    Also handles:
      - int index: 0..N-1
      - str letter: "A"/"B"/...
      - str digit index: "0"/"1"/...
    """
    if answer is None:
        return None, None

    # Handle list format (like ['B'])
    if isinstance(answer, list):
        if len(answer) == 0:
            return None, None
        answer = answer[0]  # Take first element

    # Empty string -> invalid
    if isinstance(answer, str) and answer.strip() == "":
        return None, None

    # Index form
    if isinstance(answer, int):
        if 0 <= answer < len(choices):
            letter = chr(65 + answer)
            text = _clean(choices[answer])
            return letter, text
        return None, None

    # String form
    if isinstance(answer, str):
        a = answer.strip()

        # "A"/"B"/"C"/"D"/"E"
        if len(a) == 1 and a.upper() in ["A", "B", "C", "D", "E"]:
            letter = a.upper()
            idx = ord(letter) - 65
            if 0 <= idx < len(choices):
                return letter, _clean(choices[idx])
            return None, None

        # "0"/"1"/"2"/"3"
        if a.isdigit():
            idx = int(a)
            if 0 <= idx < len(choices):
                letter = chr(65 + idx)
                return letter, _clean(choices[idx])
            return None, None

    return None, None


def to_instruction(example: dict):
    """
    Convert a raw dataset example to our JSONL schema.
    Returns dict OR None (if example is unusable).

    This dataset uses:
    - 'centerpiece' for the question
    - 'options' for choices
    - 'correct_options' for the answer (as a list like ['B'])
    """
    # Get question from 'centerpiece' field
    q = _clean(example.get("centerpiece", example.get("question", "")))
    if not q:
        return None

    choices = _get_choices(example)
    if not choices:
        return None

    # Get answer from 'correct_options' field (fallback to 'answer')
    answer = example.get("correct_options", example.get("answer"))
    correct_letter, correct_text = _parse_answer(answer, choices)

    # If we cannot parse a valid answer, skip this row
    if not correct_letter:
        return None

    choice_lines = [f"{chr(65 + i)}. {_clean(c)}" for i, c in enumerate(choices)]

    instruction = (
            "Answer the following high school physics multiple-choice question. "
            "Return the correct letter and a brief explanation.\n\n"
            f"Question: {q}\n"
            "Choices:\n" + "\n".join(choice_lines)
    )

    output = (
        f"Correct answer: {correct_letter}.\n"
        f"Explanation: {correct_text}"
    )

    return {
        "instruction": instruction,
        "input": "",
        "output": output,
        "source": "mmlu_high_school_physics",
        "topic": "physics",
        "difficulty": "HS",
    }


def write_jsonl(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    random.seed(SEED)

    print(f"Loading dataset: {DATASET_NAME}")
    ds = load_dataset(DATASET_NAME)

    all_rows = []
    skipped = 0

    for split in ds.keys():
        print(f"Processing split: {split} ({len(ds[split])} examples)")
        for ex in ds[split]:
            row = to_instruction(ex)
            if row is None:
                skipped += 1
                continue
            all_rows.append(row)

    if not all_rows:
        raise RuntimeError("No usable rows were produced. Check dataset fields/keys.")

    random.shuffle(all_rows)
    n_eval = max(1, int(len(all_rows) * EVAL_RATIO))
    eval_rows = all_rows[:n_eval]
    train_rows = all_rows[n_eval:]

    write_jsonl(train_rows, OUT_TRAIN)
    write_jsonl(eval_rows, OUT_EVAL)

    print(f"\n✅ Total usable rows: {len(all_rows)} | skipped: {skipped}")
    print(f"✅ Train: {len(train_rows)} -> {OUT_TRAIN}")
    print(f"✅ Eval : {len(eval_rows)} -> {OUT_EVAL}")


if __name__ == "__main__":
    main()