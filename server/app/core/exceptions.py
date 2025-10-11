from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class AuthException(HTTPException):
    """Base authentication exception"""
    def __init__(
            self,
            detail : str,
            status_code : int = status.HTTP_401_UNAUTHORIZED,
            headers : Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers or {"WWW-Authenticate": "Bearer"}
        )
        
class InvalidCredentialsError(AuthException):
      """Invalid credentials exception"""
      def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail=detail)

class InvalidTokenError(AuthException):
    """Invalid token exception"""
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(detail=detail)        


class TokenBlacklistedError(AuthException):
    """Token blacklisted exception"""
    def __init__(self, detail: str = "Token has been revoked"):
        super().__init__(detail=detail)
       

class UserNotFoundError(HTTPException):
    """User not found exception"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserExistsError(HTTPException):
    """User already exists exception"""
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)       