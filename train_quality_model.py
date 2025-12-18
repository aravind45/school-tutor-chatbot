#!/usr/bin/env python3
"""
Train tutor model with high-quality data
"""

import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import os

def train_quality_tutor():
    """Train the tutor model with quality data"""
    
    print("🚀 Starting Quality Tutor Training")
    print("="*50)
    
    # Model configuration
    model_name = "unsloth/llama-3.2-3b-instruct-bnb-4bit"
    max_seq_length = 2048
    dtype = None  # Auto-detect
    load_in_4bit = True
    
    # Load model
    print("📥 Loading base model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )
    
    # Configure for training
    print("⚙️ Configuring model for training...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # LoRA rank
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )
    
    # Load training data
    print("📚 Loading training data...")
    dataset = load_dataset("json", data_files="data_comprehensive_final/train_massive.jsonl", split="train")
    
    print(f"📊 Dataset size: {len(dataset)} examples")
    
    # Format data for training
    def formatting_prompts_func(examples):
        instructions = examples["instruction"]
        inputs = examples["input"]
        outputs = examples["output"]
        texts = []
        
        for instruction, input_text, output in zip(instructions, inputs, outputs):
            if input_text:
                text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
            else:
                text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
            texts.append(text)
        
        return {"text": texts}
    
    dataset = dataset.map(formatting_prompts_func, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=300,  # More steps for larger dataset
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="tutor_model_massive",
        save_steps=100,
        save_total_limit=3,
    )
    
    # Create trainer
    print("🏋️ Setting up trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False,
        args=training_args,
    )
    
    # Train
    print("🔥 Starting training...")
    trainer_stats = trainer.train()
    
    # Save model
    print("💾 Saving trained model...")
    model.save_pretrained("tutor_model_massive")
    tokenizer.save_pretrained("tutor_model_massive")
    
    print("✅ Training completed!")
    print(f"📁 Model saved to: tutor_model_massive")
    
    return trainer_stats

if __name__ == "__main__":
    # Set environment variables for Windows compatibility
    os.environ["TORCHDYNAMO_DISABLE"] = "1"
    os.environ["TORCH_COMPILE"] = "0"
    
    try:
        stats = train_quality_tutor()
        print("🎉 Training successful!")
    except Exception as e:
        print(f"❌ Training failed: {e}")
        print("💡 Try running with smaller batch size or fewer steps")
