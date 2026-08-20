import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from week11.rag import chunk_text, embed_text

load_dotenv()
deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

with open("week11/ai agent未来发展趋势.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text, chunk_size=500, overlap=50)

chroma_client = chromadb.PersistentClient(path="./week13/chroma_db")
collection = chroma_client.get_or_create_collection(name="my_docs")

ids = []
documents = []
embeddings = []
metadatas = []

for i, c in enumerate(chunks):
    ids.append(f"chunk_{i}")
    documents.append( c )
    embedding = embed_text(c)
    embeddings.append(embedding)
    metadatas.append({
        "chunk_index": i,
        "source": "ai_agent未来发展趋势.txt",
    })
print(f"共生成 {len(documents)} 个文本块")
print(f"第一个文本块内容: {documents[0][:100]}...")
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)
print(f"已写入，当前条数：{collection.count()}")