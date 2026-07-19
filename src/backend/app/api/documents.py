from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pathlib import Path
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
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

    # create_document(db, filename=file.filename, filepath=str(file_path), status="uploaded")

    # return {
    #     "filename": file.filename,
    #     "status": "uploaded"
    # }


    service = DocumentService(db)

    document = service.upload_document(
        filename=file.filename,
        filepath=str(file_path)
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "created_at": document.created_at
    }

@router.get("/all", response_model=list[DocumentResponse])
def get_all_documents(db = Depends(get_db)):
    service = DocumentService(db)

    documents = service.get_all_documents()

    return documents

@router.delete("/{document_id}")
def delete_document(document_id: int, db = Depends(get_db)):
    service = DocumentService(db)

    service.delete_document(document_id)

    return {
        "message": f"Document with ID {document_id} has been deleted."
    }

@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: int,
    db = Depends(get_db)
):

    service = DocumentService(db)

    try:
        return service.get_document(document_id)

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
@router.put("/{document_id}/processing")
def set_processing(
    document_id: int,
    db = Depends(get_db)
):

    service = DocumentService(db)

    document = service.mark_processing(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@router.put("/{document_id}/ready")
def set_ready(
    document_id: int,
    db = Depends(get_db)
):

    service = DocumentService(db)

    document = service.mark_ready(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@router.put("/{document_id}/failed")
def set_failed(
    document_id: int,
    db = Depends(get_db)
):

    service = DocumentService(db)

    document = service.mark_failed(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document