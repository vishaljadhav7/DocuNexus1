from typing import Optional, Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import security_service
from app.core.exceptions import InvalidTokenError, TokenBlacklistedError
from app.services.auth import auth_service


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for protected routes"""
    
    def __init__(self, app, protected_paths : Optional[list]= None):
        super().__init__(app)
        self.protected_paths = protected_paths or []

    async def dispatch(self, request : Request, call_next : Callable):
        """Process the request"""
       
        if request.method == "OPTIONS":
            return Response(status_code=200)
  
     
        # Check if path requires authentication
        if not self._is_protected_path(request.url.path):
            return await call_next(request)
              
        try:
            # Extract token from header
            authorization = request.headers.get("Authorization")
            # print("authorization from middleware =>>>>> ", authorization)
            token = security_service.extract_token_from_header(authorization)

            user_id, jti = await auth_service.validate_access_token(token)
            
            request.state.user_id = user_id
            request.state.jti = jti

            return await call_next(request)
        
        except (InvalidTokenError, TokenBlacklistedError) as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers=e.headers
            )
            
        except Exception as e:
            # logger.error(f"Unexpected error in auth middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Authentication service temporarily unavailable"}
            )    
         
            

    def _is_protected_path(self, path : str) -> bool:
        """Check if path requires authentication"""
        for protected_path in self.protected_paths:
            if path.startswith(protected_path):
                return True