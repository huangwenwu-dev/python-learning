# mymath.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "错误: 除数不能为 0"
    
    if __name__ =="__main__":
        print("自测 divide(10, 0):", divide(10, 0))