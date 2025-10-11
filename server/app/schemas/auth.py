from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class SignInRequest(BaseModel):
    """Sign in request schema"""
    email: str = EmailStr
    password: str = Field(..., min_length=8, max_length=20)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe@email.com",
                "password": "SecurePass123!"
            }
        }
    }


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Token payload data"""
    sub: str  # user_id 
    exp: int
    iat: int
    type: str  # "access" or "refresh"


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    
    
class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int
    type: Optional[str] = None