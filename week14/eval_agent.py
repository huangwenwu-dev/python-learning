"""
用 LangSmith evaluate() 在 dataset "rag_eval_v1" 上跑 Agent。

evaluator A: code_rule   —— 只判 id in (1, 4, 9)，规则式打分，其余题 return None（不打分）。
evaluator B: llm_judge   —— deepseek-chat 结构化输出打分，语义 + 数字双重核对。

运行方式（在 python-learning 根目录下）：
    python -m week14.eval_agent
"""
import re
import uuid
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
from langsmith import evaluate
from langsmith.schemas import Example

from week13.rag_agent import agent


# ---------- target: 跑 Agent ----------

def run_agent(inputs: dict) -> dict:
    question = inputs["input"]
    turns = question if isinstance(question, list) else [question]

    thread_id = f"eval-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    result = None
    for turn in turns:
        result = agent.invoke({"messages": [{"role": "user", "content": turn}]}, config)

    return {"answer": result["messages"][-1].content}


# ---------- evaluator A: code_rule ----------

def code_rule(outputs: dict, reference_outputs: dict, example: Example) -> Optional[dict]:
    metadata = example.metadata or {}
    qid = metadata.get("id")
    if qid not in (1, 4, 9):
        # 当前 langsmith SDK 不接受 evaluator 返回 None（会报 ValueError），
        # 用空的 EvaluationResults 表示"这条不打这个分"，不会写入 feedback。
        return {"results": []}

    answer = outputs.get("answer", "")

    if qid == 1:
        hit = re.search(r"(5|10|15)\s*天", answer) is not None
        score = 0 if hit else 1
        comment = "回答中出现了5/10/15天等具体天数，疑似幻觉" if hit else "未出现具体天数，符合预期"
        return {"key": "code_rule", "score": score, "comment": comment}

    if qid == 4:
        hit = "钉钉" in answer
        return {
            "key": "code_rule",
            "score": 1 if hit else 0,
            "comment": "提到了钉钉" if hit else "未提到钉钉",
        }

    if qid == 9:
        keywords = ("未找到", "未明确规定", "没有相关规定")
        hit = any(k in answer for k in keywords)
        return {
            "key": "code_rule",
            "score": 1 if hit else 0,
            "comment": "明确声明手册未规定" if hit else "未声明缺失，疑似编造",
        }


# ---------- evaluator B: llm_judge ----------

class JudgeResult(BaseModel):
    score: int = Field(description="0 或 1，1 表示回答正确，0 表示回答错误")
    reason: str = Field(description="打分理由，简要说明依据")


_judge_llm = ChatDeepSeek(model="deepseek-chat", temperature=0).with_structured_output(
    JudgeResult
)

JUDGE_PROMPT = """你是一名严格的答案评审员。给定用户问题、AI 助手的回答、以及参考答案，请判断助手回答是否正确。

判断标准（两项都要检查，任意一项不满足就判错）：
1. 语义是否正确回答了用户问题，含义要与参考答案一致（不要求逐字相同，允许改写）。
2. 数字核对：如果助手回答中出现了具体数字（天数、金额、比例、时长、倍数等），必须与参考答案中的数字逐一核对；只要出现了参考答案中没有的数字，或者数字与参考答案不一致，就判为错误（score=0），即使语义大体正确也不能算对。
{note_section}

请给出 score(0 或 1) 和简要 reason。

【用户问题】
{question}

【参考答案】
{reference_answer}

【助手回答】
{answer}
"""


def llm_judge(inputs: dict, outputs: dict, reference_outputs: dict, example: Example) -> dict:
    metadata = example.metadata or {}
    note = metadata.get("note", "")
    note_section = f"3. 本题额外判卷要求(如有,优先于上述通用标准):{note}" if note else ""
    question = inputs.get("input", "")
    if isinstance(question, list):
        question = "\n".join(question)
    answer = outputs.get("answer", "")
    reference_answer = reference_outputs.get("reference_answer", "")

    prompt = JUDGE_PROMPT.format(
        question=question, reference_answer=reference_answer, answer=answer, note_section=note_section
    )
    result: JudgeResult = _judge_llm.invoke(prompt)
    return {"key": "llm_judge", "score": result.score, "comment": result.reason}


if __name__ == "__main__":
    evaluate(
        run_agent,
        data="rag_eval_v1",
        evaluators=[code_rule, llm_judge],
        experiment_prefix="rag-eval-v2-note",
        max_concurrency=1,  # agent 共用一个 sqlite checkpointer 连接，不并发更安全
    )