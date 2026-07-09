import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])    # 看数组属性
print(arr.shape)
print(arr.ndim)
print(arr.dtype)
print(arr.size)

arr = np.array([10, 20, 30, 40, 50])    # 一维索引切片
print(arr[0])
print(arr[2])
print(arr[4])

arr = np.array([[1, 2, 3],      # 二维索引切片
                [4, 5, 6],
                [7, 8, 9]])
print(arr[0, 0])
print(arr[2, 2])
print(arr[0, :]) # 第0行全部列
print(arr[:, 0]) # 全部行第0列


arr = np.array([10, 25, 30, 5, 40])    # 布尔索引
print(arr[(arr > 10) & (arr < 40)])

arr = np.array([20, 40, 60, 80, 100])   # 花式索引
print(arr[[0, 2, 4]])