"""
Domain Events for CoachPro Application.

Domain events represent important business events that have occurred
in the domain and may trigger side effects or integrations.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from core.events import DomainEvent


@dataclass
class ClientCreatedEvent(DomainEvent):
    """Event raised when a new client is created."""

    client_id: str
    email: str
    full_name: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.client_id
        self.aggregate_type = "Client"


@dataclass
class ClientUpdatedEvent(DomainEvent):
    """Event raised when a client is updated."""

    client_id: str
    updated_fields: Dict[str, Any]

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.client_id
        self.aggregate_type = "Client"


@dataclass
class ClientDeactivatedEvent(DomainEvent):
    """Event raised when a client is deactivated."""

    client_id: str
    reason: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.client_id
        self.aggregate_type = "Client"


@dataclass
class ClientArchivedEvent(DomainEvent):
    """Event raised when a client is archived."""

    client_id: str
    reason: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.client_id
        self.aggregate_type = "Client"


@dataclass
class SessionCreatedEvent(DomainEvent):
    """Event raised when a new workout session is created."""

    session_id: str
    client_id: str
    session_name: str
    session_date: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.session_id
        self.aggregate_type = "WorkoutSession"


@dataclass
class SessionUpdatedEvent(DomainEvent):
    """Event raised when a workout session is updated."""

    session_id: str
    client_id: str
    updated_fields: Dict[str, Any]

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.session_id
        self.aggregate_type = "WorkoutSession"


@dataclass
class SessionCompletedEvent(DomainEvent):
    """Event raised when a workout session is completed."""

    session_id: str
    client_id: str
    completion_date: str
    total_exercises: int
    total_volume: float
    duration_minutes: Optional[int] = None

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.session_id
        self.aggregate_type = "WorkoutSession"


@dataclass
class ExerciseAddedToSessionEvent(DomainEvent):
    """Event raised when an exercise is added to a session."""

    session_id: str
    client_id: str
    exercise_id: int
    exercise_name: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.session_id
        self.aggregate_type = "WorkoutSession"


@dataclass
class ExerciseExclusionUpdatedEvent(DomainEvent):
    """Event raised when a client's exercise exclusions are updated."""

    client_id: str
    excluded_exercise_ids: list

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.client_id
        self.aggregate_type = "Client"


@dataclass
class NutritionPlanCreatedEvent(DomainEvent):
    """Event raised when a nutrition plan is created."""

    plan_id: str
    client_id: str
    plan_type: str
    target_calories: Optional[int] = None

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.plan_id
        self.aggregate_type = "NutritionPlan"


@dataclass
class NutritionPlanUpdatedEvent(DomainEvent):
    """Event raised when a nutrition plan is updated."""

    plan_id: str
    client_id: str
    updated_fields: Dict[str, Any]

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.plan_id
        self.aggregate_type = "NutritionPlan"


@dataclass
class MealAddedEvent(DomainEvent):
    """Event raised when a meal is added to a nutrition plan."""

    plan_id: str
    client_id: str
    meal_name: str
    meal_type: str
    calories: Optional[int] = None

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.plan_id
        self.aggregate_type = "NutritionPlan"


@dataclass
class ExerciseCreatedEvent(DomainEvent):
    """Event raised when an exercise is created."""

    exercise_id: str
    exercise_name: str
    muscle_group: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.exercise_id
        self.aggregate_type = "Exercise"


@dataclass
class ExerciseUpdatedEvent(DomainEvent):
    """Event raised when an exercise is updated."""

    exercise_id: str
    updated_fields: Dict[str, Any]

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.exercise_id
        self.aggregate_type = "Exercise"


@dataclass
class ExerciseDeletedEvent(DomainEvent):
    """Event raised when an exercise is deleted."""

    exercise_id: str
    reason: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.exercise_id
        self.aggregate_type = "Exercise"


@dataclass
class ExerciseImportedEvent(DomainEvent):
    """Event raised when exercises are imported from external source."""

    import_id: str
    source: str
    exercises_count: int
    success_count: int
    failure_count: int

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.import_id
        self.aggregate_type = "ExerciseImport"


@dataclass
class PDFGeneratedEvent(DomainEvent):
    """Event raised when a PDF document is generated."""

    pdf_id: str
    client_id: str
    document_type: str
    file_size_bytes: int
    generation_time_ms: float

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.pdf_id
        self.aggregate_type = "PDFDocument"


@dataclass
class WorkoutGeneratedEvent(DomainEvent):
    """Event raised when an automatic workout is generated."""

    generation_id: str
    client_id: str
    workout_type: str
    exercise_count: int
    duration_minutes: int
    algorithm_used: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.generation_id
        self.aggregate_type = "WorkoutGeneration"


@dataclass
class ProgressMilestoneReachedEvent(DomainEvent):
    """Event raised when a client reaches a progress milestone."""

    milestone_id: str
    client_id: str
    milestone_type: str
    milestone_value: Any
    achievement_date: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.milestone_id
        self.aggregate_type = "ProgressMilestone"


@dataclass
class SystemHealthCheckEvent(DomainEvent):
    """Event raised for system health monitoring."""

    check_id: str
    component: str
    status: str
    response_time_ms: float
    memory_usage_mb: float

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.check_id
        self.aggregate_type = "SystemHealth"


@dataclass
class UserActionEvent(DomainEvent):
    """Event raised for user activity tracking."""

    action_id: str
    user_id: str
    action_type: str
    resource_type: str
    resource_id: str
    duration_ms: Optional[float] = None

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.action_id
        self.aggregate_type = "UserAction"


@dataclass
class DataExportRequestedEvent(DomainEvent):
    """Event raised when a data export is requested."""

    export_id: str
    client_id: str
    data_types: list
    format: str
    requested_by: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.export_id
        self.aggregate_type = "DataExport"


@dataclass
class DataDeletionRequestedEvent(DomainEvent):
    """Event raised when data deletion is requested (GDPR compliance)."""

    deletion_id: str
    client_id: str
    data_types: list
    requested_by: str
    reason: str

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.deletion_id
        self.aggregate_type = "DataDeletion"


@dataclass
class ErrorOccurredEvent(DomainEvent):
    """Event raised when significant errors occur."""

    error_id: str
    error_type: str
    error_message: str
    component: str
    severity: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Set aggregate information."""
        self.aggregate_id = self.error_id
        self.aggregate_type = "SystemError"
