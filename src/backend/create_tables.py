from app.core.database import engine
from app.models.document import Base
from app.models.document_chunk import DocumentChunk

Base.metadata.create_all(bind=engine)