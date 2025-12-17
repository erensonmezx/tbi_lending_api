from pydantic import BaseModel
from typing import Any, Optional

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Any] = None
    correlation_id: Optional[str] = None

class NotFoundError(Exception):
    def __init__(self, message: str = "Not found", details: Any = None):
        self.message = message
        self.details = details
        super().__init__(message)

class ValidationError(Exception):
    def __init__(self, message: str = "Validation error", details: Any = None):
        self.message = message
        self.details = details
        super().__init__(message)
