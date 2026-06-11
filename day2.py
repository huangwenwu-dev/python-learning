name = "文"
age = 24
print(name)
print(age)


a = "你好"
b = 18
c = 3.14
d = True

print(type(a))
print(type(b))
print(type(c))
print(type(d))


name = "文"
age = 24
print(f"你好, {name}, 你今年{age}岁")


name = input("请输入你的名字")
print(f"你好, {name}")


name = input("请输入你的姓名")
age = input("请输入你的年龄")
nest_age = int(age) - 1
print(f"你好, {name}, 你去年{nest_age}岁")