# mymath.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    if b == 0:
        return "错误：除数不能为 0"
    return a / b

if __name__ == "__main__":
    # 自测区:只在直接运行 mymath.py 时执行
    print("自测 add:", add(2, 3))
    print("自测 divide:", divide(10, 0))