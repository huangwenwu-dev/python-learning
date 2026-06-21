import mymath

print("===== 安全计算器 =====")
try:
    a = int(input("第一个数："))
    b = int(input("第二个数："))
    print("加：", mymath.add(a, b))
    print("减：", mymath.subtract(a, b))
    print("除：", mymath.divide(a, b))
except ValueError:
    print("❌ 请输入数字, 不要输入字母和符号!")