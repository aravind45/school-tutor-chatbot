"""
train_tutor_windows.py

LoRA fine-tuning for a School Tutor chatbot using:
- Unsloth (4-bit loading)
- TRL SFTTrainer (v0.26.1 compatible)
- JSONL dataset:
    data/train.jsonl
    data/eval.jsonl

Expected JSONL keys per line:
{"instruction": "...", "input": "", "output": "..."}

Notes:
- TRL 0.26.1 SFTTrainer does NOT accept `max_seq_length` as a constructor arg.
  We set tokenizer.model_max_length instead and rely on truncation.
"""
import os

# Disable TorchDynamo / Inductor (Windows fix)
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["TORCH_COMPILE"] = "0"

import inspect
import torch
torch._dynamo.config.suppress_errors = True


# Import unsloth BEFORE trl/transformers/peft for best patching
import unsloth
from unsloth import FastLanguageModel

from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer



# -----------------------------
# Config
# -----------------------------
MODEL_NAME = "unsloth/llama-3-8b-bnb-4bit"  # change as needed
OUTPUT_DIR = "tutor_model_ap_windows"
MAX_SEQ_LENGTH = 2048

TRAIN_PATH = "data_ap_combined/train.jsonl"
EVAL_PATH  = "data_ap_combined/eval.jsonl"


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
    Builds the training text field ("text") that SFTTrainer consumes.
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

    print("🚀 Loading base model with Unsloth (4-bit)...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )

    # Important for TRL: enforce a max length via tokenizer
    tokenizer.model_max_length = MAX_SEQ_LENGTH

    print("🧩 Applying LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_alpha=16,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    print("📦 Loading JSONL datasets...")
    train_dataset, eval_dataset = load_jsonl_dataset()

    # Fail-fast schema checks
    required = {"instruction", "output"}
    missing_train = required - set(train_dataset.column_names)
    missing_eval  = required - set(eval_dataset.column_names)
    if missing_train:
        raise ValueError(f"Train dataset missing columns: {missing_train}")
    if missing_eval:
        raise ValueError(f"Eval dataset missing columns: {missing_eval}")

    print("🧾 Formatting prompts into `text` field...")
    train_dataset = train_dataset.map(formatting_prompts_func, batched=True, num_proc=1)
    eval_dataset  = eval_dataset.map(formatting_prompts_func, batched=True, num_proc=1)

    # Sanity print
    print("\n--- Sample formatted training text (first 400 chars) ---")
    print(train_dataset[0]["text"][:400])
    print("------------------------------------------------------\n")

    print("⚙️ Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=200,               # Reduced for AP dataset size
        learning_rate=2e-4,          # if unstable, try 1e-4
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=25,

        save_steps=100,
        save_total_limit=2,

        # Transformers 4.57+: uses eval_strategy (not evaluation_strategy)
        eval_strategy="steps",
        eval_steps=100,

        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        report_to="none",
    )

    print("🎯 Creating trainer...")

    print("🎯 Creating trainer.")

    import inspect
    sig = inspect.signature(SFTTrainer.__init__)

    trainer_kwargs = {
        "model": model,
        "train_dataset": train_dataset,
        "eval_dataset": eval_dataset,
        "args": training_args,
    }

    # Tokenizer arg name changed across TRL versions
    if "tokenizer" in sig.parameters:
        trainer_kwargs["tokenizer"] = tokenizer
    elif "processing_class" in sig.parameters:
        trainer_kwargs["processing_class"] = tokenizer

    # TRL 0.26.x: dataset_text_field is often removed; use formatting_func instead.
    # Since you already created a "text" column, we can return it directly.
    if "dataset_text_field" in sig.parameters:
        trainer_kwargs["dataset_text_field"] = "text"
    elif "formatting_func" in sig.parameters:
        trainer_kwargs["formatting_func"] = lambda ex: ex["text"]
    else:
        # last resort: keep train_dataset already mapped to "text" and hope defaults exist
        pass

    # Only pass packing if supported
    if "packing" in sig.parameters:
        trainer_kwargs["packing"] = False

    trainer = SFTTrainer(**trainer_kwargs)

    if "tokenizer" in sig.parameters:
        trainer_kwargs["tokenizer"] = tokenizer
    elif "processing_class" in sig.parameters:
        # In some TRL builds, `processing_class` replaces tokenizer
        trainer_kwargs["processing_class"] = tokenizer
    else:
        # last-resort fallback
        trainer_kwargs["tokenizer"] = tokenizer

    # IMPORTANT: Do NOT pass max_seq_length to SFTTrainer in TRL 0.26.1
    # trainer_kwargs["max_seq_length"] = MAX_SEQ_LENGTH  # <-- intentionally omitted

    trainer = SFTTrainer(**trainer_kwargs)

    print("🏁 Starting training...")
    trainer.train()

    print("💾 Saving model + tokenizer...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"✅ Saved to: {OUTPUT_DIR}")

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

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_dir,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )
    tokenizer.model_max_length = MAX_SEQ_LENGTH
    FastLanguageModel.for_inference(model)

    prompts = [
        "Explain Newton's 2nd law with a simple example.",
        "A car starts from rest and accelerates at 2 m/s^2 for 5 s. What is its final velocity?",
        "How do you choose kinematics equations in AP Physics 1 problems?",
    ]

    for p in prompts:
        prompt = build_prompt(p)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

        gen_kwargs = {"max_new_tokens": 250}
        if deterministic:
            gen_kwargs.update({"do_sample": False})
        else:
            gen_kwargs.update({"do_sample": True, "temperature": 0.7})

        outputs = model.generate(**inputs, **gen_kwargs)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\n" + "=" * 80)
        print("PROMPT:\n", p)
        print("\nMODEL OUTPUT:\n", text)
        print("=" * 80 + "\n")


def main():
    out_dir = train_tutor_model()
    test_tutor_model(out_dir, deterministic=True)


if __name__ == "__main__":
    main()
