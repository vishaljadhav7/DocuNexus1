from fastapi import APIRouter, UploadFile, File, status
from app.database import AsyncSessionDep
from app.services.document_processor import DocumentProcessor  
from app.api.dependencies import CurrentUserDep
from fastapi import HTTPException
from app.models.document import Document, ProcessingStatus

document_processor = DocumentProcessor()

document_router = APIRouter(prefix='/api/v1/document', tags=["Document"])


@document_router.post(
    "/upload",
    # response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Document is loaded and being processed."
    )
async def upload_file(
    db : AsyncSessionDep,
    user :  CurrentUserDep, 
    doc_file: UploadFile = File(...),
    # pinecone_service: PineconeService = Depends(get_pinecone_service)
):
    document = await document_processor.process_document(db=db, user=user, file=doc_file) 
    
    return document

    
@document_router.get(
    "/{document_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Get document processing status."
)
async def get_document_status(
    document_id: str,
    db: AsyncSessionDep,
    user: CurrentUserDep  # Optional: Ensure user owns the document
):
    document = await db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {
        "document_id": document.id,
        "status": document.processing_status,
        "error_message": document.error_message if document.processing_status == ProcessingStatus.FAILED.value else None
    }    