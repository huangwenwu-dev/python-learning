import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    check_embedding_ctx_length=False,
)

vector_store = Chroma(
    collection_name="my_docs",
    embedding_function=embeddings,
    persist_directory="./week13/chroma_db",
)
def search(query, source=None, k=3):
    kwargs = {"k": k}
    if source:
        kwargs["filter"] = {"source": source}
    retriever = vector_store.as_retriever(search_kwargs=kwargs)
    docs = retriever.invoke(query)
    if not docs:
        print("没有找到相关内容")
        return
    return docs
if __name__ == "__main__":
    search("年假怎么算")
    search("年假怎么算", source="ai agent未来发展趋势.txt")
    search("年假怎么算", source="电商运营资料.txt")