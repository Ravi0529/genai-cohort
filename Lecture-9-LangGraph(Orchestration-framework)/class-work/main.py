from typing_extensions import TypedDict
from typing import Literal
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from langsmith.wrappers import wrap_openai
from pydantic import (
    BaseModel,
)  # this BaseModel is for validation of the code, just like Zod
from dotenv import load_dotenv

load_dotenv()

client = wrap_openai(OpenAI())


# Schema
class DetectCallResponse(
    BaseModel
):  # For strictness in response, that the return should be boolean(True or False)
    is_question_ai: bool


class CodingAIResponse(BaseModel):
    answer: str


class State(TypedDict):
    ai_message: str
    user_message: str
    is_coding_question: bool


def detect_query(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is related
    to coding question or not.
    Return the response in specified JSON boolean only.
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=DetectCallResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    state["is_coding_question"] = result.choices[0].message.parsed.is_question_ai
    return state


def route_edge(
    state: State,
) -> Literal["solve_coding_question", "solve_simple_question"]:
    is_coding_question = state.get("is_coding_question")
    if is_coding_question:
        return "solve_coding_question"
    else:
        return "solve_simple_question"


def solve_coding_question(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to resolve the user query based on coding 
    problem he is facing
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CodingAIResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state


def solve_simple_question(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to chat with user
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=CodingAIResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)
graph_builder.add_node("route_edge", route_edge)

graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges("detect_query", route_edge)

graph_builder.add_edge("solve_coding_question", END)
graph_builder.add_edge("solve_simple_question", END)

graph = graph_builder.compile()


### Using the Graph
def call_graph():
    state = {
        "user_message": "give me a code to add 2 numbers in python",
        "ai_message": "",
        "is_coding_question": False,  # Default value, will be updated by detect_query
    }
    result = graph.invoke(state)
    # print("Final result: ", result)
    print("Final result: ", result["ai_message"])


call_graph()
