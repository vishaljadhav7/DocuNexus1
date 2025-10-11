from typing import Annotated, Optional
from fastapi import Depends, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.core.security import security_service
from app.core.exceptions import (
    InvalidTokenError,
    UserNotFoundError
)
from app.services.auth import auth_service
# from app.core.exceptions import VectorStoreError


async def get_current_user_from_token(
        request : Request,
        db : AsyncSession = Depends(get_db)
) -> User :
    """Get current user from access token in header"""
    
    # Get user_id from request state (set by middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        # Fallback: extract and validate token
        authorization = request.headers.get("Authorization")
        token = security_service.extract_token_from_header(authorization)
        
        # Validate token and check blacklist
        user_id, jti = await auth_service.validate_access_token(token)
        
        # Store in request state for potential reuse
        request.state.user_id = user_id
        request.state.token_jti = jti

    result = await db.execute(
        select(User).where(User.id == user_id)
    )         

    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundError()
    
    return user

async def get_refresh_token_from_cookie(
    refresh_token: Optional[str] = Cookie(None)
) -> str:
    """Extract refresh token from cookie"""
    if not refresh_token:
        raise InvalidTokenError("Refresh token not found")
    return refresh_token



CurrentUserDep = Annotated[User, Depends(get_current_user_from_token)]
RefreshTokenDep = Annotated[str, Depends(get_refresh_token_from_cookie)]