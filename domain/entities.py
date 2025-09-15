"""
Domain Entities and Value Objects.

Contains the core business entities that represent the main concepts
in the CoachPro domain, following DDD principles.
"""

from __future__ import annotations

import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional, Set

from core.events import DomainEvent


class Entity(ABC):
    """
    Base class for all domain entities.

    Entities have identity and their equality is based on their ID,
    not their attributes.
    """

    def __init__(self, id: Optional[Any] = None):
        self._id = id or self._generate_id()
        self._domain_events: List[DomainEvent] = []

    @property
    def id(self) -> Any:
        """Get entity ID."""
        return self._id

    def _generate_id(self) -> str:
        """Generate a new ID for the entity."""
        return str(uuid.uuid4())

    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published."""
        self._domain_events.append(event)

    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events."""
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        """Clear all domain events."""
        self._domain_events.clear()

    def __eq__(self, other: object) -> bool:
        """Entity equality based on ID."""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)


class AggregateRoot(Entity):
    """
    Base class for aggregate roots.

    Aggregate roots are the entry points to aggregates and are responsible
    for maintaining consistency within the aggregate boundary.
    """

    def __init__(self, id: Optional[Any] = None):
        super().__init__(id)
        self._version = 0

    @property
    def version(self) -> int:
        """Get aggregate version for optimistic concurrency control."""
        return self._version

    def increment_version(self) -> None:
        """Increment version after changes."""
        self._version += 1


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Base class for value objects.

    Value objects have no identity and their equality is based on
    their attributes. They are immutable.
    """

    def __eq__(self, other: object) -> bool:
        """Value object equality based on all attributes."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Hash based on all attributes."""
        return hash(tuple(sorted(self.__dict__.items())))


# Client Domain
@dataclass(frozen=True)
class PersonalInfo(ValueObject):
    """Value object representing personal information."""

    first_name: str
    last_name: str
    email: str
    birth_date: Optional[datetime] = None
    phone: Optional[str] = None

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    def __post_init__(self):
        """Validate personal info."""
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email format")


@dataclass(frozen=True)
class PhysicalProfile(ValueObject):
    """Value object representing physical characteristics."""

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None

    @property
    def bmi(self) -> Optional[float]:
        """Calculate BMI if height and weight are available."""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return self.weight_kg / (height_m**2)
        return None

    def __post_init__(self):
        """Validate physical profile."""
        if self.height_cm is not None and self.height_cm <= 0:
            raise ValueError("Height must be positive")
        if self.weight_kg is not None and self.weight_kg <= 0:
            raise ValueError("Weight must be positive")
        if (
            self.body_fat_percentage is not None
            and not 0 <= self.body_fat_percentage <= 100
        ):
            raise ValueError("Body fat percentage must be between 0 and 100")


@dataclass(frozen=True)
class FitnessGoals(ValueObject):
    """Value object representing fitness goals."""

    primary_goal: str
    target_weight_kg: Optional[float] = None
    target_body_fat_percentage: Optional[float] = None
    target_date: Optional[datetime] = None
    notes: str = ""

    VALID_GOALS = {
        "weight_loss",
        "muscle_gain",
        "strength_improvement",
        "endurance_improvement",
        "body_recomposition",
        "maintenance",
        "rehabilitation",
    }

    def __post_init__(self):
        """Validate fitness goals."""
        if self.primary_goal not in self.VALID_GOALS:
            raise ValueError(
                f"Invalid primary goal. Must be one of: {self.VALID_GOALS}"
            )


