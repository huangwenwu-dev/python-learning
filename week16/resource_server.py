from pathlib import Path
from typing import Annotated

from pydantic import Field

from mcp.server import MCPServer

SANDBOX_DIR = Path(__file__).parent / "sandbox"

mcp = MCPServer("Resource Server")


def safe_path(path: str) -> Path | None:
    """把 path 拼到 SANDBOX_DIR 下并校验是否仍在 sandbox 内，不在就返回 None"""
    sandbox_root = SANDBOX_DIR.resolve()
    target = (SANDBOX_DIR / path).resolve()
    if not target.is_relative_to(sandbox_root):
        return None
    return target


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
    target = safe_path(path)
    if target is None:
        return f"拒绝：路径「{path}」超出 sandbox 范围"
    if not target.exists():
        return f"文件「{path}」不存在，请检查 sandbox 文件夹里的文件名"
    return target.read_text(encoding="utf-8")


@mcp.tool()
def write_file(
    path: Annotated[str, Field(description="sandbox 文件夹里的相对路径，例如 c.txt")],
    content: Annotated[str, Field(description="要写入文件的文本内容")],
) -> str:
    """在 sandbox 文件夹内写入文件，不允许写到 sandbox 外面"""
    target = safe_path(path)
    if target is None:
        return f"拒绝：路径「{path}」超出 sandbox 范围"

    if not target.parent.exists():
        return f"拒绝：父目录「{target.parent}」不存在，请先创建目录"

    existed = target.exists()
    target.write_text(content, encoding="utf-8")
    size = len(content.encode("utf-8"))

    if existed:
        return f"已覆盖写入：{target}（{size} 字节）"
    return f"写入成功：{target}（{size} 字节）"


if __name__ == "__main__":
    mcp.run(transport="stdio")
