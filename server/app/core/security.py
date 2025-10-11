from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.exceptions import InvalidTokenError
from app.config import get_settings 
import uuid

settings = get_settings()

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


class SecurityService:
    """Security service for password hashing and JWT operations"""

    @staticmethod
    def hash_password(password : str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password) 
    
    @staticmethod
    def create_access_token(user_id: str) -> tuple[str, int]:
        expire_seconds = settings.access_token_expire_minutes * 60 
        now = datetime.now(timezone.utc)
        expire = now + timedelta(seconds=expire_seconds)
        jti = str(uuid.uuid4())
     
        payload = {
            "sub" : user_id,
            "jti": jti,
            "exp" : expire,
            "iat" : now,
            "type" : "access"
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        return token, jti, expire_seconds
    

    @staticmethod
    def create_refresh_token(user_id: str) -> tuple[str, int] :
        expire_seconds = settings.refresh_token_expire_days * 24 * 60 * 60
        now = datetime.now(timezone.utc)
        expire = now + timedelta(seconds=expire_seconds)
        jti = str(uuid.uuid4())
         
        payload = {
            "sub" : user_id,
            "jti": jti,
            "exp" : expire,
            "iat" : now,
            "type": "refresh"
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        return token, jti, expire_seconds
    
    @staticmethod
    def decode_token(token : str, token_type: str = 'access') -> Dict[str, Any] :
        try:
            payload = jwt.decode(token, key=settings.secret_key, algorithms=settings.algorithm)
            
            if payload.get("type") != token_type:
                print(f"Token type mismatch: expected '{token_type}', got '{payload.get('type')}'")
                raise InvalidTokenError("Invalid token type")
            
            # Optional: Validate required fields
            required_fields = ["sub", "jti", "exp", "iat"]
            for field in required_fields:
                if field not in payload:
                    print(f"Missing required field: {field}")
                    raise InvalidTokenError(f"Missing required field: {field}")
            
            return payload
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {str(e)}")
            raise InvalidTokenError(f"Invalid token: {str(e)}")
        
    @staticmethod
    def get_token_remaining_ttl(token_payload : Dict[str, Any]) -> int:
        try:
            exp_timestamp = token_payload.get('exp')
            if not exp_timestamp:
                return 0   
            
            now_timestamp = datetime.now(timezone.utc).timestamp()
            remaining = int(exp_timestamp - now_timestamp)
            return max(0, remaining)
        except (TypeError, ValueError):
            return 0   

    @staticmethod
    def extract_token_from_header(authorization : Optional[str]) -> str:
        """Extract token from Authorization header"""
        if not authorization:
            raise InvalidTokenError("Authorization header missing")
        
        parts = authorization.split()

        if(len(parts) != 2 or parts[0].lower() != 'bearer'):
              raise InvalidTokenError("Invalid authorization header format")
        
        return parts[1]


security_service = SecurityService()           