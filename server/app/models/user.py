from typing import List
from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        init=False
    )

    email: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    credits: Mapped[int] = mapped_column(
        Integer,      
        default=20,
        nullable=False,
        init=False
    )

    created_at : Mapped[datetime] = mapped_column(
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
    
    my_docs: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="user",
        lazy="noload", 
        init=False,
        cascade="all, delete-orphan"
    )
    
    query_responses : Mapped[List["QueryResponse"]] = relationship(
        "QueryResponse",
        back_populates="user",
        lazy="noload",
        init=False,
        cascade="all, delete-orphan"
    )