class Client(AggregateRoot):
    """
    Client aggregate root representing a coaching client.

    Encapsulates all client-related data and business rules.
    """

    def __init__(
        self,
        personal_info: PersonalInfo,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self._personal_info = personal_info
        self._physical_profile: Optional[PhysicalProfile] = None
        self._fitness_goals: Optional[FitnessGoals] = None
        self._excluded_exercise_ids: Set[int] = set()
        self._is_active = True
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

        # Add domain event
        from domain.events import ClientCreatedEvent

        self.add_domain_event(
            ClientCreatedEvent(
                client_id=str(self.id),
                email=personal_info.email,
                full_name=personal_info.full_name,
            )
        )

    @property
    def personal_info(self) -> PersonalInfo:
        """Get personal information."""
        return self._personal_info

    @property
    def physical_profile(self) -> Optional[PhysicalProfile]:
        """Get physical profile."""
        return self._physical_profile

    @property
    def fitness_goals(self) -> Optional[FitnessGoals]:
        """Get fitness goals."""
        return self._fitness_goals

    @property
    def excluded_exercise_ids(self) -> Set[int]:
        """Get excluded exercise IDs."""
        return self._excluded_exercise_ids.copy()

    @property
    def is_active(self) -> bool:
        """Check if client is active."""
        return self._is_active

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at

    def update_personal_info(self, personal_info: PersonalInfo) -> None:
        """Update personal information."""
        if personal_info != self._personal_info:
            self._personal_info = personal_info
            self._touch_updated_at()
            self.increment_version()

    def update_physical_profile(self, physical_profile: PhysicalProfile) -> None:
        """Update physical profile."""
        if physical_profile != self._physical_profile:
            self._physical_profile = physical_profile
            self._touch_updated_at()
            self.increment_version()

    def set_fitness_goals(self, fitness_goals: FitnessGoals) -> None:
        """Set fitness goals."""
        if fitness_goals != self._fitness_goals:
            self._fitness_goals = fitness_goals
            self._touch_updated_at()
            self.increment_version()

    def add_exercise_exclusion(self, exercise_id: int) -> None:
        """Add an exercise to exclusions."""
        if exercise_id not in self._excluded_exercise_ids:
            self._excluded_exercise_ids.add(exercise_id)
            self._touch_updated_at()
            self.increment_version()

    def remove_exercise_exclusion(self, exercise_id: int) -> None:
        """Remove an exercise from exclusions."""
        if exercise_id in self._excluded_exercise_ids:
            self._excluded_exercise_ids.remove(exercise_id)
            self._touch_updated_at()
            self.increment_version()

    def set_exercise_exclusions(self, exercise_ids: Set[int]) -> None:
        """Set all exercise exclusions."""
        if exercise_ids != self._excluded_exercise_ids:
            self._excluded_exercise_ids = exercise_ids.copy()
            self._touch_updated_at()
            self.increment_version()

    def deactivate(self) -> None:
        """Deactivate client."""
        if self._is_active:
            self._is_active = False
            self._touch_updated_at()
            self.increment_version()

    def reactivate(self) -> None:
        """Reactivate client."""
        if not self._is_active:
            self._is_active = True
            self._touch_updated_at()
            self.increment_version()

    def can_perform_exercise(self, exercise_id: int) -> bool:
        """Check if client can perform an exercise."""
        return exercise_id not in self._excluded_exercise_ids

    def _touch_updated_at(self) -> None:
        """Update the last modified timestamp."""
        self._updated_at = datetime.utcnow()


# Exercise Domain
@dataclass(frozen=True)
class MuscleGroup(ValueObject):
    """Value object representing muscle groups."""

    primary: str
    secondary: List[str] = field(default_factory=list)

    VALID_MUSCLE_GROUPS = {
        "chest",
        "back",
        "shoulders",
        "biceps",
        "triceps",
        "forearms",
        "abs",
        "obliques",
        "lower_back",
        "glutes",
        "quadriceps",
        "hamstrings",
        "calves",
        "traps",
        "lats",
        "delts",
    }

    def __post_init__(self):
        """Validate muscle groups."""
        if self.primary not in self.VALID_MUSCLE_GROUPS:
            raise ValueError(f"Invalid primary muscle group: {self.primary}")

        for muscle in self.secondary:
            if muscle not in self.VALID_MUSCLE_GROUPS:
                raise ValueError(f"Invalid secondary muscle group: {muscle}")


@dataclass(frozen=True)
class ExerciseMetadata(ValueObject):
    """Value object containing exercise metadata."""

    difficulty_level: str
    equipment_needed: List[str] = field(default_factory=list)
    instructions: str = ""
    tips: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    DIFFICULTY_LEVELS = {"beginner", "intermediate", "advanced", "expert"}

    def __post_init__(self):
        """Validate exercise metadata."""
        if self.difficulty_level not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"Invalid difficulty level: {self.difficulty_level}")


