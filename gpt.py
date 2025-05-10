# gpt.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def ask_gpt(prompt):
    print("🤖 Asking GPT...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
