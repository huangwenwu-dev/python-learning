import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="python", args=["resource_server.py"])


async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("连接成功")

            # ① 固定资源列表
            resources_result = await session.list_resources()
            print(resources_result)
            for resource in resources_result.resources:
                print(f"名字: {resource.name}")
                print(f"URI: {resource.uri}")
                print(f"说明: {resource.description}")

            # ② 资源模板列表
            templates_result = await session.list_resource_templates()
            print(templates_result)
            for template in templates_result.resource_templates:
                print(f"名字: {template.name}")
                print(f"URI模板: {template.uri_template}")
                print(f"说明: {template.description}")

            # ③ 工具列表
            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(tool)
                print(f"名字: {tool.name}")
                print(f"说明: {tool.description}")
                print(f"参数说明: {tool.input_schema}")

            # ④ read_resource("sandbox://readme")
            r1 = await session.read_resource("sandbox://readme")
            print(r1)
            print(r1.contents[0].text)

            # ⑤ read_resource("sandbox://a.txt")
            r2 = await session.read_resource("sandbox://a.txt")
            print(r2)
            print(r2.contents[0].text)

            # ⑥ call_tool("read_file", {"path": "a.txt"})
            r3 = await session.call_tool("read_file", {"path": "a.txt"})
            print(r3.is_error, r3.structured_content)
            print(r3.content)


if __name__ == "__main__":
    asyncio.run(main())