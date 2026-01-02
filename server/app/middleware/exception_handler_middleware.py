from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Union

from app.core.exceptions import (
    DomainException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
    ValidationError,
    DatabaseError,
    ExternalServiceError,
    BusinessRuleViolationError,
)

logger = logging.getLogger(__name__)


class ErrorResponse:
    """Standardized error response format"""
    def __init__(
        self,
        error_code: str,
        message: str,
        details: dict = None,
        status_code: int = 500
    ):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        self.status_code = status_code

    def to_dict(self):
        response = {
            "error": {
                "code": self.error_code,
                "message": self.message,
            }
        }
        if self.details:
            response["error"]["details"] = self.details
        return response


def map_exception_to_status_code(exc: DomainException) -> int:
    """Map domain exceptions to HTTP status codes"""
    exception_status_map = {
        AuthenticationError: status.HTTP_401_UNAUTHORIZED,
        AuthorizationError: status.HTTP_403_FORBIDDEN,
        ResourceNotFoundError: status.HTTP_404_NOT_FOUND,
        ResourceAlreadyExistsError: status.HTTP_409_CONFLICT,
        ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        BusinessRuleViolationError: status.HTTP_400_BAD_REQUEST,
        DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ExternalServiceError: status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    
    # Check exception class hierarchy
    for exc_class, status_code in exception_status_map.items():
        if isinstance(exc, exc_class):
            return status_code
    
    return status.HTTP_500_INTERNAL_SERVER_ERROR


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Handle all domain exceptions"""
    status_code = map_exception_to_status_code(exc)
    
    # Log based on severity
    if status_code >= 500:
        logger.error(
            f"Domain exception: {exc.error_code}",
            extra={
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "path": request.url.path,
            },
            exc_info=True
        )
    else:
        logger.warning(
            f"Domain exception: {exc.error_code}",
            extra={
                "error_code": exc.error_code,
                "message": exc.message,
                "path": request.url.path,
            }
        )
    
    error_response = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
        status_code=status_code
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.to_dict()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI/Pydantic validation errors"""
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    
    error_response = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.to_dict()
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions"""
    logger.warning(f"HTTP exception on {request.url.path}: {exc.detail}")
    
    error_response = ErrorResponse(
        error_code="HTTP_ERROR",
        message=exc.detail if isinstance(exc.detail, str) else "An error occurred",
        status_code=exc.status_code
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict()
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.error(
        f"Unhandled exception on {request.url.path}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method}
    )
    
    error_response = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.to_dict()
    )


def register_exception_handlers(app):
    """Register all exception handlers with FastAPI app"""
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)