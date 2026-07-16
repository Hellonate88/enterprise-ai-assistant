from app.models.document import Document

def create_document(db, filename, filepath, status):
    document = Document(
        filename=filename,
        filepath=filepath,
        status=status
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document