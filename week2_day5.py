class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 正在吃东西")

    def sound(self):
        print("发出某种声音...")


class Cat(Animal):                  # Cat 继承 Animal
    def __init__(self, name, breed):
        super().__init__(name)      # 继承父类的初始化
        self.breed = breed          # 加自己的属性

    def sound(self):                # 重写父类的 sound
        print(f"{self.name}（{self.breed}）：喵喵~")


# 使用
cat = Cat("咪咪", "橘猫")
cat.eat()       # 继承自父类 → 咪咪 正在吃东西
cat.sound()     # 重写后的 → 咪咪（橘猫）：喵喵~

class Dog(Animal):
    def sound(self):
        print(f"{self.name}：汪汪!")

animals = [Cat("咪咪", "橘猫"), Dog("旺财")]
for a in animals:
    a.eat()       # 大家都会吃(继承)
    a.sound()     # 但各叫各的(重写)