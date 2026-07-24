# LangChain 1.x 最小示例：init_chat_model + messages 列表 + invoke，无老 API
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()  # 读取 .env 里的 DEEPSEEK_API_KEY
model = init_chat_model("deepseek:deepseek-v4-pro", temperature=0)

# 单轮对话，不带历史记忆
messages = [
    SystemMessage("你是一个AI回答助手, 每次回答不超过一句话"),
    HumanMessage("langchain是什么"),
]
response = model.invoke(messages)  # 返回 AIMessage 对象
print(response.content)