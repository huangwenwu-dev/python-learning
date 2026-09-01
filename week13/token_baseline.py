from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

def create_user_agent(user_id):
    return create_agent(
        model="deepseek:deepseek-chat",
        tools=[],
        checkpointer=InMemorySaver(),
    )

questions = [
    "今天天气怎么样？",
    "对了，我养了一只叫花花的猫。",
    "花花特别爱吃三文鱼。",
    "你读过《三体》吗？",
    "给我讲个笑话吧。",
    "Python和Java哪个更适合做AI？",
    "我昨天去了一个很有意思的展览。",
    "推荐一本关于历史的书。",
    "什么是量子计算？",
    "你觉得AI会取代程序员吗？",
    "我想学弹吉他，有什么建议？",
    "最近有什么好看的电影？",
    "你平时怎么处理长上下文？",
    "我中午吃了披萨。",
    "你了解RAG吗？",
    "从北京到上海坐高铁多久？",
    "我昨天跑步了5公里。",
    "比特币现在什么价格？",
    "周末有什么好去处？",
    "我的猫叫什么名字？",
]

agent = create_user_agent("test") 
config = {"configurable": {"thread_id": "test_thread"}}
for i, q in enumerate(questions, 1):
    result = agent.invoke(
        {"messages": [("user", q)]},
        config=config
    )
    last = result["messages"][-1]
    print(last.usage_metadata)

result = agent.invoke(
    {"messages": [("user", "我的猫叫什么名字？它爱吃什么？")]},
    config=config
)
print(result["messages"][-1].content)