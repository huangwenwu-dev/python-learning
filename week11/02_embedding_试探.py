import json            # 用来把结果存成 json 文件、读回来
import os            # 用来读取系统环境变量（API Key）
from dotenv import load_dotenv            # 从 .env 文件加载环境变量
from openai import OpenAI            # 阿里云百炼兼容 OpenAI 接口，所以用官方 openai 库调用

load_dotenv()            # 读取项目根目录下的 .env 文件，把里面的变量写进环境变量
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")            # 创建客户端：key不写死在代码里，从环境变量取；base_url指向百炼的兼容模式接口

response = client.embeddings.create(            # 调用向量化接口，把一段文本转成一串数字（向量）
    model="text-embedding-v3",            # 指定用哪个向量模型
    input="今天天气真好"            # 要转成向量的文本
)
print(response)            # 打印完整返回结果，看看接口返回的数据结构长什么样

vector = response.data[0].embedding            # 取出返回结果里的向量本体（一个浮点数列表）
print(len(vector))            # 打印向量的维度，确认模型输出的向量长度

index = [{"text": "今天天气真好", "vector": vector, "index": 0},]            # 组装一条记录：原文、向量、编号，为后面批量存多条做准备
with open("week11/week11_index.json", "w", encoding='utf8') as f:            # 以写入模式打开json文件，utf8编码保证中文正常写入
    json.dump(index, f, ensure_ascii=False)            # 写入json；ensure_ascii=False让中文直接存成汉字，而不是被转义成\uXXXX
