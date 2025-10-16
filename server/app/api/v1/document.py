from fastapi import APIRouter, UploadFile, File, status
from app.database import AsyncSessionDep
from app.services.document_processor import DocumentProcessor  
from app.services.document_service import DocumentService
from app.api.dependencies import CurrentUserDep
from fastapi import HTTPException
from app.models.document import ProcessingStatus
from app.schemas.document import DocumentListResponse, DocumentUploadResponse, DocumentStatusResponse, DocumentListItem, DocumentDeleteResponse
import logging

logger = logging.getLogger(__name__)


document_processor = DocumentProcessor()
document_service = DocumentService()

document_router = APIRouter(prefix='/api/v1/documents', tags=["Document"])


@document_router.post(
    "/",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Document is loaded and being processed."
    )
async def upload_file(
    db : AsyncSessionDep,
    user :  CurrentUserDep, 
    doc_file: UploadFile = File(..., description="PDF document to upload"),
    # pinecone_service: PineconeService = Depends(get_pinecone_service)
):
    document = await document_processor.process_document(db=db, user=user, file=doc_file) 
    
    return document

    
@document_router.get(
    "/{document_id}/status",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document processing status."
)
async def get_document_status(
    document_id: str,
    db: AsyncSessionDep,
    user: CurrentUserDep 
):
    
    document = await document_service.get_user_document(
        user_id=user.id,
        document_id=document_id,
        db=db
    )
    

    return DocumentStatusResponse(
        document_id=document.id,
        status=document.processing_status,
        error_message = document.error_message if document.processing_status == ProcessingStatus.FAILED.value else None
    )


@document_router.get(
    "/{document_id}",
    response_model=DocumentListItem,
    status_code=status.HTTP_200_OK,
    summary="Fetch user document."
    )
async def delete_document(
    document_id: str,
    user: CurrentUserDep = None, 
    db: AsyncSessionDep = None 
):
    
    document = await document_service.get_user_document(user_id=user.id, document_id=document_id, db=db)
    return document
    

@document_router.get(
    "/",
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch all user documents."
    )
async def get_documents(
    user: CurrentUserDep, 
    db: AsyncSessionDep
):
    logger.info(f"User {user.id} fetching documents")
    
    # Get documents
    documents = await document_service.get_user_documents(
        user_id=user.id,
        db=db
    )
    
    return documents
    
    
@document_router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse
    )
async def delete_document(
    document_id: str,
    user: CurrentUserDep = None, 
    db: AsyncSessionDep = None 
):
    
    await document_service.delete_user_document(
    user_id=user.id,
    document_id=document_id,
    db=db)
    
    return DocumentDeleteResponse(
        message=f"Document {document_id} deleted successfully",
        document_id=document_id
    )
