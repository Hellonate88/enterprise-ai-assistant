from app.core.database import engine
from app.models.document import Base

Base.metadata.create_all(bind=engine)