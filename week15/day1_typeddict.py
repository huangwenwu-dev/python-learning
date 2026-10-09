from typing import TypedDict
from pydantic import BaseModel

class State(TypedDict):
    city: str
    weather: str

s: State = {"city": 123}
print(s)

class StateP(BaseModel):
    city: str
    weather: str

p = StateP(city = 123)
print(p)
