import logging
import time
from pathlib import Path
from typing import Annotated, TypedDict
from operator import add
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
llm = init_chat_model("deepseek-v4-pro", model_provider="deepseek")

# 日志：按本文件所在目录定位 logs/trip.log，不管从哪个目录运行都写到 week18/logs/ 下
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("trip_agent")
logger.setLevel(logging.DEBUG)
_file_handler = logging.FileHandler(LOG_DIR / "trip.log", encoding="utf-8")  # 默认 mode="a"，接着写不覆盖
_file_handler.setFormatter(logging.Formatter(
    "%(asctime)s.%(msecs)03d | %(levelname)s | %(node)s | %(thread_id)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
logger.addHandler(_file_handler)
logger.propagate = False  # 不往 root logger 冒泡，屏幕上只保留原有的 print


def _log(level: int, node: str, config: RunnableConfig, message: str) -> None:
    thread_id = config.get("configurable", {}).get("thread_id", "unknown")
    logger.log(level, message, extra={"node": node, "thread_id": thread_id})


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
def check_weather(state: TripState, config: RunnableConfig):
    print("[check_weather] 收到:", state)
    _log(logging.INFO, "check_weather", config, "开始执行")
    t0 = time.monotonic()
    weather = FAKE_WEATHER.get(state["city"], "未知")
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "check_weather", config, f"执行结束，耗时 {elapsed_ms}ms")
    return {"weather": weather, "logs": ["check_weather 来过"]}


# ④ 任务2:生成行程
def make_itinerary(state: TripState, config: RunnableConfig):
    print("[make_itinerary] 收到:", state)
    _log(logging.INFO, "make_itinerary", config, "开始执行")
    t0 = time.monotonic()
    if state["weather"] == "雨" or state["weather"] == "雪":
        style = "室内"
    else:
        style = "户外"
    prompt = f"请为去{state['city']}玩{state['days']}天、倾向{style}活动的行程，写一段100字以内的中文行程描述。"
    _log(
        logging.DEBUG, "make_itinerary", config,
        f"city={state['city']}, days={state['days']}, weather={state['weather']}, style={style}",
    )
    _log(logging.INFO, "make_itinerary", config, "开始调模型")
    itinerary = llm.invoke(prompt).content
    _log(logging.INFO, "make_itinerary", config, f"模型返回，共 {len(itinerary)} 字")
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "make_itinerary", config, f"执行结束，耗时 {elapsed_ms}ms")
    return {"style": style, "itinerary": itinerary, "logs": ["make_itinerary 来过"]}


# ⑤ 任务3:核算预算
def check_budget(state: TripState, config: RunnableConfig):
    print("[check_budget] 收到:", state)
    _log(logging.INFO, "check_budget", config, "开始执行")
    t0 = time.monotonic()
    budget = DAILY_COST[state["style"]] * state["days"]
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "check_budget", config, f"执行结束，耗时 {elapsed_ms}ms")
    return {"budget": budget, "logs": ["check_budget 来过"]}


# ⑥ 人工确认
def ask_human(state: TripState, config: RunnableConfig):
    print("[ask_human] 开始执行")
    _log(logging.INFO, "ask_human", config, "开始执行")
    t0 = time.monotonic()
    answer = interrupt(f"行程:{state['itinerary']},预算 {state['budget']} 元,批准吗?")
    print("[ask_human] 拿到回答:", answer)
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "ask_human", config, f"执行结束，耗时 {elapsed_ms}ms")
    return {"decision": answer, "logs": ["ask_human 来过"]}


# ⑦ 分拣员 + 两个出口
def route_by_decision(state: TripState) -> str:
    if state["decision"] == "批准":
        return "book"
    return "replan"


def book(state: TripState, config: RunnableConfig):
    print(f"[book] 已预订,扣款 {state['budget']} 元")   # 有副作用的动作放在批准之后
    _log(logging.INFO, "book", config, "开始执行")
    t0 = time.monotonic()
    _log(logging.WARNING, "book", config, f"发生扣款，金额 {state['budget']}")
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "book", config, f"执行结束，耗时 {elapsed_ms}ms")
    return {"logs": ["book 来过"]}


def replan(state: TripState, config: RunnableConfig):
    print("[replan] 预算被拒,标记为需要重新规划")
    _log(logging.INFO, "replan", config, "开始执行")
    t0 = time.monotonic()
    elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    _log(logging.INFO, "replan", config, f"执行结束，耗时 {elapsed_ms}ms")
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