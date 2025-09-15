"""
Async Repository Interfaces.

Defines async interfaces for data access layer with enterprise patterns:
- Async/await support for all I/O operations
- Generic repository patterns with type safety
- Unit of Work pattern for transactions
- Specification pattern for complex queries
- Performance monitoring and caching integration
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from dataclasses import dataclass
from datetime import datetime

from domain.entities import Client, Session, Exercise
from domain.value_objects import PersonalInfo, PhysicalProfile

T = TypeVar("T")
TEntity = TypeVar("TEntity")
TId = TypeVar("TId", int, str)


@dataclass
class QueryResult(Generic[T]):
    """Result wrapper with metadata for query operations."""

    data: List[T]
    total_count: int
    page: int = 1
    page_size: int = 50
    has_next: bool = False
    has_previous: bool = False
    execution_time_ms: float = 0.0
    cache_hit: bool = False

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        return (self.total_count + self.page_size - 1) // self.page_size


@dataclass
class QueryOptions:
    """Options for query execution."""

    page: int = 1
    page_size: int = 50
    sort_by: Optional[str] = None
    sort_desc: bool = False
    include_deleted: bool = False
    use_cache: bool = True
    cache_ttl: int = 300  # 5 minutes
    track_performance: bool = True


@dataclass
class RepositoryMetrics:
    """Repository performance metrics."""

    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_query_time_ms: float = 0.0
    slow_queries: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        return (self.successful_queries / self.total_queries * 100) if self.total_queries > 0 else 0.0

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate percentage."""
        total_cache_ops = self.cache_hits + self.cache_misses
        return (self.cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0.0


class ISpecification(ABC, Generic[T]):
    """Specification pattern for complex query logic."""

    @abstractmethod
    def is_satisfied_by(self, entity: T) -> bool:
        """Check if entity satisfies the specification."""
        pass

    @abstractmethod
    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        """Convert specification to SQL WHERE clause with parameters."""
        pass

    def and_specification(self, other: ISpecification[T]) -> AndSpecification[T]:
        """Combine with another specification using AND logic."""
        return AndSpecification(self, other)

    def or_specification(self, other: ISpecification[T]) -> OrSpecification[T]:
        """Combine with another specification using OR logic."""
        return OrSpecification(self, other)

    def not_specification(self) -> NotSpecification[T]:
        """Negate this specification."""
        return NotSpecification(self)


class AndSpecification(ISpecification[T]):
    """Combines two specifications with AND logic."""

    def __init__(self, left: ISpecification[T], right: ISpecification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, entity: T) -> bool:
        return self.left.is_satisfied_by(entity) and self.right.is_satisfied_by(entity)

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        left_sql, left_params = self.left.to_sql_where()
        right_sql, right_params = self.right.to_sql_where()
        return f"({left_sql}) AND ({right_sql})", left_params + right_params


class OrSpecification(ISpecification[T]):
    """Combines two specifications with OR logic."""

    def __init__(self, left: ISpecification[T], right: ISpecification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, entity: T) -> bool:
        return self.left.is_satisfied_by(entity) or self.right.is_satisfied_by(entity)

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        left_sql, left_params = self.left.to_sql_where()
        right_sql, right_params = self.right.to_sql_where()
        return f"({left_sql}) OR ({right_sql})", left_params + right_params


class NotSpecification(ISpecification[T]):
    """Negates a specification."""

    def __init__(self, specification: ISpecification[T]):
        self.specification = specification

    def is_satisfied_by(self, entity: T) -> bool:
        return not self.specification.is_satisfied_by(entity)

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        sql, params = self.specification.to_sql_where()
        return f"NOT ({sql})", params


class IAsyncRepository(ABC, Generic[TEntity, TId]):
    """
    Generic async repository interface with enterprise patterns.

    Provides complete CRUD operations with:
    - Async/await support for all operations
    - Performance monitoring and caching
    - Specification pattern for complex queries
    - Pagination and sorting
    - Soft delete support
    - Transaction integration
    """

    @abstractmethod
    async def get_by_id(
        self,
        entity_id: TId,
        options: Optional[QueryOptions] = None
    ) -> Optional[TEntity]:
        """Get entity by ID with optional caching."""
        pass

    @abstractmethod
    async def get_all(
        self,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[TEntity]:
        """Get all entities with pagination and sorting."""
        pass

    @abstractmethod
    async def find(
        self,
        specification: ISpecification[TEntity],
        options: Optional[QueryOptions] = None
    ) -> QueryResult[TEntity]:
        """Find entities matching specification."""
        pass

    @abstractmethod
    async def create(self, entity: TEntity) -> TEntity:
        """Create new entity."""
        pass

    @abstractmethod
    async def update(self, entity: TEntity) -> TEntity:
        """Update existing entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: TId) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def soft_delete(self, entity_id: TId) -> bool:
        """Soft delete entity by ID."""
        pass

    @abstractmethod
    async def exists(self, entity_id: TId) -> bool:
        """Check if entity exists by ID."""
        pass

    @abstractmethod
    async def count(
        self,
        specification: Optional[ISpecification[TEntity]] = None
    ) -> int:
        """Count entities matching specification."""
        pass

    @abstractmethod
    async def batch_create(self, entities: List[TEntity]) -> List[TEntity]:
        """Create multiple entities in batch."""
        pass

    @abstractmethod
    async def batch_update(self, entities: List[TEntity]) -> List[TEntity]:
        """Update multiple entities in batch."""
        pass

    @abstractmethod
    async def batch_delete(self, entity_ids: List[TId]) -> int:
        """Delete multiple entities in batch."""
        pass

    @abstractmethod
    async def get_metrics(self) -> RepositoryMetrics:
        """Get repository performance metrics."""
        pass

    @abstractmethod
    async def clear_cache(self, pattern: Optional[str] = None) -> None:
        """Clear repository cache."""
        pass


class IAsyncClientRepository(IAsyncRepository[Client, int]):
    """
    Async Client repository interface with domain-specific operations.
    """

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Client]:
        """Find client by email address."""
        pass

    @abstractmethod
    async def find_by_name(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> QueryResult[Client]:
        """Find clients by name with partial matching."""
        pass

    @abstractmethod
    async def find_active_clients(
        self,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Client]:
        """Find all active clients."""
        pass

    @abstractmethod
    async def find_clients_with_sessions_in_period(
        self,
        start_date: datetime,
        end_date: datetime,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Client]:
        """Find clients with sessions in date range."""
        pass

    @abstractmethod
    async def get_client_statistics(self, client_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics for a client."""
        pass

    @abstractmethod
    async def update_physical_profile(
        self,
        client_id: int,
        physical_profile: PhysicalProfile
    ) -> bool:
        """Update client's physical profile."""
        pass

    @abstractmethod
    async def archive_inactive_clients(self, days_inactive: int = 90) -> int:
        """Archive clients inactive for specified days."""
        pass


class IAsyncSessionRepository(IAsyncRepository[Session, int]):
    """
    Async Session repository interface with workout-specific operations.
    """

    @abstractmethod
    async def find_by_client(
        self,
        client_id: int,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find sessions by client ID."""
        pass

    @abstractmethod
    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        client_id: Optional[int] = None,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find sessions in date range."""
        pass

    @abstractmethod
    async def find_upcoming_sessions(
        self,
        client_id: Optional[int] = None,
        days_ahead: int = 7,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find upcoming sessions."""
        pass

    @abstractmethod
    async def find_completed_sessions(
        self,
        client_id: Optional[int] = None,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find completed sessions."""
        pass

    @abstractmethod
    async def get_session_analytics(
        self,
        client_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get session analytics and metrics."""
        pass

    @abstractmethod
    async def clone_session(
        self,
        session_id: int,
        new_date: datetime
    ) -> Session:
        """Clone existing session for new date."""
        pass

    @abstractmethod
    async def bulk_schedule_sessions(
        self,
        template_session_id: int,
        dates: List[datetime],
        client_id: Optional[int] = None
    ) -> List[Session]:
        """Bulk schedule sessions from template."""
        pass


class IAsyncExerciseRepository(IAsyncRepository[Exercise, int]):
    """
    Async Exercise repository interface with exercise-specific operations.
    """

    @abstractmethod
    async def find_by_category(
        self,
        category: str,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Exercise]:
        """Find exercises by category."""
        pass

    @abstractmethod
    async def find_by_muscle_group(
        self,
        muscle_group: str,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Exercise]:
        """Find exercises by muscle group."""
        pass

    @abstractmethod
    async def search_by_name(
        self,
        search_term: str,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Exercise]:
        """Search exercises by name."""
        pass

    @abstractmethod
    async def find_by_equipment(
        self,
        equipment: str,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Exercise]:
        """Find exercises by equipment."""
        pass

    @abstractmethod
    async def find_popular_exercises(
        self,
        limit: int = 20,
        days_back: int = 30
    ) -> List[Exercise]:
        """Find most popular exercises."""
        pass

    @abstractmethod
    async def get_exercise_usage_stats(
        self,
        exercise_id: int
    ) -> Dict[str, Any]:
        """Get usage statistics for an exercise."""
        pass

    @abstractmethod
    async def find_similar_exercises(
        self,
        exercise_id: int,
        limit: int = 5
    ) -> List[Exercise]:
        """Find similar exercises based on muscle groups and movement patterns."""
        pass

    @abstractmethod
    async def bulk_import_exercises(
        self,
        exercise_data: List[Dict[str, Any]]
    ) -> List[Exercise]:
        """Bulk import exercises from data."""
        pass


class IAsyncUnitOfWork(ABC):
    """
    Unit of Work pattern for managing transactions across repositories.

    Ensures data consistency across multiple repository operations
    within a single transaction boundary.
    """

    # Repository properties
    clients: IAsyncClientRepository
    sessions: IAsyncSessionRepository
    exercises: IAsyncExerciseRepository

    @abstractmethod
    async def __aenter__(self) -> IAsyncUnitOfWork:
        """Enter async context and begin transaction."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context and handle transaction commit/rollback."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit all pending changes."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback all pending changes."""
        pass

    @abstractmethod
    async def save_changes(self) -> int:
        """Save all changes and return number of affected rows."""
        pass


# Common Specifications for reuse across repositories

class ActiveEntitySpecification(ISpecification[T]):
    """Specification for active (non-deleted) entities."""

    def is_satisfied_by(self, entity: T) -> bool:
        return getattr(entity, 'is_active', True) and not getattr(entity, 'is_deleted', False)

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "is_active = 1 AND is_deleted = 0", ()


class DateRangeSpecification(ISpecification[T]):
    """Specification for entities within a date range."""

    def __init__(self, start_date: datetime, end_date: datetime, date_field: str = 'created_at'):
        self.start_date = start_date
        self.end_date = end_date
        self.date_field = date_field

    def is_satisfied_by(self, entity: T) -> bool:
        entity_date = getattr(entity, self.date_field, None)
        return entity_date and self.start_date <= entity_date <= self.end_date

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return f"{self.date_field} BETWEEN ? AND ?", (self.start_date, self.end_date)


class TextSearchSpecification(ISpecification[T]):
    """Specification for text search across multiple fields."""

    def __init__(self, search_term: str, fields: List[str]):
        self.search_term = search_term.lower()
        self.fields = fields

    def is_satisfied_by(self, entity: T) -> bool:
        for field in self.fields:
            value = getattr(entity, field, '')
            if value and self.search_term in str(value).lower():
                return True
        return False

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        conditions = [f"LOWER({field}) LIKE ?" for field in self.fields]
        search_pattern = f"%{self.search_term}%"
        return f"({' OR '.join(conditions)})", tuple([search_pattern] * len(self.fields))


class PaginationSpecification(ISpecification[T]):
    """Specification for pagination logic."""

    def __init__(self, page: int, page_size: int):
        self.page = max(1, page)
        self.page_size = max(1, page_size)
        self.offset = (self.page - 1) * self.page_size

    def is_satisfied_by(self, entity: T) -> bool:
        # Not applicable for in-memory filtering
        return True

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "1=1", ()  # Pagination handled in LIMIT/OFFSET

    def to_sql_limit(self) -> tuple[str, tuple[Any, ...]]:
        """Get SQL LIMIT clause for pagination."""
        return "LIMIT ? OFFSET ?", (self.page_size, self.offset)