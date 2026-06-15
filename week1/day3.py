shopping_list = ["苹果", "香蕉", "香梨", "桃子"]
new_item = input("要加什么到清单? ")
shopping_list.append(new_item)
remove_item = input("要删除清单里的哪一项? ")
shopping_list.remove(remove_item)
print("你的购物清单是: ")
for item in shopping_list:
    print("-", item)