import numpy as np

arr = np.arange(6)
print(arr.shape)
arr2 = arr.reshape(2, 3)        # reshape 改变形状
print(arr2)
print(arr2.shape)
print(arr2.T)
arr3 = arr.reshape(3, 2)
print(arr3)
print(arr3.shape)

arr4 = np.arange(12)
print(arr4.reshape(4, -1))      # 自动推断维度
print(arr4.reshape(-1, 2))

arr5 = np.array([[1, 2, 3],      # flatten 拉平
                 [4, 5, 6]])
print(arr5.flatten())

arr6 = np.array([[1, 2, 3],       # T 转置（行列互换） 
                 [4, 5, 6]])
print(arr6.T)