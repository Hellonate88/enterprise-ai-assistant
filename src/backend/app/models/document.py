from datetime import datetime

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

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)