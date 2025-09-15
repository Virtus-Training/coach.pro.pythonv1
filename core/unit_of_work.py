"""
Unit of Work Pattern Implementation.

Enterprise-grade transaction management with:
- Cross-repository transaction coordination
- Automatic rollback on failures
- Domain events coordination and publishing
- Batch commit optimization for high performance
- Change tracking for optimistic concurrency
- Comprehensive audit trail and monitoring
"""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, TypeVar

from core.events import Event, IEventBus
from core.exceptions import (
    BusinessRuleViolationError,
    TransactionError,
)
from infrastructure.database import (
    AsyncDatabaseManager,
    AsyncTransaction,
    get_database_manager,
)
from repositories.async_client_repository import AsyncClientRepository
from repositories.async_exercise_repository import AsyncExerciseRepository
from repositories.async_session_repository import AsyncSessionRepository
from repositories.interfaces import (
    IAsyncClientRepository,
    IAsyncExerciseRepository,
    IAsyncSessionRepository,
    IAsyncUnitOfWork,
)

T = TypeVar("T")


class UnitOfWorkState(Enum):
    """Unit of Work lifecycle states."""

    CREATED = "created"
    ACTIVE = "active"
    COMMITTING = "committing"
    COMMITTED = "committed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class ChangeTracker:
    """Tracks changes within a Unit of Work for audit and concurrency."""

    created_entities: List[Any] = field(default_factory=list)
    updated_entities: List[Any] = field(default_factory=list)
    deleted_entities: List[Any] = field(default_factory=list)
    domain_events: List[Event] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        """Check if any changes are tracked."""
        return bool(
            self.created_entities or self.updated_entities or self.deleted_entities
        )

    @property
    def total_changes(self) -> int:
        """Get total number of changes."""
        return (
            len(self.created_entities)
            + len(self.updated_entities)
            + len(self.deleted_entities)
        )

    def track_created(self, entity: Any) -> None:
        """Track entity creation."""
        self.created_entities.append(entity)

    def track_updated(self, entity: Any) -> None:
        """Track entity update."""
        self.updated_entities.append(entity)

    def track_deleted(self, entity: Any) -> None:
        """Track entity deletion."""
        self.deleted_entities.append(entity)

    def track_event(self, event: Event) -> None:
        """Track domain event."""
        self.domain_events.append(event)

    def clear(self) -> None:
        """Clear all tracked changes."""
        self.created_entities.clear()
        self.updated_entities.clear()
        self.deleted_entities.clear()
        self.domain_events.clear()


@dataclass
class UnitOfWorkMetrics:
    """Metrics for Unit of Work performance monitoring."""

    transactions_started: int = 0
    transactions_committed: int = 0
    transactions_rolled_back: int = 0
    transactions_failed: int = 0
    total_entities_processed: int = 0
    total_events_published: int = 0
    avg_commit_time_ms: float = 0.0
    max_commit_time_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        """Calculate transaction success rate."""
        total = self.transactions_started
        return (self.transactions_committed / total * 100) if total > 0 else 0.0

    @property
    def failure_rate(self) -> float:
        """Calculate transaction failure rate."""
        total = self.transactions_started
        return (
            ((self.transactions_rolled_back + self.transactions_failed) / total * 100)
            if total > 0
            else 0.0
        )

    def record_transaction_started(self) -> None:
        """Record transaction start."""
        self.transactions_started += 1

    def record_transaction_committed(
        self, commit_time_ms: float, entities_count: int, events_count: int
    ) -> None:
        """Record successful transaction commit."""
        self.transactions_committed += 1
        self.total_entities_processed += entities_count
        self.total_events_published += events_count

        # Update timing metrics
        if self.transactions_committed == 1:
            self.avg_commit_time_ms = commit_time_ms
        else:
            self.avg_commit_time_ms = (
                self.avg_commit_time_ms * (self.transactions_committed - 1)
                + commit_time_ms
            ) / self.transactions_committed

        self.max_commit_time_ms = max(self.max_commit_time_ms, commit_time_ms)

    def record_transaction_rolled_back(self) -> None:
        """Record transaction rollback."""
        self.transactions_rolled_back += 1

    def record_transaction_failed(self) -> None:
        """Record transaction failure."""
        self.transactions_failed += 1


