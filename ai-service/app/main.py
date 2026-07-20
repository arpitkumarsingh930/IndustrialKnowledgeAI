from app.database import SessionLocal
from app.models import DocumentChunk, Entity, Relationship
from app.entity_extractor import extract_entities, extract_relationships
from app.neo4j_service import save_entity, save_relationship
from app.embedder import get_embedding
from app.vector_db import save_embedding

db = SessionLocal()

chunks = db.query(DocumentChunk).all()

print(f"Found {len(chunks)} chunks")

for chunk in chunks:

    print("\nProcessing Chunk:", chunk.chunk_index)

    # Generate embedding
    embedding = get_embedding(chunk.chunk_text)

    # Save embedding to ChromaDB
    save_embedding(
        chunk.id,
        chunk.chunk_text,
        embedding
    )

    print(f"Embedding saved for chunk {chunk.chunk_index}")

    # Extract entities and relationships
    entities = extract_entities(chunk.chunk_text)
    relationships = extract_relationships(chunk.chunk_text)

    # Save entities
    for e in entities:

        print(e)

        entity = Entity(
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
            entity_text=e["text"],
            entity_label=e["label"]
        )

        db.add(entity)

        save_entity(
            e["text"],
            e["label"]
        )

    # Save relationships
    for rel in relationships:

        relationship = Relationship(
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
            source_entity=rel["source"],
            relation=rel["relation"],
            target_entity=rel["target"]
        )

        db.add(relationship)

        save_relationship(
            rel["source"],
            rel["relation"],
            rel["target"]
        )

db.commit()

print("\nAll entities, relationships, and embeddings saved successfully!")