class Exercise(Entity):
    """
    Exercise entity representing a fitness exercise.
    """

    def __init__(
        self,
        name: str,
        muscle_group: MuscleGroup,
        exercise_type: str,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self._name = name.strip()
        self._muscle_group = muscle_group
        self._exercise_type = exercise_type
        self._metadata: Optional[ExerciseMetadata] = None
        self._is_active = True

        if not self._name:
            raise ValueError("Exercise name cannot be empty")

    @property
    def name(self) -> str:
        """Get exercise name."""
        return self._name

    @property
    def muscle_group(self) -> MuscleGroup:
        """Get muscle group."""
        return self._muscle_group

    @property
    def exercise_type(self) -> str:
        """Get exercise type."""
        return self._exercise_type

    @property
    def metadata(self) -> Optional[ExerciseMetadata]:
        """Get exercise metadata."""
        return self._metadata

    @property
    def is_active(self) -> bool:
        """Check if exercise is active."""
        return self._is_active

    def set_metadata(self, metadata: ExerciseMetadata) -> None:
        """Set exercise metadata."""
        self._metadata = metadata

    def deactivate(self) -> None:
        """Deactivate exercise."""
        self._is_active = False

    def reactivate(self) -> None:
        """Reactivate exercise."""
        self._is_active = True


# Session Domain
@dataclass(frozen=True)
class ExerciseSet(ValueObject):
    """Value object representing a set of an exercise."""

    reps: int
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None
    distance_meters: Optional[float] = None
    rest_seconds: Optional[int] = None
    notes: str = ""

    def __post_init__(self):
        """Validate exercise set."""
        if self.reps < 0:
            raise ValueError("Reps cannot be negative")
        if self.weight_kg is not None and self.weight_kg < 0:
            raise ValueError("Weight cannot be negative")
        if self.duration_seconds is not None and self.duration_seconds < 0:
            raise ValueError("Duration cannot be negative")
        if self.distance_meters is not None and self.distance_meters < 0:
            raise ValueError("Distance cannot be negative")


@dataclass(frozen=True)
class SessionExercise(ValueObject):
    """Value object representing an exercise within a session."""

    exercise_id: int
    sets: List[ExerciseSet]
    notes: str = ""
    order: int = 1

    @property
    def total_volume(self) -> float:
        """Calculate total volume (weight * reps)."""
        return sum((s.weight_kg or 0) * s.reps for s in self.sets)

    @property
    def total_reps(self) -> int:
        """Calculate total repetitions."""
        return sum(s.reps for s in self.sets)

    def __post_init__(self):
        """Validate session exercise."""
        if not self.sets:
            raise ValueError("Exercise must have at least one set")
        if self.order < 1:
            raise ValueError("Exercise order must be positive")


class WorkoutSession(AggregateRoot):
    """
    Workout session aggregate root.

    Represents a complete training session with exercises and metadata.
    """

    def __init__(
        self,
        client_id: int,
        name: str,
        session_date: datetime,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self._client_id = client_id
        self._name = name.strip()
        self._session_date = session_date
        self._exercises: List[SessionExercise] = []
        self._notes = ""
        self._duration_minutes: Optional[int] = None
        self._is_completed = False
        self._created_at = datetime.utcnow()

        if not self._name:
            raise ValueError("Session name cannot be empty")

        # Add domain event
        from domain.events import SessionCreatedEvent

        self.add_domain_event(
            SessionCreatedEvent(
                session_id=str(self.id),
                client_id=str(client_id),
                session_name=name,
                session_date=session_date.isoformat(),
            )
        )

    @property
    def client_id(self) -> int:
        """Get client ID."""
        return self._client_id

    @property
    def name(self) -> str:
        """Get session name."""
        return self._name

    @property
    def session_date(self) -> datetime:
        """Get session date."""
        return self._session_date

    @property
    def exercises(self) -> List[SessionExercise]:
        """Get session exercises."""
        return self._exercises.copy()

    @property
    def notes(self) -> str:
        """Get session notes."""
        return self._notes

    @property
    def duration_minutes(self) -> Optional[int]:
        """Get session duration in minutes."""
        return self._duration_minutes

    @property
    def is_completed(self) -> bool:
        """Check if session is completed."""
        return self._is_completed

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at

    def add_exercise(self, exercise: SessionExercise) -> None:
        """Add exercise to session."""
        self._exercises.append(exercise)
        self.increment_version()

    def remove_exercise(self, exercise_id: int) -> None:
        """Remove exercise from session."""
        initial_count = len(self._exercises)
        self._exercises = [e for e in self._exercises if e.exercise_id != exercise_id]

        if len(self._exercises) < initial_count:
            self.increment_version()

    def set_notes(self, notes: str) -> None:
        """Set session notes."""
        if notes != self._notes:
            self._notes = notes
            self.increment_version()

    def set_duration(self, duration_minutes: int) -> None:
        """Set session duration."""
        if duration_minutes != self._duration_minutes:
            self._duration_minutes = duration_minutes
            self.increment_version()

    def complete_session(self) -> None:
        """Mark session as completed."""
        if not self._is_completed:
            self._is_completed = True
            self.increment_version()

    def calculate_total_volume(self) -> float:
        """Calculate total session volume."""
        return sum(exercise.total_volume for exercise in self._exercises)

    def calculate_total_exercises(self) -> int:
        """Calculate total number of exercises."""
        return len(self._exercises)

    def calculate_total_sets(self) -> int:
        """Calculate total number of sets."""
        return sum(len(exercise.sets) for exercise in self._exercises)
