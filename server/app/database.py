from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker 
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from app.config import get_settings
from fastapi import Depends

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)    

AsyncSessionLocal = async_sessionmaker(
   engine,
   class_=AsyncSession, 
   expire_on_commit=False,
   autocommit=False,
   autoflush=False
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
     """Dependency to get database session"""
     async with AsyncSessionLocal() as session:
          try:
               yield session
          finally:
              await session.close()     
              
# Type alias for dependency injection
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]                        
              