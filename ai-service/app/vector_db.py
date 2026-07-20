import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="industrial_knowledge"
)


def save_embedding(chunk_id, text, embedding):
    collection.add(
        ids=[str(chunk_id)],
        documents=[text],
        embeddings=[embedding]
    )


def search(query_embedding, top_k=8):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )