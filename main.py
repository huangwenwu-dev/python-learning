import mymath

print("===== 简易计算器(用自定义模块)=====")
a = int(input("第一个数："))
b = int(input("第二个数："))

print("加：", mymath.add(a, b))
print("减：", mymath.subtract(a, b))
print("除：", mymath.divide(a, b))