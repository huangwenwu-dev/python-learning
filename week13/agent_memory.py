from memory_store import save_memory, load_memory, build_system_prompt
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

def create_user_agent(user_id):
    return create_agent(
        model="deepseek:deepseek-chat",
        tools=[],
        checkpointer=InMemorySaver(),
        system_prompt=build_system_prompt(user_id)
    )

save_memory("u003", "天气", "今天好热")
print(build_system_prompt("u003"))