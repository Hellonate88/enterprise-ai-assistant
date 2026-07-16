from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from app.schemas.document import DocumentResponse
from app.services.document_service import create_document
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


UPLOAD_FOLDER = Path("app/storage")


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db = Depends(get_db)
):

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_FOLDER / file.filename


    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    create_document(db, filename=file.filename, filepath=str(file_path), status="uploaded")

    return {
        "filename": file.filename,
        "status": "uploaded"
    }