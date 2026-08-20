import chromadb
from dotenv import load_dotenv
load_dotenv()
from week11.rag import embed_text

chroma_client = chromadb.PersistentClient(path="./week13/chroma_db")
collection = chroma_client.get_or_create_collection(name="my_docs")

question = "AI Agent 的市场规模有多大？"
q_vector = embed_text(question)

results = collection.query(
    query_embeddings=[q_vector],
    n_results=3,
    where={"source": "ai_agent未来发展趋势.txt"}
)
for id_, doc, dist in zip(
    results["ids"][0],
    results["documents"][0],
    results["distances"][0]
):
    print(f"{id_} | 距离 {dist:.4f} | {doc[:80]}...")