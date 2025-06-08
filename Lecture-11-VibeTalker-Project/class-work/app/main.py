from dotenv import load_dotenv

load_dotenv()

import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
import asyncio
from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI
import os
from graph import create_chat_graph

openai = AsyncOpenAI()

config = {"configurable": {"thread_id": "1"}}

MONGODB_URI = os.getenv("MONGODB_URI")


def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)

        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 5

            while True:
                print("Listening...")
                audio = r.listen(source)

                print("Processing audio...")
                sst = r.recognize_google(audio)

                print("User: ", sst)
                for event in graph.stream(
                    {"messages": [{"role": "user", "content": sst}]},
                    config,
                    stream_mode="values",
                ):
                    if "messages" in event:
                        event["messages"][-1].pretty_print()


async def speak(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instruction="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#      asyncio.run(speak(text="This is a sample voice. Hi Ravi."))
