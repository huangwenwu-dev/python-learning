from typing import Literal
from pydantic import BaseModel, Field, field_validator
from langchain.tools import tool
from datetime import datetime

# 用 BaseModel 显式定义参数 schema：docstring 和 Field(description=...) 都是写给 LLM 看的，
# 决定它「要不要调用这个工具」「该传什么参数」，不是写给人看的注释
class GetWeatherInput(BaseModel):
    """查询指定城市当前天气的参数。
    适用场景：用户询问某个城市"现在天气怎么样""今天多少度""要不要带伞"等问题。
    不适用场景：查询未来天气预报（本工具只返回当前时刻的模拟天气，不支持多天预报）。
    """
    city: str = Field(
        ...,
        description="要查询天气的城市名称，例如'北京'、'上海'、'广州'，需使用中文城市名"
    )
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="返回的温度单位，只能是 'celsius'（摄氏度）或 'fahrenheit'（华氏度），不接受其他取值"
    )

    @field_validator("units", mode="before")
    @classmethod
    def normalize_units(cls, v): 
        对照表 = {"摄氏度": "celsius", "华氏度": "fahrenheit"}
        return 对照表.get(v, v)

# args_schema 关联上面定义的参数模型，函数签名可以简单写，真正的约束和说明看 schema
@tool(args_schema=GetWeatherInput)
def get_weather(city: str, units: Literal["celsius", "fahrenheit"] = "celsius") -> str:
    """查询指定城市的当前天气（模拟数据，非真实 API 调用）。
    适用于用户询问某个城市当前天气状况或气温的场景。
    不支持多天天气预报，只返回当前模拟天气。
    """
    try:
        # mock 数据：城市 -> 摄氏度温度 + 天气状况
        mock_db = {
            "北京": {"temp_c": 28, "condition": "晴"},
            "上海": {"temp_c": 31, "condition": "多云"},
            "广州": {"temp_c": 33, "condition": "雷阵雨"},
        }

        if city not in mock_db:
            return f"错误：暂不支持查询城市'{city}'的天气，当前仅支持：{list(mock_db.keys())}"
        info = mock_db[city]
        temp_c = info["temp_c"]
        if units == "fahrenheit":
            temp = temp_c * 9 / 5 + 32
            unit_label = "°F"
        else:
            temp = temp_c
            unit_label = "°C"
        return f"{city}当前天气：{info['condition']}，温度 {temp}{unit_label}"
    except Exception as e:
        # 捕获所有异常，返回错误说明字符串而不是抛出，避免中断 agent 的执行流程
        return f"查询天气时出错：{str(e)}"

# 没写 args_schema：@tool 会根据函数签名 + 类型注解自动生成参数 schema
# （city 目前没用到，是简化版实现，实时时间不依赖城市）
@tool
def get_time(city: str) -> str:
    """查询指定城市的当前时间, 返回实时准确时间。
    适用于用户询问"现在几点了""今天多少号"等问题。
    只查当前时刻,不做日期计算"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp
if __name__ == "__main__":
    print(get_time.invoke({"city": "北京"}))

    # 以下几行是在看 @tool 自动生成了什么：工具名、描述（取自 docstring）、
    # 参数模型对象、以及该模型对应的 JSON Schema（LLM 最终看到的就是这份 schema）
    print(get_time.name)
    print(get_time.description)
    print(get_time.args_schema)
    print(get_time.args_schema.model_json_schema())

    # invoke 手动调用工具做测试；注意 units 传了非法值 "摄氏度"，
    # 不在 Literal 允许范围内，用来验证 pydantic 的校验是否生效
    print(get_weather.invoke({"city": "北京", "units": "摄氏度"}))