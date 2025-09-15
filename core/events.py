"""
Enterprise Event System for Event-Driven Architecture.

Provides a robust event bus with:
- Type-safe event handling
- Async event processing
- Event middleware pipeline
- Error handling and resilience
- Event replay capabilities
"""

from __future__ import annotations

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

T = TypeVar("T", bound="Event")


@dataclass
class Event:
    """
    Base event class for the event system.

    All domain events should inherit from this class.
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def with_correlation(self, correlation_id: str) -> Event:
        """Create a new event with correlation ID."""
        self.correlation_id = correlation_id
        return self

    def with_causation(self, causation_id: str) -> Event:
        """Create a new event with causation ID."""
        self.causation_id = causation_id
        return self


@dataclass
class DomainEvent(Event):
    """Base class for domain events."""

    aggregate_id: str = ""
    aggregate_type: str = ""
    version: int = 1


# Event Handler Types
EventHandler = Callable[[T], Union[None, Awaitable[None]]]
EventMiddleware = Callable[[Event, Callable], Union[Any, Awaitable[Any]]]


class IEventBus(ABC):
    """Abstract event bus interface."""

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """Publish an event to all registered handlers."""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Subscribe a handler to an event type."""
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Unsubscribe a handler from an event type."""
        pass


class EventBus(IEventBus):
    """
    Professional event bus implementation.

    Features:
    - Type-safe event handling
    - Async and sync handler support
    - Middleware pipeline
    - Error handling with dead letter queue
    - Event replay capabilities
    - Performance monitoring

    Example:
        >>> event_bus = EventBus()
        >>>
        >>> @event_bus.subscribe(UserCreatedEvent)
        >>> async def send_welcome_email(event: UserCreatedEvent):
        >>>     await email_service.send_welcome(event.user_id)
        >>>
        >>> await event_bus.publish(UserCreatedEvent(user_id="123"))
    """

    def __init__(self):
        self._handlers: Dict[Type[Event], List[EventHandler]] = {}
        self._middleware: List[EventMiddleware] = []
        self._dead_letter_queue: List[Event] = []
        self._event_store: List[Event] = []
        self._metrics = EventBusMetrics()

    async def publish(self, event: Event) -> None:
        """Publish an event to all registered handlers."""
        self._event_store.append(event)
        self._metrics.increment_published()

        try:
            # Apply middleware pipeline
            await self._execute_middleware_pipeline(event)

            # Get handlers for this event type
            handlers = self._get_handlers_for_event(event)

            if not handlers:
                self._metrics.increment_no_handlers()
                return

            # Execute handlers concurrently
            tasks = []
            for handler in handlers:
                task = self._execute_handler_safely(handler, event)
                tasks.append(task)

            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            self._metrics.increment_failed()
            await self._handle_publish_error(event, e)

    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Subscribe a handler to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)
        self._metrics.increment_handlers()

    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """Unsubscribe a handler from an event type."""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
                self._metrics.decrement_handlers()
            except ValueError:
                pass  # Handler not found

    def add_middleware(self, middleware: EventMiddleware) -> None:
        """Add middleware to the event processing pipeline."""
        self._middleware.append(middleware)

    def get_events(
        self,
        event_type: Optional[Type[Event]] = None,
        correlation_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Event]:
        """Get events from the event store with optional filtering."""
        events = self._event_store

        if event_type:
            events = [e for e in events if isinstance(e, event_type)]

        if correlation_id:
            events = [e for e in events if e.correlation_id == correlation_id]

        return events[-limit:] if limit else events

    async def replay_events(
        self,
        from_timestamp: Optional[datetime] = None,
        event_types: Optional[List[Type[Event]]] = None,
    ) -> None:
        """Replay events from the event store."""
        events = self._event_store

        if from_timestamp:
            events = [e for e in events if e.timestamp >= from_timestamp]

        if event_types:
            events = [e for e in events if type(e) in event_types]

        for event in events:
            await self.publish(event)

    def get_metrics(self) -> EventBusMetrics:
        """Get event bus performance metrics."""
        return self._metrics

    def _get_handlers_for_event(self, event: Event) -> List[EventHandler]:
        """Get all handlers that can handle this event type."""
        handlers = []
        event_type = type(event)

        # Direct handlers
        if event_type in self._handlers:
            handlers.extend(self._handlers[event_type])

        # Inheritance-based handlers
        for registered_type, type_handlers in self._handlers.items():
            if registered_type != event_type and issubclass(
                event_type, registered_type
            ):
                handlers.extend(type_handlers)

        return handlers

    async def _execute_middleware_pipeline(self, event: Event) -> None:
        """Execute middleware pipeline for event processing."""

        async def final_handler(e: Event):
            pass  # Final handler does nothing

        pipeline = final_handler

        # Build middleware pipeline in reverse order
        for middleware in reversed(self._middleware):
            current_pipeline = pipeline

            async def middleware_handler(
                e: Event, mw=middleware, next_handler=current_pipeline
            ):
                if asyncio.iscoroutinefunction(mw):
                    await mw(e, next_handler)
                else:
                    mw(e, next_handler)

            pipeline = middleware_handler

        await pipeline(event)

    async def _execute_handler_safely(
        self, handler: EventHandler, event: Event
    ) -> None:
        """Execute a handler with error handling."""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)

            self._metrics.increment_handled()

        except Exception as e:
            self._metrics.increment_handler_errors()
            await self._handle_handler_error(handler, event, e)

    async def _handle_publish_error(self, event: Event, error: Exception) -> None:
        """Handle errors during event publishing."""
        self._dead_letter_queue.append(event)
        # Log error (in real implementation, use proper logging)
        print(f"Error publishing event {event.event_id}: {error}")

    async def _handle_handler_error(
        self, handler: EventHandler, event: Event, error: Exception
    ) -> None:
        """Handle errors in event handlers."""
        # Log error (in real implementation, use proper logging)
        print(
            f"Error in handler {handler.__name__} for event {event.event_id}: {error}"
        )


@dataclass
class EventBusMetrics:
    """Metrics for event bus performance monitoring."""

    events_published: int = 0
    events_handled: int = 0
    handler_errors: int = 0
    events_failed: int = 0
    events_no_handlers: int = 0
    total_handlers: int = 0

    def increment_published(self) -> None:
        """Increment published events counter."""
        self.events_published += 1

    def increment_handled(self) -> None:
        """Increment handled events counter."""
        self.events_handled += 1

    def increment_handler_errors(self) -> None:
        """Increment handler errors counter."""
        self.handler_errors += 1

    def increment_failed(self) -> None:
        """Increment failed events counter."""
        self.events_failed += 1

    def increment_no_handlers(self) -> None:
        """Increment no handlers counter."""
        self.events_no_handlers += 1

    def increment_handlers(self) -> None:
        """Increment total handlers counter."""
        self.total_handlers += 1

    def decrement_handlers(self) -> None:
        """Decrement total handlers counter."""
        self.total_handlers = max(0, self.total_handlers - 1)

    @property
    def success_rate(self) -> float:
        """Calculate event handling success rate."""
        if self.events_published == 0:
            return 0.0
        return (self.events_handled / self.events_published) * 100.0

    @property
    def error_rate(self) -> float:
        """Calculate error rate."""
        if self.events_handled == 0:
            return 0.0
        return (self.handler_errors / self.events_handled) * 100.0


# Decorator for easy handler registration
def event_handler(event_bus: EventBus, event_type: Type[T]):
    """
    Decorator for registering event handlers.

    Usage:
        @event_handler(event_bus, UserCreatedEvent)
        async def send_welcome_email(event: UserCreatedEvent):
            await email_service.send_welcome(event.user_id)
    """

    def decorator(func: EventHandler[T]) -> EventHandler[T]:
        event_bus.subscribe(event_type, func)
        return func

    return decorator


# Common middleware implementations
class LoggingMiddleware:
    """Middleware for logging events."""

    async def __call__(self, event: Event, next_handler: Callable) -> None:
        print(f"[EVENT] {type(event).__name__} - {event.event_id}")
        await next_handler(event)


class TimingMiddleware:
    """Middleware for timing event processing."""

    async def __call__(self, event: Event, next_handler: Callable) -> None:
        import time

        start_time = time.time()

        await next_handler(event)

        duration = time.time() - start_time
        print(f"[TIMING] {type(event).__name__} processed in {duration:.3f}s")


class ValidationMiddleware:
    """Middleware for event validation."""

    async def __call__(self, event: Event, next_handler: Callable) -> None:
        # Validate event (implement your validation logic)
        if not event.event_id:
            raise ValueError("Event must have an ID")

        await next_handler(event)
