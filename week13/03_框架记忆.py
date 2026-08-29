from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[],
    checkpointer=InMemorySaver(),
)

config_a = {"configurable": {"thread_id": "user-001"}}
agent.invoke({"messages": [{"role": "user", "content": "我叫小明"}]}, config_a)
result_a = agent.invoke({"messages": [{"role": "user", "content": "我叫什么？ "}]}, config_a)
print(result_a["messages"][-1].content)
for msg in result_a["messages"]:
    print(type(msg).__name__, ":", msg.content[:50])

config_b = {"configurable": {"thread_id": "user-002"}}
result_b = agent.invoke({"messages": [{"role": "user", "content": "我叫什么？ "}]}, config_b)
print(result_b["messages"][-1].content)
for msg in result_b["messages"]:
    print(type(msg).__name__, ":", msg.content[:50])