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
        新内容 = input("请输入待办内容")
        新待办 = {"content":新内容, "done":False}
        todos.append(新待办)
        print("添加成功! ")
    elif choice == "3":
        for 序号, todo in enumerate(todos, start=1):
            print(序号, todo["content"])
        序号 = int(input("删第几个: "))
        todos.pop(序号 - 1)
        print("删除成功! ")
    elif choice == "4":
        print("退出")
        break
    else:
        print("无效输入")