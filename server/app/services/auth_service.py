from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import SignInRequest
from app.schemas.user import UserCreate
from server.app.services.security_service import security_service
from app.core.exceptions import (
    InvalidCredentialsError,           
    InvalidTokenError,
    ResourceNotFoundError,
    CacheError
)
from app.services.user import user_service
from app.redis_client import redis_client, RedisOperationError
import logging
# from app.redis_client import RedisOperationError
from app.repositories.user_repository import user_repository

logger = logging.getLogger(__name__)

class AuthService:
    
    async def sign_up(self, db: AsyncSession, user_data: UserCreate) -> User:
        """ Register a new user """
        # Hash password
        hashed_password = security_service.hash_password(user_data.password)
        
        # Create user model
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        # Repository handles uniqueness constraints
        return await user_repository.create(db, user)
    
    async def sign_in(
        self, 
        db: AsyncSession, 
        credentials: SignInRequest
    ) -> Tuple[User, str, str, int]:
        """ Authenticate user and generate tokens """
        # Get user by email
        user = await user_repository.get_by_email(db, credentials.email)
        if not user:
            raise InvalidCredentialsError()
        
        # Verify password
        if not security_service.verify_password(credentials.password, user.hashed_password):
            raise InvalidCredentialsError()
        
        # Generate tokens
        access_token, access_jti, access_expires = security_service.create_access_token(user.id)
        refresh_token, refresh_jti, refresh_expires = security_service.create_refresh_token(user.id)
        
        # Store refresh token in Redis
        try:
            await redis_client.store_refresh_token_jti(
                user_id=user.id, 
                jti=refresh_jti, 
                ttl_seconds=refresh_expires
            )
        except RedisOperationError as e:
            logger.error(f"Failed to store refresh token for user {user.id}: {e}")
            raise CacheError("store_refresh_token")
        
        return user, access_token, refresh_token, access_expires
    
    async def sign_out(self, user_id: str, access_token: str) -> None:
        """ Sign out user - blacklist access token and delete refresh token """
        # Decode and validate token
        token_data = security_service.decode_token(access_token, token_type="access")
        remaining_ttl = token_data["exp"] - token_data["iat"]
        
        # Blacklist access token if not expired
        if remaining_ttl > 0:
            try:
                await redis_client.blacklist_access_token_jti(
                    jti=token_data["jti"], 
                    ttl_seconds=remaining_ttl
                )
            except RedisOperationError as e:
                logger.error(f"Failed to blacklist token for user {user_id}: {e}")
                raise CacheError("blacklist_token")
        
        # Delete refresh token
        try:
            await redis_client.delete_refresh_token_jti(user_id=user_id)
        except RedisOperationError as e:
            logger.error(f"Failed to delete refresh token for user {user_id}: {e}")
            raise CacheError("delete_refresh_token")
    
    async def refresh_access_token(
        self,
        db: AsyncSession,
        refresh_token: str
    ) -> Tuple[str, str, int, int]:
        """
        Generate new access token using refresh token
        """
        # Decode refresh token
        refresh_payload = security_service.decode_token(refresh_token, token_type="refresh")
        user_id = refresh_payload["sub"]
        current_refresh_jti = refresh_payload["jti"]
        
        # Verify refresh token exists in Redis
        try:
            stored_jti = await redis_client.get_refresh_token_jti(user_id)
            if not stored_jti or stored_jti != current_refresh_jti:
                raise InvalidTokenError("Refresh token has been revoked")
        except RedisOperationError as e:
            logger.error(f"Failed to verify refresh token for user {user_id}: {e}")
            raise CacheError("verify_refresh_token")
        
        # Verify user exists
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundError("User", user_id)
        
        # Generate new tokens
        new_access_token, access_jti, access_expires = security_service.create_access_token(user_id)
        new_refresh_token, new_refresh_jti, refresh_expires = security_service.create_refresh_token(user_id)
        
        # Store new refresh token
        try:
            await redis_client.store_refresh_token_jti(
                user_id=user_id,
                jti=new_refresh_jti,
                ttl_seconds=refresh_expires
            )
        except RedisOperationError as e:
            logger.error(f"Failed to store new refresh token for user {user_id}: {e}")
            raise CacheError("store_refresh_token")
        
        return new_access_token, new_refresh_token, access_expires, refresh_expires
    
    async def validate_access_token(self, access_token: str) -> Tuple[str, str]:
        """
        Validate access token and check blacklist
        """
        # Decode token
        token_payload = security_service.decode_token(access_token, token_type="access")
        user_id = token_payload["sub"]
        jti = token_payload["jti"]
        
        # Check if blacklisted
        try:
            is_blacklisted = await redis_client.is_access_token_blacklisted(jti=jti)
            if is_blacklisted:
                raise InvalidTokenError("Token has been revoked")
        except RedisOperationError as e:
            logger.error(f"Failed to check blacklist status for JTI {jti}: {e}")
            raise CacheError("check_blacklist")
        
        return user_id, jti
    

auth_service = AuthService()    