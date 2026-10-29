import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="python", args=["tools_server.py"])


async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("连接成功")

            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(tool)
                print(f"名字: {tool.name}")
                print(f"说明: {tool.description}")
                print(f"参数说明: {tool.input_schema}")

            result1 = await session.call_tool("list_files", {})
            print(result1.is_error, result1.structured_content)

            result2 = await session.call_tool("file_size", {"path": "a.txt"})
            print(result2.is_error, result2.structured_content)
            print(result2.content)

            result3 = await session.call_tool("count_lines", {"path": "a.txt"})
            print(result3.is_error, result3.structured_content)


if __name__ == "__main__":
    asyncio.run(main())