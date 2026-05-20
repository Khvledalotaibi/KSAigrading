from dotenv import load_dotenv
import os
import re
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("API_KEY"))

def normalize(text):
    text = re.sub(r'\([^)]*\)', '', text)
    return text.strip()

# Read files
with open("canswers.txt", "r") as f:
    correct = [normalize(line.strip()) for line in f if line.strip() and not line.startswith("Question")]

with open("sanswers.txt", "r") as f:
    student = [line.strip() for line in f if line.strip() and not line.startswith("Question")]

min_len = min(len(correct), len(student))
correct = correct[:min_len]
student = student[:min_len]

ai_correct = 0
total = len(correct)

for i, (exp, stu) in enumerate(zip(correct, student), 1):
    prompt = f"""Grade if the student's answer is correct.

Expected: {exp}
Student: {stu}

Rules:
- Ignore case, spaces, punctuation
- "Six" = "6", "Five" = "5", "Seven" = "7"
- If expected says "any two", student needs at least two matches
- More items than expected is still correct
- Different wording but same meaning is correct

Reply ONLY: YES or NO"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    verdict = response.choices[0].message.content.strip().upper()
    is_correct = (verdict == "YES")
    
    if is_correct:
        ai_correct += 1
    
    print(f"Q{i}: {stu[:25]} vs {exp[:25]} → {verdict} {'✅' if is_correct else '❌'}")

print(f"\nAccuracy: {ai_correct}/{total} = {(ai_correct/total)*100:.1f}%")