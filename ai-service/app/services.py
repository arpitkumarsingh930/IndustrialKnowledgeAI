from app.embedder import get_embedding
from app.vector_db import save_embedding
from app.entity_extractor import extract_entities, extract_relationships
from app.neo4j_service import save_entity, save_relationship


def process_document(document_id: int, chunks: list[str]):

    for index, chunk in enumerate(chunks):

        # Generate embedding
        embedding = get_embedding(chunk)

        # Save to ChromaDB
        chunk_id = f"{document_id}_{index}"
        save_embedding(chunk_id, chunk, embedding)

        # Extract entities
        entities = extract_entities(chunk)

        for entity in entities:
            save_entity(
                entity["text"],
                entity["label"]
            )

        # Extract relationships
        relationships = extract_relationships(chunk)

        for relation in relationships:
            save_relationship(
                relation["source"],
                relation["relation"],
                relation["target"]
            )