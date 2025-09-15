"""
Strategy Pattern Implementation.

Provides interchangeable algorithms and business rules that can be
selected at runtime. Useful for workout generation, nutrition calculation,
and progress tracking strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from domain.entities import Client, Exercise, WorkoutSession


class IStrategy(ABC):
    """Base interface for all strategy implementations."""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the strategy with given context."""
        pass


class WorkoutGenerationStrategy(IStrategy):
    """Base class for workout generation strategies."""

    @abstractmethod
    def generate_workout(
        self,
        client: Client,
        available_exercises: List[Exercise],
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate a workout for the client."""
        pass

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute workout generation strategy."""
        return self.generate_workout(
            client=context["client"],
            available_exercises=context["available_exercises"],
            preferences=context.get("preferences", {}),
        )


class BeginnerWorkoutStrategy(WorkoutGenerationStrategy):
    """Workout generation strategy for beginners."""

    def generate_workout(
        self,
        client: Client,
        available_exercises: List[Exercise],
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate beginner-friendly workout."""
        # Filter exercises suitable for beginners
        beginner_exercises = [
            ex
            for ex in available_exercises
            if (
                ex.metadata
                and ex.metadata.difficulty_level in ["beginner", "intermediate"]
            )
            and client.can_perform_exercise(ex.id)
        ]

        # Focus on compound movements and basic exercises
        compound_exercises = [
            ex for ex in beginner_exercises if ex.exercise_type == "compound"
        ]

        # Select 4-6 exercises for a balanced workout
        selected_exercises = self._select_balanced_exercises(
            compound_exercises, beginner_exercises, max_exercises=6
        )

        # Generate sets with conservative rep ranges
        workout_exercises = []
        for i, exercise in enumerate(selected_exercises):
            sets = self._generate_beginner_sets(exercise, preferences)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": i + 1,
                    "rest_seconds": 90,  # Longer rest for beginners
                    "notes": "Focus on proper form",
                }
            )

        return {
            "name": "Beginner Full Body Workout",
            "exercises": workout_exercises,
            "estimated_duration": len(selected_exercises) * 8,  # 8 minutes per exercise
            "difficulty": "beginner",
            "notes": "Focus on learning proper form before increasing weight",
        }

    def _select_balanced_exercises(
        self,
        compound_exercises: List[Exercise],
        all_exercises: List[Exercise],
        max_exercises: int,
    ) -> List[Exercise]:
        """Select a balanced set of exercises."""
        selected = []
        muscle_groups_covered = set()

        # Prioritize compound movements
        for exercise in compound_exercises:
            if len(selected) >= max_exercises:
                break

            primary_muscle = exercise.muscle_group.primary
            if primary_muscle not in muscle_groups_covered:
                selected.append(exercise)
                muscle_groups_covered.add(primary_muscle)

        # Fill remaining slots with isolation exercises
        isolation_exercises = [
            ex
            for ex in all_exercises
            if ex.exercise_type == "isolation" and ex not in selected
        ]

        for exercise in isolation_exercises:
            if len(selected) >= max_exercises:
                break

            primary_muscle = exercise.muscle_group.primary
            if primary_muscle not in muscle_groups_covered:
                selected.append(exercise)
                muscle_groups_covered.add(primary_muscle)

        return selected

    def _generate_beginner_sets(
        self,
        exercise: Exercise,
        preferences: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate sets appropriate for beginners."""
        if exercise.exercise_type == "compound":
            # Compound exercises: 3 sets of 8-12 reps
            return [
                {
                    "reps": 10,
                    "weight_kg": None,
                    "notes": "Start with bodyweight or light weight",
                },
                {"reps": 10, "weight_kg": None, "notes": "Focus on form"},
                {
                    "reps": 8,
                    "weight_kg": None,
                    "notes": "Increase weight slightly if form is good",
                },
            ]
        else:
            # Isolation exercises: 2 sets of 12-15 reps
            return [
                {"reps": 15, "weight_kg": None, "notes": "Use light weight"},
                {"reps": 12, "weight_kg": None, "notes": "Focus on muscle connection"},
            ]


class IntermediateWorkoutStrategy(WorkoutGenerationStrategy):
    """Workout generation strategy for intermediate trainees."""

    def generate_workout(
        self,
        client: Client,
        available_exercises: List[Exercise],
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate intermediate-level workout."""
        # Filter exercises suitable for intermediate level
        suitable_exercises = [
            ex for ex in available_exercises if client.can_perform_exercise(ex.id)
        ]

        # Determine workout split based on preferences
        workout_type = preferences.get("workout_type", "upper_lower")
        focus = preferences.get("focus", "balanced")

        if workout_type == "push_pull_legs":
            return self._generate_ppl_workout(suitable_exercises, focus)
        elif workout_type == "upper_lower":
            return self._generate_upper_lower_workout(suitable_exercises, focus)
        else:
            return self._generate_full_body_workout(suitable_exercises, focus)

    def _generate_ppl_workout(
        self,
        exercises: List[Exercise],
        focus: str,
    ) -> Dict[str, Any]:
        """Generate push/pull/legs workout."""
        # This would contain logic for PPL split
        # For brevity, returning a simplified version
        push_muscles = {"chest", "shoulders", "triceps"}
        push_exercises = [
            ex for ex in exercises if ex.muscle_group.primary in push_muscles
        ]

        selected = push_exercises[:5]  # Select top 5 push exercises
        workout_exercises = []

        for i, exercise in enumerate(selected):
            sets = self._generate_intermediate_sets(exercise, focus)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": i + 1,
                    "rest_seconds": 60,
                }
            )

        return {
            "name": "Push Day - Intermediate",
            "exercises": workout_exercises,
            "estimated_duration": len(selected) * 12,
            "difficulty": "intermediate",
        }

    def _generate_upper_lower_workout(
        self,
        exercises: List[Exercise],
        focus: str,
    ) -> Dict[str, Any]:
        """Generate upper/lower body split workout."""
        upper_muscles = {"chest", "back", "shoulders", "biceps", "triceps"}
        upper_exercises = [
            ex for ex in exercises if ex.muscle_group.primary in upper_muscles
        ]

        selected = upper_exercises[:6]
        workout_exercises = []

        for i, exercise in enumerate(selected):
            sets = self._generate_intermediate_sets(exercise, focus)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": i + 1,
                    "rest_seconds": 75,
                }
            )

        return {
            "name": "Upper Body - Intermediate",
            "exercises": workout_exercises,
            "estimated_duration": len(selected) * 15,
            "difficulty": "intermediate",
        }

    def _generate_full_body_workout(
        self,
        exercises: List[Exercise],
        focus: str,
    ) -> Dict[str, Any]:
        """Generate full body workout."""
        # Select one exercise per major muscle group
        muscle_groups = ["chest", "back", "shoulders", "quadriceps", "hamstrings"]
        selected = []

        for muscle_group in muscle_groups:
            muscle_exercises = [
                ex for ex in exercises if ex.muscle_group.primary == muscle_group
            ]
            if muscle_exercises:
                selected.append(muscle_exercises[0])  # Take first available

        workout_exercises = []
        for i, exercise in enumerate(selected):
            sets = self._generate_intermediate_sets(exercise, focus)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": i + 1,
                    "rest_seconds": 90,
                }
            )

        return {
            "name": "Full Body - Intermediate",
            "exercises": workout_exercises,
            "estimated_duration": len(selected) * 12,
            "difficulty": "intermediate",
        }

    def _generate_intermediate_sets(
        self,
        exercise: Exercise,
        focus: str,
    ) -> List[Dict[str, Any]]:
        """Generate sets for intermediate level."""
        if focus == "strength":
            return [
                {"reps": 6, "weight_kg": None, "notes": "Heavy weight"},
                {"reps": 6, "weight_kg": None, "notes": "Heavy weight"},
                {"reps": 8, "weight_kg": None, "notes": "Slightly lighter"},
            ]
        elif focus == "hypertrophy":
            return [
                {"reps": 10, "weight_kg": None},
                {"reps": 12, "weight_kg": None},
                {"reps": 12, "weight_kg": None},
                {"reps": 15, "weight_kg": None, "notes": "Drop set"},
            ]
        else:  # balanced
            return [
                {"reps": 8, "weight_kg": None},
                {"reps": 10, "weight_kg": None},
                {"reps": 12, "weight_kg": None},
            ]


class AdvancedWorkoutStrategy(WorkoutGenerationStrategy):
    """Workout generation strategy for advanced trainees."""

    def generate_workout(
        self,
        client: Client,
        available_exercises: List[Exercise],
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate advanced-level workout with periodization."""
        # Advanced trainees need more specialized programming
        program_type = preferences.get("program_type", "powerbuilding")
        current_phase = preferences.get("phase", "hypertrophy")

        suitable_exercises = [
            ex for ex in available_exercises if client.can_perform_exercise(ex.id)
        ]

        if program_type == "powerlifting":
            return self._generate_powerlifting_workout(
                suitable_exercises, current_phase
            )
        elif program_type == "bodybuilding":
            return self._generate_bodybuilding_workout(
                suitable_exercises, current_phase
            )
        else:  # powerbuilding
            return self._generate_powerbuilding_workout(
                suitable_exercises, current_phase
            )

    def _generate_powerlifting_workout(
        self,
        exercises: List[Exercise],
        phase: str,
    ) -> Dict[str, Any]:
        """Generate powerlifting-focused workout."""
        # Focus on the big three: squat, bench, deadlift
        main_lifts = ["squat", "bench press", "deadlift"]
        main_exercises = [
            ex
            for ex in exercises
            if any(lift in ex.name.lower() for lift in main_lifts)
        ]

        accessory_exercises = [
            ex
            for ex in exercises
            if ex not in main_exercises
            and ex.exercise_type in ["compound", "isolation"]
        ]

        workout_exercises = []
        order = 1

        # Add main lift with appropriate sets based on phase
        if main_exercises:
            main_lift = main_exercises[0]
            main_sets = self._generate_powerlifting_sets(main_lift, phase)
            workout_exercises.append(
                {
                    "exercise_id": main_lift.id,
                    "exercise_name": main_lift.name,
                    "sets": main_sets,
                    "order": order,
                    "rest_seconds": 180,  # Long rest for heavy lifting
                    "notes": "Main lift - focus on technique",
                }
            )
            order += 1

        # Add 3-4 accessory exercises
        for exercise in accessory_exercises[:4]:
            sets = self._generate_accessory_sets(exercise, phase)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": order,
                    "rest_seconds": 120,
                }
            )
            order += 1

        return {
            "name": f"Powerlifting - {phase.title()} Phase",
            "exercises": workout_exercises,
            "estimated_duration": len(workout_exercises) * 18,
            "difficulty": "advanced",
            "phase": phase,
        }

    def _generate_bodybuilding_workout(
        self,
        exercises: List[Exercise],
        phase: str,
    ) -> Dict[str, Any]:
        """Generate bodybuilding-focused workout."""
        # High volume, muscle-focused training
        selected_exercises = exercises[:8]  # More exercises for volume
        workout_exercises = []

        for i, exercise in enumerate(selected_exercises):
            sets = self._generate_bodybuilding_sets(exercise, phase)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": i + 1,
                    "rest_seconds": 60,  # Shorter rest for pump
                    "notes": "Focus on mind-muscle connection",
                }
            )

        return {
            "name": f"Bodybuilding - {phase.title()} Phase",
            "exercises": workout_exercises,
            "estimated_duration": len(workout_exercises) * 10,
            "difficulty": "advanced",
            "phase": phase,
        }

    def _generate_powerbuilding_workout(
        self,
        exercises: List[Exercise],
        phase: str,
    ) -> Dict[str, Any]:
        """Generate powerbuilding workout (strength + hypertrophy)."""
        # Combine powerlifting and bodybuilding approaches
        compound_exercises = [ex for ex in exercises if ex.exercise_type == "compound"]
        isolation_exercises = [
            ex for ex in exercises if ex.exercise_type == "isolation"
        ]

        workout_exercises = []
        order = 1

        # Start with compound movements (strength focus)
        for exercise in compound_exercises[:2]:
            sets = self._generate_powerlifting_sets(exercise, phase)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": order,
                    "rest_seconds": 150,
                }
            )
            order += 1

        # Add isolation exercises (hypertrophy focus)
        for exercise in isolation_exercises[:4]:
            sets = self._generate_bodybuilding_sets(exercise, phase)
            workout_exercises.append(
                {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": sets,
                    "order": order,
                    "rest_seconds": 75,
                }
            )
            order += 1

        return {
            "name": f"Powerbuilding - {phase.title()} Phase",
            "exercises": workout_exercises,
            "estimated_duration": len(workout_exercises) * 12,
            "difficulty": "advanced",
            "phase": phase,
        }

    def _generate_powerlifting_sets(
        self,
        exercise: Exercise,
        phase: str,
    ) -> List[Dict[str, Any]]:
        """Generate powerlifting-specific sets."""
        if phase == "strength":
            return [
                {"reps": 3, "weight_kg": None, "notes": "90% 1RM"},
                {"reps": 3, "weight_kg": None, "notes": "90% 1RM"},
                {"reps": 1, "weight_kg": None, "notes": "95% 1RM"},
            ]
        elif phase == "peaking":
            return [
                {"reps": 1, "weight_kg": None, "notes": "Opener"},
                {"reps": 1, "weight_kg": None, "notes": "Second attempt"},
                {"reps": 1, "weight_kg": None, "notes": "Third attempt"},
            ]
        else:  # hypertrophy/volume
            return [
                {"reps": 6, "weight_kg": None, "notes": "80% 1RM"},
                {"reps": 6, "weight_kg": None, "notes": "80% 1RM"},
                {"reps": 8, "weight_kg": None, "notes": "75% 1RM"},
                {"reps": 8, "weight_kg": None, "notes": "75% 1RM"},
            ]

    def _generate_bodybuilding_sets(
        self,
        exercise: Exercise,
        phase: str,
    ) -> List[Dict[str, Any]]:
        """Generate bodybuilding-specific sets."""
        if phase == "cutting":
            return [
                {"reps": 15, "weight_kg": None, "notes": "Higher reps for definition"},
                {"reps": 15, "weight_kg": None},
                {"reps": 20, "weight_kg": None, "notes": "Pump set"},
            ]
        else:  # bulking/hypertrophy
            return [
                {"reps": 8, "weight_kg": None},
                {"reps": 10, "weight_kg": None},
                {"reps": 12, "weight_kg": None},
                {"reps": 15, "weight_kg": None, "notes": "Drop set"},
            ]

    def _generate_accessory_sets(
        self,
        exercise: Exercise,
        phase: str,
    ) -> List[Dict[str, Any]]:
        """Generate accessory exercise sets."""
        return [
            {"reps": 10, "weight_kg": None},
            {"reps": 12, "weight_kg": None},
            {"reps": 15, "weight_kg": None},
        ]


