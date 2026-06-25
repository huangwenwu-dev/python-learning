import json

Person = {"name":"老王", "颜色":"红色", "偏好设置":{"字体大小":15}, "开启通知":"True"}

with open("config.json", "w", encoding='utf8') as f:
    json.dump(Person, f, ensure_ascii=False, indent=2)

with open("config.json", "r", encoding='utf8') as f:
    data = json.load(f)
    print(data["偏好设置"]["字体大小"])