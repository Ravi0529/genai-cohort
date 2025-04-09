from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import ast

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Always list all the steps in the JSON format
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
ans = { step: "string", content: "string" }
Return: list[ans]

Example:
Input: What is 2 + 2.
Output: { "step": "analyse", "content": "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }
Output: { "step": "think", "content": "To perform the addition i must go from left to right and add all the operands" }
Output: { "step": "output", "content": "4" }
Output: { "step": "validate", "content": "seems like 4 is correct ans for 2 + 2" }
Output: { "step": "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers" }
"""

messages = []

query = input("> ")

messages.append(query)

while True:
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

    # Parse to list of dicts
    steps = ast.literal_eval(raw_text)
    messages.append(response.text)

    for step in steps:
        print(f"🧠: [{step['step']}] {step['content']}")
        if step["step"].lower() == "result":
            print("✅ Final result reached. Exiting loop.")
            exit()
