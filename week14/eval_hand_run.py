from week14.eval_agent import code_rule, llm_judge   # 复用两个评判器
from langsmith import evaluate
from week14.eval_hand import handwritten_rag

def run_hand(inputs: dict) -> dict:
    question = inputs["input"]
    if isinstance(question, list):
        question = question[-1]
    result = handwritten_rag({"question": question})
    return {"answer": result["answer"]}

if __name__ == "__main__":
    evaluate(
        run_hand,
        data="rag_eval_v1",
        evaluators=[code_rule, llm_judge],
        experiment_prefix="handwritten-v1",
        max_concurrency=1,
    )