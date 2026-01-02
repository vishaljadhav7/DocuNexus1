from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class QueryResponse(Base):

    __tablename__ = "query_responses"
    
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
    
    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    query_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    response_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
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
    
    user: Mapped["User"] = relationship(
        "User",       
        back_populates="query_responses",
        lazy="noload",
        init=False
    )
    
    document: Mapped["Document"] = relationship(
        "Document",
        lazy="noload",
        init=False,
        back_populates="document_query",
    )
