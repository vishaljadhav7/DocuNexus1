from app.database import AsyncSession 
from app.models.document import Document
from typing import List, Optional
from sqlalchemy import delete, select, func
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DocumentNotFoundError, RAGException
from app.schemas.document import DocumentListResponse, DocumentListItem
from app.models.document import ProcessingStatus
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Service layer for document operations"""
    
    
    @staticmethod
    async def get_user_documents(user_id: str, db: AsyncSession) -> List[Document]:

        try:
            stmt = select(Document).where(
                Document.user_id == user_id
            ).order_by(Document.created_at.desc())
            
            result = await db.execute(stmt)
            documents = result.scalars().all()
            
            document_items = []
            for doc in documents:
                status_value = doc.processing_status
                if hasattr(status_value, 'value'):
                    status_value = status_value.value
                    
                    document_items.append(
                        DocumentListItem(
                            id=doc.id,
                            filename=doc.filename,
                            user_id=doc.user_id,
                            file_size=doc.file_size,
                            cloudinary_public_id=doc.cloudinary_public_id,
                            cloudinary_url=doc.cloudinary_url,
                            processing_status=ProcessingStatus(status_value),
                            created_at=doc.created_at,
                            updated_at=doc.updated_at,
                            insights=doc.insights,
                            insights_available=doc.insights_available,
                        )
                    )
    
            return DocumentListResponse(
                documents=document_items,
                total=len(document_items)
            )       
            
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching documents for user {user_id}: {str(e)}")
            raise RAGException(detail="Failed to retrieve documents")
    
    
    @staticmethod
    async def get_user_document(
        user_id: str, 
        document_id: str, 
        db: AsyncSession
    ) -> DocumentListItem:   
        try:
            stmt = select(Document).where(
                Document.user_id == user_id,
                Document.id == document_id
            )
            
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()
            
            if document is None:
                raise DocumentNotFoundError(document_id=document_id)
            
            return DocumentListItem(
                id = document.id,
                filename=document.filename,
                user_id=document.user_id,
                file_size=document.file_size,
                cloudinary_url=document.cloudinary_url,
                cloudinary_public_id=document.cloudinary_public_id,
                created_at=document.created_at,
                updated_at=document.updated_at,
                processing_status=document.processing_status,
                insights_available = document.insights_available,
                insights=document.insights
            )
            
        except DocumentNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching document {document_id}: {str(e)}")
            raise RAGException(detail="Failed to retrieve document")
    
    
    @staticmethod
    async def delete_user_document(
        user_id: str, 
        document_id: str, 
        db: AsyncSession
    ) -> bool:

        try:
            # First verify the document exists and belongs to the user
            stmt = select(Document).where(
                Document.id == document_id,
                Document.user_id == user_id
            )
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()
            
            if document is None:
                raise DocumentNotFoundError(document_id=document_id)
            
            # Perform the deletion
            delete_stmt = delete(Document).where(
                Document.id == document_id,
                Document.user_id == user_id
            )
            
            await db.execute(delete_stmt)
            await db.commit()
            
            logger.info(f"Document {document_id} deleted successfully for user {user_id}")
            return True
            
        except DocumentNotFoundError:
            await db.rollback()
            raise
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error deleting document {document_id}: {str(e)}")
            raise RAGException(detail="Failed to delete document")
    
    
    @staticmethod
    async def get_user_documents_count(user_id: str, db: AsyncSession) -> int:
        try:
            stmt = select(func.count(Document.id)).where(
                Document.user_id == user_id
            )
            result = await db.execute(stmt)
            count = result.scalar_one()
            
            return count
            
        except SQLAlchemyError as e:
            logger.error(f"Database error counting documents for user {user_id}: {str(e)}")
            raise RAGException(detail="Failed to count documents")
    
    
    @staticmethod
    async def update_document_status(
        document_id: str,
        status: str,
        error_message: Optional[str],
        db: AsyncSession
    ) -> Document:

        try:
            stmt = select(Document).where(Document.id == document_id)
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()
            
            if document is None:
                raise DocumentNotFoundError(document_id=document_id)
            
            document.processing_status = status
            if error_message:
                document.error_message = error_message
            
            await db.commit()
            await db.refresh(document)
            
            return document
            
        except DocumentNotFoundError:
            await db.rollback()
            raise
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error updating document {document_id}: {str(e)}")
            raise RAGException(detail="Failed to update document status")