from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    tries: int

def try_book(state: State):
    print("第几次:", state["tries"] + 1)
    return {"tries": state["tries"] + 1}

def route_try(state: State) -> str:
    if state["tries"] < 100:
        return "try_book"
    else:
        return END

builder = StateGraph(State)
builder.add_node("try_book", try_book)
builder.add_edge(START, "try_book")
builder.add_conditional_edges("try_book", route_try)
graph = builder.compile()
result = graph.invoke({"tries": 0}, config={"recursion_limit": 10})
print(result)