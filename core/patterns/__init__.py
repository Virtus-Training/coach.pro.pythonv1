"""
Enterprise Design Patterns.

This module contains implementation of common enterprise design patterns:
- Factory Pattern for object creation
- Builder Pattern for complex object construction
- Strategy Pattern for algorithm families
- Command Pattern for action encapsulation
- Observer Pattern for event handling
"""

from .builder import (
    ClientBuilder,
    IBuilder,
    NutritionPlanBuilder,
    SessionBuilder,
    WorkoutPlanBuilder,
)
from .command import (
    CommandInvoker,
    CreateClientCommand,
    GenerateWorkoutCommand,
    ICommand,
    UpdateClientCommand,
)
from .factory import (
    AbstractFactory,
    ClientFactory,
    ExerciseFactory,
    IFactory,
    SessionFactory,
)
from .strategy import (
    IStrategy,
    NutritionCalculationStrategy,
    ProgressTrackingStrategy,
    WorkoutGenerationStrategy,
)

__all__ = [
    # Factory Pattern
    "IFactory",
    "AbstractFactory",
    "ClientFactory",
    "SessionFactory",
    "ExerciseFactory",
    # Builder Pattern
    "IBuilder",
    "ClientBuilder",
    "SessionBuilder",
    "WorkoutPlanBuilder",
    "NutritionPlanBuilder",
    # Strategy Pattern
    "IStrategy",
    "WorkoutGenerationStrategy",
    "NutritionCalculationStrategy",
    "ProgressTrackingStrategy",
    # Command Pattern
    "ICommand",
    "CommandInvoker",
    "CreateClientCommand",
    "UpdateClientCommand",
    "GenerateWorkoutCommand",
]
