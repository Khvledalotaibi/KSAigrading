from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    print("ERROR: API_KEY not found in .env file")
    exit()

print(f"API key loaded: {api_key[:10]}... (length: {len(api_key)})")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(f"AI Response: {response.choices[0].message.content}")