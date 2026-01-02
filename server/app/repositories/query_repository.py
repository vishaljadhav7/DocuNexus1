from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from app.models.query import QueryResponse
from app.models.document import DocumentChunk
from app.core.exceptions import DatabaseError, ChunkNotFoundError

logger = logging.getLogger(__name__)


class QueryRepository:
    """Handles database operations for queries"""
    
    async def create(
        self,
        query_response: QueryResponse,
        db: AsyncSession
    ) -> QueryResponse:
        """Save query response to database"""
        try:
            db.add(query_response)
            await db.commit()
            await db.refresh(query_response)
            return query_response
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create query response: {str(e)}")
            raise DatabaseError("create query response", str(e))
    
    async def get_queries_by_document_id(
        self,
        document_id: str,
        db: AsyncSession
    ) -> List[QueryResponse]:
        """Get all queries for a document"""
        try:
            stmt = select(QueryResponse).where(
                QueryResponse.document_id == document_id
            ).order_by(QueryResponse.created_at.desc())
            
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to fetch queries for document {document_id}: {str(e)}")
            raise DatabaseError("fetch queries", str(e))
    
    async def get_chunks_by_embedding_ids(
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
            raise  # Re-raise domain exception
        except Exception as e:
            logger.error(f"Failed to fetch chunks: {str(e)}")
            raise DatabaseError("fetch chunks by embedding IDs", str(e))