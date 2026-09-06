from dotenv import load_dotenv
load_dotenv()
from week13.rag_agent import agent

config = {"configurable": {"thread_id": "day1-trace"}}
q = input("你: ")
result = agent.invoke({"messages": [{"role": "user", "content": q}]}, config)
print(result["messages"][-1].content)