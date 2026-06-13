def greet(name, greeting="你好"):
    return f"{greeting},{name}!"

print(greet("小明"))            # 没填 greeting → 用默认"你好" → 你好,小明!
print(greet("小红", "早上好"))   # 填了 → 用新的 → 早上好,小红!


def introduce(name, age, city):
    return f"{name},{age}岁,来自{city}"

# 普通(按位置):必须记住顺序
print(introduce("小明", 18, "北京"))

# 关键字(按名字):顺序随便,看得也明白
print(introduce(age=18, city="上海", name="小红"))


def min_max(numbers):
    return min(numbers), max(numbers)   # 同时返回最小和最大

low, high = min_max([3, 1, 9, 5])       # 用两个变量分别接住
print("最小:", low)    # 1
print("最大:", high)   # 9


count = 0

def add_one():
    global count    # 声明:我要改的是外面那个 count
    count += 1

add_one()
print(count)   # 1


def calc(a, b, op="+"):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:                     # 防呆:除数不能为 0
            return "错误:除数不能为 0"
        return a / b
    else:
        return f"不支持的运算符:{op}"

print(calc(6, 3))            # 没填 op → 默认 + → 9
print(calc(6, 3, "-"))       # 按位置传 → 3
print(calc(6, 3, op="*"))    # 关键字参数 → 18
print(calc(6, 0, "/"))       # 防呆 → 错误:除数不能为 0
print(calc(6, 3, "%"))       # 不支持 → 提示