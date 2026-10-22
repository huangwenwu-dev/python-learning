from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, AIMessage

def bot(state: MessagesState):
    msgs = state["messages"]
    print("bot 收到几条消息:", len(msgs))
    n = sum(1 for m in msgs if isinstance(m, HumanMessage))
    return {"messages": [AIMessage(content=f"我已经看到你说的{n}条话")]}

builder = StateGraph(MessagesState)
builder.add_node("bot", bot)
builder.add_edge(START, "bot")
builder.add_edge("bot", END)
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}

for text in ["你好", "今天天气怎么样", "再见"]:
    result = graph.invoke({"messages": [HumanMessage(content=text)]}, config)
    print("机器人:", result["messages"][-1].content)