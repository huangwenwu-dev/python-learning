import numpy as np

a = np.array([[1, 2],
              [3, 4]])
b = np.array([[5, 6],
              [7, 8]])
print(a * b)                # 逐元素称
print(a @ b)                # 矩阵乘法

c = np.array([1, 2, 3])
d = np.array([4, 5, 6])
print(np.dot(c, d))          # 向量点积(神经网络里的加权求和)
print(c @ d)

e = np.array([[1, 2, 3],
              [4, 5, 6]])
f = np.array([[1, 2],
              [3, 4],
              [5, 6]])
print(e @ f)                  # 矩阵乘法的形状规则(中间要相等)
print((e @ f).shape)

g = np.array([[1, 2, 3],
              [4, 5, 6]])
h = np.array([[6, 5, 4],
              [3, 2, 1]])
print(h.T)                     # 转置救场
print(g @ h.T)