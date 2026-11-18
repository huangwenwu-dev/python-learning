from save_tool import save_copy

filenames = [
    "test.txt",
    "../hack.txt",
    "../../hack.txt",
    r"C:\Users\Public\hack.txt",
    "sub/../test2.txt",
]

for idx, filename in enumerate(filenames, start=1):
    result = save_copy.run(filename=filename, content="攻击测试")
    print(f"{idx} {filename} -> {result}")
