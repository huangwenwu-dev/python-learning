import os  # 系统与环境变量
import json  # 读写 json
import numpy as np  # 向量运算
from dotenv import load_dotenv  # 加载 .env
from openai import OpenAI  # SDK 客户端

load_dotenv()  # 读取 .env 到环境变量
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")  # 初始化客户端

with open("week11/week11_index.json", "r", encoding="utf-8") as f:  # 打开索引文件
    index = json.load(f)  # 解析为 list

print(type(index[0]["text"]))  # 看第一条 text 类型
print(len(index))  # 看总条数
print(index[0]["text"][:5])  # 看第一条前5字

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

问题 = "AI Agent 有哪些发展趋势？"  # 查询问题
问题向量 = embed_text(问题)  # 问题转向量
print(type(问题向量))  # 看向量类型
print(len(问题向量))  # 看向量维度

结果 = []  # 存放(分数,文本)
for 块 in index:  # 遍历每个文本块
    分数 = cosine_similarity(问题向量, 块["vector"])  # 算相似度
    结果.append((分数, 块["text"]))  # 记录结果

top3 = sorted(结果, reverse=True)[:3]  # 分数最高3个
print("---- Top 3 ----")
for 分数, 文字 in top3:  # 逐个打印
    print(f"{分数:.3f}  {文字[:50]}")

bottom3 = sorted(结果)[:3]  # 分数最低3个
print("---- Bottom 3 ----")
for 分数, 文字 in bottom3:  # 逐个打印
    print(f"{分数:.3f}  {文字[:50]}")
