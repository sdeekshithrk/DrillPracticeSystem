from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

async def generate_feedback(answer_type: str, problem_text: str, expected: str, student: str):

    prompt = f"""
Be a guide to the student who is trying to solve problems in logic and set theory.
Guide the student with concepts and mistakes in their solution but never reveal the answer.

Problem Statement: {problem_text}

Answer Type: {answer_type}
Expected (internal reference only, DO NOT reveal): {expected}
Student Answer: {student}

Use only readable logic symbols, no latex or other coded format.
Keep paragraphs short and clearly separated (1–2 sentences each).
Never reveal the correct answer.
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2,
    )

    return res.choices[0].message.content
