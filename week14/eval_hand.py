import io, contextlib
from week14.hand_rag import load_index, ask

index = load_index("week14/w14_index.json")

def handwritten_rag(inputs: dict) -> dict:
    question = inputs["question"]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        答案 = ask(question, index)
    return {"answer": 答案, "retrieved": buf.getvalue()}

if __name__ == "__main__":
    print(handwritten_rag({"question": "公司允许员工用AI工具写代码吗？"}))