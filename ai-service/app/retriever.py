from app.embedder import get_embedding
from app.vector_db import search

def retrieve(query):

    embedding = get_embedding(query)

    results = search(embedding)

    return results