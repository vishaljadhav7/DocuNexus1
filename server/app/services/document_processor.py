# app/services/document_processor.py

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import Settings
from app.services.cloudinary_service import CloudinaryService
from app.repositories.document_repository import DocumentRepository
from pathlib import Path
from app.core.exceptions import (
    FileUploadError,
    DocumentProcessingError,
    UnsupportedFileTypeError,
    FileTooLargeError
)
from app.models.document import Document, ProcessingStatus
from app.tasks.document_tasks import process_document_task
from app.schemas.document import DocumentUploadResponse
import logging
    
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Document processing orchestrator"""
    
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.document_repo = DocumentRepository()
        self.settings = Settings()
        self.max_file_size_mb = 10  # Configure as needed
    
    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file - raises domain exceptions"""
        if not file.filename:
            raise FileUploadError("No filename provided")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        supported_types = ['.pdf']
        
        if file_ext not in supported_types:
            raise UnsupportedFileTypeError(file_ext, supported_types)
        
        # Check file size if available
        if hasattr(file, 'size') and file.size:
            max_bytes = self.max_file_size_mb * 1024 * 1024
            if file.size > max_bytes:
                raise FileTooLargeError(self.max_file_size_mb)
    
    async def process_document(
        self,
        file: UploadFile,
        user: dict,
        db: AsyncSession
    ) -> DocumentUploadResponse:
        """
        Process uploaded document
        
        Raises domain exceptions that are handled by global middleware
        """
        # Validate file
        self._validate_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Validate actual file size
        max_bytes = self.max_file_size_mb * 1024 * 1024
        if len(file_content) > max_bytes:
            raise FileTooLargeError(self.max_file_size_mb)
        
        logger.info(f"Processing document: {file.filename} ({len(file_content)} bytes)")
        
        try:
            # Upload to Cloudinary
            cloudinary_result = await self.cloudinary_service.upload_pdf(
                file_content,
                file.filename,
                user.id
            )
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {str(e)}")
            raise DocumentProcessingError(
                "Failed to upload document to cloud storage",
                details={"error": str(e)}
            )
        
        # Create document record
        document = Document(
            user_id=user.id,
            filename=Path(file.filename).stem,
            cloudinary_url=cloudinary_result['url'],
            cloudinary_public_id=cloudinary_result['public_id'],
            file_size=cloudinary_result['size']
        )
        
        # Save to database via repository
        document = await self.document_repo.create(document, db)
        
        logger.info(f"Document created: {document.id}")
        
        # Queue background processing
        try:
            task = process_document_task.delay(str(document.id))
            logger.info(f"Queued processing task: {task.id}")
        except Exception as e:
            logger.error(f"Failed to queue task: {str(e)}")
            # Don't fail the upload, document is saved
        
        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            cloudinary_url=document.cloudinary_url,
            processing_status=ProcessingStatus.PROCESSING,
            created_at=document.created_at,
            insights_available=document.insights_available,
            message="Document uploaded successfully. Processing in background."
        )