from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from operator import add

def my_add(old, new):
    print("合并被调用: 旧 =", old, "| 新 =", new)
    return old + new

class State(TypedDict):
    logs: Annotated[list, my_add]

def check(state: State):
    print("A 收到:", state)
    return{"logs": ["A 来过"]}

def make(state: State):
    print("B 收到:", state)
    return {"logs": ["B 来过"]}

builder = StateGraph(State)
builder.add_node("check", check)
builder.add_node("make", make)
builder.add_edge(START, "check")
builder.add_edge("check", "make")
builder.add_edge("make", END)

graph = builder.compile()
# result = graph.invoke({})
result = graph.invoke({"logs": ["进门"]})
print(result["logs"])
# for step in graph.stream({"logs": ["进门"]}, stream_mode="updates"):
#     print(step)