from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    city: str
    weather: str
    plan: str

def check_weather(state: State):
    print("A 收到:", state)
    return {"weather": "雨"}

def make_plan(state: State):
    print("B 收到:", state)
    return {"plan": f"{state['city']}今天{state['weather']}, 不适合散步"}

builder = StateGraph(State)
builder.add_node("check_weather", check_weather)
builder.add_node("make_plan", make_plan)
builder.add_edge(START, "check_weather")
builder.add_edge("check_weather", "make_plan")
builder.add_edge("make_plan", END)

graph = builder.compile()
result = graph.invoke({"city": "成都"})
print("最终:", result)
# for step in graph.stream({"city": "成都"}, stream_mode="updates"):
#     print(step)