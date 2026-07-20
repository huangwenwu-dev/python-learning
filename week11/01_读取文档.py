with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:
    text = f.read()
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + 500]
        chunks.append(chunk)
        start = start + 450
    print(len(chunks))

for i, c in enumerate(chunks):
    print(f"--- 块{i+1}({len(c)}字）---")
    print(c[:50])
print(chunks[0][-50:])
print(chunks[1][:50])