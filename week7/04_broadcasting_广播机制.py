import numpy as np

a = np.array([1, 2, 3])         # 逐元素运算
b = np.array([10, 20, 30])
print(a + b)
print(b - a)
print(a * b)
print(b / a)
print(a ** 2)

arr = np.array([1, 2, 3, 4])    # 数组与标量运算
print(arr + 10)
print(arr * 2)
print(arr - 1)

matrix = np.array([[1, 2, 3],   # 广播机制
                   [4, 5, 6]])
row = np.array([10, 20, 30])
print(matrix + row)

