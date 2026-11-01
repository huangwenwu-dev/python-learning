from pathlib import Path
from typing import Annotated

from pydantic import Field

from mcp.server import MCPServer

SANDBOX_DIR = Path(__file__).parent / "sandbox"

mcp = MCPServer("Resource Server")


@mcp.resource("sandbox://{name}")
def read_sandbox_resource(name: str) -> str:
    """按文件名读取 sandbox 文件夹里文件的文本内容"""
    target = SANDBOX_DIR / name
    if not target.exists():
        return f"文件「{name}」不存在，请检查 sandbox 文件夹里的文件名"
    return target.read_text(encoding="utf-8")


@mcp.resource("sandbox://readme")
def read_readme() -> str:
    """固定说明文字，介绍 sandbox 文件夹里有哪些文件"""
    return "这是 week16 的练习文件夹，里面有 a.txt 和 b.md"


@mcp.tool()
def read_file(
    path: Annotated[str, Field(description="sandbox 文件夹里的文件名，例如 a.txt")]
) -> str:
    """读取 sandbox 文件夹中指定文件的文本内容"""
    target = SANDBOX_DIR / path
    if not target.exists():
        return f"文件「{path}」不存在，请检查 sandbox 文件夹里的文件名"
    return target.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
