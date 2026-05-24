import logging
import time
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.models.query import QueryResponse
from app.schemas.query import ChunkSummaryDTO
from app.core.exceptions import ExternalServiceError, DatabaseError
import asyncio
from app.repositories.query_repository import QueryRepository

logger = logging.getLogger(__name__)


class RAGServiceError(ExternalServiceError):
    """RAG-specific service error"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=f"RAG query execution failed: {message}",
            error_code="RAG_ERROR",
            details=details
        )

class RAGAgentService:
    """Advanced RAG service with prompt engineering"""
    
    def __init__(self):
        self.settings = get_settings()
        self.query_repo = QueryRepository()
        try:
             self.llm = ChatGoogleGenerativeAI(
               model=self.settings.gemini_model,
               google_api_key=self.settings.gemini_api_key,
            #    version="v1",
               temperature=0.3
            )
        except Exception as e:
             logger.error(f"Failed to initialize RAG service: {str(e)}")
             raise RAGServiceError(
                 "Failed to initialize LLM",
                 details={"error": str(e)}
             )

    def _create_agent_prompt(self, query: str, context: str) -> str:
        return f"""You are a Contract Analysis AI. Answer queries about legal documents with precision and brevity.
    
    ===== INPUT =====
    USER QUERY: {query}
    CONTRACT SECTIONS: {context}
    
    ===== RULES =====
    - Answer in 3-4 bullet points MAX
    - Each bullet: 1 sentence only
    - Cite only section references explicitly present in the context, do not fabricate clause numbers
    - Flag risks or red flags with ⚠️
    - If context lacks the answer: "Not addressed in provided sections."
    - No filler, no repetition, no legal jargon unless explaining it
    - Base answers ONLY on provided context
    
    ===== FORMAT =====
    - [Direct answer]
    - [Supporting clause reference]
    - ⚠️ [Risk or concern, if any]
    - [One actionable next step, if relevant]
    
    ===== BEGIN ====="""
    
    def _format_context(self, chunk_summaries: List[ChunkSummaryDTO]) -> str:
        if not chunk_summaries:
            return "No relevant contract sections found."
        
        sections = []
        for idx, chunk in enumerate(chunk_summaries, 1):
            # Clean and format each section
            summary = chunk.summary
            
            # Add metadata
            metadata = []
            if hasattr(chunk, 'relevance_score') and chunk.relevance_score:
                metadata.append(f"Relevance: {chunk.relevance_score:.0%}")
            
            meta_str = f" [{', '.join(metadata)}]" if metadata else ""
            
            sections.append(f"\n{'='*40}\nSECTION {idx}{meta_str}\n{'-'*20}\n{summary}")
        
        return "\n".join(sections)
    
    async def execute_query(
        self,
        query_text: str,
        chunk_summaries: List[ChunkSummaryDTO],
        document_id: str,
        user_id: str,
        db: AsyncSession
    ) -> QueryResponse:
        """
        Execute RAG query and save response.
        """
        logger.info("1. In RAG service execute_query")
        start_time = time.time()
        
        try:
            # Format context and create prompt
            context = self._format_context(chunk_summaries)
            prompt = self._create_agent_prompt(query_text, context)
            
            # Call LLM
            response = await self._call_llm(prompt)
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            logger.info(f"RAG query processed in {processing_time_ms}ms")
            
            query_obj = QueryResponse(
                user_id=user_id,
                query_text=query_text,
                document_id=document_id,
                response_text=response
            )
            
            query_response = await self.query_repo.create(query_response= query_obj,db=db)
            
            return query_response
            
        except RAGServiceError:
            # Re-raise RAG-specific errors
            raise
        except DatabaseError:
            # Re-raise database errors
            raise
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected RAG error: {str(e)}", exc_info=True)
            raise RAGServiceError(
                "Unexpected error during RAG processing",
                details={"error": str(e), "query_text": query_text[:100]}
            )

    async def _call_llm(self, prompt: str) -> str:
        """
        Call LLM with retry logic.
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = await self.llm.ainvoke(prompt)
            
                content = response.content
                if isinstance(content, list):
                    return content[0]["text"]
                return content
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if we should retry
                is_retryable = any(
                    keyword in error_msg 
                    for keyword in ['rate limit', 'timeout', 'quota', 'connection']
                )
                
                if attempt < max_retries - 1 and is_retryable:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"LLM call failed (attempt {attempt + 1}/{max_retries}), "
                        f"retrying in {wait_time}s: {str(e)}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"LLM call failed after {attempt + 1} attempts: {str(e)}")
                    raise RAGServiceError(
                        "LLM API call failed",
                        details={
                            "error": str(e),
                            "attempts": attempt + 1,
                            "is_retryable": is_retryable
                        }
                    )


rag_service = RAGAgentService()