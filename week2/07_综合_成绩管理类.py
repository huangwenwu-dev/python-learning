class Student:
    def __init__(self, name):
        self.name = name
        self.__scores = []

    def add_score(self, score):
        if 0 <= score <= 100:
            self.__scores.append(score)
        else:
            print(f"无效分数 {score}，未添加")

    def get_scores(self):
        return self.__scores

    def average(self):
        if len(self.__scores) == 0:
            return 0
        return sum(self.__scores) / len(self.__scores)

    def highest(self):
        if len(self.__scores) == 0:
            return None
        return max(self.__scores)

stu = Student("小明")
for s in [85, 92, 78, 88]:
    stu.add_score(s)
stu.add_score(200)

print(f"学生姓名:{stu.name}")
print(f"各科成绩:{stu.get_scores()}")
print(f"平均分:{stu.average():.1f}")
print(f"最高分:{stu.highest()}")


students = [Student("小明"), Student("小红")]
students[0].add_score(90)
students[1].add_score(85)
for stu in students:
    print(f"{stu.name} 平均分:{stu.average():.1f}")