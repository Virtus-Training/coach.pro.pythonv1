"""
Enterprise Design Patterns.

This module contains implementation of common enterprise design patterns:
- Factory Pattern for object creation
- Builder Pattern for complex object construction
- Strategy Pattern for algorithm families
- Command Pattern for action encapsulation
- Observer Pattern for event handling
"""

from .factory import (
    IFactory,
    AbstractFactory,
    ClientFactory,
    SessionFactory,
    ExerciseFactory,
)
from .builder import (
    IBuilder,
    ClientBuilder,
    SessionBuilder,
    WorkoutPlanBuilder,
    NutritionPlanBuilder,
)
from .strategy import (
    IStrategy,
    WorkoutGenerationStrategy,
    NutritionCalculationStrategy,
    ProgressTrackingStrategy,
)
from .command import (
    ICommand,
    CommandInvoker,
    CreateClientCommand,
    UpdateClientCommand,
    GenerateWorkoutCommand,
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