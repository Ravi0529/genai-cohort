### Checkpointing ---> It stores the state of every node in the graph, so that when the user asks a question, it can continue from the last state instead of starting fresh every time.
### ---> You can integrate any DB to store the state using checkpointing.


# from .graph import graph
from dotenv import load_dotenv
load_dotenv()

from graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver

MONGODB_URI = "mongodb://localhost:27017/"
config = {
    "configurable": {"thread_id": "1"}
}  # this is just like a unique user id, so that the graph can store the state for each user separately


def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        while True:
            user_input = input("> ")
            if user_input.lower() == "clear":
                break
            # graph.invoke() vs graph.stream()
            # invoke ---> returns the final result after processing all messages(all nodes)
            # stream ---> returns a result after every node is processed

            # result = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
            # print(result)

            # for event in graph.stream(
            #     {"messages": [{"role": "user", "content": user_input}]},
            #     stream_mode="values",
            # ):
            #     if "messages" in event:
            #         event["messages"][
            #             -1
            #         ].pretty_print()  # issue here is ---> no previous messages are stored by the graph, everytime the user asks a question, it fresh starts the graph (i.e. no checkpointing)

            for event in graph_with_mongo.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config,
                stream_mode="values",
            ):
                if "messages" in event:
                    event["messages"][-1].pretty_print()


init()
