from langchain.agents import create_agent
from my_tools import get_time, get_weather
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

load_dotenv()

class WeatherReport(BaseModel):
    """天气查询的结构化结果。"""
    city: str = Field(description="城市名")
    temperature: int = Field(description="温度(摄氏度)")
    condition: str = Field(description="天气状况, 如晴、雨")
    suggestion: str = Field(description="出行建议, 如打车、走路")

class ChatReply(BaseModel):
    """普通聊天回答, 用于不需要查询天气情况。"""
    reply: str = Field(description="普通聊天回复")

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_time, get_weather],
    response_format=ToolStrategy(WeatherReport | ChatReply),
    system_prompt="""你是一个时间和天气的查询助手。
    当用户询问时间或天气时，调相应的工具。
    当用户问其他问题是直接回答，不调工具。"""
)

while True:
    user_input = input("\n你: ")
    if user_input.strip() == "quit":
        print("再见")
        break 
    if not user_input.strip():
        continue
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        sr = result.get("structured_response")

        if isinstance(sr, WeatherReport):
            print(f"【{sr.city}】{sr.condition}, {sr.temperature}°C")
            print(f"建议：{sr.suggestion}")

        elif isinstance(sr, ChatReply):
            print(sr.reply)

        else:
            print("未获取到有效回复")
    except Exception as e:
        print(f"出错了: {e}")