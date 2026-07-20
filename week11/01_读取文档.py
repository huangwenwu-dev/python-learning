def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start = start + chunk_size - overlap
    return chunks

with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:
    text = f.read()
chunks = chunk_text(text, 500, 50)
print(len(chunks))
for i, c in enumerate(chunks):
    print(f"--- 块{i+1}({len(c)}字）---")
    print(c[:50])