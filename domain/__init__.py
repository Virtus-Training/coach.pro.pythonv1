"""
Domain Layer - Core Business Logic and Rules.

This module contains the heart of the CoachPro application:
- Domain entities and value objects
- Business rules and invariants
- Domain services
- Repository interfaces
- Domain events

Following Domain-Driven Design principles, this layer is:
- Independent of external concerns
- Rich with business logic
- Focused on solving business problems
"""

from .entities import (
    AggregateRoot,
    Entity,
    ValueObject,
)
from .events import (
    ClientCreatedEvent,
    NutritionPlanUpdatedEvent,
    SessionCreatedEvent,
)
from .interfaces import (
    IDomainService,
    IRepository,
    ISpecification,
    IUnitOfWork,
)

__all__ = [
    # Interfaces
    "IRepository",
    "IUnitOfWork",
    "IDomainService",
    "ISpecification",
    # Base Classes
    "Entity",
    "AggregateRoot",
    "ValueObject",
    # Domain Events
    "ClientCreatedEvent",
    "SessionCreatedEvent",
    "NutritionPlanUpdatedEvent",
]
