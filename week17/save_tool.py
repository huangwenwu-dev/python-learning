from pathlib import Path

from crewai.tools import tool   # type: ignore

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


@tool("save_copy")
def save_copy(filename: str, content: str) -> str:
    """把终稿文本保存到 week17/output 文件夹，仅供编辑定稿后存档使用。

    参数：
    filename —— 要保存的文件名，例如 cup.txt；
    content —— 要保存的终稿全文。

    文件名拼出的真实路径必须落在 output 文件夹内部（不能等于 output 本身，
    也不能借助 ../ 或绝对路径跑到外面），否则会拒绝保存并说明原因，不会报错。
    若 output 文件夹不存在会自动创建；若文件已存在则直接覆盖。
    """
    target = OUTPUT_DIR / filename
    resolved = target.resolve()
    output_root = OUTPUT_DIR.resolve()

    if resolved == output_root or not resolved.is_relative_to(output_root):
        return (
            f"拒绝保存：文件名「{filename}」解析后的路径是 {resolved}，"
            f"它不在 output 文件夹（{output_root}）内部，或者就是 output 文件夹本身，"
            "出于安全考虑禁止写入。"
        )

    try:
        output_root.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
    except OSError as e:
        return f"拒绝保存：写入文件时出现错误（{e}）。"

    return f"已保存到{resolved}，共{len(content)}字"
