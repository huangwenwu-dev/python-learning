def greet(name):
    return f"你好,{name}!"

user_name = input("请输入你的名字:")   # 输入
result = greet(user_name)              # 处理(交给函数)
print(result)                          # 输出