"""
Enterprise Exception Hierarchy.

Provides a comprehensive exception system with:
- Structured error handling
- Error context and metadata
- Localization support
- Logging integration
- Recovery strategies
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""

    VALIDATION = "validation"
    BUSINESS_RULE = "business_rule"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    SYSTEM = "system"
    EXTERNAL_SERVICE = "external_service"
    DATABASE = "database"
    NETWORK = "network"


@dataclass
class ErrorContext:
    """Context information for errors."""

    operation: str = ""
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None

    def add_metadata(self, key: str, value: Any) -> ErrorContext:
        """Add metadata to error context."""
        self.metadata[key] = value
        return self

    def with_operation(self, operation: str) -> ErrorContext:
        """Set the operation context."""
        self.operation = operation
        return self

    def with_user(self, user_id: str) -> ErrorContext:
        """Set the user context."""
        self.user_id = user_id
        return self

    def with_correlation(self, correlation_id: str) -> ErrorContext:
        """Set the correlation ID."""
        self.correlation_id = correlation_id
        return self


class CoachProException(Exception):
    """
    Base exception for all CoachPro application errors.

    Provides structured error handling with context, severity,
    and recovery information.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "COACHPRO_ERROR",
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[ErrorContext] = None,
        inner_exception: Optional[Exception] = None,
        recoverable: bool = False,
        user_message: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext()
        self.inner_exception = inner_exception
        self.recoverable = recoverable
        self.user_message = user_message or message

    def with_context(self, context: ErrorContext) -> CoachProException:
        """Add context to the exception."""
        self.context = context
        return self

    def with_metadata(self, key: str, value: Any) -> CoachProException:
        """Add metadata to exception context."""
        self.context.add_metadata(key, value)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary representation."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "user_message": self.user_message,
            "category": self.category.value,
            "severity": self.severity.value,
            "recoverable": self.recoverable,
            "context": {
                "operation": self.context.operation,
                "user_id": self.context.user_id,
                "correlation_id": self.context.correlation_id,
                "request_id": self.context.request_id,
                "metadata": self.context.metadata,
            },
            "inner_exception": str(self.inner_exception) if self.inner_exception else None,
        }


class ValidationError(CoachProException):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[Dict[str, List[str]]] = None,
        error_code: str = "VALIDATION_ERROR",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            context=context,
            recoverable=True,
        )
        self.field_errors = field_errors or {}

    def add_field_error(self, field: str, error: str) -> ValidationError:
        """Add a field-specific error."""
        if field not in self.field_errors:
            self.field_errors[field] = []
        self.field_errors[field].append(error)
        return self

    def has_field_errors(self) -> bool:
        """Check if there are field-specific errors."""
        return bool(self.field_errors)

    def get_field_errors(self, field: str) -> List[str]:
        """Get errors for a specific field."""
        return self.field_errors.get(field, [])

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with field errors."""
        result = super().to_dict()
        result["field_errors"] = self.field_errors
        return result


class BusinessRuleError(CoachProException):
    """Exception for business rule violations."""

    def __init__(
        self,
        message: str,
        rule_name: str,
        error_code: str = "BUSINESS_RULE_VIOLATION",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.BUSINESS_RULE,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            recoverable=True,
        )
        self.rule_name = rule_name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with rule information."""
        result = super().to_dict()
        result["rule_name"] = self.rule_name
        return result


class NotFoundError(CoachProException):
    """Exception for resource not found errors."""

    def __init__(
        self,
        resource_type: str,
        resource_id: Union[str, int],
        error_code: str = "RESOURCE_NOT_FOUND",
        context: Optional[ErrorContext] = None,
    ):
        message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.NOT_FOUND,
            severity=ErrorSeverity.LOW,
            context=context,
            recoverable=False,
        )
        self.resource_type = resource_type
        self.resource_id = str(resource_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with resource information."""
        result = super().to_dict()
        result.update({
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        })
        return result


class ConflictError(CoachProException):
    """Exception for resource conflict errors."""

    def __init__(
        self,
        message: str,
        conflicting_resource: Optional[str] = None,
        error_code: str = "RESOURCE_CONFLICT",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.CONFLICT,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            recoverable=True,
        )
        self.conflicting_resource = conflicting_resource


class AuthenticationError(CoachProException):
    """Exception for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_FAILED",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            context=context,
            recoverable=False,
            user_message="Please check your credentials and try again.",
        )


