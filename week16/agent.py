import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient  # type: ignore

load_dotenv()

BIG_PYTHON = r"C:\Users\文\AppData\Local\Programs\Python\Python314\python.exe"
SERVER_PATH = r"C:\Users\文\Desktop\python-learning\week16\resource_server.py"
QUESTION = "a.txt 有几行字"


async def main():
    client = MultiServerMCPClient(
        {
            "sandbox": {
                "command": BIG_PYTHON,
                "args": [SERVER_PATH],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()

    print(f"拿到 {len(tools)} 个工具：")
    for tool in tools:
        print(f"- 名字: {tool.name}")
        print(f"  说明: {tool.description}")
        print(f"  参数: {tool.args}")

    agent = create_agent(model="deepseek:deepseek-v4-pro", tools=tools)

    result = await agent.ainvoke({"messages": [{"role": "user", "content": QUESTION}]})

    print("\n模型调用的工具：")
    for message in result["messages"]:
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                print(f"- 工具名: {call['name']}, 参数: {call['args']}")

    print("\n最终答案：")
    print(result["messages"][-1].content)
    # print(agent.get_graph().draw_mermaid())


if __name__ == "__main__":
    asyncio.run(main())
