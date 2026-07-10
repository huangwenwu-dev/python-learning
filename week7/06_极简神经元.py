import numpy as np

a = np.array([[1, 3, 7],
              [2, 5, 8],
              [3, 6, 9]])
b = np.array([2, 5, 8])
c = a @ b
print(c)
print(c.shape)
d = 0.5
print(d)
print(c + d)