from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    city: str
    budget: int
    decision: str
    logs: Annotated[list, add]


def make_budget(state: State):
    print("make_budget 执行")
    return {"budget": 3000, "logs": ["make_budget 来过"]}


def ask_human(state: State):
    print("ask_human 开始执行")
    question = f"去{state['city']}预算{state['budget']}元,批准吗?"
    answer = interrupt(question)
    print("ask_human 拿到回答:", answer)
    return {"decision": answer, "logs": ["ask_human 来过"]}


def route_by_decision(state: State) -> str:
    if state["decision"] == "批准":
        return "book"
    return "replan"


def book(state: State):
    print("book 执行")
    return {"logs": ["book 来过"]}


def replan(state: State):
    print("replan 执行")
    return {"logs": ["replan 来过"]}


builder = StateGraph(State)
builder.add_node("make_budget", make_budget)
builder.add_node("ask_human", ask_human)
builder.add_node("book", book)
builder.add_node("replan", replan)
builder.add_edge(START, "make_budget")
builder.add_edge("make_budget", "ask_human")
builder.add_conditional_edges("ask_human", route_by_decision)
builder.add_edge("book", END)
builder.add_edge("replan", END)

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}

result = graph.invoke({"city": "成都", "logs": ["进门"]}, config)
print("第一次返回:", result)

snapshot = graph.get_state(config)
print("暂停中 next:", snapshot.next)
print("暂停中 values:", snapshot.values)

result = graph.invoke(Command(resume="批准"), config)
print("第二次返回:", result)