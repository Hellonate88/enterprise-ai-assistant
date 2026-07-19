from datetime import datetime
from sqlalchemy import Enum as SQLEnum
from app.models.document_status import DocumentStatus
from sqlalchemy.orm import DeclarativeBase
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

    created_at = Column(DateTime, default=datetime.utcnow)