from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class User(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=0, le=150)
    email: Optional[str] = None
    vip: bool = False

u1 = User(name="小明", age=18, email="xiaoming.com")
print("✅ u1 创建成功", u1.model_dump())

bad_cases = [
    {"name": "小明", "age": 200},
    {"name": "", "age": 18},
    {"name": "小红", "age": "abc"},
]
for case in bad_cases:
    try:
        User(**case)
        print("意外通过了:", case)
    except ValidationError as e:
        print(f"❌ 拦下 {case} —— {e.error_count()} 个错误")