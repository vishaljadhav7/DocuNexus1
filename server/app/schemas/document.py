"""
Pydantic schemas for document-related API operations
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.document import ProcessingStatus

class DocumentUploadResponse(BaseModel):
    """Response schema for document upload"""
    model_config = ConfigDict(from_attributes=True)
    
    document_id: str
    filename: str
    cloudinary_url: str
    processing_status: ProcessingStatus
    created_at: datetime
    insights_available: bool
    message: str


class DocumentStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    document_id: str
    processing_status: ProcessingStatus
    error_message: Optional[str] = None

class DocumentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    filename: str
    user_id: str
    file_size: int
    cloudinary_url: str
    cloudinary_public_id: str
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    insights_available: bool
    insights: Optional[dict] = None
    error_message : Optional[str] = None


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    documents: List[DocumentListItem]
    total: int


class DocumentDeleteResponse(BaseModel):
    message: str
    document_id: str


class DocumentDetailResponse(BaseModel):
    """Response schema for detailed document view"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    filename: str
    user_id: str
    file_size: int
    cloudinary_url: str
    cloudinary_public_id: str
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    insights_available: bool
    insights: Optional[dict] = None