import os
import json
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()  # 读取 .env 到环境变量
deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")  # 用于生成回答（LLM）
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")  # 用于文本向量化（Embedding）


# ========== 准备阶段：切分文本 → 向量化 → 建索引/存取索引 ==========

def chunk_text(text, chunk_size, overlap):
    # 按固定长度 + 重叠切分文本，避免语义在切分边界被截断
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start = start + chunk_size - overlap  # 下一块从"当前块末尾-重叠"处开始
    return chunks

def embed_text(text):
    # 调用向量模型，把一段文本转成一个高维向量
    response = client.embeddings.create(
        model="text-embedding-v3",
        input=text
    )
    return response.data[0].embedding

def build_index(chunks):
    # 给每个文本块生成向量，组装成可检索的索引列表
    index = []
    for i, c in enumerate(chunks):
        vector = embed_text(c)
        index.append({"text": c, "vector": vector, "index": i})
    return index

def save_index(index, path):
    # 索引落盘为 JSON，避免每次运行重复调用 embedding 接口
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)

def load_index(path):
    # 从磁盘读回索引
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ========== 问答阶段：检索相似块 → 拼 Prompt → 调 LLM 生成回答 ==========

def cosine_similarity(a, b):
    # 余弦相似度：衡量两个向量方向的接近程度，值越大越相似
    a = np.array(a)
    b = np.array(b)
    分子 = np.dot(a, b)
    模a = np.sqrt(np.sum(a**2))
    模b = np.sqrt(np.sum(b**2))
    分母 = 模a * 模b
    if 分母 == 0:
        return 0
    cos = 分子 / 分母
    return cos

def search(query, index, top_k=3):
    # 把问题向量化，和索引里每个块比相似度，取分数最高的 top_k 个块
    问题向量 = embed_text(query)
    结果 = []
    for 块 in index:
        分数 = cosine_similarity(问题向量, 块["vector"])
        结果.append((分数, 块["text"]))
    top = sorted(结果, reverse=True)[:top_k]
    return [文本 for 分数, 文本 in top]

def build_prompt(query, chunks):
    # 把检索到的资料和用户问题拼成给 LLM 的提示词，并约束"资料不足就说不知道"，减少编造
    context = "\n".join(chunks)
    prompt = f"""你是知识问答助手，请只根据下面提供的资料回答问题。
如果资料内容不足以回答这个问题，就直接说"根据现有资料，我无法回答这个问题"，不要编造。
    【资料】:
    {context}
    【问题】:
    {query}"""
    return prompt

def call_llm(prompt):
    # 调用 LLM，temperature=0 让回答更稳定、少发散
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = deepseek_client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def ask(query, index):
    # 问答阶段的完整流程：检索 -> 打印命中块（便于调试）-> 拼 Prompt -> 生成回答
    chunks = search(query, index)
    print("---检索到的块---")
    for i, c in enumerate(chunks):
        print(f"[块{i}] {c[:200]}")
    prompt = build_prompt(query, chunks)
    answer = call_llm(prompt)
    return answer


# ========== 主流程：索引存在则加载，否则新建；循环接收用户提问 ==========

def main():
    path = "week11/week11_index.json"
    if os.path.exists(path):
        # 索引已存在：直接加载，跳过重复的 embedding 调用
        index = load_index(path)
        print("索引已存在, 直接加载")
    else:
        # 索引不存在：读原文 -> 切块 -> 向量化建索引 -> 保存
        with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text, 500, 50)
        index = build_index(chunks)
        save_index(index, path)
        print("索引不存在, 新建并已保存")
    while True:
        a = input("用户提出问题")
        if a == "退出":
            break
        答案 = ask(a, index)
        print(答案)
main()
