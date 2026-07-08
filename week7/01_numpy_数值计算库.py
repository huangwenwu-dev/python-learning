import numpy as np

arr = np.array([1, 2, 3, 4])    # ===== 任务1：创建一维和二维数组 =====
print(arr)
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(arr2d)

a = np.arange(0, 10, 2)    # ===== 任务2：四种快速创建方式 =====
print(a)
b = np.zeros(4)
print(b)
c = np.ones((3, 4))
print(c)
d = np.linspace(0, 10, 5)
print(d)

arr = np.array([1, 2, 3, 4])    # ===== 任务3：数组 vs 列表，对比 *3 的区别（今日重点）=====
result = arr * 3
print("数组*3:", result)
nums = [1, 2, 3, 4]
print("列表*3:", nums * 3)


e = np.array([1, 2, 3, 4])     # ===== 任务4：两个数组的逐元素 + 和 * =====
f = np.array([10, 20, 30, 40])
print(e * f)
print(e + f)