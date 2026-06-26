import json

Person = {"name":"小明", "age":18, "from":"江西"}

try:
    with open("config.json", encoding='utf8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = Person
    with open("config.json", "w", encoding='utf8') as f:
        json.dump(Person, f, ensure_ascii=False)
except json.JSONDecodeError:
    print("友好提示, 文件格式坏了")
    config = Person
print(config)