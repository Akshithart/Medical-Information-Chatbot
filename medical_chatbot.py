import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv("secrets.env")

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question, context):

    prompt = f"""
You are a medical information assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{question}

Requirements:
- Give a detailed answer.
- Use bullet points when needed.
- If information is unavailable, say:
  'Information not found in uploaded document.'

Answer:
"""

    response = model.generate_content(
        prompt
    )

    return response.text