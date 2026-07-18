import json
import os                                           #  导入 + 加载 .env
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

class PersonInfo(BaseModel):
    name:str
    age:int = Field(ge=0, le=150)

def ask_llm(prompt):
    messages = [
        {"role": "system", "content": "你是信息提取器,只输出 JSON 本身,不要任何解释、不要 ```json 代码块。}"},
        {"role": "user", "content": f"从这句话提取姓名、年龄、城市,按此格式输出{{\"name\": \"姓名\", \"age\": 年龄数字}}"
        f"name 是字符串,age 是整数。如果没提到年龄,age 填 null。句子:{prompt}"}
    ]
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=messages,
                temperature=0
            )
            result = response.choices[0].message.content
            data = json.loads(result)
            person = PersonInfo.model_validate(data)
            return person
        except json.JSONDecodeError as e:
            print(f"第{i+1}次失败(JSON不合法): {e}")
        except ValidationError as e:
            print(f"第{i+1}次失败(字段不对): {e}")
        except Exception as e:
            print(f"第{i+1}次失败(其他): {e}")
    print("读取失败")
    return None

sentences = [
    "李雷今年25岁, 住在上海",           # 标准款
    "我叫张伟，三十岁了",                # 年龄是中文数字
    "韩梅梅在广州开了家咖啡店",          # 没有年龄
    "王芳，芳龄二八",                    # 需要推理（二八=16？28？）
    "赵四今年零岁",                      # 边界值 0
    "刘能活了152年",                     # 超出上限 150
    "今天天气不错",                      # 根本没有人
]
for s in sentences:
    person = ask_llm(s)
    if person:
        print(f"✅ {person.name} - {person.age}")
    else:
        print(f"❌ 这句没搞定：{s}")