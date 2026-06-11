import random

answer = random.randint(1, 100)
count = 0

while True:
    user_input = input("猜一个数字(1-100): ")

    if not user_input.isdigit():        # 不是纯数字
        print("请输入数字哦~")
        continue                        # 跳过这一圈，重新问

    guess = int(user_input)
    count += 1

    if guess < 1 or guess > 100:        # 第五天的逻辑运算，范围防呆
        print("请输入 1 到 100 之间的数")
        continue

    if guess == answer:
        print(f"🎉 猜对了！你一共猜了 {count} 次")
        break
    elif guess < answer:
        print("太小了，往大猜")
    else:
        print("太大了，往小猜")