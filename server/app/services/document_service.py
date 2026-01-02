from app.database import AsyncSession
from app.models.document import Document, ProcessingStatus
from app.repositories.document_repository import DocumentRepository, DocumentChunkRepository
from app.schemas.document import DocumentListResponse, DocumentListItem
from app.schemas.query import ChunkSummaryDTO
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
   
class DocumentService:
    """Business logic for document operations"""
    
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.chunk_repo = DocumentChunkRepository()
    
    async def get_user_documents(
        self,
        user_id: str,
        db: AsyncSession
    ) -> DocumentListResponse:
        """Get all documents for a user with formatted response"""
        # Repository handles errors
        documents = await self.document_repo.get_user_documents(user_id, db)
        
        # Transform to response format
        document_items = [
            DocumentListItem(
                id=doc.id,
                filename=doc.filename,
                user_id=doc.user_id,
                file_size=doc.file_size,
                cloudinary_public_id=doc.cloudinary_public_id,
                cloudinary_url=doc.cloudinary_url,
                processing_status=doc.processing_status,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                insights=doc.insights,
                insights_available=doc.insights_available,
            )
            for doc in documents
        ]
        
        return DocumentListResponse(
            documents=document_items,
            total=len(document_items)
        )
    
    async def get_user_document(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> DocumentListItem:
        """Get single document for user"""
        # Repository handles errors and ownership check
        document = await self.document_repo.get_user_document(user_id, document_id, db)
        
        return DocumentListItem(
            id=document.id,
            filename=document.filename,
            user_id=document.user_id,
            file_size=document.file_size,
            cloudinary_url=document.cloudinary_url,
            cloudinary_public_id=document.cloudinary_public_id,
            created_at=document.created_at,
            updated_at=document.updated_at,
            processing_status=document.processing_status,
            insights_available=document.insights_available,
            insights=document.insights
        )
    
    async def delete_user_document(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> bool:
        """Delete a document"""
        # Repository handles ownership verification and deletion
        return await self.document_repo.delete(document_id, user_id, db)
    
    async def get_user_documents_count(
        self,
        user_id: str,
        db: AsyncSession
    ) -> int:
        """Count user's documents"""
        return await self.document_repo.count_user_documents(user_id, db)
    
    async def update_document_status(
        self,
        document_id: str,
        status: str,
        error_message: Optional[str],
        db: AsyncSession
    ) -> Document:
        """Update document processing status"""
        return await self.document_repo.update_status(
            document_id,
            ProcessingStatus(status),
            error_message,
            db
        )
    
    async def get_chunk_summaries_by_embedding_ids(
        self,
        embedding_ids: List[str],
        db: AsyncSession
    ) -> List[ChunkSummaryDTO]:
        """Get chunk summaries for RAG"""
        if not embedding_ids:
            return []
        
        chunks = await self.chunk_repo.get_by_embedding_ids(embedding_ids, db)
        
        # Transform to DTOs
        chunk_dtos = [
            ChunkSummaryDTO(
                embedding_id=chunk.embedding_id,
                summary=chunk.summary,
                relevance_score=None
            )
            for chunk in chunks
        ]
        
        logger.info(f"Retrieved {len(chunk_dtos)} chunk summaries for RAG")
        return chunk_dtos
    
    async def verify_document_ownership(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> bool:
        """Verify user owns document"""
        return await self.document_repo.verify_ownership(user_id, document_id, db)