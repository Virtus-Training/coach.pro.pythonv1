"""
Factory Pattern Implementation.

Provides factory classes for creating domain objects with proper
initialization and validation. Supports both simple factory and
abstract factory patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from domain.entities import (
    Client,
    PersonalInfo,
    PhysicalProfile,
    FitnessGoals,
    Exercise,
    MuscleGroup,
    ExerciseMetadata,
    WorkoutSession,
    SessionExercise,
    ExerciseSet,
)

T = TypeVar("T")


class IFactory(ABC, Generic[T]):
    """Generic factory interface."""

    @abstractmethod
    def create(self, **kwargs) -> T:
        """Create an instance of type T."""
        pass


class AbstractFactory(ABC):
    """
    Abstract Factory for creating families of related objects.

    Provides a high-level interface for creating objects without
    specifying their concrete classes.
    """

    @abstractmethod
    def create_client_factory(self) -> IFactory[Client]:
        """Create client factory."""
        pass

    @abstractmethod
    def create_session_factory(self) -> IFactory[WorkoutSession]:
        """Create session factory."""
        pass

    @abstractmethod
    def create_exercise_factory(self) -> IFactory[Exercise]:
        """Create exercise factory."""
        pass


class ClientFactory(IFactory[Client]):
    """
    Factory for creating Client aggregates.

    Handles complex client creation with validation and proper
    initialization of value objects.
    """

    def create(self, **kwargs) -> Client:
        """
        Create a new client.

        Args:
            first_name: Client's first name
            last_name: Client's last name
            email: Client's email address
            birth_date: Optional birth date
            phone: Optional phone number
            height_cm: Optional height in centimeters
            weight_kg: Optional weight in kilograms
            primary_goal: Primary fitness goal
            **kwargs: Additional arguments

        Returns:
            New Client instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate required fields
        required_fields = ["first_name", "last_name", "email"]
        for field in required_fields:
            if not kwargs.get(field):
                raise ValueError(f"Required field '{field}' is missing")

        # Create personal info
        personal_info = PersonalInfo(
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            email=kwargs["email"],
            birth_date=kwargs.get("birth_date"),
            phone=kwargs.get("phone"),
        )

        # Create client
        client = Client(
            personal_info=personal_info,
            id=kwargs.get("id"),
        )

        # Add physical profile if data provided
        if any(key in kwargs for key in ["height_cm", "weight_kg", "body_fat_percentage"]):
            physical_profile = PhysicalProfile(
                height_cm=kwargs.get("height_cm"),
                weight_kg=kwargs.get("weight_kg"),
                body_fat_percentage=kwargs.get("body_fat_percentage"),
                muscle_mass_kg=kwargs.get("muscle_mass_kg"),
            )
            client.update_physical_profile(physical_profile)

        # Add fitness goals if provided
        if kwargs.get("primary_goal"):
            fitness_goals = FitnessGoals(
                primary_goal=kwargs["primary_goal"],
                target_weight_kg=kwargs.get("target_weight_kg"),
                target_body_fat_percentage=kwargs.get("target_body_fat_percentage"),
                target_date=kwargs.get("target_date"),
                notes=kwargs.get("goal_notes", ""),
            )
            client.set_fitness_goals(fitness_goals)

        return client

    def create_from_dict(self, data: Dict[str, Any]) -> Client:
        """Create client from dictionary data."""
        return self.create(**data)

    def create_demo_client(self) -> Client:
        """Create a demo client for testing/development."""
        return self.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            height_cm=180.0,
            weight_kg=80.0,
            primary_goal="muscle_gain",
            target_weight_kg=85.0,
        )


