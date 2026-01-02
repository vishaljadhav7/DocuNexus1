from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.exceptions import InvalidTokenError
from app.config import get_settings
import uuid
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

class SecurityService:
    """Security service for password hashing and JWT operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(user_id: str) -> tuple[str, str, int]:
        expire_seconds = settings.access_token_expire_minutes * 60
        now = datetime.now(timezone.utc)
        expire = now + timedelta(seconds=expire_seconds)
        jti = str(uuid.uuid4())
        
        payload = {
            "sub": user_id,
            "jti": jti,
            "exp": expire,
            "iat": now,
            "type": "access"
        }
        
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        return token, jti, expire_seconds
    
    @staticmethod
    def create_refresh_token(user_id: str) -> tuple[str, str, int]:
        expire_seconds = settings.refresh_token_expire_days * 24 * 60 * 60
        now = datetime.now(timezone.utc)
        expire = now + timedelta(seconds=expire_seconds)
        jti = str(uuid.uuid4())
        
        payload = {
            "sub": user_id,
            "jti": jti,
            "exp": expire,
            "iat": now,
            "type": "refresh"
        }
        
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        return token, jti, expire_seconds
    
    @staticmethod
    def decode_token(token: str, token_type: str = 'access') -> Dict[str, Any]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token, 
                key=settings.secret_key, 
                algorithms=[settings.algorithm]
            )
            
            # Validate token type
            if payload.get("type") != token_type:
                logger.warning(
                    f"Token type mismatch: expected '{token_type}', "
                    f"got '{payload.get('type')}'"
                )
                raise InvalidTokenError("Invalid token type")
            
            # Validate required fields
            required_fields = ["sub", "jti", "exp", "iat"]
            missing_fields = [f for f in required_fields if f not in payload]
            if missing_fields:
                logger.warning(f"Missing required fields: {missing_fields}")
                raise InvalidTokenError(f"Missing required fields: {', '.join(missing_fields)}")
            
            return payload
            
        except JWTError as e:
            logger.warning(f"JWT decode error: {str(e)}")
            raise InvalidTokenError(f"Invalid token: {str(e)}")
    
    @staticmethod
    def extract_token_from_header(authorization: Optional[str]) -> str:
        """Extract token from Authorization header"""
        if not authorization:
            raise InvalidTokenError("Authorization header missing")
        
        parts = authorization.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise InvalidTokenError("Invalid authorization header format")
        
        return parts[1]

security_service = SecurityService()