"""
Pydantic schemas for document-related API operations
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum
from app.models.document import ProcessingStatus

class DocumentUploadResponse(BaseModel):
    """Response schema for document upload"""      
    model_config = ConfigDict(from_attributes=True)
    
    document_id: str
    filename: str
    cloudinary_url: str
    processing_status: ProcessingStatus
    created_at: datetime
    message : str
    
    
class DocumentStatusResponse(BaseModel):
    """Response schema for document status check"""
    document_id: str
    status: ProcessingStatus
    error_message: Optional[str] = None
    

class DocumentListItem(BaseModel):
    """Schema for document in list view"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    filename: str
    user_id : str
    file_size: int
    cloudinary_url: str
    cloudinary_public_id : str
    # error_message : Optional[str]
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at : datetime
    


class DocumentListResponse(BaseModel):
    """Response schema for list of documents"""
    documents: List[DocumentListItem]
    total: int


class DocumentDeleteResponse(BaseModel):
    """Response schema for document deletion"""
    message: str
    document_id: str