from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    tries: int

def try_book(state: State):
    print("第几次:", state["tries"] + 1)
    return {"tries": state["tries"] + 1}

def route_try(state: State) -> str:
    if state["tries"] < 3:
        return "try_book"
    else:
        return END

builder = StateGraph(State)
builder.add_node("try_book", try_book)
builder.add_edge(START, "try_book")
builder.add_conditional_edges("try_book", route_try)
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}
print("第一次:", graph.invoke({"tries": 0}, config))
print("第二次:", graph.invoke({"tries": 0}, config))