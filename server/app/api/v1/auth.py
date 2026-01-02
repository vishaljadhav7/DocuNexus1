from fastapi import APIRouter, Request, Response, status
import logging
from app.database import AsyncSessionDep
from app.api.dependencies import CurrentUserDep
from app.schemas.user import UserCreate, UserResponse, UserSignInResponse
from app.schemas.auth import SignInRequest, MessageResponse
from server.app.services.auth_service import auth_service
from server.app.services.security_service import security_service
from app.config import get_settings
from app.core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/v1", tags=["Authentication"])

@router.post(
    "/sign_up",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def sign_up(
    user_data: UserCreate,
    db: AsyncSessionDep
):
    """Register new user """
    user = await auth_service.sign_up(db, user_data)
    logger.info(f"New user registered: {user.id}")
    return UserResponse.model_validate(user)


@router.post(
    "/sign_in",
    response_model=UserSignInResponse,
    summary="Sign in user"
)
async def sign_in(
    response: Response,
    credentials: SignInRequest,
    db: AsyncSessionDep
):
    """Sign in user """
    user, access_token, refresh_token, expires_in = await auth_service.sign_in(
        db, credentials
    )
    
    # Set refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        path="/api/v1/refresh"
    )
    
    logger.info(f"User {user.id} signed in successfully")
    return UserSignInResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        access_token=access_token,
        expires_in=expires_in
    )


@router.post(
    "/sign_out",
    response_model=MessageResponse,
    summary="Sign out user"
)
async def sign_out(
    request: Request,
    response: Response,
    current_user: CurrentUserDep
):
    """Sign out user """
    authorization = request.headers.get("Authorization")
    access_token = security_service.extract_token_from_header(authorization)
    
    await auth_service.sign_out(current_user.id, access_token)
    
    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/refresh"
    )
    
    logger.info(f"User {current_user.id} signed out successfully")
    return MessageResponse(message="Successfully signed out")


@router.post(
    "/refresh",
    response_model=UserSignInResponse,
    summary="Refresh access token"
)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSessionDep
):
    """Refresh access token using refresh token from cookie"""
    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidTokenError("Refresh token not found")
    
    # Get new tokens
    new_access_token, new_refresh_token, access_expires, refresh_expires = \
        await auth_service.refresh_access_token(db, refresh_token)
    
    # Update refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        path="/api/v1/refresh"
    )
    
    logger.info("Access token refreshed successfully")
    return {
        "access_token": new_access_token,
        "expires_in": access_expires
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
async def get_current_user(current_user: CurrentUserDep):
    """Get current authenticated user"""
    return UserResponse.model_validate(current_user)