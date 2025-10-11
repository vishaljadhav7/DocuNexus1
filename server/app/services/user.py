from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import UserExistsError
from app.core.security import security_service

class UserService:

    """User service for user operations"""

    async def create_user(
        self, db: AsyncSession, user_data: UserCreate
    ):
        existing_user = await self.get_user_by_email(
            db,
            email=user_data.email
        )
        
        if existing_user:
            raise UserExistsError('User Exist')
        
        hash_password = security_service.hash_password(user_data.password) 
         
        user = User(
            email=user_data.email,
            hashed_password=hash_password,
            username=user_data.username
        )    
        
        db.add(user)
        
        await db.commit()
        await db.refresh(user)
        
        return user
            

    async def get_by_user_id(
       self, db:AsyncSession, user_id: str
    ) -> User :
        
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        
        return result.scalar_one_or_none()

    async def get_user_by_email(
      self, db: AsyncSession, email: Optional[str] = None       
    ) -> Optional[User]:
       
       if not email:
           return None

       result = await db.execute(
            select(User).where(User.email == email)
        )
       return result.scalar_one_or_none()            

user_service = UserService()
