import os            # 读取环境变量（API Key）
import json            # 把索引结果存成json、写文件
from dotenv import load_dotenv            # 加载 .env 文件里的环境变量
from openai import OpenAI            # 阿里云百炼兼容 OpenAI 接口，用官方 openai 库调用

load_dotenv()            # 读取 .env，把 DASHSCOPE_API_KEY 等变量写进环境变量
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")            # 创建客户端，key不写死，从环境变量取

def chunk_text(text, chunk_size, overlap):            # 把长文本切成固定长度、带重叠的小块
    chunks = []            # 存放切好的所有块
    start = 0            # 当前块的起始下标
    while start < len(text):            # 起点没走出文本末尾就继续切
        chunk = text[start:start + chunk_size]            # 从start截取chunk_size个字符
        chunks.append(chunk)            # 存进结果列表
        start = start + chunk_size - overlap            # 前移起点，退回overlap，制造重叠
    return chunks            # 返回所有块

def embed_text(text):            # 把一段文本转成向量
    response = client.embeddings.create(            # 调用向量化接口
        model="text-embedding-v3",            # 指定向量模型
        input=text            # 待转换的文本
    )
    return response.data[0].embedding            # 只取出向量本体返回，调用者不用关心接口返回的其它字段

def build_index(chunks):            # 把所有文本块批量转成向量，组装成索引
    index = []            # 存放每一块对应的记录
    for i, c in enumerate(chunks):            # 遍历每一块，i是编号，c是块内容
        vector = embed_text(c)            # 把这一块转成向量
        index.append({"text": c, "vector": vector, "index": i})            # 记录原文、向量、编号三样，后面检索既要算相似度(vector)又要能定位取回原文(text/index)
    return index            # 返回完整索引

with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:            # 只读打开原文档，utf-8编码
    text = f.read()            # 读成一个字符串

chunks = chunk_text(text, 500, 50)            # 切分：每块500字，重叠50字
index = build_index(chunks)            # 把每块都向量化，组装成索引列表

with open("week11/week11_index.json", "w", encoding="utf8") as f:            # 写入模式打开json文件
    json.dump(index, f, ensure_ascii=False)            # 写入索引；ensure_ascii=False让中文直接存汉字，不转义

print(f"共 {len(chunks)} 块,索引已保存")            # 打印切块数量，确认流程跑完
