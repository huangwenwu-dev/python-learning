with open("test.txt", encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())
