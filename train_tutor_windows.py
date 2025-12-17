"""
train_tutor.py

End-to-end LoRA fine-tuning script for a School Tutor chatbot using:
- Unsloth (4-bit loading)
- TRL SFTTrainer
- JSONL dataset at: data/train.jsonl and data/eval.jsonl

Windows-compatible version with torch compile disabled.
"""

import os
import json
import torch

# CRITICAL: Disable torch compile on Windows before importing unsloth
os.environ["DISABLE_UNSLOTH_COMPILE"] = "1"
torch._dynamo.config.suppress_errors = True

from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel

# -----------------------------
# Config
# -----------------------------
MODEL_NAME = "unsloth/llama-3-8b-bnb-4bit"  # change if you want a different base
OUTPUT_DIR = "tutor_model_lora"
MAX_SEQ_LENGTH = 2048

TRAIN_PATH = "data/train.jsonl"
EVAL_PATH = "data/eval.jsonl"


# -----------------------------
# Dataset helpers
# -----------------------------
def load_jsonl_dataset(train_path=TRAIN_PATH, eval_path=EVAL_PATH):
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Missing train file: {train_path}")
    if not os.path.exists(eval_path):
        raise FileNotFoundError(f"Missing eval file: {eval_path}")

    ds = load_dataset("json", data_files={"train": train_path, "eval": eval_path})
    print(f"✅ Loaded train: {len(ds['train'])} | eval: {len(ds['eval'])}")
    return ds["train"], ds["eval"]


def formatting_prompts_func(examples):
    """
    Builds the exact training text the model learns.
    """
    instructions = examples["instruction"]
    inputs = examples.get("input", [""] * len(instructions))
    outputs = examples["output"]

    texts = []
    for inst, inp, out in zip(instructions, inputs, outputs):
        inst = (inst or "").strip()
        inp = (inp or "").strip()
        out = (out or "").strip()

        if inp:
            text = (
                "### Instruction:\n"
                f"{inst}\n\n"
                "### Input:\n"
                f"{inp}\n\n"
                "### Response:\n"
                f"{out}"
            )
        else:
            text = (
                "### Instruction:\n"
                f"{inst}\n\n"
                "### Response:\n"
                f"{out}"
            )
        texts.append(text)

    return {"text": texts}


# -----------------------------
# Training
# -----------------------------
def train_tutor_model():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load base model + tokenizer (4-bit)
    print("🚀 Loading model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )

    # Apply LoRA
    print("🔧 Applying LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    # Load dataset
    print("📚 Loading datasets...")
    train_dataset, eval_dataset = load_jsonl_dataset()

    # Basic schema validation (fail fast)
    required_cols = {"instruction", "output"}
    missing_train = required_cols - set(train_dataset.column_names)
    missing_eval = required_cols - set(eval_dataset.column_names)
    if missing_train:
        raise ValueError(f"Train dataset missing columns: {missing_train}")
    if missing_eval:
        raise ValueError(f"Eval dataset missing columns: {missing_eval}")

    # Create formatted "text" field
    print("🔄 Formatting prompts...")
    train_dataset = train_dataset.map(formatting_prompts_func, batched=True)
    eval_dataset = eval_dataset.map(formatting_prompts_func, batched=True)

    # Sanity print (prevents 90% of wasted runs)
    print("\n--- Sample formatted training text (first 500 chars) ---")
    print(train_dataset[0]["text"][:500])
    print("------------------------------------------------------\n")

    # Training arguments (EVAL SETTINGS MUST BE INSIDE THIS BLOCK)
    print("⚙️ Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=1000,  # adjust as needed
        learning_rate=2e-4,  # if outputs look unstable, try 1e-4
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=25,

        # Checkpointing
        save_steps=100,
        save_total_limit=2,

        # Evaluation
        eval_strategy="steps",
        eval_steps=100,

        # Misc
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        report_to="none",
    )

    print("🎯 Creating trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        args=training_args,
        max_seq_length=MAX_SEQ_LENGTH,
        dataset_text_field="text",
        packing=False,
    )

    print("🚂 Starting training...")
    trainer.train()

    # Save LoRA adapter + tokenizer
    print("💾 Saving model...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"✅ Saved model + tokenizer to: {OUTPUT_DIR}")

    return OUTPUT_DIR


# -----------------------------
# Inference / test
# -----------------------------
def build_prompt(user_instruction: str, user_input: str = "") -> str:
    user_instruction = (user_instruction or "").strip()
    user_input = (user_input or "").strip()

    if user_input:
        return (
            "### Instruction:\n"
            f"{user_instruction}\n\n"
            "### Input:\n"
            f"{user_input}\n\n"
            "### Response:\n"
        )
    return (
        "### Instruction:\n"
        f"{user_instruction}\n\n"
        "### Response:\n"
    )


@torch.no_grad()
def test_tutor_model(model_dir=OUTPUT_DIR, deterministic=True):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"\n🧪 Loading model for testing from {model_dir}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_dir,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)

    # Keep model on GPU if available; otherwise CPU
    if device == "cpu":
        # Note: 4-bit CPU inference may be slow or unsupported depending on setup.
        # If you hit issues, run inference on a CUDA machine.
        pass

    prompts = [
        "Explain Newton's 2nd law with a simple example.",
        "A car starts from rest and accelerates at 2 m/s^2 for 5 s. What is its final velocity?",
        "How do you choose kinematics equations in AP Physics 1 problems?",
    ]

    for p in prompts:
        prompt = build_prompt(p)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

        gen_kwargs = dict(
            max_new_tokens=250,
        )

        if deterministic:
            gen_kwargs.update(dict(do_sample=False))
        else:
            gen_kwargs.update(dict(do_sample=True, temperature=0.7))

        outputs = model.generate(**inputs, **gen_kwargs)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\n" + "=" * 80)
        print("PROMPT:\n", p)
        print("\nMODEL OUTPUT:\n", text)
        print("=" * 80 + "\n")


def main():
    print("=" * 80)
    print("🎓 HIGH SCHOOL TUTOR FINE-TUNING (Windows Compatible)")
    print("=" * 80)

    # Check GPU
    if torch.cuda.is_available():
        print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️ No GPU detected! Training will be very slow.")

    print()

    out_dir = train_tutor_model()
    # Deterministic test by default
    test_tutor_model(out_dir, deterministic=True)


if __name__ == "__main__":
    main()