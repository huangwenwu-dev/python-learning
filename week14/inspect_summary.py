from week14.ab_summary_experiment import build_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from dotenv import load_dotenv
load_dotenv()

DB_PATH = "week14/checkpoints_ab.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn)

agent = build_agent(True, checkpointer)
config = {"configurable": {"thread_id": "ab-b-83129792"}}
state = agent.get_state(config)
for m in state.values["messages"]:
    print("=" * 40)
    print(type(m).__name__)
    print(m.content)