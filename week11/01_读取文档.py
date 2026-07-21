# 固定长度切分+重叠：硬切断会把一句话拆到两块，检索时哪块都拿不到完整语义
def chunk_text(text, chunk_size, overlap):   # 定义函数：传入原文、每块字数、重叠字数
    chunks = []      # 存放切好的所有块
    start = 0    # 当前块的起始下标，从文本开头开始
    while start < len(text):     # 起点还没走出文本末尾，就继续切
        chunk = text[start:start + chunk_size]    # 从 start 开始截取 chunk_size 个字符，得到一块
        chunks.append(chunk)     # 把这一块存进结果列表
        start = start + chunk_size - overlap     # 起点前移：走一整块的距离，再退回 overlap，形成重叠
    return chunks    # 返回切好的所有块

with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:    # 以只读、utf-8编码打开文件
    text = f.read()      # 把文件全部内容读成一个字符串

chunks = chunk_text(text, 500, 50)   # 调用函数：每块500字，相邻块重叠50字
print(len(chunks))   # 打印总共切出多少块
for i, c in enumerate(chunks):   # 遍历每一块，i是序号（从0开始），c是块内容
    print(f"--- 块{i+1}({len(c)}字）---")   # 打印块的编号（从1开始）和这块的字数
    print(c[:50])    # 打印这块的前50个字，看看内容大概是什么