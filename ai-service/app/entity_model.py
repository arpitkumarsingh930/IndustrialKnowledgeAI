from sqlalchemy import Column, Integer, BigInteger, String, Text
from app.database import Base


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(BigInteger)

    chunk_index = Column(Integer)

    entity_text = Column(Text)

    entity_label = Column(String(100))
class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(BigInteger)

    chunk_index = Column(Integer)

    source_entity = Column(String)

    relation = Column(String)

    target_entity = Column(String)