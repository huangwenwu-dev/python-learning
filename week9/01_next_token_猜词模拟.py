import random
a = {"好": 0.3, "差": 0.25, "热": 0.25, "蓝": 0.2}

words = list(a.keys())
probs = list(a.values())

for i in range(20):
    print(random.choices(words, weights=probs)[0])