import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

messages = [
    {"role": "system", "content": "你是一个只回答'正面'或'负面'的情感分类器。}"},
    {"role": "user", "content": "这家餐厅的菜好精致, 适合拍照。"}
]

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=messages
)

print(response.choices[0].message.content)