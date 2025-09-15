"""
Domain Layer Interfaces.

Defines the contracts that the domain layer expects from external systems.
These interfaces are implemented in the infrastructure layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from core.events import Event

# Type variables for generic interfaces
T = TypeVar("T")  # Entity type
TId = TypeVar("TId")  # ID type


class IRepository(ABC, Generic[T, TId]):
    """
    Generic repository interface for aggregate roots.

    Provides basic CRUD operations and follows the Repository pattern
    to abstract data access concerns from business logic.
    """

    @abstractmethod
    async def get_by_id(self, id: TId) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update existing entity."""
        pass

    @abstractmethod
    async def delete(self, id: TId) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def exists(self, id: TId) -> bool:
        """Check if entity exists."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total entities."""
        pass

    @abstractmethod
    async def find(self, specification: ISpecification[T]) -> List[T]:
        """Find entities matching specification."""
        pass

    @abstractmethod
    async def find_one(self, specification: ISpecification[T]) -> Optional[T]:
        """Find first entity matching specification."""
        pass


class IUnitOfWork(ABC):
    """
    Unit of Work pattern for managing transactions across repositories.

    Maintains a list of objects affected by a business transaction
    and coordinates writing out changes.
    """

    @abstractmethod
    async def begin(self) -> None:
        """Begin a transaction."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        pass

    @abstractmethod
    async def save_changes(self) -> int:
        """Save all changes to the database."""
        pass

    @abstractmethod
    def register_new(self, entity: Any) -> None:
        """Register a new entity."""
        pass

    @abstractmethod
    def register_dirty(self, entity: Any) -> None:
        """Register a dirty entity."""
        pass

    @abstractmethod
    def register_deleted(self, entity: Any) -> None:
        """Register an entity for deletion."""
        pass

    @abstractmethod
    def register_clean(self, entity: Any) -> None:
        """Register a clean entity."""
        pass


class ISpecification(ABC, Generic[T]):
    """
    Specification pattern for encapsulating business rules.

    Allows combining business rules in a composable way
    and reusing them across different contexts.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies this specification."""
        pass

    def and_(self, other: ISpecification[T]) -> ISpecification[T]:
        """Logical AND with another specification."""
        return AndSpecification(self, other)

    def or_(self, other: ISpecification[T]) -> ISpecification[T]:
        """Logical OR with another specification."""
        return OrSpecification(self, other)

    def not_(self) -> ISpecification[T]:
        """Logical NOT of this specification."""
        return NotSpecification(self)


class AndSpecification(ISpecification[T]):
    """AND combination of two specifications."""

    def __init__(self, left: ISpecification[T], right: ISpecification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies both specifications."""
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(
            candidate
        )


