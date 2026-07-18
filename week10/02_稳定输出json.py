import json
import os                                           #  导入 + 加载 .env
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()                                       #  读取 .env 文件,把 Key 加载进环境变量

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")         #  创建客户端(Key 从环境变量读,不写在代码里!)

sentences = ["李雷今年25岁,住在上海。", "韩梅梅住在广州。", "在深圳工作的张伟,今年30。"]
for 句子 in sentences:
    messages = [                                                                                        # 组织 messages
        {"role": "system", "content": "你是信息提取器,只输出 JSON 本身,不要任何解释、不要 ```json 代码块。}"},
        {"role": "user", "content": f"从这句话提取姓名、年龄、城市,按此格式输出{{\"name\": \"姓名\", \"age\": 年龄数字}}"
        f"name 是字符串,age 是整数。如果没提到年龄,age 填 null。句子:{句子}"}
    ]

    response = client.chat.completions.create(        #  发出请求
        model="deepseek-v4-flash",
        messages=messages,
        temperature=0
    )

    result = response.choices[0].message.content
    data = json.loads(result)
    print(data["name"], data["age"])