import numpy as np

Q = np.random.rand(3, 4)
K = np.random.rand(3, 4)
V = np.random.rand(3, 4)
print(Q.shape)

scores = Q @ K.T
print(scores.shape)

e = np.exp(scores)
print(e)
row_sum = e.sum(axis=1, keepdims=True)
print(row_sum)
print(row_sum.shape)
weights = e / row_sum
print(weights.sum(axis=1))

output = weights @ V
print(output.shape)