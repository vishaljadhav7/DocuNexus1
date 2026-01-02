from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from typing import List, Optional
from app.models.document import Document, DocumentChunk, ProcessingStatus
from app.core.exceptions import DocumentNotFoundError, DatabaseError, ChunkNotFoundError
import logging

logger = logging.getLogger(__name__)


class DocumentRepository:
    """Handles all database operations for documents"""
    
    async def create(self, document: Document, db: AsyncSession) -> Document:
        """Create a new document"""
        try:
            db.add(document)
            await db.commit()
            await db.refresh(document)
            return document
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create document: {str(e)}")
            raise DatabaseError("create document", str(e))
    
    async def get_by_id(
        self, 
        document_id: str, 
        db: AsyncSession
    ) -> Optional[Document]:
        """Get document by ID""" 
        try:
            stmt = select(Document).where(Document.id == document_id)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to fetch document {document_id}: {str(e)}")
            raise DatabaseError("fetch document", str(e))\
  
    async def get_by_id_or_raise(
        self,
        document_id: str,
        db: AsyncSession
    ) -> Document:
        """Get document by ID - raises exception if not found."""
        document = await self.get_by_id(document_id, db)
        if not document:
            raise DocumentNotFoundError(document_id)
        return document                
    
    async def get_user_document(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> Document:
        """Get document belonging to specific user"""
        try:
            stmt = select(Document).where(
                Document.id == document_id,
                Document.user_id == user_id
            )
            result = await db.execute(stmt)
            document = result.scalar_one_or_none()
            
            if not document:
                raise DocumentNotFoundError(document_id)
            
            return document
        except DocumentNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to fetch user document: {str(e)}")
            raise DatabaseError("fetch user document", str(e))
    
    async def get_user_documents(
        self,
        user_id: str,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 5
    ) -> List[Document]:
        """Get all documents for a user"""
        try:
            stmt = (
                select(Document)
                .where(Document.user_id == user_id)
                .order_by(Document.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to fetch user documents: {str(e)}")
            raise DatabaseError("fetch user documents", str(e))
    
    
    async def update_status(
        self,
        document_id: str,
        status: ProcessingStatus,
        error_message: Optional[str],
        db: AsyncSession
    ) -> Document:
        """Update document processing status"""
        try:
            document = await self.get_by_id(document_id, db)
            
            if not document:
                raise DocumentNotFoundError(document_id)
            
            document.processing_status = status
            if error_message:
                document.error_message = error_message
            
            await db.commit()
            await db.refresh(document)
            return document
        except DocumentNotFoundError:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update document status: {str(e)}")
            raise DatabaseError("update document status", str(e))
    
    async def delete(
        self,
        document_id: str,
        user_id: str,
        db: AsyncSession
    ) -> bool:
        """Delete a document (with ownership check)."""
        try:
            # First verify document exists and user owns it
            document = await self.get_by_id_or_raise(document_id, db)
            
            if document.user_id != user_id:
                raise DocumentNotFoundError(document_id)
            
            await db.delete(document)
            await db.commit()
            logger.info(f"Document {document_id} deleted successfully")
            return True
            
        except DocumentNotFoundError:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to delete document: {str(e)}")
            raise DatabaseError("delete document", str(e))
    
    async def verify_ownership(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> bool:
        """Check if user owns document"""
        try:
            stmt = select(Document.id).where(
                Document.id == document_id,
                Document.user_id == user_id
            )
            result = await db.execute(stmt)
            return result.scalar_one_or_none() is not None
        except Exception as e:
            logger.error(f"Failed to verify ownership: {str(e)}")
            raise DatabaseError("verify document ownership", str(e))


class DocumentChunkRepository:
    """Handles database operations for document chunks"""
    
    async def create_bulk(
        self,
        chunks: List[DocumentChunk],
        db: AsyncSession
    ) -> List[DocumentChunk]:
        """Create multiple chunks"""
        try:
            db.add_all(chunks)
            await db.commit()
            
            # Refresh all chunks
            for chunk in chunks:
                await db.refresh(chunk)
            
            return chunks
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create chunks: {str(e)}")
            raise DatabaseError("create chunks", str(e))
    
    async def get_by_embedding_ids(
        self,
        embedding_ids: List[str],
        db: AsyncSession
    ) -> List[DocumentChunk]:
        """Get chunks by embedding IDs"""
        if not embedding_ids:
            return []
        
        try:
            stmt = select(DocumentChunk).where(
                DocumentChunk.embedding_id.in_(embedding_ids)
            )
            result = await db.execute(stmt)
            chunks = result.scalars().all()
            
            if not chunks:
                raise ChunkNotFoundError(embedding_ids)
            
            return chunks
        except ChunkNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to fetch chunks: {str(e)}")
            raise DatabaseError("fetch chunks by embedding IDs", str(e))