from .graph import graph
from dotenv import load_dotenv

load_dotenv()


def init():
    while True:
        user_input = input("> ")
        if user_input.lower() == "clear":
            break
        # graph.invoke() vs graph.stream()
        # invoke ---> returns the final result after processing all messages(all nodes)
        # stream ---> returns a result after every node is processed

        # result = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
        # print(result)

        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            stream_mode="values",
        ):
            if "messages" in event:
                event["messages"][
                    -1
                ].pretty_print()  # issue here is ---> no previous messages are stored by the graph, everytime the user asks a question, it fresh starts the graph (i.e. no checkpointing)


init()
