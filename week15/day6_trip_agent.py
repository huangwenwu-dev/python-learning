from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# ① 单子长什么样
class TripState(TypedDict):
    city: str          # 投单时给
    days: int          # 投单时给
    weather: str       # check_weather 交
    style: str         # make_itinerary 交
    itinerary: str     # make_itinerary 交
    budget: int        # check_budget 交
    decision: str      # ask_human 交
    logs: Annotated[list, add]


# ② 模拟数据(假装是外部接口)
FAKE_WEATHER = {"成都": "雨", "三亚": "晴", "北京": "晴", "哈尔滨": "雪"}
DAILY_COST = {"室内": 400, "户外": 600}


# ③ 任务1:查天气
def check_weather(state: TripState):
    print("[check_weather] 收到:", state)
    weather = FAKE_WEATHER.get(state["city"], "未知")
    return {"weather": weather, "logs": ["check_weather 来过"]}


# ④ 任务2:生成行程
def make_itinerary(state: TripState):
    print("[make_itinerary] 收到:", state)
    if state["weather"] == "雨" or state["weather"] == "雪":
        style = "室内"
    else:
        style = "户外"
    itinerary = f"{state['city']}{state['days']}天{style}游"
    return {"style": style, "itinerary": itinerary, "logs": ["make_itinerary 来过"]}


# ⑤ 任务3:核算预算
def check_budget(state: TripState):
    print("[check_budget] 收到:", state)
    budget = DAILY_COST[state["style"]] * state["days"]
    return {"budget": budget, "logs": ["check_budget 来过"]}


# ⑥ 人工确认
def ask_human(state: TripState):
    print("[ask_human] 开始执行")
    answer = interrupt(f"行程:{state['itinerary']},预算 {state['budget']} 元,批准吗?")
    print("[ask_human] 拿到回答:", answer)
    return {"decision": answer, "logs": ["ask_human 来过"]}


# ⑦ 分拣员 + 两个出口
def route_by_decision(state: TripState) -> str:
    if state["decision"] == "批准":
        return "book"
    return "replan"


def book(state: TripState):
    print(f"[book] 已预订,扣款 {state['budget']} 元")   # 有副作用的动作放在批准之后
    return {"logs": ["book 来过"]}


def replan(state: TripState):
    print("[replan] 预算被拒,标记为需要重新规划")
    return {"logs": ["replan 来过"]}


# ⑧ 接线 + 装档案柜
builder = StateGraph(TripState)
builder.add_node("check_weather", check_weather)
builder.add_node("make_itinerary", make_itinerary)
builder.add_node("check_budget", check_budget)
builder.add_node("ask_human", ask_human)
builder.add_node("book", book)
builder.add_node("replan", replan)

builder.add_edge(START, "check_weather")
builder.add_edge("check_weather", "make_itinerary")
builder.add_edge("make_itinerary", "check_budget")
builder.add_edge("check_budget", "ask_human")
builder.add_conditional_edges("ask_human", route_by_decision, {"book": "book", "replan": "replan"})
builder.add_edge("book", END)
builder.add_edge("replan", END)

graph = builder.compile(checkpointer=InMemorySaver())


# ⑨ 投单、暂停、恢复
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "trip-3"}}

    first = graph.invoke({"city": "哈尔滨", "days": 2, "logs": ["进门"]}, config)
    print("暂停,请示内容:", first["__interrupt__"][0].value)
    print("暂停中 next:", graph.get_state(config).next)

    final = graph.invoke(Command(resume="批准"), config)
    print("最终单子:", final)

    print(graph.get_graph().draw_mermaid())