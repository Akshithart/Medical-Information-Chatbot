from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_answer(
    question,
    context
):

    prompt = f"""
You are a medical assistant.

Answer ONLY the question.

Rules:
- Maximum 2 sentences.
- Maximum 40 words.
- Do not repeat the context.
- Give only the final answer.

Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )

    return result[0]["generated_text"]