class ExerciseFactory(IFactory[Exercise]):
    """
    Factory for creating Exercise entities.

    Provides various creation methods for different exercise types
    and sources (manual, imported, etc.).
    """

    def create(self, **kwargs) -> Exercise:
        """
        Create a new exercise.

        Args:
            name: Exercise name
            primary_muscle: Primary muscle group
            secondary_muscles: List of secondary muscle groups
            exercise_type: Type of exercise
            difficulty_level: Difficulty level
            equipment_needed: List of required equipment
            instructions: Exercise instructions
            **kwargs: Additional arguments

        Returns:
            New Exercise instance
        """
        # Validate required fields
        if not kwargs.get("name"):
            raise ValueError("Exercise name is required")
        if not kwargs.get("primary_muscle"):
            raise ValueError("Primary muscle group is required")
        if not kwargs.get("exercise_type"):
            raise ValueError("Exercise type is required")

        # Create muscle group
        muscle_group = MuscleGroup(
            primary=kwargs["primary_muscle"],
            secondary=kwargs.get("secondary_muscles", []),
        )

        # Create exercise
        exercise = Exercise(
            name=kwargs["name"],
            muscle_group=muscle_group,
            exercise_type=kwargs["exercise_type"],
            id=kwargs.get("id"),
        )

        # Add metadata if provided
        if kwargs.get("difficulty_level"):
            metadata = ExerciseMetadata(
                difficulty_level=kwargs["difficulty_level"],
                equipment_needed=kwargs.get("equipment_needed", []),
                instructions=kwargs.get("instructions", ""),
                tips=kwargs.get("tips", []),
                warnings=kwargs.get("warnings", []),
            )
            exercise.set_metadata(metadata)

        return exercise

    def create_from_wger_data(self, wger_data: Dict[str, Any]) -> Exercise:
        """Create exercise from wger.de API data."""
        return self.create(
            name=wger_data.get("name", ""),
            primary_muscle=self._map_wger_muscle(wger_data.get("muscles", [])),
            secondary_muscles=self._map_wger_secondary_muscles(wger_data.get("muscles_secondary", [])),
            exercise_type=self._map_wger_category(wger_data.get("category", {})),
            difficulty_level="intermediate",  # Default for wger imports
            equipment_needed=self._map_wger_equipment(wger_data.get("equipment", [])),
            instructions=wger_data.get("description", ""),
        )

    def create_compound_exercise(self, name: str, muscle_groups: List[str]) -> Exercise:
        """Create a compound exercise targeting multiple muscle groups."""
        if not muscle_groups:
            raise ValueError("Compound exercise must target at least one muscle group")

        return self.create(
            name=name,
            primary_muscle=muscle_groups[0],
            secondary_muscles=muscle_groups[1:],
            exercise_type="compound",
            difficulty_level="intermediate",
        )

    def create_isolation_exercise(self, name: str, target_muscle: str) -> Exercise:
        """Create an isolation exercise targeting a specific muscle."""
        return self.create(
            name=name,
            primary_muscle=target_muscle,
            exercise_type="isolation",
            difficulty_level="beginner",
        )

    def _map_wger_muscle(self, muscles: List[Dict]) -> str:
        """Map wger muscle data to our muscle groups."""
        if not muscles:
            return "chest"  # Default

        muscle_mapping = {
            "Pectorals": "chest",
            "Latissimus Dorsi": "back",
            "Biceps brachii": "biceps",
            "Triceps brachii": "triceps",
            "Shoulders": "shoulders",
            "Quadriceps femoris": "quadriceps",
            "Hamstrings": "hamstrings",
            "Glutes": "glutes",
            "Calves": "calves",
            "Abs": "abs",
        }

        muscle_name = muscles[0].get("name", "chest")
        return muscle_mapping.get(muscle_name, "chest")

    def _map_wger_secondary_muscles(self, muscles: List[Dict]) -> List[str]:
        """Map wger secondary muscles to our format."""
        return [self._map_wger_muscle([muscle]) for muscle in muscles]

    def _map_wger_category(self, category: Dict) -> str:
        """Map wger category to exercise type."""
        category_mapping = {
            "Arms": "isolation",
            "Legs": "compound",
            "Abs": "isolation",
            "Chest": "compound",
            "Back": "compound",
            "Shoulders": "isolation",
        }

        category_name = category.get("name", "compound")
        return category_mapping.get(category_name, "compound")

    def _map_wger_equipment(self, equipment: List[Dict]) -> List[str]:
        """Map wger equipment to our format."""
        return [eq.get("name", "").lower() for eq in equipment]


