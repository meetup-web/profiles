from dataclasses import dataclass, field
from enum import Enum, auto


class ErrorType(Enum):
    NOT_FOUND = auto()
    VALIDATION_ERROR = auto()
    APPLICATION_ERROR = auto()
    PERMISSION_ERROR = auto()
    CONFLICT_ERROR = auto()
    AUTHORIZATION_ERROR = auto()


@dataclass(frozen=True)
class ApplicationError(Exception):
    message: str = field(default="Application error")
    error_type: ErrorType = field(default=ErrorType.APPLICATION_ERROR)
