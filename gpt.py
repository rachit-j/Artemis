# gpt.py
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

import asyncio
import edge_tts
import tempfile
import subprocess
import os

async def speak(text, voice="en-US-AriaNeural"):
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        output_path = fp.name

    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_path)

    # Play the audio (macOS: use afplay; Linux: use mpg123 or aplay)
    try:
        subprocess.run(["afplay", output_path])  # macOS
    except FileNotFoundError:
        subprocess.run(["mpg123", output_path])  # fallback for Linux

    os.unlink(output_path)  # Clean up


def ask_gpt(prompt):
    print("🤖 Asking GPT...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        result = response.choices[0].message.content.strip()
        print("GPT:", result)
        asyncio.run(speak(result))  # 🔊 Now works!
        return result
    except Exception as e:
        return f"Error: {e}"
