from operator import add
from typing import Annotated,  TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    city: str
    weather: str
    plan: str
    logs: Annotated[list, add]

def check_weather(state: State):
    print("check_weather 收到:", state)
    if state["city"] == "成都":
        weather = "雨"
    elif state["city"] == "哈尔滨":
        weather = "阴"
    else:
        weather = "晴"
    return {"weather": weather, "logs": ["check_weather 来过"]}
   

def route_by_weather(state: State) -> str:
    print("route_by_weather 收到:", state)
    if state["weather"] == "雨":
        return "雨"
    else:
        return "晴"

def indoor_plan(state: State):
    print("indoor_plan 收到:", state)
    return {"plan": f"{state['city']}下雨，安排室内：博物馆 + 咖啡馆", "logs": ["indoor_plan 来过"]}


def outdoor_plan(state: State):
    print("outdoor_plan 收到:", state)
    return {"plan": f"{state['city']}晴天，安排室外：西湖 + 骑行", "logs": ["outdoor_plan 来过"]}

def summary(state: State):
    print("summary 收到:", state)
    return {"plan": f"最终方案：{state['city']}（{state['weather']}）→ {state['plan']}", "logs": ["summary 来过"]}

builder = StateGraph(State)
builder.add_node("check_weather", check_weather)
builder.add_node("indoor_plan", indoor_plan)
builder.add_node("outdoor_plan", outdoor_plan)
builder.add_node("summary", summary)
builder.add_edge(START, "check_weather")
builder.add_conditional_edges(
    "check_weather",
    route_by_weather,
    {"雨": "indoor_plan", "晴": "outdoor_plan"},
)
builder.add_edge("indoor_plan", "summary")
builder.add_edge("outdoor_plan", "summary")
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}
config2 = {"configurable": {"thread_id": "2"}}
# result = graph.invoke({"city": "成都", "logs": ["进门"]}, config)
# result = graph.invoke({"city": "三亚", "logs": ["进门"]}, config2)
# print("最终 state:", result)

snapshot = graph.get_state(config)
print("快照 values:", snapshot.values)
print("快照 next:", snapshot.next)

# print("----- 翻档案袋 -----")
# for s in graph.get_state_history(config):
#     print(s.next, s.values.get("logs"))