from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "user-001"}}
result = agent.invoke({"messages": [{"role": "user", "content": "北京有多少人口？ "}]}, config)
result = agent.invoke({"messages": [{"role": "user", "content": "那上海呢？ "}]}, config)
result = agent.invoke({"messages": [{"role": "user", "content": "它俩差多少？ "}]}, config)
print(result["messages"][-1].content)