import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

messages = [
    {"role": "user", "content": "我叫小明"},
]
resp = client.chat.completions.create(model="deepseek-chat", messages=messages)
reply = resp.choices[0].message.content
print("第1轮:", reply)
print("tokens:", resp.usage.prompt_tokens)

messages.append({"role": "assistant", "content": reply})
messages.append({"role": "user", "content": "我叫什么？ "}) 

resp = client.chat.completions.create(model="deepseek-chat", messages=messages)
reply = resp.choices[0].message.content
print("第2轮:", reply)
print("tokens:", resp.usage.prompt_tokens)