# app/api/v1/document.py

from fastapi import APIRouter, UploadFile, File, status
from app.database import AsyncSessionDep
from app.services.document_processor import DocumentProcessor
from app.services.document_service import DocumentService
from app.api.dependencies import CurrentUserDep
from app.schemas.document import (
    DocumentListResponse,
    DocumentUploadResponse,
    DocumentStatusResponse,
    DocumentListItem,
    DocumentDeleteResponse
)
import logging

logger = logging.getLogger(__name__)

document_processor = DocumentProcessor()
document_service = DocumentService()

document_router = APIRouter(prefix='/api/v1/documents', tags=["Document"])


@document_router.post(
    "/",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and process document"
)
async def upload_file(
    db: AsyncSessionDep,
    user: CurrentUserDep,
    doc_file: UploadFile = File(..., description="PDF document to upload"),
):
    """
    Upload a PDF document for processing.

    """
    document = await document_processor.process_document(
        db=db,
        user=user,
        file=doc_file
    )
    return document


@document_router.get(
    "/{document_id}/status",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document processing status"
)
async def get_document_status(
    document_id: str,
    db: AsyncSessionDep,
    user: CurrentUserDep
):
    """Get the processing status of a document."""
    document = await document_service.get_user_document(
        user_id=user.id,
        document_id=document_id,
        db=db
    )
    
    return DocumentStatusResponse(
        document_id=document.id,
        processing_status=document.processing_status,
        error_message=document.error_message
    )


@document_router.get(
    "/{document_id}",
    response_model=DocumentListItem,
    status_code=status.HTTP_200_OK,
    summary="Get document details"
)
async def get_document(
    document_id: str,
    user: CurrentUserDep,
    db: AsyncSessionDep
):
    """Retrieve details of a specific document."""
    return await document_service.get_user_document(
        user_id=user.id,
        document_id=document_id,
        db=db
    )


@document_router.get(
    "/",
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all user documents"
)
async def get_documents(
    user: CurrentUserDep,
    db: AsyncSessionDep
):
    """Retrieve all documents belonging to the authenticated user."""
    logger.info(f"User {user.id} fetching documents")
    
    return await document_service.get_user_documents(
        user_id=user.id,
        db=db
    )


@document_router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a document"
)
async def delete_document(
    document_id: str,
    user: CurrentUserDep,
    db: AsyncSessionDep
):
    """Delete a document and all associated data."""
    await document_service.delete_user_document(
        user_id=user.id,
        document_id=document_id,
        db=db
    )
    
    return DocumentDeleteResponse(
        message=f"Document deleted successfully",
        document_id=document_id
    )