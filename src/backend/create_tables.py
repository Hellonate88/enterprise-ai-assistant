from sqlalchemy import inspect, text

from app.core.database import engine
from app.models.document import Base
from app.models.document_chunk import DocumentChunk
from app.models.chunk_embedding import ChunkEmbedding

Base.metadata.create_all(bind=engine)

document_columns = {
    column["name"] for column in inspect(engine).get_columns("documents")
}

if "text" not in document_columns:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE documents ADD COLUMN text VARCHAR"))