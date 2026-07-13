import tiktoken         # 导入 tiktoken，用来把文字切成 token

enc = tiktoken.get_encoding("cl100k_base")      # 选择一种分词规则

print(enc.encode("今天天气真好"))   # 把中文句子切成 token，并打印 token 编号列表
a = enc.encode("今天天气真好")
for i in a:                 # 逐个查看每个 token 编号对应的原始文字片段
    print(i, enc.decode([i]) )
print(enc.decode([30320, 242]))     # 把指定 token 编号还原成文字

print(enc.encode("The weather is nice today"))  # 把英文句子切成 token，并打印 token 编号列表
b = enc.encode("The weather is nice today")
for i in b:                 # 逐个查看每个英文 token 对应的文字片段
    print(i, enc.decode([i]) )

print(enc.encode("饕鬄"))       # 把复杂中文词切成 token，并打印编号列表
c = enc.encode("饕鬄")
for i in c:
    print(i, enc.decode([i]))

print(enc.encode("unbelievable"))   # 把英文单词切成 token，并打印编号列表
d = enc.encode("unbelievable")
for i in d:
    print(i, enc.decode([i]))
print(len(a), len(b), len(c), len(d))   # 分别打印四段文字被切成了多少个 token