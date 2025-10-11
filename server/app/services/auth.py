from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import SignInRequest
from app.schemas.user import UserCreate
from app.core.security import security_service
from app.core.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError
)
from app.services.user import user_service
from app.redis_client import redis_client
import logging
from app.redis_client import RedisOperationError


logger = logging.getLogger(__name__)

class AuthService:
    
    async def sign_up(self, db : AsyncSession, user_data : UserCreate) -> User:
        """Register a new user"""
        return await user_service.create_user(db, user_data)
    
    async def sign_in(self, db : AsyncSession, credentials : SignInRequest) -> Tuple [User, str, str, int]:
        """ Authenticate user and return user, access_token, refresh_token, expires_in """
        
        user = await user_service.get_user_by_email(db, credentials.email)
        
        if not user: 
            raise InvalidCredentialsError()
        
        if not security_service.verify_password(credentials.password, user.hashed_password):
            raise InvalidCredentialsError()
        

        access_token, access_jti, access_expires = security_service.create_access_token(user.id)
        
        refresh_token, refresh_jti, refresh_expires = security_service.create_refresh_token(user.id)
        
        # # Store refresh token in Redis
        try:
            await redis_client.store_refresh_token_jti(user_id=user.id, jti=refresh_jti, ttl_seconds=refresh_expires)
        except RedisOperationError as e:
            logger.error(f"Failed to store refresh token JTI for user {user.id}: {e}")        
            raise InvalidTokenError("Authentication service temporarily unavailable") 
        
        return user, access_token, refresh_token, access_expires
    
    async def sign_out(self, user_id : str, access_token : str) -> None : 
        token_data = security_service.decode_token(access_token, token_type="access")
        remaining_ttl = token_data["exp"] - token_data["iat"]
        
        if remaining_ttl > 0:
            await redis_client.blacklist_access_token_jti(jti=token_data.get('jti'), ttl_seconds=remaining_ttl)
        
        
        # # Delete refresh token from Redis
        await redis_client.delete_refresh_token_jti(user_id=user_id)
    
    async def refresh_access_token(
        self,
        db: AsyncSession,
        refresh_token: str
    ) -> Tuple[str, int]:
        refresh_payload = security_service.decode_token(refresh_token, token_type="refresh")
        user_id = refresh_payload["sub"]
        current_refresh_jti = refresh_payload["jti"]
        
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise UserNotFoundError()
        
        
         # Generate new tokens
        new_access_token, access_jti, access_expires = security_service.create_access_token(user_id)
        
        new_refresh_token, new_refresh_jti, refresh_expires = security_service.create_refresh_token(user_id)
        
        pass
    
    async def validate_access_token(self, access_token: str) -> Tuple[str, str]:
        token_payload = security_service.decode_token(access_token, token_type="access")
        user_id = token_payload["sub"]
        jti = token_payload["jti"]
        
        try:
            remaining_ttl = token_payload["exp"] - token_payload["iat"]
            if remaining_ttl < 0:
                raise InvalidTokenError("Token has been revoked")
            is_blacklisted = await redis_client.is_access_token_blacklisted(jti=jti)
            if is_blacklisted:
                raise InvalidTokenError("Token has been revoked")
        except RedisOperationError as e:
             logger.error(f"Failed to check blacklist status for JTI {jti}: {e}")
             raise InvalidTokenError("Authentication service temporarily unavailable")
         
        return user_id, jti
    

auth_service = AuthService()    