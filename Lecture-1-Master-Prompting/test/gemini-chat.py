from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = """
You are a cat. Your name is Neko.
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    contents="Hello there! what's your name?",
)

print(response.text)
