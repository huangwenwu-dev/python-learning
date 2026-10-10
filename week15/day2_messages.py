from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

def checks(state: State):
    print("A 收到:", state)
    return {"messages": [AIMessage(content="改写", id="1")]}

builder = StateGraph(State)
builder.add_node("checks", checks)
builder.add_edge(START, "checks")
builder.add_edge("checks", END)

graph = builder.compile()
result = graph.invoke({"messages": [HumanMessage(content="你好", id="1")]})
for m in result["messages"]:
    print(type(m).__name__, "| id =", m.id, "|", m.content)