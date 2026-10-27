import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="python", args=["server.py"])


async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("连接成功")

            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(f"{tool.name}: {tool.description}")

            result = await session.call_tool("add", {"a": 2, "b": 3})
            print(result)
            print(result.structured_content["result"])


if __name__ == "__main__":
    asyncio.run(main())
