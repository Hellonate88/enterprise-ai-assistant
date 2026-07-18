from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    filename: str

    #filepath: str

    status: str

    created_at: datetime