class NutritionCalculationStrategy(IStrategy):
    """Base class for nutrition calculation strategies."""

    @abstractmethod
    def calculate_daily_needs(
        self,
        client: Client,
        goal: str,
        activity_level: str,
    ) -> Dict[str, Any]:
        """Calculate daily nutritional needs."""
        pass

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute nutrition calculation strategy."""
        return self.calculate_daily_needs(
            client=context["client"],
            goal=context["goal"],
            activity_level=context.get("activity_level", "moderate"),
        )


class MifflinStJeorStrategy(NutritionCalculationStrategy):
    """Nutrition calculation using Mifflin-St Jeor equation."""

    def calculate_daily_needs(
        self,
        client: Client,
        goal: str,
        activity_level: str,
    ) -> Dict[str, Any]:
        """Calculate needs using Mifflin-St Jeor equation."""
        if not client.physical_profile:
            raise ValueError("Client physical profile is required for calculation")

        profile = client.physical_profile
        if not profile.weight_kg or not profile.height_cm:
            raise ValueError("Weight and height are required")

        # Calculate BMR using Mifflin-St Jeor equation
        # Assume male for now (in real implementation, this would come from client data)
        bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * 30) + 5

        # Apply activity factor
        activity_factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9,
        }

        activity_factor = activity_factors.get(activity_level, 1.55)
        tdee = bmr * activity_factor

        # Adjust for goal
        goal_adjustments = {
            "weight_loss": -500,  # 500 calorie deficit
            "muscle_gain": 300,  # 300 calorie surplus
            "maintenance": 0,
            "aggressive_cut": -750,
            "lean_bulk": 200,
        }

        calorie_adjustment = goal_adjustments.get(goal, 0)
        target_calories = int(tdee + calorie_adjustment)

        # Calculate macros
        macros = self._calculate_macros(target_calories, goal)

        return {
            "bmr": int(bmr),
            "tdee": int(tdee),
            "target_calories": target_calories,
            "macros": macros,
            "activity_level": activity_level,
            "goal": goal,
            "method": "Mifflin-St Jeor",
        }

    def _calculate_macros(self, calories: int, goal: str) -> Dict[str, Any]:
        """Calculate macronutrient targets."""
        macro_splits = {
            "weight_loss": {"protein": 35, "carbs": 30, "fat": 35},
            "muscle_gain": {"protein": 25, "carbs": 50, "fat": 25},
            "maintenance": {"protein": 25, "carbs": 45, "fat": 30},
            "aggressive_cut": {"protein": 40, "carbs": 25, "fat": 35},
            "lean_bulk": {"protein": 25, "carbs": 45, "fat": 30},
        }

        split = macro_splits.get(goal, macro_splits["maintenance"])

        return {
            "protein_grams": int((calories * split["protein"] / 100) / 4),
            "carb_grams": int((calories * split["carbs"] / 100) / 4),
            "fat_grams": int((calories * split["fat"] / 100) / 9),
            "protein_percentage": split["protein"],
            "carb_percentage": split["carbs"],
            "fat_percentage": split["fat"],
        }


class ProgressTrackingStrategy(IStrategy):
    """Base class for progress tracking strategies."""

    @abstractmethod
    def calculate_progress(
        self,
        client: Client,
        sessions: List[WorkoutSession],
        time_period: str,
    ) -> Dict[str, Any]:
        """Calculate client progress metrics."""
        pass

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute progress tracking strategy."""
        return self.calculate_progress(
            client=context["client"],
            sessions=context["sessions"],
            time_period=context.get("time_period", "monthly"),
        )


