from datetime import datetime

时间字符串 = datetime.now().strftime("%Y-%m-%d %H:%M")
内容 = input("请输入今天的日志: ")

with open("log.txt", "a", encoding='utf8') as f:
    f.write(时间字符串 + " " + 内容 + "\n")
