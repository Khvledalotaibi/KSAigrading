from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("API_KEY"))

# Read files
with open("questions.txt", "r") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]

with open("answers.txt", "r") as f:
    answers = [line.strip() for line in f.readlines() if line.strip()]

# Grade each
correct = 0
total = len(questions)

for i, (q, expected) in enumerate(zip(questions, answers), 1):
    prompt = f"""Grade this student answer.

Question: {q}
Expected items: {expected}
Student answer: {expected.lower()}  (this is a test — the student gave the complete correct answer)

Return ONLY score as X/Y where Y is number of items in expected."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"Q{i}: {response.choices[0].message.content}")