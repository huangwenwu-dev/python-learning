import json

person = {"name":"老王", "age":18, "爱好":["打麻将", "抽烟", "打扑克"]}
b = json.dumps(person, ensure_ascii=False)
c = json.loads(b)
print(c["爱好"])