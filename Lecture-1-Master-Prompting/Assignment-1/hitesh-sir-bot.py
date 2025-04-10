from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import ast

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("system-prompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

messages = []

while True:
    query = input("> ")

    if query.lower() in {"exit", "quit", "bye"}:
        print("Exiting chat. Goodbye!")
        break

    messages.append(query)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=messages,
    )

    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        # Parse to list of dicts
        steps = ast.literal_eval(raw_text)
        print(steps)
    except Exception as e:
        print("Error parsing response:", e)
        print("Raw response:", raw_text)

    messages.append(response.text)
