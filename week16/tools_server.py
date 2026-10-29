from pathlib import Path
from typing import Annotated

from pydantic import Field

from mcp.server import MCPServer

SANDBOX_DIR = Path(__file__).parent / "sandbox"

mcp = MCPServer("Tools Server")


@mcp.tool()
def list_files() -> list[str]:
    """列出 sandbox 文件夹中所有文件的文件名"""
    return [p.name for p in SANDBOX_DIR.iterdir() if p.is_file()]


@mcp.tool()
def file_size(
    path: Annotated[str, Field(description="sandbox 文件夹里的文件名，例如 a.txt")]
) -> int | str:
    """返回 sandbox 文件夹中指定文件的字节数；文件不存在时返回中文说明"""
    target = SANDBOX_DIR / path
    if not target.exists():
        return f"文件「{path}」不存在，请先用 list_files 查看 sandbox 文件夹里有哪些文件"
    return target.stat().st_size


@mcp.tool()
def count_lines(
    path: Annotated[str, Field(description="sandbox 文件夹里的文件名，例如 a.txt")]
) -> int:
    """返回 sandbox 文件夹中指定文件的行数，空文件返回 0"""
    count = 0
    with open(SANDBOX_DIR / path, encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count


if __name__ == "__main__":
    mcp.run(transport="stdio")
