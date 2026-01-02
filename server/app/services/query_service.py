from typing import List
from app.repositories.document_repository import DocumentRepository
from app.repositories.query_repository import QueryRepository
from app.services.gemini_service import GeminiService
from app.services.pinecone_service import PineconeService
from app.services.rag_agent_service import RAGAgentService
from app.schemas.query import ChunkSummaryDTO, QueryResponseDTO
from app.models.query import QueryResponse
from app.database import AsyncSession
from app.core.exceptions import DocumentNotFoundError, EmbeddingError, VectorStoreError

import logging


logger = logging.getLogger(__name__)


class QueryService:
    """Orchestrates the query processing workflow"""
    
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.gemini_service = GeminiService()
        self.rag_service = RAGAgentService()
        self.query_repo = QueryRepository()
    
    async def process_contract_query(
        self,
        query_text: str,
        document_id: str,
        user_id: str,
        pinecone_service,
        db: AsyncSession
    ) -> QueryResponse:
        """ Process a user query against a contract document """
        
        # Verify ownership
        await self._verify_ownership(user_id, document_id, db)
        
        # Generate embedding
        query_embedding = await self._generate_embedding(query_text)
        
        # Vector search
        embedding_ids = await self._search_similar_chunks(
            query_embedding,
            pinecone_service
        )
        
        # Retrieve chunks
        chunk_summaries = await self._retrieve_chunk_summaries(
            embedding_ids,
            db
        )
        
        # Execute RAG
        query_response = await self._execute_rag_query(
            query_text=query_text,
            chunk_summaries=chunk_summaries,
            document_id=document_id,
            user_id=user_id,
            db=db
        )
        
        return query_response
    
    async def _verify_ownership(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> None:
        """
        Verify user owns the document.
        """
        owns_document = await self.document_repo.verify_ownership(
            user_id=user_id,
            document_id=document_id,
            db=db
        )
        
        if not owns_document:
            raise DocumentNotFoundError(document_id)
    
    async def _generate_embedding(self, query_text: str) -> List[float]:
        """
        Generate embedding for query text.
        """
        try:
            embedding = await self.gemini_service.generate_embedding(query_text)
            
            if not embedding:
                raise EmbeddingError("Embedding generation returned empty result")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise EmbeddingError(f"Failed to generate query embedding: {str(e)}")
    
    async def _search_similar_chunks(
        self,
        query_embedding: List[float],
        pinecone_service : PineconeService,
        top_k: int = 5
    ) -> List[str]:
        """
        Search vector store for similar chunks.
        """
        if not pinecone_service:
            raise VectorStoreError(
                operation="query",
                details="Vector store service not available"
            )
        
        try:
            results = await pinecone_service.query_similar(
                query_vector=query_embedding,
                top_k=top_k
            )
            
            embedding_ids = [result['id'] for result in results]
            
            if not embedding_ids:
                logger.warning("No similar chunks found in vector store")
                return []
            
            return embedding_ids
            
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            raise VectorStoreError(
                operation="query",
                details=str(e)
            )
    
    async def _retrieve_chunk_summaries(
        self,
        embedding_ids: List[str],
        db: AsyncSession
    ) -> List[ChunkSummaryDTO]:
        """
        Retrieve and format chunk summaries.
        """
        if not embedding_ids:
            return []
        
        chunks = await self.document_repo.get_chunks_by_embedding_ids(
            embedding_ids=embedding_ids,
            db=db
        )
        
        return [
            ChunkSummaryDTO(
                embedding_id=chunk.embedding_id,
                summary=chunk.summary,
                relevance_score=None
            )
            for chunk in chunks
        ]
    
    async def _execute_rag_query(
        self,
        query_text: str,
        chunk_summaries: List[ChunkSummaryDTO],
        document_id: str,
        user_id: str,
        db: AsyncSession
    ) -> QueryResponse:
        """
        Execute RAG query with LLM and save to database.
        """
        query_response = await self.rag_service.execute_query(
            query_text=query_text,
            chunk_summaries=chunk_summaries,
            document_id=document_id,
            user_id=user_id,
            db=db
        )
        
        return query_response
    
    
    async def get_document_queries(
        self,
        user_id: str,
        document_id: str,
        db: AsyncSession
    ) -> List[QueryResponseDTO]:
        """
        Get all queries for a document.
        """
        # Verify ownership first
        await self._verify_ownership(user_id, document_id, db)
        
        queries = await self.query_repo.get_queries_by_document_id(document_id, db)
        
        return [
            QueryResponseDTO(
                id=query.id,
                response_text=query.response_text,
                created_at=query.created_at,
                query_text=query.query_text
            )
            for query in queries
        ]