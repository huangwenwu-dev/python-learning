class Student:
    def __init__(self, name, score):
        self.name = name           # 名字可以公开
        self.__score = score       # 分数私有,要保护

    def get_score(self):
        return self.__score

    def set_score(self, new_score):
        if 0 <= new_score <= 100:
            self.__score = new_score
            print(f"{self.name} 的分数已更新为 {new_score}")
        else:
            print(f"无效分数 {new_score},必须在 0-100 之间")


# 使用
stu = Student("小明", 85)
print(f"{stu.name} 的初始分数:{stu.get_score()}")   # 通过方法读

stu.set_score(92)        # 合法修改
stu.set_score(150)       # 非法,被拦
print(f"{stu.name} 的最终分数:{stu.get_score()}")   # 92,没被改坏