from models import User

user1 = User(name="小明", age=18)
user2 = User(name="小红", age=20)

print("===== 用户信息 =====")
print(f"{user1.name},{user1.age}岁")
print(f"{user2.name},{user2.age}岁")

user3 = User(name="老六", age="22")
print(f"{user3.name},{user3.age}岁(类型: {type(user3.age).__name__})")
