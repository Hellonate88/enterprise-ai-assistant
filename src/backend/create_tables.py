from app.core.database import engine
from app.models.document import Base
from app.models.document_chunk import DocumentChunk
from app.models.chunk_embedding import ChunkEmbedding

Base.metadata.create_all(bind=engine)