import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="python", args=["resource_server.py"])

# 每一条：(工具名, 参数)
tests = [
    ("write_file", {"path": "../hack.txt", "content": "x"}),
    ("read_file", {"path": "../tools_server.py"}),
    ("read_file", {"path": "a.txt"}),
]

async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            for number, (tool, args) in enumerate(tests, start=1):
                result = await session.call_tool(tool, args)
                print(f"第 {number} 条: {tool} {args['path']}")
                print("is_error:", result.is_error)
                print(result.content[0].text[:100])
                print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())