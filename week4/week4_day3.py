from pydantic import BaseModel, Field, field_validator, ValidationError

class RegisterForm(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=0, le=150)
    email: str

    @field_validator('username')
    @classmethod
    def no_spaces(cls, v):
        if ' ' in v:
            raise ValueError('用户名不能包含空格')
        return v

    @field_validator('email')
    @classmethod
    def must_have_at(cls, v):
        if '@' not in v:
            raise ValueError('邮箱必须包含 @')
        return v


def register(data: dict):
    """模拟处理一条注册请求"""
    try:
        form = RegisterForm.model_validate(data)     # 进门校验
        print("✅ 注册成功！入库数据：", form.model_dump())   # 出门打包
    except ValidationError as e:
        print("❌ 注册失败：")
        for err in e.errors():                        # 逐条打印错误
            print(f"   字段「{err['loc'][0]}」：{err['msg']}")


# ===== 模拟一批注册请求 =====
register({"username": "xiaoming", "age": 18, "email": "xm@example.com"})  # 正常
register({"username": "ab", "age": 18, "email": "a@b.com"})              # 用户名太短
register({"username": "xiao ming", "age": 18, "email": "a@b.com"})       # 含空格
register({"username": "xiaohong", "age": 200, "email": "bademail"})      # 年龄越界 + 邮箱无@