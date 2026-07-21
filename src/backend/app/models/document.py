from datetime import datetime
from sqlalchemy import Enum as SQLEnum
from app.models.document_status import DocumentStatus
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    filepath = Column(String)

    status = Column(
        SQLEnum(DocumentStatus), #Database-level validation
        nullable=False,
        default=DocumentStatus.UPLOADED
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan" #当删除 Document 时：相关 Chunk 自动删除
    )
    text = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)