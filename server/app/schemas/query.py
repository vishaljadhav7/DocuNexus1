from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class QueryRequest(BaseModel):
    """Request payload for /query endpoint"""
    query_text: str = Field(..., min_length=5, max_length=1000)
    document_id: str
    # context_limit: int = Field(default=5, ge=1, le=10)


class ChunkSummaryDTO(BaseModel):
    """Data transfer object for chunk summaries"""
    embedding_id: str
    summary: str
    relevance_score: Optional[float] = None


class QueryResponseDTO(BaseModel):
    """Response payload for /query endpoint"""
    id: str
    response_text: str
    query_text: str
    confidence_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True