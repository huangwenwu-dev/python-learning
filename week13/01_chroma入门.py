import chromadb
client = chromadb.PersistentClient(path="./week13/chroma_db")
collection = client.get_or_create_collection(name="my_docs")