class AuthorizationError(CoachProException):
    """Exception for authorization errors."""

    def __init__(
        self,
        message: str = "Access denied",
        required_permission: Optional[str] = None,
        error_code: str = "ACCESS_DENIED",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            context=context,
            recoverable=False,
            user_message="You don't have permission to perform this action.",
        )
        self.required_permission = required_permission


class DatabaseError(CoachProException):
    """Exception for database-related errors."""

    def __init__(
        self,
        message: str,
        operation: str = "unknown",
        table: Optional[str] = None,
        error_code: str = "DATABASE_ERROR",
        context: Optional[ErrorContext] = None,
        inner_exception: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            context=context,
            inner_exception=inner_exception,
            recoverable=True,
            user_message="A database error occurred. Please try again later.",
        )
        self.operation = operation
        self.table = table

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with database information."""
        result = super().to_dict()
        result.update({
            "operation": self.operation,
            "table": self.table,
        })
        return result


class ExternalServiceError(CoachProException):
    """Exception for external service errors."""

    def __init__(
        self,
        service_name: str,
        message: str,
        status_code: Optional[int] = None,
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        context: Optional[ErrorContext] = None,
        inner_exception: Optional[Exception] = None,
    ):
        super().__init__(
            message=f"External service '{service_name}' error: {message}",
            error_code=error_code,
            category=ErrorCategory.EXTERNAL_SERVICE,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            inner_exception=inner_exception,
            recoverable=True,
            user_message="An external service is currently unavailable. Please try again later.",
        )
        self.service_name = service_name
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with service information."""
        result = super().to_dict()
        result.update({
            "service_name": self.service_name,
            "status_code": self.status_code,
        })
        return result


class ConfigurationError(CoachProException):
    """Exception for configuration errors."""

    def __init__(
        self,
        message: str,
        setting_name: Optional[str] = None,
        error_code: str = "CONFIGURATION_ERROR",
        context: Optional[ErrorContext] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            context=context,
            recoverable=False,
        )
        self.setting_name = setting_name


# Exception Handlers and Utilities
class ExceptionHandler:
    """Central exception handler with logging and recovery."""

    def __init__(self):
        self._handlers: Dict[type, callable] = {}

    def register_handler(self, exception_type: type, handler: callable):
        """Register a specific handler for an exception type."""
        self._handlers[exception_type] = handler

    def handle(self, exception: Exception) -> Optional[Any]:
        """Handle an exception using registered handlers."""
        exception_type = type(exception)

        # Direct handler
        if exception_type in self._handlers:
            return self._handlers[exception_type](exception)

        # Parent class handlers
        for registered_type, handler in self._handlers.items():
            if issubclass(exception_type, registered_type):
                return handler(exception)

        # Default handling
        return self._default_handler(exception)

    def _default_handler(self, exception: Exception) -> None:
        """Default exception handling."""
        if isinstance(exception, CoachProException):
            self._log_coachpro_exception(exception)
        else:
            self._log_generic_exception(exception)

    def _log_coachpro_exception(self, exception: CoachProException) -> None:
        """Log CoachPro specific exceptions."""
        print(f"[{exception.severity.value.upper()}] {exception.error_code}: {exception.message}")
        if exception.context.correlation_id:
            print(f"Correlation ID: {exception.context.correlation_id}")

    def _log_generic_exception(self, exception: Exception) -> None:
        """Log generic exceptions."""
        print(f"[ERROR] {type(exception).__name__}: {str(exception)}")


# Global exception handler instance
exception_handler = ExceptionHandler()