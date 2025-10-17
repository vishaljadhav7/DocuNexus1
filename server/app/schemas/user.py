from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .auth import TokenResponse

class UserBase(BaseModel):
    email : EmailStr
    username : str = Field(..., min_length=3, max_length=20)
    

class UserCreate(UserBase):
    password : str = Field(..., min_length=8, max_length=20)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePass123!"
            }
        }        
    )
    
class UserSignInResponse(UserBase, TokenResponse):
    id : str
    created_at: datetime

    
    model_config = ConfigDict(from_attributes=True)
    
class UserResponse(UserBase):
    id : str
    created_at: datetime
    updated_at: Optional[datetime]
    credits: int
    
    model_config = ConfigDict(from_attributes=True)
    
class UserInDB(UserResponse):
    hashed_password: str