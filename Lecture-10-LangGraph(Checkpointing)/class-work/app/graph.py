from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

llm = init_chat_model(
    model_provider="openai", model="gpt-4o-mini"
)  # Initialize the chat model using OpenAI's GPT-3.5 Turbo (using langchain --> going more abstract)


class State(TypedDict):
    messages: Annotated[
        list, add_messages
    ]  # Annotated type with metadata (type: list, metadata: add_messages)


def chatbot(state: State):
    return {
        "messages": [llm.invoke(state["messages"])]
    }  # llm invokes all the messages in the state


graph_builder = StateGraph(State)

### Nodes and Edges
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Graph without any Memory or Checkpointing
graph = graph_builder.compile()

# Graph with Checkpointing
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
