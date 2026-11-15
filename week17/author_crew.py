from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Task   # type: ignore

load_dotenv()

llm = LLM(model="deepseek/deepseek-v4-pro")

writer = Agent(
    role="电商文案",
    goal="写出让人想下单的商品文案",
    backstory="做过3年淘宝详情页文案，说话口语化，不堆形容词",
    llm=llm,
)

write_task = Task(
    description=(
        "给一款法兰绒毛毯写一段商品文案，有 70×100、100×150、130×150、150×200、180×200 "
        "五个尺寸，卖点是可以机洗、不掉毛"
    ),
    expected_output="一段100字左右的中文文案，最后一句是促销语",
    agent=writer,
)

crew = Crew(agents=[writer], tasks=[write_task])

result = crew.kickoff()

print(result)
print(result.raw)
