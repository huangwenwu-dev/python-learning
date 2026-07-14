import numpy as np

Q = np.random.rand(3, 4)    # 准备 Q、K、V 三个矩阵
K = np.random.rand(3, 4)    # 这里的 (3, 4) 表示：3 个词，每个词用 4 个数字表示
V = np.random.rand(3, 4)
print(Q.shape)              # 查看 Q 的形状，应该是 (3, 4)

scores = Q @ K.T            # K.T 表示把 K 转置，从 (3, 4) 变成 (4, 3)
print(scores.shape)

e = np.exp(scores)          # np.exp 会对 scores 里的每个数字做指数运算
print(e)
row_sum = e.sum(axis=1, keepdims=True)      # axis=1 表示按行求和
print(row_sum)                              # keepdims=True 表示保留二维形状，方便后面做除法
print(row_sum.shape)
weights = e / row_sum                       # 用每个数除以它所在行的总和
print(weights.sum(axis=1))                  # 检查每一行是否加起来等于 1

output = weights @ V                        # 按百分比混合 V 里的信息
print(output.shape)