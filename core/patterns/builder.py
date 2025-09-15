"""
Builder Pattern Implementation.

Provides builder classes for constructing complex objects step by step.
Particularly useful for objects with many optional parameters or
complex construction logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar

from domain.entities import (
    Client,
    PersonalInfo,
    PhysicalProfile,
    FitnessGoals,
    WorkoutSession,
    SessionExercise,
    ExerciseSet,
)

T = TypeVar("T")


class IBuilder(ABC):
    """Generic builder interface."""

    @abstractmethod
    def build(self) -> T:
        """Build and return the final object."""
        pass

    @abstractmethod
    def reset(self) -> IBuilder:
        """Reset the builder to initial state."""
        pass


class ClientBuilder(IBuilder):
    """
    Builder for creating Client objects with fluent interface.

    Allows step-by-step construction of clients with validation
    and optional components.

    Example:
        client = (ClientBuilder()
            .with_personal_info("John", "Doe", "john@example.com")
            .with_physical_stats(180, 75)
            .with_goal("muscle_gain")
            .exclude_exercises([1, 2, 3])
            .build())
    """

    def __init__(self):
        self.reset()

    def reset(self) -> ClientBuilder:
        """Reset builder to initial state."""
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._email: Optional[str] = None
        self._birth_date: Optional[datetime] = None
        self._phone: Optional[str] = None
        self._height_cm: Optional[float] = None
        self._weight_kg: Optional[float] = None
        self._body_fat_percentage: Optional[float] = None
        self._muscle_mass_kg: Optional[float] = None
        self._primary_goal: Optional[str] = None
        self._target_weight_kg: Optional[float] = None
        self._target_body_fat_percentage: Optional[float] = None
        self._target_date: Optional[datetime] = None
        self._goal_notes: str = ""
        self._excluded_exercises: set[int] = set()
        self._client_id: Optional[int] = None
        return self

    def with_id(self, client_id: int) -> ClientBuilder:
        """Set client ID."""
        self._client_id = client_id
        return self

    def with_personal_info(
        self,
        first_name: str,
        last_name: str,
        email: str,
        birth_date: Optional[datetime] = None,
        phone: Optional[str] = None,
    ) -> ClientBuilder:
        """Set personal information."""
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._birth_date = birth_date
        self._phone = phone
        return self

    def with_birth_date(self, birth_date: datetime) -> ClientBuilder:
        """Set birth date."""
        self._birth_date = birth_date
        return self

    def with_age(self, age_years: int) -> ClientBuilder:
        """Set age (calculates birth date)."""
        self._birth_date = datetime.now() - timedelta(days=age_years * 365.25)
        return self

    def with_phone(self, phone: str) -> ClientBuilder:
        """Set phone number."""
        self._phone = phone
        return self

    def with_physical_stats(
        self,
        height_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        body_fat_percentage: Optional[float] = None,
        muscle_mass_kg: Optional[float] = None,
    ) -> ClientBuilder:
        """Set physical statistics."""
        if height_cm is not None:
            self._height_cm = height_cm
        if weight_kg is not None:
            self._weight_kg = weight_kg
        if body_fat_percentage is not None:
            self._body_fat_percentage = body_fat_percentage
        if muscle_mass_kg is not None:
            self._muscle_mass_kg = muscle_mass_kg
        return self

    def with_height(self, height_cm: float) -> ClientBuilder:
        """Set height in centimeters."""
        self._height_cm = height_cm
        return self

    def with_weight(self, weight_kg: float) -> ClientBuilder:
        """Set weight in kilograms."""
        self._weight_kg = weight_kg
        return self

    def with_body_fat(self, body_fat_percentage: float) -> ClientBuilder:
        """Set body fat percentage."""
        self._body_fat_percentage = body_fat_percentage
        return self

    def with_goal(
        self,
        primary_goal: str,
        target_weight_kg: Optional[float] = None,
        target_body_fat_percentage: Optional[float] = None,
        target_date: Optional[datetime] = None,
        notes: str = "",
    ) -> ClientBuilder:
        """Set fitness goals."""
        self._primary_goal = primary_goal
        self._target_weight_kg = target_weight_kg
        self._target_body_fat_percentage = target_body_fat_percentage
        self._target_date = target_date
        self._goal_notes = notes
        return self

    def with_weight_loss_goal(self, target_weight_kg: float, target_date: Optional[datetime] = None) -> ClientBuilder:
        """Set weight loss goal."""
        return self.with_goal(
            primary_goal="weight_loss",
            target_weight_kg=target_weight_kg,
            target_date=target_date,
        )

    def with_muscle_gain_goal(self, target_weight_kg: float, target_date: Optional[datetime] = None) -> ClientBuilder:
        """Set muscle gain goal."""
        return self.with_goal(
            primary_goal="muscle_gain",
            target_weight_kg=target_weight_kg,
            target_date=target_date,
        )

    def exclude_exercise(self, exercise_id: int) -> ClientBuilder:
        """Exclude a single exercise."""
        self._excluded_exercises.add(exercise_id)
        return self

    def exclude_exercises(self, exercise_ids: List[int]) -> ClientBuilder:
        """Exclude multiple exercises."""
        self._excluded_exercises.update(exercise_ids)
        return self

    def build(self) -> Client:
        """Build the final Client object."""
        # Validate required fields
        if not self._first_name:
            raise ValueError("First name is required")
        if not self._last_name:
            raise ValueError("Last name is required")
        if not self._email:
            raise ValueError("Email is required")

        # Create personal info
        personal_info = PersonalInfo(
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            birth_date=self._birth_date,
            phone=self._phone,
        )

        # Create client
        client = Client(
            personal_info=personal_info,
            id=self._client_id,
        )

        # Add physical profile if any physical data provided
        if any([self._height_cm, self._weight_kg, self._body_fat_percentage, self._muscle_mass_kg]):
            physical_profile = PhysicalProfile(
                height_cm=self._height_cm,
                weight_kg=self._weight_kg,
                body_fat_percentage=self._body_fat_percentage,
                muscle_mass_kg=self._muscle_mass_kg,
            )
            client.update_physical_profile(physical_profile)

        # Add fitness goals if provided
        if self._primary_goal:
            fitness_goals = FitnessGoals(
                primary_goal=self._primary_goal,
                target_weight_kg=self._target_weight_kg,
                target_body_fat_percentage=self._target_body_fat_percentage,
                target_date=self._target_date,
                notes=self._goal_notes,
            )
            client.set_fitness_goals(fitness_goals)

        # Set exercise exclusions
        if self._excluded_exercises:
            client.set_exercise_exclusions(self._excluded_exercises)

        return client


class SessionBuilder(IBuilder):
    """
    Builder for creating WorkoutSession objects with fluent interface.

    Example:
        session = (SessionBuilder()
            .for_client(client_id=1)
            .named("Push Day")
            .on_date(datetime.now())
            .add_exercise(1, [
                ExerciseSet(reps=8, weight_kg=80),
                ExerciseSet(reps=8, weight_kg=80),
            ])
            .with_duration(60)
            .build())
    """

    def __init__(self):
        self.reset()

    def reset(self) -> SessionBuilder:
        """Reset builder to initial state."""
        self._client_id: Optional[int] = None
        self._name: Optional[str] = None
        self._session_date: Optional[datetime] = None
        self._exercises: List[Dict[str, Any]] = []
        self._notes: str = ""
        self._duration_minutes: Optional[int] = None
        self._session_id: Optional[int] = None
        return self

    def with_id(self, session_id: int) -> SessionBuilder:
        """Set session ID."""
        self._session_id = session_id
        return self

    def for_client(self, client_id: int) -> SessionBuilder:
        """Set the client for this session."""
        self._client_id = client_id
        return self

    def named(self, name: str) -> SessionBuilder:
        """Set session name."""
        self._name = name
        return self

    def on_date(self, session_date: datetime) -> SessionBuilder:
        """Set session date."""
        self._session_date = session_date
        return self

    def today(self) -> SessionBuilder:
        """Set session date to today."""
        self._session_date = datetime.now()
        return self

    def tomorrow(self) -> SessionBuilder:
        """Set session date to tomorrow."""
        self._session_date = datetime.now() + timedelta(days=1)
        return self

    def add_exercise(
        self,
        exercise_id: int,
        sets: List[ExerciseSet],
        notes: str = "",
        order: Optional[int] = None,
    ) -> SessionBuilder:
        """Add an exercise to the session."""
        exercise_data = {
            "exercise_id": exercise_id,
            "sets": sets,
            "notes": notes,
            "order": order or len(self._exercises) + 1,
        }
        self._exercises.append(exercise_data)
        return self

    def add_strength_exercise(
        self,
        exercise_id: int,
        sets_data: List[tuple[int, float]],  # (reps, weight_kg)
        notes: str = "",
    ) -> SessionBuilder:
        """Add a strength exercise with rep/weight pairs."""
        sets = [
            ExerciseSet(reps=reps, weight_kg=weight_kg)
            for reps, weight_kg in sets_data
        ]
        return self.add_exercise(exercise_id, sets, notes)

    def add_cardio_exercise(
        self,
        exercise_id: int,
        duration_minutes: int,
        distance_km: Optional[float] = None,
        notes: str = "",
    ) -> SessionBuilder:
        """Add a cardio exercise."""
        sets = [
            ExerciseSet(
                reps=1,
                duration_seconds=duration_minutes * 60,
                distance_meters=distance_km * 1000 if distance_km else None,
            )
        ]
        return self.add_exercise(exercise_id, sets, notes)

    def add_bodyweight_exercise(
        self,
        exercise_id: int,
        sets_reps: List[int],  # List of reps for each set
        notes: str = "",
    ) -> SessionBuilder:
        """Add a bodyweight exercise."""
        sets = [ExerciseSet(reps=reps) for reps in sets_reps]
        return self.add_exercise(exercise_id, sets, notes)

    def with_notes(self, notes: str) -> SessionBuilder:
        """Set session notes."""
        self._notes = notes
        return self

    def with_duration(self, duration_minutes: int) -> SessionBuilder:
        """Set session duration."""
        self._duration_minutes = duration_minutes
        return self

    def build(self) -> WorkoutSession:
        """Build the final WorkoutSession object."""
        # Validate required fields
        if not self._client_id:
            raise ValueError("Client ID is required")
        if not self._name:
            raise ValueError("Session name is required")

        # Use current time if no date specified
        session_date = self._session_date or datetime.utcnow()

        # Create session
        session = WorkoutSession(
            client_id=self._client_id,
            name=self._name,
            session_date=session_date,
            id=self._session_id,
        )

        # Add exercises
        for exercise_data in self._exercises:
            session_exercise = SessionExercise(
                exercise_id=exercise_data["exercise_id"],
                sets=exercise_data["sets"],
                notes=exercise_data["notes"],
                order=exercise_data["order"],
            )
            session.add_exercise(session_exercise)

        # Set optional properties
        if self._notes:
            session.set_notes(self._notes)

        if self._duration_minutes:
            session.set_duration(self._duration_minutes)

        return session


class WorkoutPlanBuilder(IBuilder):
    """
    Builder for creating multi-session workout plans.

    Example:
        plan = (WorkoutPlanBuilder()
            .for_client(client_id=1)
            .named("Push/Pull/Legs Split")
            .for_weeks(4)
            .add_session_template("Push Day", push_exercises)
            .add_session_template("Pull Day", pull_exercises)
            .add_session_template("Leg Day", leg_exercises)
            .build())
    """

    def __init__(self):
        self.reset()

    def reset(self) -> WorkoutPlanBuilder:
        """Reset builder to initial state."""
        self._client_id: Optional[int] = None
        self._plan_name: Optional[str] = None
        self._weeks: int = 1
        self._session_templates: List[Dict[str, Any]] = []
        self._start_date: Optional[datetime] = None
        return self

    def for_client(self, client_id: int) -> WorkoutPlanBuilder:
        """Set the client for this plan."""
        self._client_id = client_id
        return self

    def named(self, plan_name: str) -> WorkoutPlanBuilder:
        """Set plan name."""
        self._plan_name = plan_name
        return self

    def for_weeks(self, weeks: int) -> WorkoutPlanBuilder:
        """Set number of weeks."""
        self._weeks = weeks
        return self

    def starting_on(self, start_date: datetime) -> WorkoutPlanBuilder:
        """Set start date."""
        self._start_date = start_date
        return self

    def starting_today(self) -> WorkoutPlanBuilder:
        """Set start date to today."""
        self._start_date = datetime.now()
        return self

    def add_session_template(
        self,
        template_name: str,
        exercises: List[Dict[str, Any]],
        days_per_week: int = 1,
    ) -> WorkoutPlanBuilder:
        """Add a session template to the plan."""
        template = {
            "name": template_name,
            "exercises": exercises,
            "days_per_week": days_per_week,
        }
        self._session_templates.append(template)
        return self

    def build(self) -> Dict[str, Any]:
        """Build the workout plan (returns plan data structure)."""
        if not self._client_id:
            raise ValueError("Client ID is required")
        if not self._plan_name:
            raise ValueError("Plan name is required")
        if not self._session_templates:
            raise ValueError("At least one session template is required")

        start_date = self._start_date or datetime.now()
        sessions = []

        # Generate sessions for each week
        for week in range(self._weeks):
            week_start = start_date + timedelta(weeks=week)

            for template in self._session_templates:
                for day in range(template["days_per_week"]):
                    session_date = week_start + timedelta(days=day * 2)  # Every other day

                    session_builder = SessionBuilder()
                    session_builder = (session_builder
                        .for_client(self._client_id)
                        .named(f"{template['name']} - Week {week + 1}")
                        .on_date(session_date))

                    # Add exercises from template
                    for exercise_data in template["exercises"]:
                        sets = [
                            ExerciseSet(**set_data)
                            for set_data in exercise_data.get("sets", [])
                        ]
                        session_builder = session_builder.add_exercise(
                            exercise_data["exercise_id"],
                            sets,
                            exercise_data.get("notes", ""),
                        )

                    sessions.append(session_builder.build())

        return {
            "plan_name": self._plan_name,
            "client_id": self._client_id,
            "start_date": start_date,
            "weeks": self._weeks,
            "sessions": sessions,
            "templates": self._session_templates,
        }


class NutritionPlanBuilder(IBuilder):
    """
    Builder for creating nutrition plans.

    Example:
        plan = (NutritionPlanBuilder()
            .for_client(client_id=1)
            .with_target_calories(2500)
            .with_macro_split(protein=30, carbs=40, fats=30)
            .add_meal("Breakfast", breakfast_foods)
            .add_meal("Lunch", lunch_foods)
            .build())
    """

    def __init__(self):
        self.reset()

    def reset(self) -> NutritionPlanBuilder:
        """Reset builder to initial state."""
        self._client_id: Optional[int] = None
        self._target_calories: Optional[int] = None
        self._protein_percentage: Optional[float] = None
        self._carb_percentage: Optional[float] = None
        self._fat_percentage: Optional[float] = None
        self._meals: List[Dict[str, Any]] = []
        self._plan_name: Optional[str] = None
        return self

    def for_client(self, client_id: int) -> NutritionPlanBuilder:
        """Set the client for this plan."""
        self._client_id = client_id
        return self

    def named(self, plan_name: str) -> NutritionPlanBuilder:
        """Set plan name."""
        self._plan_name = plan_name
        return self

    def with_target_calories(self, calories: int) -> NutritionPlanBuilder:
        """Set target daily calories."""
        self._target_calories = calories
        return self

    def with_macro_split(
        self,
        protein: float,
        carbs: float,
        fats: float,
    ) -> NutritionPlanBuilder:
        """Set macronutrient percentages."""
        if abs((protein + carbs + fats) - 100) > 0.1:
            raise ValueError("Macro percentages must sum to 100")

        self._protein_percentage = protein
        self._carb_percentage = carbs
        self._fat_percentage = fats
        return self

    def for_weight_loss(self) -> NutritionPlanBuilder:
        """Set typical weight loss macro split."""
        return self.with_macro_split(protein=35, carbs=30, fats=35)

    def for_muscle_gain(self) -> NutritionPlanBuilder:
        """Set typical muscle gain macro split."""
        return self.with_macro_split(protein=25, carbs=50, fats=25)

    def for_maintenance(self) -> NutritionPlanBuilder:
        """Set typical maintenance macro split."""
        return self.with_macro_split(protein=25, carbs=45, fats=30)

    def add_meal(
        self,
        meal_name: str,
        foods: List[Dict[str, Any]],
        target_calories: Optional[int] = None,
    ) -> NutritionPlanBuilder:
        """Add a meal to the plan."""
        meal = {
            "name": meal_name,
            "foods": foods,
            "target_calories": target_calories,
        }
        self._meals.append(meal)
        return self

    def add_breakfast(self, foods: List[Dict[str, Any]]) -> NutritionPlanBuilder:
        """Add breakfast meal."""
        return self.add_meal("Breakfast", foods)

    def add_lunch(self, foods: List[Dict[str, Any]]) -> NutritionPlanBuilder:
        """Add lunch meal."""
        return self.add_meal("Lunch", foods)

    def add_dinner(self, foods: List[Dict[str, Any]]) -> NutritionPlanBuilder:
        """Add dinner meal."""
        return self.add_meal("Dinner", foods)

    def add_snack(self, foods: List[Dict[str, Any]], snack_name: str = "Snack") -> NutritionPlanBuilder:
        """Add snack meal."""
        return self.add_meal(snack_name, foods)

    def build(self) -> Dict[str, Any]:
        """Build the nutrition plan."""
        if not self._client_id:
            raise ValueError("Client ID is required")
        if not self._meals:
            raise ValueError("At least one meal is required")

        # Calculate macro targets if calories are provided
        macro_targets = None
        if self._target_calories and all([
            self._protein_percentage,
            self._carb_percentage,
            self._fat_percentage,
        ]):
            macro_targets = {
                "protein_grams": (self._target_calories * self._protein_percentage / 100) / 4,
                "carb_grams": (self._target_calories * self._carb_percentage / 100) / 4,
                "fat_grams": (self._target_calories * self._fat_percentage / 100) / 9,
            }

        return {
            "client_id": self._client_id,
            "plan_name": self._plan_name or "Custom Nutrition Plan",
            "target_calories": self._target_calories,
            "macro_percentages": {
                "protein": self._protein_percentage,
                "carbs": self._carb_percentage,
                "fats": self._fat_percentage,
            },
            "macro_targets": macro_targets,
            "meals": self._meals,
            "created_at": datetime.utcnow(),
        }


# Helper function for quick builder access
class BuilderFactory:
    """Factory for creating builders."""

    @staticmethod
    def client() -> ClientBuilder:
        """Create a new ClientBuilder."""
        return ClientBuilder()

    @staticmethod
    def session() -> SessionBuilder:
        """Create a new SessionBuilder."""
        return SessionBuilder()

    @staticmethod
    def workout_plan() -> WorkoutPlanBuilder:
        """Create a new WorkoutPlanBuilder."""
        return WorkoutPlanBuilder()

    @staticmethod
    def nutrition_plan() -> NutritionPlanBuilder:
        """Create a new NutritionPlanBuilder."""
        return NutritionPlanBuilder()


# Convenience functions
def build_client() -> ClientBuilder:
    """Create a new ClientBuilder."""
    return ClientBuilder()


def build_session() -> SessionBuilder:
    """Create a new SessionBuilder."""
    return SessionBuilder()


def build_workout_plan() -> WorkoutPlanBuilder:
    """Create a new WorkoutPlanBuilder."""
    return WorkoutPlanBuilder()


def build_nutrition_plan() -> NutritionPlanBuilder:
    """Create a new NutritionPlanBuilder."""
    return NutritionPlanBuilder()