class VolumeProgressStrategy(ProgressTrackingStrategy):
    """Track progress based on training volume."""

    def calculate_progress(
        self,
        client: Client,
        sessions: List[WorkoutSession],
        time_period: str,
    ) -> Dict[str, Any]:
        """Calculate volume-based progress."""
        if not sessions:
            return {"error": "No sessions to analyze"}

        # Group sessions by time periods
        period_data = self._group_by_period(sessions, time_period)

        # Calculate metrics for each period
        progress_data = {}
        for period, period_sessions in period_data.items():
            total_volume = sum(s.calculate_total_volume() for s in period_sessions)
            total_sessions = len(period_sessions)
            avg_volume_per_session = (
                total_volume / total_sessions if total_sessions > 0 else 0
            )

            progress_data[period] = {
                "total_volume": total_volume,
                "session_count": total_sessions,
                "avg_volume_per_session": avg_volume_per_session,
            }

        # Calculate overall trends
        periods = sorted(progress_data.keys())
        if len(periods) >= 2:
            first_period = progress_data[periods[0]]
            last_period = progress_data[periods[-1]]

            volume_change = last_period["total_volume"] - first_period["total_volume"]
            volume_change_percent = (
                (volume_change / first_period["total_volume"]) * 100
                if first_period["total_volume"] > 0
                else 0
            )

            trend = {
                "volume_change": volume_change,
                "volume_change_percent": volume_change_percent,
                "trend": "increasing"
                if volume_change > 0
                else "decreasing"
                if volume_change < 0
                else "stable",
            }
        else:
            trend = {"trend": "insufficient_data"}

        return {
            "tracking_method": "volume_based",
            "time_period": time_period,
            "period_data": progress_data,
            "overall_trend": trend,
            "total_sessions_analyzed": len(sessions),
        }

    def _group_by_period(
        self,
        sessions: List[WorkoutSession],
        time_period: str,
    ) -> Dict[str, List[WorkoutSession]]:
        """Group sessions by time period."""
        grouped = {}

        for session in sessions:
            if time_period == "weekly":
                # Group by ISO week
                key = session.session_date.strftime("%Y-W%U")
            elif time_period == "monthly":
                # Group by month
                key = session.session_date.strftime("%Y-%m")
            else:  # daily
                key = session.session_date.strftime("%Y-%m-%d")

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(session)

        return grouped


# Strategy Context Class
class StrategyContext:
    """Context class for managing strategies."""

    def __init__(self):
        self._strategies: Dict[str, Dict[str, IStrategy]] = {
            "workout_generation": {
                "beginner": BeginnerWorkoutStrategy(),
                "intermediate": IntermediateWorkoutStrategy(),
                "advanced": AdvancedWorkoutStrategy(),
            },
            "nutrition_calculation": {
                "mifflin_st_jeor": MifflinStJeorStrategy(),
            },
            "progress_tracking": {
                "volume_based": VolumeProgressStrategy(),
            },
        }

    def get_strategy(self, category: str, strategy_name: str) -> Optional[IStrategy]:
        """Get a specific strategy."""
        return self._strategies.get(category, {}).get(strategy_name)

    def execute_strategy(
        self,
        category: str,
        strategy_name: str,
        context: Dict[str, Any],
    ) -> Any:
        """Execute a specific strategy."""
        strategy = self.get_strategy(category, strategy_name)
        if not strategy:
            raise ValueError(f"Strategy not found: {category}.{strategy_name}")

        return strategy.execute(context)

    def register_strategy(
        self,
        category: str,
        strategy_name: str,
        strategy: IStrategy,
    ) -> None:
        """Register a new strategy."""
        if category not in self._strategies:
            self._strategies[category] = {}

        self._strategies[category][strategy_name] = strategy

    def list_strategies(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """List available strategies."""
        if category:
            return {category: list(self._strategies.get(category, {}).keys())}

        return {
            cat: list(strategies.keys()) for cat, strategies in self._strategies.items()
        }


# Global strategy context instance
strategy_context = StrategyContext()
