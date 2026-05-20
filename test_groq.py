from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Your exam question
question = "List three types of computer memory."
rubric = ["RAM", "ROM", "Cache"]
student_answer = "RAM and ROM"

prompt = f"""Grade this student answer against the rubric.

Rubric (expected items): {rubric}
Student answer: {student_answer}

Return ONLY:
- Items found (list)
- Score (X/3)
- One-sentence feedback
"""

for i in range(5):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"Run {i+1}: {response.choices[0].message.content[:50]}...")