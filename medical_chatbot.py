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
Answer the question using ONLY the context.

Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ]