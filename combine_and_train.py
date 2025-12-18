#!/usr/bin/env python3
"""
Combine all quality training data and create training script
"""

import json
import os
import shutil

def combine_training_data():
    """Combine all quality training data sources"""
    
    combined_data = []
    
    # Read quality data
    quality_file = "data_quality/train.jsonl"
    if os.path.exists(quality_file):
        with open(quality_file, 'r', encoding='utf-8') as f:
            for line in f:
                combined_data.append(json.loads(line))
        print(f"✅ Added {len(combined_data)} examples from quality data")
    
    # Read comprehensive data
    comprehensive_file = "data_comprehensive_final/train.jsonl"
    if os.path.exists(comprehensive_file):
        start_count = len(combined_data)
        with open(comprehensive_file, 'r', encoding='utf-8') as f:
            for line in f:
                combined_data.append(json.loads(line))
        print(f"✅ Added {len(combined_data) - start_count} examples from comprehensive data")
    
    # Create final training directory
    final_dir = "data_final_training"
    os.makedirs(final_dir, exist_ok=True)
    
    # Save combined data
    final_file = f"{final_dir}/train.jsonl"
    with open(final_file, 'w', encoding='utf-8') as f:
        for item in combined_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"\n🎯 FINAL TRAINING DATA:")
    print(f"📁 Location: {final_file}")
    print(f"📊 Total examples: {len(combined_data)}")
    
    # Statistics
    subjects = {}
    for item in combined_data:
        subject = item.get('subject', 'Unknown')
        subjects[subject] = subjects.get(subject, 0) + 1
    
    print("\n📈 Subject Distribution:")
    for subject, count in subjects.items():
        print(f"  {subject}: {count} examples")
    
    return final_file, len(combined_data)

def create_training_script():
    """Create the training script for the new data"""
    
    training_script = """#!/usr/bin/env python3
\"\"\"
Train tutor model with high-quality data
\"\"\"

import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import os

def train_quality_tutor():
    \"\"\"Train the tutor model with quality data\"\"\"
    
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
    dataset = load_dataset("json", data_files="data_final_training/train.jsonl", split="train")
    
    print(f"📊 Dataset size: {len(dataset)} examples")
    
    # Format data for training
    def formatting_prompts_func(examples):
        instructions = examples["instruction"]
        inputs = examples["input"]
        outputs = examples["output"]
        texts = []
        
        for instruction, input_text, output in zip(instructions, inputs, outputs):
            if input_text:
                text = f"### Instruction:\\n{instruction}\\n\\n### Input:\\n{input_text}\\n\\n### Response:\\n{output}"
            else:
                text = f"### Instruction:\\n{instruction}\\n\\n### Response:\\n{output}"
            texts.append(text)
        
        return {"text": texts}
    
    dataset = dataset.map(formatting_prompts_func, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=100,  # Adjust based on data size
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="tutor_model_quality",
        save_steps=50,
        save_total_limit=2,
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
    model.save_pretrained("tutor_model_quality")
    tokenizer.save_pretrained("tutor_model_quality")
    
    print("✅ Training completed!")
    print(f"📁 Model saved to: tutor_model_quality")
    
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
"""
    
    with open("train_quality_model.py", 'w', encoding='utf-8') as f:
        f.write(training_script)
    
    print("✅ Created training script: train_quality_model.py")

def main():
    """Main function to combine data and create training script"""
    
    print("🔄 PREPARING QUALITY TRAINING DATA")
    print("="*50)
    
    # Combine all training data
    final_file, total_examples = combine_training_data()
    
    # Create training script
    create_training_script()
    
    print(f"\n🎯 READY TO TRAIN!")
    print(f"📊 Total training examples: {total_examples}")
    print(f"📁 Training data: {final_file}")
    print(f"🚀 Training script: train_quality_model.py")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Run: python train_quality_model.py")
    print(f"2. Wait for training to complete")
    print(f"3. Update model_service.py to use 'tutor_model_quality'")
    print(f"4. Test the new model!")
    
    if total_examples < 50:
        print(f"\n⚠️  WARNING: Only {total_examples} training examples.")
        print(f"   Consider adding more data for better results.")
        print(f"   Recommended: 100+ examples for good performance")

if __name__ == "__main__":
    main()