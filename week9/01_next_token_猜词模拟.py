import random                   # 导入 random 模块，用来做随机选择
a = {"好": 0.3, "差": 0.25, "热": 0.25, "蓝": 0.2}

words = list(a.keys())          # 把字典里的键取出来，变成列表
probs = list(a.values())        # 把字典里的值取出来，变成列表

for i in range(20):     # 重复 20 次，每次按照上面的概率随机选出一个字并打印
    print(random.choices(words, weights=probs)[0])