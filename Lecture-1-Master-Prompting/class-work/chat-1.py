from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": "Which one is smaller? 9.8 or 9.11",
        }  # Zero Shot Prompting, no system prompt
    ],
)

print(result.choices[0].message.content)
