from langchain.agents import create_agent
from week13.rag_tools import search_documents
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv
load_dotenv()
import sqlite3

conn = sqlite3.connect("week13/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[search_documents],
    system_prompt="""你是一个文档助手。
    1. 当用户询问知识库中的内容时，先用 search_documents 工具检索资料，再根据资料回答。
    2. 只根据检索到的资料回答，不要编造。资料中没有的，明确说"资料中未找到相关信息"。
    3. 闲聊或常识问题，可以直接回答，不必检索。""",
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model="deepseek:deepseek-chat",
            trigger=("tokens", 2000),
            keep=("messages", 4),
        )
    ],
)

config = {"configurable": {"thread_id": "day6-test"}}

while True:
    q = input("你: ")
    if q == "quit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": q}]}, config)
    print(result["messages"][-1].content)
    tool_msgs = [m for m in result["messages"] if m.__class__.__name__ == "ToolMessage"]
    if tool_msgs:
        print(f"[日志] 检索了，共 {len(tool_msgs)} 次")
        for m in tool_msgs:
            print(f"[日志] 返回前80字: {m.content[:200]}")
    else:
        print("[日志] 未检索")
    print(f"[日志] token: {result['messages'][-1].usage_metadata}")