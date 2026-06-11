class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print("汪汪!")                                   # 打印动作,不返回

    def info(self):
        return f"我叫{self.name},今年{self.age}岁,汪!"    # 返回字符串

# 创建并使用
dog1 = Dog("旺财", 3)
dog2 = Dog("小黑", 5)

dog1.bark()                  # 直接执行 → 汪汪!
print(dog1.info())           # info 返回字符串,要 print 才看得到 → 我叫旺财...
print(dog2.info())           # 我叫小黑...