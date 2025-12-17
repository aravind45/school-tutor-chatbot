from unsloth import FastLanguageModel
import torch


def load_and_chat():
    """Load fine-tuned model and chat with it"""

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="./llama-highschool-tutor",  # Your trained model
        max_seq_length=2048,
        dtype=torch.float16,
        load_in_4bit=True,
    )

    FastLanguageModel.for_inference(model)

    print("🤖 High School Tutor is ready! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("\n📚 Student: ").strip()

        if user_input.lower() == 'quit':
            break

        prompt = f"""### Instruction:
{user_input}

### Response:
"""

        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            temperature=0.7,
            do_sample=True,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean up response
        if "### Response:" in response:
            response = response.split("### Response:")[1].strip()

        print(f"\n🤖 Tutor: {response}")
        print("-" * 50)


if __name__ == "__main__":
    load_and_chat()