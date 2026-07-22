import os
import json
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()  # 读取 .env 到环境变量
deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")  # 初始化客户端

with open("week11/week11_index.json", "r", encoding="utf-8") as f:  # 打开索引文件
    index = json.load(f)  # 解析为 list

def cosine_similarity(a, b):  # 余弦相似度函数
    a = np.array(a)  # 转数组
    b = np.array(b)  # 转数组
    分子 = np.dot(a, b)  # 点积
    模a = np.sqrt(np.sum(a**2))  # a的模长
    模b = np.sqrt(np.sum(b**2))  # b的模长
    分母 = 模a * 模b  # 模长相乘
    if 分母 == 0:  # 防止除零
        return 0
    cos = 分子 / 分母  # 余弦值
    return cos

def embed_text(text):  # 文本转向量函数
    response = client.embeddings.create(  # 调用向量接口
        model="text-embedding-v3",  # 指定模型
        input=text  # 输入文本
    )
    return response.data[0].embedding  # 取出向量

def search(query, top_k=3):  # 检索：返回和问题最相关的 top_k 段文本
    问题向量 = embed_text(query)  # 把问题也转成向量，才能和索引里的向量比较
    结果 = []  # 存 (相似度, 原文) 对
    for 块 in index:  # 遍历索引里每一段已切分的文本
        分数 = cosine_similarity(问题向量, 块["vector"])  # 问题向量 与 该段向量 的相似度
        结果.append((分数, 块["text"]))  # 记录分数和对应原文
    top = sorted(结果, reverse=True)[:top_k]  # 按分数从高到低排序，取前 top_k 个
    return [文本 for 分数, 文本 in top]  # 只返回文本，分数不需要带出去

def build_prompt(query, chunks):  # 把检索到的资料和问题拼成一段完整的提示词
    context = "\n".join(chunks)  # 多段资料用换行拼接成一段上下文
    prompt = f"""你是知识问答助手，请只根据下面提供的资料回答问题。
如果资料内容不足以回答这个问题，就直接说"根据现有资料，我无法回答这个问题"，不要编造。
    【资料】:
    {context}
    【问题】:
    {query}"""
    return prompt

def ask(query):  # RAG 主流程：检索 -> 拼提示词 -> 调用大模型
    chunks = search(query)  # 第一步：检索相关资料
    prompt = build_prompt(query, chunks)  # 第二步：把资料和问题拼成提示词
    answer = call_llm(prompt)  # 第三步：把提示词交给大模型生成回答
    return answer

def call_llm(prompt):  # 调用 DeepSeek 对话接口，返回生成的文本
    messages = [
        {"role": "user", "content": prompt}  # 只有一条用户消息，没有历史对话
    ]
    response = deepseek_client.chat.completions.create(
        model="deepseek-v4-flash",  # 使用的对话模型
        messages=messages,
        temperature=0  # 0 表示尽量确定性输出，减少随机发挥
    )
    return response.choices[0].message.content  # 取出模型回复的文本内容

print("=== 走 RAG(带资料) ===")
print(ask("AI Agent 有哪些发展趋势?"))  # 带检索资料再回答，对比效果

print("=== 直接问(不带资料) ===")
print(call_llm("AI Agent 有哪些发展趋势?"))  # 不带资料，直接问大模型，用来对照 RAG 的效果