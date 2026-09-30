from langchain.agents import create_agent
from week14.frame_tools import search_documents
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()
import sqlite3

conn = sqlite3.connect("week14/checkpoints_day6.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

llm = init_chat_model(
    "deepseek:deepseek-v4-flash",
    temperature=0,
    extra_body={"thinking": {"type": "disabled"}},
)

summary_llm = init_chat_model(
    "deepseek:deepseek-v4-flash",
    temperature=0,
    extra_body={"thinking": {"type": "disabled"}},
)

agent = create_agent(
    model=llm,
    tools=[search_documents],
    system_prompt="""你是一个文档助手。
    1. 当用户询问知识库中的内容时，先用 search_documents 工具检索资料，再根据资料回答。
    2. 只根据检索到的资料回答，不要编造。资料中没有的，明确说"资料中未找到相关信息"。
    3. 闲聊或常识问题，可以直接回答，不必检索。""",
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model=summary_llm,
            trigger=("tokens", 2000),
            keep=("messages", 4),
        )
    ],
)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "w14d6-eval"}}
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