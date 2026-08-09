from langchain.agents import create_agent
from my_tools import get_time, get_weather
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-v4-pro",
    tools=[get_time, get_weather],
    system_prompt="你是一个能查询天气和时间的助手"
)
result = agent.invoke({
    "messages":[{"role":"user", "content":"现在江西热还是北京热？"}]
})
print(result["messages"][-1].content)

inputs = {"messages": [{"role": "user", "content": "北京现在几点了? "}]}
for chunk in agent.stream(inputs, stream_mode="updates"):
    print(chunk)
    print("---")