todos = [{"content":"买菜", "done":True}, {"content":"做饭", "done":False}, {"content":"洗碗", "done":False}]

while True:
    print("1.查看全部", "2.添加", "3.删除", "4.退出")
    choice = input("用户输入的数字")
    if choice == "1":
        print("---待办清单---")
        for todo in todos:
            内容 = todo["content"]
            状态 = todo["done"]
            if 状态:
                状态文字 = "✅ 已完成"
            else:
                状态文字 = "⬜ 未完成"
            print(内容, 状态文字)
    elif choice == "2":
        print("添加")
    elif choice == "3":
        print("删除")
    elif choice == "4":
        print("退出")
        break
    else:
        print("无效输入")