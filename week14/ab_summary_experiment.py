"""
摘要压缩 A/B 对比实验：本地脚本，不涉及 LangSmith experiment / dataset / evaluator。

版本 A：关闭 SummarizationMiddleware
版本 B：开启 SummarizationMiddleware（参数与 week13/rag_agent.py 保持一致）
A/B 除了这一个开关外，model / tools / system_prompt / checkpointer 配置完全相同。

用法（在 python-learning 根目录下执行，两次跑同一个文件、切换 --version）：
    python -m week14.ab_summary_experiment --version a
    python -m week14.ab_summary_experiment --version b

每次运行使用全新的 thread_id，20 轮问题在同一个 thread 内连续对话（checkpointer 保留历史，
没有历史就没有压缩可言）。结果按轮次落盘为 jsonl，一行一轮：
    turn / question / input_tokens / output_tokens / total_tokens / message_count / answer

脚本只如实记录 token 和答案原文，不判断答案对错、不算准确率。
"""
import argparse
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.sqlite import SqliteSaver

from week13.rag_tools import search_documents

SYSTEM_PROMPT = """你是一个文档助手。
1. 当用户询问知识库中的内容时，先用 search_documents 工具检索资料，再根据资料回答。
2. 只根据检索到的资料回答，不要编造。资料中没有的，明确说"资料中未找到相关信息"。
3. 闲聊或常识问题，可以直接回答，不必检索。"""

# 固定 20 轮对话，不要改
QUESTIONS = [
    "今天天气怎么样？",
    "我最近搬到杭州了，以后推荐餐厅按这个城市来。",
    "我养了一只猫叫豆豆，特别挑食。",
    "年假有几天？",
    "公司的薪酬结构包括哪些部分？",
    "年假当年没休完怎么办？",
    "公司的考勤打卡方式是什么？",
    "我漏打卡了怎么处理？",
    "那迟到呢？",
    "公司允许员工用AI工具写代码吗？",
    "我入职半年，能休年假吗？",
    "我今天迟到了45分钟，会怎么处理？",
    "员工请事假如何扣工资？",
    "AI Agent在工业制造领域有哪些落地案例？",
    "解释一下什么是向量数据库。",
    "Python里装饰器怎么用？",
    "什么是提示工程？",
    "我之前说我搬到哪了？我的猫叫什么名字？",
    "那你觉得杭州有哪些适合养猫的公园？",
    "谢谢",
]

DB_PATH = "week14/checkpoints_ab.db"
RESULT_DIR = Path("week14/ab_results")


def build_agent(enable_summary: bool, checkpointer):
    middleware = []
    if enable_summary:
        middleware.append(
            SummarizationMiddleware(
                model="deepseek:deepseek-chat",
                trigger=("tokens", 2000),
                keep=("messages", 4),
            )
        )
    return create_agent(
        model="deepseek:deepseek-chat",
        tools=[search_documents],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
        middleware=middleware,
    )


def run(version: str):
    enable_summary = version == "b"
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    agent = build_agent(enable_summary, checkpointer)

    # 每次运行开全新 thread，避免不同次运行的历史互相污染
    thread_id = f"ab-{version}-{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": thread_id}}

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = "summary_on" if enable_summary else "summary_off"
    out_path = RESULT_DIR / f"{version}_{tag}_{ts}.jsonl"

    with out_path.open("w", encoding="utf-8") as f:
        for i, q in enumerate(QUESTIONS, 1):
            result = agent.invoke({"messages": [{"role": "user", "content": q}]}, config)
            last = result["messages"][-1]
            usage = last.usage_metadata or {}
            record = {
                "turn": i,
                "question": q,
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "message_count": len(result["messages"]),
                "answer": last.content,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            print(
                f"[{i:02d}/20] in={record['input_tokens']} "
                f"out={record['output_tokens']} msgs={record['message_count']}"
            )

    conn.close()
    print(f"\n完成，version={version}（summary={'on' if enable_summary else 'off'}），"
          f"thread_id={thread_id}\n结果写入 {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", choices=["a", "b"], required=True,
        help="a = 关闭摘要压缩, b = 开启摘要压缩",
    )
    args = parser.parse_args()
    run(args.version)
