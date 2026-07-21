from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.document import Base

class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)

    char_count = Column(Integer, nullable=False)

    document = relationship("Document", back_populates="chunks")