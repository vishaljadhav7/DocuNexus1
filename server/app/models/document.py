from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
import uuid 
import enum

from app.database import Base


class ProcessingStatus(str, enum.Enum):
    UPLOADED = 'uploaded'
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    """Document model for uploaded PDFs"""
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        init=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    cloudinary_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    cloudinary_public_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus, values_callable=lambda enum: [e.value for e in enum], native_enum=False),
        default=ProcessingStatus.UPLOADED,
        nullable=False,
        init=False
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
        init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )
    
    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        init=False
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="my_docs",
        init=False
    )



class DocumentChunk(Base):
    """Document chunks with metadata and summaries"""
    __tablename__ = "document_chunks"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        init=False
    )
    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('documents.id'),
        nullable=False,
        index=True
    )
    embedding_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True
    )
    content: Mapped[Dict] = mapped_column(
        JSONB,
        nullable=False
    )
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )
    
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="chunks",
        init=False,
        lazy="noload"
    )