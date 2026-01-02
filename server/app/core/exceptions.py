
#  Base Exceptions
class DomainException(Exception):
    """Base exception for all domain errors"""
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

#  Authentication Exceptions 
class AuthenticationError(DomainException):
    """Authentication failed"""
    pass

class InvalidCredentialsError(AuthenticationError):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            error_code="INVALID_CREDENTIALS"
        )

class InvalidTokenError(AuthenticationError):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(
            message=message, 
            error_code="INVALID_TOKEN"
        )

class TokenExpiredError(AuthenticationError):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            error_code="TOKEN_EXPIRED"
        )


#  Authorization Exceptions 
class AuthorizationError(DomainException):
    """User lacks permission"""
    def __init__(self, resource: str = None):
        message = "Access denied"
        if resource:
            message += f" to {resource}"
        super().__init__(message=message, error_code="ACCESS_DENIED")


#  Resource Exceptions 
class ResourceNotFoundError(DomainException):
    """Resource doesn't exist"""
    def __init__(self, resource_type: str, identifier: str):
        super().__init__(
            message=f"{resource_type} not found",
            error_code="RESOURCE_NOT_FOUND",
            details={"resource_type": resource_type, "identifier": identifier}
        )

class ResourceAlreadyExistsError(DomainException):
    """Resource already exists"""
    def __init__(self, resource_type: str, field: str, value: str):
        super().__init__(
            message=f"{resource_type} already exists",
            error_code="RESOURCE_ALREADY_EXISTS",
            details={"field": field, "value": value}
        )


#  Document Exceptions 
class DocumentNotFoundError(ResourceNotFoundError):
    def __init__(self, document_id: str):
        super().__init__("Document", document_id)
        
class DocumentAccessDeniedError(AuthorizationError):
    """User doesn't own the document"""
    def __init__(self, document_id: str, user_id: str):
        super().__init__(resource="document")
        self.details = {"document_id": document_id, "user_id": user_id}        

class DocumentProcessingError(DomainException):
    """Document processing failed"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_code="DOCUMENT_PROCESSING_ERROR",
            details=details
        )

class FileUploadError(DomainException):
    """File upload failed""" 
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="FILE_UPLOAD_ERROR"
        )

class ChunkNotFoundError(ResourceNotFoundError):
    def __init__(self, embedding_ids: list):
        super().__init__(
            "DocumentChunk", 
            f"embedding_ids: {embedding_ids}"
        )


#  External Service Exceptions 
class ExternalServiceError(DomainException):
    """External service failed"""
    pass

class VectorStoreError(ExternalServiceError):
    def __init__(self, operation: str, details: str = None):
        message = f"Vector store error during {operation}"
        super().__init__(
            message=message,
            error_code="VECTOR_STORE_ERROR",
            details={"operation": operation, "details": details}
        )

class EmbeddingError(ExternalServiceError):
    def __init__(self, message: str):
        super().__init__(
            message=f"Embedding generation failed: {message}",
            error_code="EMBEDDING_ERROR"
        )

class CloudinaryError(ExternalServiceError):
    def __init__(self, operation: str, details: str = None):
        super().__init__(
            message=f"Cloudinary error during {operation}",
            error_code="CLOUDINARY_ERROR",
            details={"operation": operation, "details": details}
        )


#  Validation Exceptions 
class ValidationError(DomainException):
    """Input validation failed"""
    def __init__(self, message: str, field: str = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )

class FileTooLargeError(ValidationError):
    def __init__(self, max_size_mb: int):
        super().__init__(
            message=f"File too large. Maximum size: {max_size_mb}MB",
            field="file"
        )

class UnsupportedFileTypeError(ValidationError):
    def __init__(self, file_type: str, supported_types: list):
        super().__init__(
            message=f"Unsupported file type: {file_type}. Supported: {', '.join(supported_types)}",
            field="file"
        )


#  Database Exceptions 
class DatabaseError(DomainException):
    """Database operation failed"""
    def __init__(self, operation: str, details: str = None):
        message = f"Database error during {operation}"
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details={"operation": operation, "details": details}
        )


#  Business Logic Exceptions 
class BusinessRuleViolationError(DomainException):
    """Business rule violated"""
    def __init__(self, rule: str, details: dict = None):
        super().__init__(
            message=f"Business rule violation: {rule}",
            error_code="BUSINESS_RULE_VIOLATION",
            details=details
        )