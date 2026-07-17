import os                                           #  导入 + 加载 .env
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()                                       #  读取 .env 文件,把 Key 加载进环境变量

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")         #  创建客户端(Key 从环境变量读,不写在代码里!)

messages = [                                                                                        # 组织 messages
    {"role": "system", "content": "你是一个只回答'正面'或'负面'的情感分类器。}"},
    {"role": "user", "content": "这家餐厅的菜好精致, 适合拍照。"}
]

response = client.chat.completions.create(        #  发出请求
    model="deepseek-v4-flash",
    messages=messages
)

print(response.choices[0].message.content)        # 5取出并打印回复