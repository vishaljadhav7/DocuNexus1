from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import Settings
from app.services.cloudinary_service import CloudinaryService
from pathlib import Path
from app.core.exceptions import FileUploadError, DocumentProcessingError
from app.models.document import Document, ProcessingStatus
from app.tasks.document_tasks import process_document_task

import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Main document processing orchestrator"""
    
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.settings = Settings()
    
    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file.filename:
            raise FileUploadError("No filename provided")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.pdf']:
            raise FileUploadError(
                f"Unsupported file type: {file_ext}. "
                # f"Supported types: {', '.join(self.settings.allowed_file_types)}"
            )
        
        # Check file size (if available)
        if hasattr(file, 'size') and file.size and file.size > 1024 * 1024 * 1:
            # max_size_mb = self.settings.max_file_size / (1024 * 1024)
            raise FileUploadError(f"File too large. Maximum size: {1024 * 1024 * 1}MB")
    
    async def process_document(
        self,
        file: UploadFile,
        user: dict,
        db: AsyncSession
        # pinecone_service : PineconeService
    ) -> Document:
        """Process uploaded document"""
        
        try:
            # Validate file
            self._validate_file(file)
            
            # Read file content
            file_content = await file.read()
            
            # Validate actual file size
            if len(file_content) > 1024 * 1024 * 2:
                # max_size_mb = self.settings.max_file_size / (1024 * 1024)
                raise FileUploadError(f"File too large. Maximum size: {1024 * 1024 * 2}MB")
            
            logger.info(f"Processing document upload: {file.filename} ({len(file_content)} bytes)")
            
            # Upload to Cloudinary
            cloudinary_result = await self.cloudinary_service.upload_pdf(
                file_content,
                file.filename,
                user.id
            )
            
            document = Document(
                user_id=user.id,
                filename=Path(file.filename).stem,
                cloudinary_url=cloudinary_result['url'],
                cloudinary_public_id=cloudinary_result['public_id'],
                file_size=cloudinary_result['size']
            )
            
            db.add(document)
            await db.commit()
            await db.refresh(document)
            
            # Get ID AFTER commit and refresh
            document_id = document.id
            
            logger.info(f"Document ID: {document_id}")
                        
            logger.info(f"Before process_document_task.delay: {document_id}")
            task = process_document_task.delay(str(document_id))
            
            return {
                "document_id": document_id,
                "filename": document.filename,
                "cloudinary_url": document.cloudinary_url,
                "status": ProcessingStatus.PROCESSING.value,
                "task_id": task.id,
                "message": "Document uploaded successfully. Processing in background."
            }
        except FileUploadError:
            raise 
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")
            raise DocumentProcessingError(f"Failed to process document: {str(e)}")