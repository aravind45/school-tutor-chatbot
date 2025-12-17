# """
# Fine-tune Llama as a High School Tutor using Unsloth
# Make sure to install: pip install unsloth[conda] torch datasets trl accelerate
# """
#

"""
train_tutor.py

End-to-end LoRA fine-tuning script for a School Tutor chatbot using:
- Unsloth (4-bit loading)
- TRL SFTTrainer
- JSONL dataset at: data/train.jsonl and data/eval.jsonl

Expected JSONL fields per line:
{"instruction": "...", "input": "", "output": "..."}

Optional extra fields are OK (e.g., source/topic/difficulty).
"""

import os
import json
import torch


import torch
from unsloth import FastLanguageModel
from datasets import Dataset
import pandas as pd
from transformers import TrainingArguments
from trl import SFTTrainer
import json
from datasets import load_dataset

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
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )

    # Apply LoRA
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
    train_dataset = train_dataset.map(formatting_prompts_func, batched=True)
    eval_dataset = eval_dataset.map(formatting_prompts_func, batched=True)

    # Sanity print (prevents 90% of wasted runs)
    print("\n--- Sample formatted training text (first 500 chars) ---")
    print(train_dataset[0]["text"][:500])
    print("------------------------------------------------------\n")

    # Training arguments (EVAL SETTINGS MUST BE INSIDE THIS BLOCK)
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=1000,                 # adjust as needed
        learning_rate=2e-4,             # if outputs look unstable, try 1e-4
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

    trainer.train()

    # Save LoRA adapter + tokenizer
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
    out_dir = train_tutor_model()
    # Deterministic test by default
    test_tutor_model(out_dir, deterministic=True)


if __name__ == "__main__":
    main()



