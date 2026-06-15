answer = 42       # 固定答案（第七天会改成随机生成）

while True:                              # 一直循环，直到 break
    guess = int(input("猜一个数字（1-100）："))
    if guess == answer:
        print("🎉 猜对了！")
        break                            # 猜对，跳出循环结束游戏
    elif guess < answer:
        print("太小了，再大一点")
    else:
        print("太大了，再小一点")