class OrSpecification(ISpecification[T]):
    """OR combination of two specifications."""

    def __init__(self, left: ISpecification[T], right: ISpecification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies either specification."""
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(
            candidate
        )


class NotSpecification(ISpecification[T]):
    """NOT negation of a specification."""

    def __init__(self, specification: ISpecification[T]):
        self.specification = specification

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate does not satisfy the specification."""
        return not self.specification.is_satisfied_by(candidate)


class IDomainService(ABC):
    """
    Base interface for domain services.

    Domain services contain business logic that doesn't naturally
    fit within an entity or value object.
    """

    pass


class IClientRepository(IRepository[Any, int]):
    """Repository interface for Client aggregate."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Any]:
        """Get client by email address."""
        pass

    @abstractmethod
    async def get_active_clients(self) -> List[Any]:
        """Get all active clients."""
        pass

    @abstractmethod
    async def get_clients_with_exclusions(
        self, client_id: int
    ) -> tuple[Any, List[int]]:
        """Get client with their exercise exclusions."""
        pass

    @abstractmethod
    async def update_exclusions(self, client_id: int, exercise_ids: List[int]) -> None:
        """Update client exercise exclusions."""
        pass


class ISessionRepository(IRepository[Any, int]):
    """Repository interface for Session aggregate."""

    @abstractmethod
    async def get_by_client_id(self, client_id: int) -> List[Any]:
        """Get sessions for a specific client."""
        pass

    @abstractmethod
    async def get_by_date_range(self, start_date: str, end_date: str) -> List[Any]:
        """Get sessions within date range."""
        pass

    @abstractmethod
    async def get_recent_sessions(self, limit: int = 10) -> List[Any]:
        """Get most recent sessions."""
        pass


class IExerciseRepository(IRepository[Any, int]):
    """Repository interface for Exercise aggregate."""

    @abstractmethod
    async def search_by_name(self, name: str) -> List[Any]:
        """Search exercises by name."""
        pass

    @abstractmethod
    async def get_by_category(self, category: str) -> List[Any]:
        """Get exercises by category."""
        pass

    @abstractmethod
    async def get_by_muscle_group(self, muscle_group: str) -> List[Any]:
        """Get exercises by muscle group."""
        pass

    @abstractmethod
    async def get_by_equipment(self, equipment: str) -> List[Any]:
        """Get exercises by required equipment."""
        pass


class INutritionRepository(IRepository[Any, int]):
    """Repository interface for nutrition-related data."""

    @abstractmethod
    async def get_nutrition_plan_by_client(self, client_id: int) -> Optional[Any]:
        """Get nutrition plan for client."""
        pass

    @abstractmethod
    async def search_foods(self, query: str, limit: int = 20) -> List[Any]:
        """Search food items."""
        pass

    @abstractmethod
    async def get_foods_by_category(self, category: str) -> List[Any]:
        """Get foods by category."""
        pass


class IEmailService(IDomainService):
    """Domain service for email operations."""

    @abstractmethod
    async def send_welcome_email(self, client_email: str, client_name: str) -> bool:
        """Send welcome email to new client."""
        pass

    @abstractmethod
    async def send_session_reminder(self, client_email: str, session_date: str) -> bool:
        """Send session reminder email."""
        pass

    @abstractmethod
    async def send_nutrition_plan(self, client_email: str, plan_data: dict) -> bool:
        """Send nutrition plan via email."""
        pass


class IPDFGenerationService(IDomainService):
    """Domain service for PDF generation."""

    @abstractmethod
    async def generate_session_pdf(self, session_data: dict) -> bytes:
        """Generate session PDF document."""
        pass

    @abstractmethod
    async def generate_nutrition_pdf(self, nutrition_data: dict) -> bytes:
        """Generate nutrition plan PDF."""
        pass

    @abstractmethod
    async def generate_progress_report(self, client_id: int, period: str) -> bytes:
        """Generate client progress report."""
        pass


class IExerciseImportService(IDomainService):
    """Domain service for importing exercises from external sources."""

    @abstractmethod
    async def import_from_wger(self, max_exercises: int = 100) -> int:
        """Import exercises from wger.de API."""
        pass

    @abstractmethod
    async def validate_exercise_data(self, exercise_data: dict) -> bool:
        """Validate imported exercise data."""
        pass


class IWorkoutGenerationService(IDomainService):
    """Domain service for generating personalized workouts."""

    @abstractmethod
    async def generate_workout(
        self,
        client_id: int,
        workout_type: str,
        duration_minutes: int,
        equipment: List[str],
    ) -> dict:
        """Generate personalized workout for client."""
        pass

    @abstractmethod
    async def apply_client_restrictions(
        self,
        client_id: int,
        exercises: List[Any],
    ) -> List[Any]:
        """Filter exercises based on client restrictions."""
        pass


class INutritionCalculationService(IDomainService):
    """Domain service for nutrition calculations."""

    @abstractmethod
    async def calculate_daily_needs(
        self,
        client_id: int,
        goal: str,
    ) -> dict:
        """Calculate daily nutritional needs for client."""
        pass

    @abstractmethod
    async def calculate_meal_macros(self, meals: List[dict]) -> dict:
        """Calculate macronutrients for meals."""
        pass

    @abstractmethod
    async def generate_meal_plan(
        self,
        client_id: int,
        days: int,
        preferences: dict,
    ) -> dict:
        """Generate personalized meal plan."""
        pass


class IAuthenticationService(IDomainService):
    """Domain service for authentication operations."""

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user credentials."""
        pass

    @abstractmethod
    async def generate_token(self, user_data: dict) -> str:
        """Generate authentication token."""
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> Optional[dict]:
        """Validate authentication token."""
        pass


class IEventStore(ABC):
    """Interface for event sourcing store."""

    @abstractmethod
    async def append_events(self, stream_id: str, events: List[Event]) -> None:
        """Append events to stream."""
        pass

    @abstractmethod
    async def get_events(self, stream_id: str, from_version: int = 0) -> List[Event]:
        """Get events from stream."""
        pass

    @abstractmethod
    async def get_stream_version(self, stream_id: str) -> int:
        """Get current stream version."""
        pass


class ICache(ABC, Generic[T]):
    """Interface for caching operations."""

    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: T, ttl_seconds: Optional[int] = None) -> None:
        """Set value in cache."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache entries."""
        pass


class IConfigurationService(ABC):
    """Interface for configuration management."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get configuration setting."""
        pass

    @abstractmethod
    def get_connection_string(self, name: str) -> str:
        """Get database connection string."""
        pass

    @abstractmethod
    def get_feature_flag(self, flag_name: str) -> bool:
        """Get feature flag status."""
        pass

    @abstractmethod
    def is_development(self) -> bool:
        """Check if running in development mode."""
        pass

    @abstractmethod
    def is_production(self) -> bool:
        """Check if running in production mode."""
        pass
