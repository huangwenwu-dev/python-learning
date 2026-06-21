class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 创建两只不同的狗
dog1 = Dog("旺财", 3)
dog2 = Dog("小黑", 5)

# 打印它们的属性
print(f"第一只狗:{dog1.name},{dog1.age}岁")
print(f"第二只狗:{dog2.name},{dog2.age}岁")