#!/usr/bin/env python3
"""
Simple Retraining Script for AP Tutor Model

This script uses a simpler approach to avoid compilation issues
while still providing GPU-accelerated training.
"""

import os
import torch
from unsloth import FastLanguageModel
from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import json

# Configuration
MODEL_NAME = "unsloth/llama-3-8b-bnb-4bit"
OUTPUT_DIR = "tutor_model_ap_simple"
MAX_SEQ_LENGTH = 2048
TRAIN_PATH = "data_ap_combined/train.jsonl"
EVAL_PATH = "data_ap_combined/eval.jsonl"

def load_jsonl_dataset(train_path=TRAIN_PATH, eval_path=EVAL_PATH):
    """Load JSONL datasets"""
    
    def read_jsonl(path):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        return data
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training data not found: {train_path}")
    
    train_data = read_jsonl(train_path)
    eval_data = read_jsonl(eval_path) if os.path.exists(eval_path) else []
    
    print(f"✅ Loaded {len(train_data)} training examples")
    print(f"✅ Loaded {len(eval_data)} evaluation examples")
    
    return Dataset.from_list(train_data), Dataset.from_list(eval_data)

def format_prompt(example):
    """Format examples into instruction-response format"""
    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output_text = example.get("output", "")
    
    # Create the prompt in the same format used during training
    if input_text.strip():
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output_text}"
    else:
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output_text}"
    
    return {"text": prompt}

def main():
    print("="*60)
    print("🎓 Simple AP Tutor Model Retraining")
    print("="*60)
    
    # Check if data exists
    if not os.path.exists(TRAIN_PATH):
        print(f"❌ Training data not found: {TRAIN_PATH}")
        print("Please run: python build_ap_tutor_data.py")
        return
    
    # Load model with simpler settings
    print("\n1. Loading base model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )
    
    # Configure for training with simpler settings
    print("2. Configuring model for training...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )
    
    # Load datasets
    print("3. Loading training data...")
    train_dataset, eval_dataset = load_jsonl_dataset()
    
    # Format datasets
    print("4. Formatting datasets...")
    train_dataset = train_dataset.map(format_prompt, remove_columns=train_dataset.column_names)
    if len(eval_dataset) > 0:
        eval_dataset = eval_dataset.map(format_prompt, remove_columns=eval_dataset.column_names)
    
    # Show sample
    print(f"\n📝 Sample formatted training example:")
    print(train_dataset[0]['text'][:300] + "...")
    
    # Simpler training arguments
    print("5. Setting up training configuration...")
    training_args = TrainingArguments(
        per_device_train_batch_size=1,  # Smaller batch size
        gradient_accumulation_steps=8,  # Compensate with more accumulation
        warmup_steps=2,
        max_steps=50,  # Fewer steps for testing
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=5,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir=OUTPUT_DIR,
        save_steps=25,
        save_total_limit=2,
        dataloader_pin_memory=False,  # Disable to avoid issues
        report_to=None,
    )
    
    # Create trainer with simpler settings
    print("6. Creating trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LENGTH,
        dataset_num_proc=1,  # Single process to avoid issues
        packing=False,
        args=training_args,
    )
    
    # Start training
    print("7. Starting training...")
    print("🚀 Training with simplified settings...")
    
    try:
        trainer_stats = trainer.train()
        
        # Save model
        print("8. Saving improved model...")
        model.save_pretrained(OUTPUT_DIR)
        tokenizer.save_pretrained(OUTPUT_DIR)
        
        print(f"\n✅ Training completed!")
        print(f"📁 Model saved to: {OUTPUT_DIR}")
        print(f"⏱️  Training time: {trainer_stats.metrics.get('train_runtime', 'N/A')} seconds")
        print(f"🔥 Final loss: {trainer_stats.metrics.get('train_loss', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        print("Trying to save partial model...")
        try:
            model.save_pretrained(OUTPUT_DIR + "_partial")
            tokenizer.save_pretrained(OUTPUT_DIR + "_partial")
            print(f"📁 Partial model saved to: {OUTPUT_DIR}_partial")
        except:
            print("Could not save partial model")
        return
    
    print(f"\n🎯 Next steps:")
    print(f"1. Update model_service.py to use '{OUTPUT_DIR}' as model_path")
    print(f"2. Restart your server: python app.py")
    print(f"3. Test the improved AP-focused responses!")

if __name__ == "__main__":
    main()