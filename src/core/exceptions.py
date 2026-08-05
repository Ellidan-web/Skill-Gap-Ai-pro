from typing import Optional, Dict, Any


class AppException(Exception):
    """Base exception for all application errors."""
    
    def __init__(
        self,
        message: str,
        error_code: str = 'INTERNAL_ERROR',
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code='VALIDATION_ERROR',
            status_code=400,
            details=details
        )


class AuthenticationError(AppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = 'Authentication required'):
        super().__init__(
            message=message,
            error_code='AUTHENTICATION_ERROR',
            status_code=401
        )


class AuthorizationError(AppException):
    """Raised when user lacks permission."""
    
    def __init__(self, message: str = 'Permission denied'):
        super().__init__(
            message=message,
            error_code='AUTHORIZATION_ERROR',
            status_code=403
        )


class NotFoundError(AppException):
    """Raised when resource is not found."""
    
    def __init__(self, resource: str, identifier: Optional[str] = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(
            message=message,
            error_code='NOT_FOUND',
            status_code=404
        )


class ConflictError(AppException):
    """Raised when resource conflict occurs."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code='CONFLICT',
            status_code=409
        )


class RateLimitError(AppException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = 'Rate limit exceeded'):
        super().__init__(
            message=message,
            error_code='RATE_LIMIT_EXCEEDED',
            status_code=429
        )


class FileUploadError(AppException):
    """Raised when file upload fails."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code='FILE_UPLOAD_ERROR',
            status_code=400
        )


class MLProcessingError(AppException):
    """Raised when ML processing fails."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code='ML_PROCESSING_ERROR',
            status_code=500
        )