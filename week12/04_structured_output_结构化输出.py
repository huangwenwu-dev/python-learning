from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from dotenv import load_dotenv
from my_tools import get_weather

load_dotenv()

class WeatherReport(BaseModel):
    """天气查询的结构化结果。"""
    city: str = Field(description="城市名")
    temperature: int = Field(description="温度(摄氏度)")
    condition: str = Field(description="天气状况, 如晴、雨")
    suggestion: str = Field(description="出行建议, 如打车、走路")

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_weather],
    response_format=ToolStrategy(WeatherReport)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "北京现在天气怎么样? "}]
})
report = result["structured_response"]
print(report.city, report.temperature)
print(type(report))