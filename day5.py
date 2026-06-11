score = int(input("请输入分数(0~100): "))

if score < 0 or score > 100:
    print("分数无效，请输入 0 到 100 之间")
else:
    if score >= 90:
        print("优")
    elif score >= 75:
        print("良")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")