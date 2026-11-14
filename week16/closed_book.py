from pathlib import Path
from typing import Annotated
from pydantic import Field
# 假设 MCP 已经建好

SANDBOX = Path(__file__).parent / "sandbox"

@mcp.tool()
def read_file(
    path:Annotated[str, Field(description="sandbox 文件夹里的文件名, 例如 a.txt")]) -> str:
    """读取 sandbox 文件夹中指定文件的文本内容"""
    full = SANDBOX / path                          # 12 拼地址
    full = full.resolve()                          # 13 算掉 ../，换成真实位置
    if not full.is_relative_to(SANDBOX.resolve()): # 14 还在围墙里吗？
        return f"拒绝：{path} 不在 sandbox 里"      # 15 被拒：返回一句话
    return full.read_text(encoding="utf-8")        # 16 成功：读出内容