class SessionFactory(IFactory[WorkoutSession]):
    """
    Factory for creating WorkoutSession aggregates.

    Provides methods for creating sessions from templates,
    generating automatic sessions, and importing session data.
    """

    def create(self, **kwargs) -> WorkoutSession:
        """
        Create a new workout session.

        Args:
            client_id: ID of the client
            name: Session name
            session_date: Date of the session
            exercises: List of session exercises
            notes: Session notes
            duration_minutes: Session duration
            **kwargs: Additional arguments

        Returns:
            New WorkoutSession instance
        """
        # Validate required fields
        if not kwargs.get("client_id"):
            raise ValueError("Client ID is required")
        if not kwargs.get("name"):
            raise ValueError("Session name is required")

        session_date = kwargs.get("session_date", datetime.utcnow())
        if isinstance(session_date, str):
            session_date = datetime.fromisoformat(session_date)

        # Create session
        session = WorkoutSession(
            client_id=kwargs["client_id"],
            name=kwargs["name"],
            session_date=session_date,
            id=kwargs.get("id"),
        )

        # Add exercises if provided
        exercises = kwargs.get("exercises", [])
        for exercise_data in exercises:
            session_exercise = self._create_session_exercise(exercise_data)
            session.add_exercise(session_exercise)

        # Set additional properties
        if kwargs.get("notes"):
            session.set_notes(kwargs["notes"])

        if kwargs.get("duration_minutes"):
            session.set_duration(kwargs["duration_minutes"])

        return session

    def create_from_template(
        self,
        client_id: int,
        template_name: str,
        session_date: Optional[datetime] = None,
    ) -> WorkoutSession:
        """Create session from a predefined template."""
        templates = {
            "push_workout": {
                "name": "Push Workout",
                "exercises": [
                    {
                        "exercise_id": 1,  # Bench Press
                        "sets": [
                            {"reps": 8, "weight_kg": 80.0},
                            {"reps": 8, "weight_kg": 80.0},
                            {"reps": 6, "weight_kg": 85.0},
                        ],
                    },
                    {
                        "exercise_id": 2,  # Shoulder Press
                        "sets": [
                            {"reps": 10, "weight_kg": 40.0},
                            {"reps": 10, "weight_kg": 40.0},
                            {"reps": 8, "weight_kg": 42.5},
                        ],
                    },
                ],
            },
            "pull_workout": {
                "name": "Pull Workout",
                "exercises": [
                    {
                        "exercise_id": 3,  # Pull-ups
                        "sets": [
                            {"reps": 8},
                            {"reps": 6},
                            {"reps": 5},
                        ],
                    },
                ],
            },
            "leg_workout": {
                "name": "Leg Workout",
                "exercises": [
                    {
                        "exercise_id": 4,  # Squats
                        "sets": [
                            {"reps": 12, "weight_kg": 100.0},
                            {"reps": 10, "weight_kg": 110.0},
                            {"reps": 8, "weight_kg": 120.0},
                        ],
                    },
                ],
            },
        }

        template = templates.get(template_name)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")

        return self.create(
            client_id=client_id,
            name=template["name"],
            session_date=session_date or datetime.utcnow(),
            exercises=template["exercises"],
        )

    def create_cardio_session(
        self,
        client_id: int,
        cardio_type: str,
        duration_minutes: int,
        session_date: Optional[datetime] = None,
    ) -> WorkoutSession:
        """Create a cardio-focused session."""
        cardio_exercises = {
            "running": {"exercise_id": 100, "name": "Running"},
            "cycling": {"exercise_id": 101, "name": "Cycling"},
            "rowing": {"exercise_id": 102, "name": "Rowing"},
            "elliptical": {"exercise_id": 103, "name": "Elliptical"},
        }

        exercise_info = cardio_exercises.get(cardio_type, cardio_exercises["running"])

        return self.create(
            client_id=client_id,
            name=f"{cardio_type.title()} Session",
            session_date=session_date or datetime.utcnow(),
            duration_minutes=duration_minutes,
            exercises=[
                {
                    "exercise_id": exercise_info["exercise_id"],
                    "sets": [
                        {
                            "reps": 1,
                            "duration_seconds": duration_minutes * 60,
                        }
                    ],
                }
            ],
        )

    def _create_session_exercise(self, exercise_data: Dict[str, Any]) -> SessionExercise:
        """Create SessionExercise from data dictionary."""
        sets = [
            ExerciseSet(
                reps=set_data.get("reps", 0),
                weight_kg=set_data.get("weight_kg"),
                duration_seconds=set_data.get("duration_seconds"),
                distance_meters=set_data.get("distance_meters"),
                rest_seconds=set_data.get("rest_seconds"),
                notes=set_data.get("notes", ""),
            )
            for set_data in exercise_data.get("sets", [])
        ]

        return SessionExercise(
            exercise_id=exercise_data["exercise_id"],
            sets=sets,
            notes=exercise_data.get("notes", ""),
            order=exercise_data.get("order", 1),
        )


class CoachProFactory(AbstractFactory):
    """
    Concrete implementation of AbstractFactory for CoachPro domain.

    Provides access to all domain object factories with consistent
    configuration and validation.
    """

    def __init__(self):
        self._client_factory = ClientFactory()
        self._session_factory = SessionFactory()
        self._exercise_factory = ExerciseFactory()

    def create_client_factory(self) -> IFactory[Client]:
        """Create client factory."""
        return self._client_factory

    def create_session_factory(self) -> IFactory[WorkoutSession]:
        """Create session factory."""
        return self._session_factory

    def create_exercise_factory(self) -> IFactory[Exercise]:
        """Create exercise factory."""
        return self._exercise_factory

    def create_demo_data(self) -> Dict[str, Any]:
        """Create a complete set of demo data for testing."""
        # Create demo client
        client = self._client_factory.create_demo_client()

        # Create demo exercises
        exercises = [
            self._exercise_factory.create_compound_exercise(
                "Bench Press", ["chest", "triceps", "shoulders"]
            ),
            self._exercise_factory.create_isolation_exercise("Bicep Curls", "biceps"),
            self._exercise_factory.create_compound_exercise("Squats", ["quadriceps", "glutes"]),
        ]

        # Create demo session
        session = self._session_factory.create_from_template(
            client_id=client.id, template_name="push_workout"
        )

        return {
            "client": client,
            "exercises": exercises,
            "session": session,
        }


# Factory Registration for Dependency Injection
def register_factories(container) -> None:
    """Register all factories in the DI container."""
    from core.container import ServiceLifetime

    container.register(
        AbstractFactory,
        CoachProFactory,
        ServiceLifetime.SINGLETON
    )

    container.register(
        IFactory[Client],
        ClientFactory,
        ServiceLifetime.SINGLETON
    )

    container.register(
        IFactory[Exercise],
        ExerciseFactory,
        ServiceLifetime.SINGLETON
    )

    container.register(
        IFactory[WorkoutSession],
        SessionFactory,
        ServiceLifetime.SINGLETON
    )