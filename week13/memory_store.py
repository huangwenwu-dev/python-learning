import json
import os

def save_memory(user_id, key, value):
    if os.path.exists("memories.json"):
        with open("memories.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data.setdefault(user_id, {})[key] = value
    with open("memories.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_memory(user_id):
    if os.path.exists("memories.json"):
        with open("memories.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    return data.get(user_id, {})

def format_profile(profile):
     if not profile:
        return ""
     return "\n".join(f"{k}: {v}" for k, v in profile.items())

def build_system_prompt(user_id):
    profile_text = format_profile(load_memory(user_id))
    if profile_text:
        system_prompt = f"你是助手。关于用户的已知信息：\n{profile_text}"
    else:
        system_prompt = "你是助手。"
    return system_prompt