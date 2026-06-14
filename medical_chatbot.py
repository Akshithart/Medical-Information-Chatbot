from transformers import pipeline

# Load FLAN-T5 model once during startup
generator = pipeline(
    task="text2text-generation",
    model="google/flan-t5-small",
    framework="pt"
)

def generate_answer(question, context):
    """
    Generate answer using retrieved document context
    """

    prompt = f"""
You are a medical information assistant.

Answer ONLY using the provided context.
If the answer is not present in the context, say:
"I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = generator(
        prompt,
        max_length=256,
        do_sample=False
    )

    return response[0]["generated_text"].strip()


# Testing
if __name__ == "__main__":

    sample_context = """
    Diabetes symptoms include increased thirst,
    frequent urination, fatigue,
    blurred vision and weight loss.
    """

    sample_question = "What are the symptoms of diabetes?"

    answer = generate_answer(
        sample_question,
        sample_context
    )

    print("\nAnswer:")
    print(answer)