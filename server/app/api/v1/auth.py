from fastapi import APIRouter, Request, Response, status, HTTPException
import logging
from app.database import AsyncSessionDep
from app.api.dependencies import CurrentUserDep
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import SignInRequest, TokenResponse, MessageResponse
from app.services.auth import auth_service
from app.core.security import security_service 
from app.core.exceptions import InvalidTokenError
from app.config import get_settings


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
    user = await auth_service.sign_up(db, user_data)
    logger.info(f"New user registered: {user.id}")
    return UserResponse.model_validate(user)

@router.post(
    "/sign_in",
    response_model=TokenResponse,
    summary="Sign in user"
)
async def sign_in(
    response: Response,
    credentials: SignInRequest,
    db: AsyncSessionDep
):

    try:
        user, access_token, refresh_token, expires_in = await auth_service.sign_in(
            db,
            credentials
        )
        
        # Set refresh token as HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=not settings.debug,  # Use secure cookies in production
            samesite="lax",
            path="/api/v1/refresh"  # Restrict to refresh endpoint
        )
        
        logger.info(f"User {user.id} signed in successfully")
        return TokenResponse(
            access_token=access_token,
            expires_in=expires_in
        )
        
    except Exception as e:
        logger.error(f"Sign in failed for {credentials}: {e}")
        raise


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
    try:
        authorization = request.headers.get("Authorization")
        access_token = security_service.extract_token_from_header(authorization)
        
        await auth_service.sign_out(current_user.id, access_token)
        
        response.delete_cookie(
            key="refresh_token",
            path="/api/v1/refresh"
        )
        
        logger.info(f"User {current_user.id} signed out successfully")
        return MessageResponse(message="Successfully signed out")
    
    except InvalidTokenError as e:
        # Even if token is invalid, clear the cookie
        response.delete_cookie(
            key="refresh_token",
            path="/api/v1/refresh"
        )
        raise e
    except Exception as e:
        logger.error(f"Sign out failed for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sign out failed"
        )
        

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
async def get_current_user(
    current_user: CurrentUserDep
):
    return UserResponse.model_validate(current_user)        
