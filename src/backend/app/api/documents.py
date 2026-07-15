from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.schemas.document import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


UPLOAD_FOLDER = Path("app/storage")


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...)
):

    file_path = UPLOAD_FOLDER / file.filename


    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )


    return {
        "filename": file.filename,
        "status": "uploaded"
    }