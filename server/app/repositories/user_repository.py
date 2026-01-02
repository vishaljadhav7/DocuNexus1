from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.user import User
from app.core.exceptions import DatabaseError, ResourceAlreadyExistsError
import logging  

logger = logging.getLogger(__name__)

class UserRepository:
    """Data access layer for User model"""
    
    async def get_by_id(self, db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by ID {user_id}: {e}")
            raise DatabaseError("get_by_id", str(e))
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by email {email}: {e}")
            raise DatabaseError("get_by_email", str(e))
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            result = await db.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by username {username}: {e}")
            raise DatabaseError("get_by_username", str(e))
    
    async def create(self, db: AsyncSession, user: User) -> User:
        """Create new user"""
        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError as e:
            await db.rollback()
            # Parse constraint violation
            if "email" in str(e.orig):
                raise ResourceAlreadyExistsError("User", "email", user.email)
            elif "username" in str(e.orig):
                raise ResourceAlreadyExistsError("User", "username", user.username)
            else:
                raise DatabaseError("create_user", "Integrity constraint violation")
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error creating user: {e}")
            raise DatabaseError("create_user", str(e))

user_repository = UserRepository()