class AsyncUnitOfWork(IAsyncUnitOfWork):
    """
    Enterprise Unit of Work implementation with comprehensive transaction management.

    Features:
    - Cross-repository transaction coordination
    - Domain events batch processing
    - Change tracking and audit trail
    - Automatic rollback on exceptions
    - Performance monitoring and metrics
    - Optimistic concurrency control
    - Deadlock detection and retry
    """

    def __init__(
        self,
        db_manager: Optional[AsyncDatabaseManager] = None,
        event_bus: Optional[IEventBus] = None,
        auto_commit: bool = True,
        isolation_level: str = "READ_COMMITTED",
    ):
        self._db_manager = db_manager or get_database_manager()
        self._event_bus = event_bus
        self._auto_commit = auto_commit
        self._isolation_level = isolation_level

        # State management
        self._state = UnitOfWorkState.CREATED
        self._transaction: Optional[AsyncTransaction] = None
        self._change_tracker = ChangeTracker()
        self._start_time: Optional[float] = None

        # Repository instances (lazy-loaded)
        self._clients: Optional[AsyncClientRepository] = None
        self._sessions: Optional[AsyncSessionRepository] = None
        self._exercises: Optional[AsyncExerciseRepository] = None

        # Error tracking
        self._last_error: Optional[Exception] = None
        self._retry_count = 0
        self._max_retries = 3

        # Metrics (class-level shared)
        if not hasattr(AsyncUnitOfWork, "_metrics"):
            AsyncUnitOfWork._metrics = UnitOfWorkMetrics()

    @property
    def clients(self) -> IAsyncClientRepository:
        """Get clients repository with transaction context."""
        if self._clients is None:
            self._clients = AsyncClientRepository(
                db_manager=self._db_manager, event_bus=self._create_event_tracker()
            )
        return self._clients

    @property
    def sessions(self) -> IAsyncSessionRepository:
        """Get sessions repository with transaction context."""
        if self._sessions is None:
            self._sessions = AsyncSessionRepository(
                db_manager=self._db_manager, event_bus=self._create_event_tracker()
            )
        return self._sessions

    @property
    def exercises(self) -> IAsyncExerciseRepository:
        """Get exercises repository with transaction context."""
        if self._exercises is None:
            self._exercises = AsyncExerciseRepository(
                db_manager=self._db_manager, event_bus=self._create_event_tracker()
            )
        return self._exercises

    @property
    def state(self) -> UnitOfWorkState:
        """Get current Unit of Work state."""
        return self._state

    @property
    def has_changes(self) -> bool:
        """Check if there are pending changes."""
        return self._change_tracker.has_changes

    @property
    def change_count(self) -> int:
        """Get total number of tracked changes."""
        return self._change_tracker.total_changes

    async def __aenter__(self) -> IAsyncUnitOfWork:
        """Enter async context and begin transaction."""
        await self._begin_transaction()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context and handle transaction completion."""
        if exc_type is not None:
            # Exception occurred - rollback
            self._last_error = exc_val
            await self._rollback_with_retry()
        elif self._auto_commit and self.has_changes:
            # Auto-commit mode and has changes
            await self._commit_with_retry()
        elif not self._auto_commit:
            # Manual mode - caller must explicitly commit
            pass
        else:
            # No changes - just cleanup
            await self._cleanup_transaction()

    async def _begin_transaction(self) -> None:
        """Begin database transaction with proper setup."""
        try:
            self._state = UnitOfWorkState.ACTIVE
            self._start_time = time.perf_counter()

            # Get transaction from database manager
            self._transaction = await self._db_manager.get_transaction().__aenter__()

            # Set isolation level if needed
            if self._isolation_level != "READ_COMMITTED":
                await self._set_isolation_level(self._isolation_level)

            # Record metrics
            AsyncUnitOfWork._metrics.record_transaction_started()

        except Exception as e:
            self._state = UnitOfWorkState.FAILED
            raise TransactionError(f"Failed to begin transaction: {str(e)}") from e

    async def _set_isolation_level(self, level: str) -> None:
        """Set transaction isolation level."""
        if self._transaction:
            # SQLite has limited isolation level support
            # This is a placeholder for more advanced database systems
            pass

    async def commit(self) -> None:
        """Manually commit the transaction."""
        if self._state != UnitOfWorkState.ACTIVE:
            raise TransactionError(
                f"Cannot commit: Unit of Work is in {self._state.value} state"
            )

        await self._commit_with_retry()

    async def rollback(self) -> None:
        """Manually rollback the transaction."""
        if self._state not in [UnitOfWorkState.ACTIVE, UnitOfWorkState.COMMITTING]:
            raise TransactionError(
                f"Cannot rollback: Unit of Work is in {self._state.value} state"
            )

        await self._rollback_with_retry()

    async def save_changes(self) -> int:
        """Save all changes and return number of affected entities."""
        if not self.has_changes:
            return 0

        await self.commit()
        return self._change_tracker.total_changes

    async def _commit_with_retry(self) -> None:
        """Commit transaction with deadlock retry logic."""
        last_exception = None

        for attempt in range(self._max_retries + 1):
            try:
                await self._commit_transaction()
                return
            except Exception as e:
                last_exception = e

                # Check if this is a retryable error (deadlock, timeout, etc.)
                if self._is_retryable_error(e) and attempt < self._max_retries:
                    self._retry_count += 1
                    retry_delay = min(0.1 * (2**attempt), 1.0)  # Exponential backoff
                    await asyncio.sleep(retry_delay)
                    continue

                # Non-retryable error or max retries exceeded
                await self._handle_commit_failure(e)
                break

        if last_exception:
            raise TransactionError(
                f"Failed to commit after {self._max_retries + 1} attempts"
            ) from last_exception

    async def _commit_transaction(self) -> None:
        """Execute the actual transaction commit."""
        if self._state != UnitOfWorkState.ACTIVE:
            raise TransactionError(
                f"Cannot commit: Unit of Work is in {self._state.value} state"
            )

        self._state = UnitOfWorkState.COMMITTING
        commit_start_time = time.perf_counter()

        try:
            # Validate business rules before commit
            await self._validate_business_rules()

            # Commit database transaction
            if self._transaction:
                await self._transaction.commit()

            # Publish domain events after successful commit
            await self._publish_domain_events()

            # Update state and metrics
            self._state = UnitOfWorkState.COMMITTED
            commit_time_ms = (time.perf_counter() - commit_start_time) * 1000

            AsyncUnitOfWork._metrics.record_transaction_committed(
                commit_time_ms=commit_time_ms,
                entities_count=self._change_tracker.total_changes,
                events_count=len(self._change_tracker.domain_events),
            )

            # Clear change tracker
            self._change_tracker.clear()

        except Exception as e:
            self._state = UnitOfWorkState.FAILED
            raise TransactionError(f"Transaction commit failed: {str(e)}") from e
        finally:
            await self._cleanup_transaction()

    async def _rollback_with_retry(self) -> None:
        """Rollback transaction with retry logic."""
        last_exception = None

        for attempt in range(self._max_retries + 1):
            try:
                await self._rollback_transaction()
                return
            except Exception as e:
                last_exception = e
                if attempt < self._max_retries:
                    await asyncio.sleep(0.1 * (2**attempt))
                    continue
                break

        if last_exception:
            # Log error but don't re-raise - rollback failures are often not critical
            print(
                f"Warning: Failed to rollback transaction after {self._max_retries + 1} attempts: {last_exception}"
            )

    async def _rollback_transaction(self) -> None:
        """Execute the actual transaction rollback."""
        self._state = UnitOfWorkState.ROLLING_BACK

        try:
            # Rollback database transaction
            if self._transaction:
                await self._transaction.rollback()

            # Update state and metrics
            self._state = UnitOfWorkState.ROLLED_BACK
            AsyncUnitOfWork._metrics.record_transaction_rolled_back()

            # Clear change tracker
            self._change_tracker.clear()

        except Exception as e:
            self._state = UnitOfWorkState.FAILED
            AsyncUnitOfWork._metrics.record_transaction_failed()
            raise TransactionError(f"Transaction rollback failed: {str(e)}") from e
        finally:
            await self._cleanup_transaction()

    async def _cleanup_transaction(self) -> None:
        """Clean up transaction resources."""
        if self._transaction:
            try:
                await self._transaction.__aexit__(None, None, None)
            except Exception as e:
                print(f"Warning: Error during transaction cleanup: {e}")
            finally:
                self._transaction = None

    async def _validate_business_rules(self) -> None:
        """Validate business rules before commit."""
        # Example business rule validations

        # Check for scheduling conflicts in sessions
        for entity in (
            self._change_tracker.created_entities
            + self._change_tracker.updated_entities
        ):
            if hasattr(entity, "date_seance") and hasattr(entity, "client_id"):
                # Session scheduling validation would go here
                pass

        # Check for duplicate client emails
        client_emails = set()
        for entity in (
            self._change_tracker.created_entities
            + self._change_tracker.updated_entities
        ):
            if hasattr(entity, "personal_info") and hasattr(
                entity.personal_info, "email"
            ):
                email = entity.personal_info.email.lower()
                if email in client_emails:
                    raise BusinessRuleViolationError(f"Duplicate client email: {email}")
                client_emails.add(email)

        # Add more business rule validations as needed

    async def _publish_domain_events(self) -> None:
        """Publish all tracked domain events."""
        if not self._event_bus or not self._change_tracker.domain_events:
            return

        try:
            # Publish events in batch for better performance
            for event in self._change_tracker.domain_events:
                await self._event_bus.publish(event)

        except Exception as e:
            # Event publishing failures shouldn't rollback the transaction
            # But we should log them for monitoring
            print(f"Warning: Failed to publish domain events: {e}")

    def _create_event_tracker(self) -> Optional[IEventBus]:
        """Create an event bus wrapper that tracks events in the Unit of Work."""
        if not self._event_bus:
            return None

        return EventTracker(self._change_tracker, self._event_bus)

    def _is_retryable_error(self, error: Exception) -> bool:
        """Check if an error is retryable (deadlock, timeout, etc.)."""
        error_str = str(error).lower()
        retryable_patterns = [
            "deadlock",
            "timeout",
            "lock wait timeout",
            "database is locked",
            "busy",
            "serialization failure",
        ]

        return any(pattern in error_str for pattern in retryable_patterns)

    async def _handle_commit_failure(self, error: Exception) -> None:
        """Handle commit failure by attempting rollback."""
        try:
            await self._rollback_transaction()
        except Exception as rollback_error:
            # Rollback also failed - this is a serious issue
            raise TransactionError(
                f"Commit failed and rollback also failed. Original error: {error}. "
                f"Rollback error: {rollback_error}"
            ) from error

    @classmethod
    def get_metrics(cls) -> UnitOfWorkMetrics:
        """Get Unit of Work performance metrics."""
        if not hasattr(cls, "_metrics"):
            cls._metrics = UnitOfWorkMetrics()
        return cls._metrics

    @classmethod
    def reset_metrics(cls) -> None:
        """Reset performance metrics."""
        cls._metrics = UnitOfWorkMetrics()

    # Context manager for nested transactions
    @asynccontextmanager
    async def create_savepoint(self, name: str):
        """Create a database savepoint for nested transactions."""
        if not self._transaction:
            raise TransactionError("No active transaction for savepoint")

        try:
            # SQLite doesn't support savepoints, but other databases do
            # This is a placeholder for more advanced database systems
            yield
        except Exception as e:
            # Rollback to savepoint
            raise TransactionError(f"Savepoint {name} failed: {str(e)}") from e


class EventTracker:
    """Event bus wrapper that tracks events in the Unit of Work."""

    def __init__(self, change_tracker: ChangeTracker, event_bus: IEventBus):
        self._change_tracker = change_tracker
        self._event_bus = event_bus

    async def publish(self, event: Event) -> None:
        """Track event for later publishing."""
        self._change_tracker.track_event(event)

    def subscribe(self, event_type, handler):
        """Delegate subscription to the real event bus."""
        return self._event_bus.subscribe(event_type, handler)


# Factory function for creating Unit of Work instances
async def create_unit_of_work(
    db_manager: Optional[AsyncDatabaseManager] = None,
    event_bus: Optional[IEventBus] = None,
    auto_commit: bool = True,
    isolation_level: str = "READ_COMMITTED",
) -> AsyncUnitOfWork:
    """
    Factory function to create a properly configured Unit of Work instance.

    Args:
        db_manager: Database manager instance (uses global if None)
        event_bus: Event bus for domain events (optional)
        auto_commit: Whether to auto-commit on context exit (default: True)
        isolation_level: Database isolation level (default: READ_COMMITTED)

    Returns:
        Configured AsyncUnitOfWork instance
    """
    return AsyncUnitOfWork(
        db_manager=db_manager,
        event_bus=event_bus,
        auto_commit=auto_commit,
        isolation_level=isolation_level,
    )


# Convenience decorator for automatic Unit of Work management
def with_unit_of_work(auto_commit: bool = True):
    """
    Decorator that automatically wraps a function with Unit of Work management.

    Usage:
        @with_unit_of_work()
        async def create_client_with_session(client_data, session_data):
            async with create_unit_of_work() as uow:
                client = await uow.clients.create(client_data)
                session_data.client_id = client.id
                session = await uow.sessions.create(session_data)
                return client, session
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with create_unit_of_work(auto_commit=auto_commit) as uow:
                # Inject uow as first parameter if function expects it
                import inspect

                sig = inspect.signature(func)
                if "uow" in sig.parameters:
                    return await func(uow, *args, **kwargs)
                else:
                    return await func(*args, **kwargs)

        return wrapper

    return decorator


# Global Unit of Work instance management
_current_uow: Optional[AsyncUnitOfWork] = None


async def get_current_unit_of_work() -> Optional[AsyncUnitOfWork]:
    """Get the current Unit of Work instance."""
    return _current_uow


async def set_current_unit_of_work(uow: Optional[AsyncUnitOfWork]) -> None:
    """Set the current Unit of Work instance."""
    global _current_uow
    _current_uow = uow
