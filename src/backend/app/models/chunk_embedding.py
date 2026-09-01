from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.document import Base

class ChunkEmbedding(Base):

    __tablename__ = "chunk_embeddings"

    id = Column(Integer, primary_key=True)

    chunk_id = Column(
        Integer,
        ForeignKey("document_chunks.id"),
        nullable=False,
        unique=True
    )

    model = Column(String, nullable=False)

    vector_json = Column(JSON, nullable=False)

    dimension = Column(Integer, nullable=False)

    chunk = relationship(
        "DocumentChunk",
        back_populates="embedding"
    )