# import torch
# from unsloth import FastLanguageModel
# from datasets import Dataset
# import pandas as pd
# from transformers import TrainingArguments
# from trl import SFTTrainer
# import json
# from datasets import load_dataset
#
# # ============================================================================
# # CONFIGURATION
# # ============================================================================
#
# MODEL_NAME = "unsloth/llama3.3:latest"  # or your local path: "/path/to/your/llama"
# OUTPUT_DIR = "./llama-highschool-tutor"
# MAX_SEQ_LENGTH = 2048  # Adjust based on your GPU memory
#
#
# # ============================================================================
# # 1. LOAD MODEL WITH UNSLOTH OPTIMIZATIONS
# # ============================================================================
# def load_jsonl_dataset(train_path="data/train.jsonl", eval_path="data/eval.jsonl"):
#     ds = load_dataset("json", data_files={"train": train_path, "eval": eval_path})
#     print(f"✅ Loaded train: {len(ds['train'])} | eval: {len(ds['eval'])}")
#     return ds["train"], ds["eval"]
#
# def load_model():
#     """Load the model with Unsloth optimizations"""
#     print("🚀 Loading model with Unsloth optimizations...")
#
#     model, tokenizer = FastLanguageModel.from_pretrained(
#         model_name=MODEL_NAME,
#         max_seq_length=MAX_SEQ_LENGTH,
#         dtype=torch.float16,
#         load_in_4bit=True,  # 4-bit quantization for memory efficiency
#         token=None,  # Add your HF token if using gated models
#     )
#
#     print(f"✅ Model loaded. Memory efficient: {model.model.__class__.__name__}")
#     return model, tokenizer
#
#
# # ============================================================================
# # 2. CREATE TUTOR TRAINING DATASET
# # ============================================================================
#
# def create_tutor_dataset():
#     """Create a dataset of tutor-student dialogues"""
#
#     # Example training data - REPLACE WITH YOUR OWN DATA
#     tutor_data = [
#         {
#             "instruction": "Explain the Pythagorean theorem to a 10th grader",
#             "input": "",
#             "output": "The Pythagorean theorem helps us find missing sides in right triangles. It says: a² + b² = c², where c is the hypotenuse (the longest side). Think of it like this: If you build squares on each side of a right triangle, the area of the squares on the two shorter sides adds up to the area of the square on the longest side. Let me show you an example..."
#         },
#         {
#             "instruction": "How do I solve 2x + 5 = 13?",
#             "input": "",
#             "output": "Great question! Let's solve this step-by-step:\n1. Our goal is to get x by itself\n2. First, subtract 5 from both sides: 2x + 5 - 5 = 13 - 5\n3. That gives us: 2x = 8\n4. Now divide both sides by 2: 2x/2 = 8/2\n5. So x = 4\nAlways check your work: 2(4) + 5 = 8 + 5 = 13 ✓"
#         },
#         {
#             "instruction": "What causes seasons on Earth?",
#             "input": "",
#             "output": "That's a common question! Seasons happen because:\n1. Earth's axis is tilted 23.5 degrees\n2. As Earth orbits the Sun, different parts get more direct sunlight\n3. NOT because Earth is closer/farther from the Sun (that's a common misconception)\n\nIn summer: Your hemisphere is tilted toward the Sun → more direct sunlight → warmer\nIn winter: Tilted away → sunlight spreads out → cooler"
#         },
#         {
#             "instruction": "Help me analyze the theme of 'To Kill a Mockingbird'",
#             "input": "",
#             "output": "Excellent choice! Let's explore the themes together:\n\nMain themes:\n1. **Racial injustice** - The Tom Robinson trial shows prejudice in the justice system\n2. **Morality and ethics** - Atticus teaches Scout about doing what's right\n3. **Loss of innocence** - Scout and Jem learn about the world's complexities\n4. **Empathy** - 'You never really understand a person until you... climb into his skin'\n\nWhat specific aspect would you like to explore further?"
#         },
#         {
#             "instruction": "Why is water polar?",
#             "input": "",
#             "output": "Great chemistry question! Water is polar because:\n1. Oxygen is more electronegative than hydrogen\n2. Oxygen pulls electrons closer → partial negative charge (δ-)\n3. Hydrogen has partial positive charge (δ+)\n4. This creates a bent molecular shape (104.5° angle)\n5. Result: One end is slightly positive, other end slightly negative\n\nThis polarity allows water to dissolve many substances and form hydrogen bonds!"
#         }
#     ]
#
#     # Add more examples for different subjects
#     math_examples = [
#         {
#             "instruction": "Factor x² - 5x + 6",
#             "input": "",
#             "output": "Let's factor this quadratic step-by-step:\n1. We need two numbers that multiply to 6 and add to -5\n2. Factors of 6: (1,6), (2,3), (-1,-6), (-2,-3)\n3. -2 and -3 multiply to 6 and add to -5\n4. So: x² - 5x + 6 = (x - 2)(x - 3)\n\nCheck: (x-2)(x-3) = x² - 3x - 2x + 6 = x² - 5x + 6 ✓"
#         }
#     ]
#
#     science_examples = [
#         {
#             "instruction": "Explain cellular respiration",
#             "input": "",
#             "output": "Cellular respiration is how cells make energy (ATP). Think of it as the opposite of photosynthesis:\n\nThree main stages:\n1. **Glycolysis** - Glucose breaks down in cytoplasm, makes 2 ATP\n2. **Krebs Cycle** - In mitochondria, produces electron carriers\n3. **Electron Transport Chain** - Makes most ATP (32-34 ATP)\n\nOverall: C6H12O6 + 6O2 → 6CO2 + 6H2O + ATP"
#         }
#     ]
#
#     # Combine all examples
#     all_data = tutor_data + math_examples + science_examples
#
#     # Convert to Hugging Face dataset
#     df = pd.DataFrame(all_data)
#     dataset = Dataset.from_pandas(df)
#
#     print(f"✅ Created dataset with {len(dataset)} examples")
#     return dataset
#
#
# # ============================================================================
# # 3. FORMATTING FUNCTION FOR TRAINING
# # ============================================================================
#
# def formatting_prompts_func(examples):
#     """Format the examples for training"""
#     instructions = examples["instruction"]
#     inputs = examples["input"]
#     outputs = examples["output"]
#
#     texts = []
#     for instruction, input_text, output in zip(instructions, inputs, outputs):
#         # Format for instruction following
#         if input_text:
#             text = f"""### Instruction:
# {instruction}
#
# ### Input:
# {input_text}
#
# ### Response:
# {output}"""
#         else:
#             text = f"""### Instruction:
# {instruction}
#
# ### Response:
# {output}"""
#         texts.append(text)
#
#     return {"text": texts}
#
#
# # ============================================================================
# # 4. TRAINING FUNCTION
# # ============================================================================
#
# def train_tutor_model():
#     """Main training function"""
#
#     # Load model and tokenizer
#     model, tokenizer = load_model()
#
#     # Apply LoRA adapters (makes training efficient)
#     model = FastLanguageModel.get_peft_model(
#         model,
#         r=16,  # LoRA rank
#         target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
#         lora_alpha=16,
#         lora_dropout=0,
#         bias="none",
#         use_gradient_checkpointing="unsloth",
#         random_state=42,
#         use_rslora=False,
#         loftq_config=None,
#     )
#
#     # Create dataset
#     #dataset = create_tutor_dataset()
#     train_dataset, eval_dataset = load_jsonl_dataset()
#
#     # Format dataset
#     #dataset = dataset.map(formatting_prompts_func, batched=True)
#     train_dataset = train_dataset.map(formatting_prompts_func, batched=True)
#     eval_dataset = eval_dataset.map(formatting_prompts_func, batched=True)
#
#     # Training arguments
#     training_args = TrainingArguments(
#         output_dir=OUTPUT_DIR,
#         num_train_epochs=3,  # Adjust based on your dataset size
#         per_device_train_batch_size=2,  # Reduce if out of memory
#         gradient_accumulation_steps=4,
#         warmup_steps=10,
#         logging_steps=10,
#         save_steps=100,
#         learning_rate=2e-4,
#         fp16=not torch.cuda.is_bf16_supported(),
#         bf16=torch.cuda.is_bf16_supported(),
#         optim="adamw_8bit",
#         weight_decay=0.01,
#         lr_scheduler_type="linear",
#         seed=42,
#         report_to="none",  # Change to "wandb" if using wandb
#         ddp_find_unused_parameters=False,
#     )
#
#     # Create trainer
#     # trainer = SFTTrainer(
#     #     model=model,
#     #     tokenizer=tokenizer,
#     #     train_dataset=dataset,
#     #     args=training_args,
#     #     max_seq_length=MAX_SEQ_LENGTH,
#     #     dataset_text_field="text",
#     #     packing=False,  # Set to True for more efficient training if sequences are short
#     # )
#     trainer = SFTTrainer(
#         model=model,
#         tokenizer=tokenizer,
#         train_dataset=train_dataset,
#         eval_dataset=eval_dataset,
#         args=training_args,
#         max_seq_length=MAX_SEQ_LENGTH,
#         dataset_text_field="text",
#         packing=False,
#     )
#
#     # Start training
#     print("🎯 Starting training...")
#     trainer.train()
#
#     # Save the model
#     print("💾 Saving model...")
#     model.save_pretrained(OUTPUT_DIR)
#     tokenizer.save_pretrained(OUTPUT_DIR)
#     evaluation_strategy = "steps",
#     eval_steps = 100,
#     save_total_limit = 2,
#     load_best_model_at_end = False,  # can set True later if you add metric selection
#
#     # Also save in GGUF format for easier inference
#     try:
#         model.save_pretrained_gguf(OUTPUT_DIR, tokenizer, quantization_method="q4_k_m")
#         print("✅ Saved GGUF version for llama.cpp")
#     except:
#         print("⚠️ Could not save GGUF format, but model is saved in standard format")
#
#     return model, tokenizer
#
#
# # ============================================================================
# # 5. TEST THE FINE-TUNED MODEL
# # ============================================================================
#
# def test_tutor_model(model, tokenizer):
#     """Test the fine-tuned model"""
#
#     FastLanguageModel.for_inference(model)  # Enable inference mode
#
#     test_questions = [
#         "Explain photosynthesis to a 9th grader",
#         "How do I solve 3x - 7 = 14?",
#         "What's the difference between mitosis and meiosis?",
#         "Help me understand Shakespeare's sonnets",
#         "Why did World War I start?"
#     ]
#
#     print("\n" + "=" * 50)
#     print("🧪 TESTING TUTOR MODEL")
#     print("=" * 50)
#
#     for question in test_questions:
#         print(f"\n📚 Student: {question}")
#         print("-" * 40)
#
#         # Format the prompt
#         prompt = f"""### Instruction:
# {question}
#
# ### Response:
# """
#
#         inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to("cuda")
#
#         # Generate response
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=256,
#             temperature=0.7,
#             do_sample=True,
#             pad_token_id=tokenizer.pad_token_id,
#         )
#
#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#
#         # Extract just the response part
#         if "### Response:" in response:
#             response = response.split("### Response:")[1].strip()
#
#         print(f"🤖 Tutor: {response}")
#         print("-" * 40)
#
#
# # ============================================================================
# # 6. MAIN EXECUTION
# # ============================================================================
#
# if __name__ == "__main__":
#
#     print("=" * 60)
#     print("🏫 HIGH SCHOOL TUTOR FINE-TUNING WITH UNSLOTH")
#     print("=" * 60)
#
#     # Step 1: Check GPU availability
#     if torch.cuda.is_available():
#         print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
#         print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
#     else:
#         print("⚠️ No GPU detected! Training will be very slow.")
#         print("   Consider using Google Colab with T4 GPU.")
#
#     # Step 2: Train the model
#     trained_model, trained_tokenizer = train_tutor_model()
#
#     # Step 3: Test the model
#     test_tutor_model(trained_model, trained_tokenizer)
#
#     print("\n" + "=" * 60)
#     print("🎓 TRAINING COMPLETE!")
#     print(f"📁 Model saved to: {OUTPUT_DIR}")
#     print("\nTo use your tutor:")
#     print(f"1. Load with: model, tokenizer = FastLanguageModel.from_pretrained('{OUTPUT_DIR}')")
#     print("2. Use the test_tutor_model function for inference")
#     print("=" * 60)