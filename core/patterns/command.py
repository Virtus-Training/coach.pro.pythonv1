"""
Command Pattern Implementation.

Provides command objects that encapsulate requests as objects,
allowing for parameterization, queuing, logging, and undo operations.
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.events import EventBus
from domain.entities import Client, WorkoutSession
from domain.events import (
    ClientCreatedEvent,
    ClientUpdatedEvent,
    SessionCompletedEvent,
    SessionCreatedEvent,
)


class ICommand(ABC):
    """Base interface for all commands."""

    def __init__(self, command_id: Optional[str] = None):
        self.command_id = command_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.executed = False
        self.result: Any = None
        self.error: Optional[Exception] = None

    @abstractmethod
    async def execute(self) -> Any:
        """Execute the command."""
        pass

    @abstractmethod
    async def undo(self) -> Any:
        """Undo the command (if possible)."""
        pass

    @abstractmethod
    def can_undo(self) -> bool:
        """Check if command can be undone."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Get command metadata for logging/auditing."""
        return {
            "command_id": self.command_id,
            "command_type": self.__class__.__name__,
            "timestamp": self.timestamp.isoformat(),
            "executed": self.executed,
            "has_error": self.error is not None,
        }


class CompositeCommand(ICommand):
    """Command that contains multiple sub-commands."""

    def __init__(self, commands: List[ICommand], command_id: Optional[str] = None):
        super().__init__(command_id)
        self.commands = commands
        self.executed_commands: List[ICommand] = []

    async def execute(self) -> Any:
        """Execute all sub-commands in order."""
        results = []

        try:
            for command in self.commands:
                result = await command.execute()
                self.executed_commands.append(command)
                results.append(result)

            self.executed = True
            self.result = results
            return results

        except Exception as e:
            self.error = e
            # Rollback executed commands in reverse order
            await self.undo()
            raise

    async def undo(self) -> Any:
        """Undo all executed commands in reverse order."""
        undo_results = []

        # Undo in reverse order
        for command in reversed(self.executed_commands):
            if command.can_undo():
                try:
                    undo_result = await command.undo()
                    undo_results.append(undo_result)
                except Exception as e:
                    # Log error but continue undoing other commands
                    print(f"Error undoing command {command.command_id}: {e}")

        self.executed_commands.clear()
        return undo_results

    def can_undo(self) -> bool:
        """Check if all executed commands can be undone."""
        return all(cmd.can_undo() for cmd in self.executed_commands)


class CreateClientCommand(ICommand):
    """Command to create a new client."""

    def __init__(
        self,
        client_data: Dict[str, Any],
        client_repository,
        event_bus: Optional[EventBus] = None,
        command_id: Optional[str] = None,
    ):
        super().__init__(command_id)
        self.client_data = client_data
        self.client_repository = client_repository
        self.event_bus = event_bus
        self.created_client: Optional[Client] = None

    async def execute(self) -> Client:
        """Execute client creation."""
        try:
            # Create client using factory pattern
            from core.patterns.factory import ClientFactory

            factory = ClientFactory()
            client = factory.create(**self.client_data)

            # Save to repository
            saved_client = await self.client_repository.add(client)
            self.created_client = saved_client
            self.executed = True
            self.result = saved_client

            # Publish domain event
            if self.event_bus:
                event = ClientCreatedEvent(
                    client_id=str(saved_client.id),
                    email=saved_client.personal_info.email,
                    full_name=saved_client.personal_info.full_name,
                )
                await self.event_bus.publish(event)

            return saved_client

        except Exception as e:
            self.error = e
            raise

    async def undo(self) -> bool:
        """Undo client creation by deleting the client."""
        if not self.created_client:
            return False

        try:
            success = await self.client_repository.delete(self.created_client.id)
            if success:
                self.executed = False
                self.created_client = None

            return success

        except Exception as e:
            print(f"Error undoing client creation: {e}")
            return False

    def can_undo(self) -> bool:
        """Client creation can be undone by deletion."""
        return self.executed and self.created_client is not None


class UpdateClientCommand(ICommand):
    """Command to update an existing client."""

    def __init__(
        self,
        client_id: int,
        update_data: Dict[str, Any],
        client_repository,
        event_bus: Optional[EventBus] = None,
        command_id: Optional[str] = None,
    ):
        super().__init__(command_id)
        self.client_id = client_id
        self.update_data = update_data
        self.client_repository = client_repository
        self.event_bus = event_bus
        self.original_data: Optional[Dict[str, Any]] = None
        self.updated_client: Optional[Client] = None

    async def execute(self) -> Client:
        """Execute client update."""
        try:
            # Get current client
            client = await self.client_repository.get_by_id(self.client_id)
            if not client:
                raise ValueError(f"Client not found: {self.client_id}")

            # Store original data for undo
            self.original_data = {
                "personal_info": client.personal_info,
                "physical_profile": client.physical_profile,
                "fitness_goals": client.fitness_goals,
                "excluded_exercise_ids": client.excluded_exercise_ids,
            }

            # Apply updates
            if "personal_info" in self.update_data:
                client.update_personal_info(self.update_data["personal_info"])

            if "physical_profile" in self.update_data:
                client.update_physical_profile(self.update_data["physical_profile"])

            if "fitness_goals" in self.update_data:
                client.set_fitness_goals(self.update_data["fitness_goals"])

            if "excluded_exercise_ids" in self.update_data:
                client.set_exercise_exclusions(
                    set(self.update_data["excluded_exercise_ids"])
                )

            # Save to repository
            updated_client = await self.client_repository.update(client)
            self.updated_client = updated_client
            self.executed = True
            self.result = updated_client

            # Publish domain event
            if self.event_bus:
                event = ClientUpdatedEvent(
                    client_id=str(client.id),
                    updated_fields=list(self.update_data.keys()),
                )
                await self.event_bus.publish(event)

            return updated_client

        except Exception as e:
            self.error = e
            raise

    async def undo(self) -> bool:
        """Undo client update by restoring original data."""
        if not self.original_data or not self.updated_client:
            return False

        try:
            # Restore original values
            if "personal_info" in self.original_data:
                self.updated_client.update_personal_info(
                    self.original_data["personal_info"]
                )

            if (
                "physical_profile" in self.original_data
                and self.original_data["physical_profile"]
            ):
                self.updated_client.update_physical_profile(
                    self.original_data["physical_profile"]
                )

            if (
                "fitness_goals" in self.original_data
                and self.original_data["fitness_goals"]
            ):
                self.updated_client.set_fitness_goals(
                    self.original_data["fitness_goals"]
                )

            if "excluded_exercise_ids" in self.original_data:
                self.updated_client.set_exercise_exclusions(
                    self.original_data["excluded_exercise_ids"]
                )

            # Save restored state
            await self.client_repository.update(self.updated_client)
            self.executed = False
            return True

        except Exception as e:
            print(f"Error undoing client update: {e}")
            return False

    def can_undo(self) -> bool:
        """Client update can be undone."""
        return self.executed and self.original_data is not None


class GenerateWorkoutCommand(ICommand):
    """Command to generate a workout for a client."""

    def __init__(
        self,
        client_id: int,
        workout_preferences: Dict[str, Any],
        client_repository,
        exercise_repository,
        session_repository,
        strategy_context,
        event_bus: Optional[EventBus] = None,
        command_id: Optional[str] = None,
    ):
        super().__init__(command_id)
        self.client_id = client_id
        self.workout_preferences = workout_preferences
        self.client_repository = client_repository
        self.exercise_repository = exercise_repository
        self.session_repository = session_repository
        self.strategy_context = strategy_context
        self.event_bus = event_bus
        self.generated_session: Optional[WorkoutSession] = None

    async def execute(self) -> WorkoutSession:
        """Execute workout generation."""
        try:
            # Get client and available exercises
            client = await self.client_repository.get_by_id(self.client_id)
            if not client:
                raise ValueError(f"Client not found: {self.client_id}")

            available_exercises = await self.exercise_repository.get_all()

            # Determine appropriate strategy based on client level
            fitness_level = self.workout_preferences.get(
                "fitness_level", "intermediate"
            )
            strategy = self.strategy_context.get_strategy(
                "workout_generation", fitness_level
            )

            if not strategy:
                raise ValueError(f"Unknown workout strategy: {fitness_level}")

            # Generate workout
            workout_data = strategy.execute(
                {
                    "client": client,
                    "available_exercises": available_exercises,
                    "preferences": self.workout_preferences,
                }
            )

            # Create session using builder pattern
            from core.patterns.builder import SessionBuilder

            session_builder = SessionBuilder()
            session_builder = (
                session_builder.for_client(self.client_id)
                .named(workout_data["name"])
                .today()
                .with_duration(workout_data.get("estimated_duration"))
                .with_notes(workout_data.get("notes", ""))
            )

            # Add exercises from generated workout
            for exercise_data in workout_data["exercises"]:
                from domain.entities import ExerciseSet

                sets = [ExerciseSet(**set_data) for set_data in exercise_data["sets"]]

                session_builder = session_builder.add_exercise(
                    exercise_data["exercise_id"],
                    sets,
                    exercise_data.get("notes", ""),
                )

            session = session_builder.build()

            # Save to repository
            saved_session = await self.session_repository.add(session)
            self.generated_session = saved_session
            self.executed = True
            self.result = saved_session

            # Publish domain event
            if self.event_bus:
                event = SessionCreatedEvent(
                    session_id=str(saved_session.id),
                    client_id=str(self.client_id),
                    session_name=saved_session.name,
                    session_date=saved_session.session_date.isoformat(),
                )
                await self.event_bus.publish(event)

            return saved_session

        except Exception as e:
            self.error = e
            raise

    async def undo(self) -> bool:
        """Undo workout generation by deleting the session."""
        if not self.generated_session:
            return False

        try:
            success = await self.session_repository.delete(self.generated_session.id)
            if success:
                self.executed = False
                self.generated_session = None

            return success

        except Exception as e:
            print(f"Error undoing workout generation: {e}")
            return False

    def can_undo(self) -> bool:
        """Workout generation can be undone by deletion."""
        return self.executed and self.generated_session is not None


class CompleteSessionCommand(ICommand):
    """Command to mark a session as completed."""

    def __init__(
        self,
        session_id: int,
        completion_data: Dict[str, Any],
        session_repository,
        event_bus: Optional[EventBus] = None,
        command_id: Optional[str] = None,
    ):
        super().__init__(command_id)
        self.session_id = session_id
        self.completion_data = completion_data
        self.session_repository = session_repository
        self.event_bus = event_bus
        self.original_state: Optional[bool] = None
        self.completed_session: Optional[WorkoutSession] = None

    async def execute(self) -> WorkoutSession:
        """Execute session completion."""
        try:
            # Get session
            session = await self.session_repository.get_by_id(self.session_id)
            if not session:
                raise ValueError(f"Session not found: {self.session_id}")

            # Store original completion state
            self.original_state = session.is_completed

            # Apply completion data
            if "notes" in self.completion_data:
                session.set_notes(self.completion_data["notes"])

            if "duration_minutes" in self.completion_data:
                session.set_duration(self.completion_data["duration_minutes"])

            # Mark as completed
            session.complete_session()

            # Save to repository
            updated_session = await self.session_repository.update(session)
            self.completed_session = updated_session
            self.executed = True
            self.result = updated_session

            # Publish domain event
            if self.event_bus:
                event = SessionCompletedEvent(
                    session_id=str(session.id),
                    client_id=str(session.client_id),
                    completion_date=datetime.utcnow().isoformat(),
                    total_exercises=session.calculate_total_exercises(),
                    total_volume=session.calculate_total_volume(),
                    duration_minutes=session.duration_minutes,
                )
                await self.event_bus.publish(event)

            return updated_session

        except Exception as e:
            self.error = e
            raise

    async def undo(self) -> bool:
        """Undo session completion by restoring original state."""
        if self.original_state is None or not self.completed_session:
            return False

        try:
            # This is a simplified undo - in reality you'd need to store more state
            # For now, we can't easily "uncomplete" a session due to the domain model design
            # This would require refactoring the domain model to support state changes
            print(
                "Warning: Session completion cannot be undone with current domain model"
            )
            return False

        except Exception as e:
            print(f"Error undoing session completion: {e}")
            return False

    def can_undo(self) -> bool:
        """Session completion cannot currently be undone."""
        return False  # Would need domain model changes to support this


class CommandInvoker:
    """
    Command invoker that manages command execution and provides
    undo/redo functionality.
    """

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.executed_commands: List[ICommand] = []
        self.undo_stack: List[ICommand] = []

    async def execute_command(self, command: ICommand) -> Any:
        """Execute a command and add it to history."""
        try:
            result = await command.execute()

            # Add to history if execution was successful
            if command.executed:
                self.executed_commands.append(command)

                # Limit history size
                if len(self.executed_commands) > self.max_history:
                    self.executed_commands.pop(0)

                # Clear redo stack when new command is executed
                self.undo_stack.clear()

            return result

        except Exception:
            # Command failed, don't add to history
            raise

    async def undo_last_command(self) -> bool:
        """Undo the last executed command."""
        if not self.executed_commands:
            return False

        last_command = self.executed_commands.pop()

        if last_command.can_undo():
            try:
                await last_command.undo()
                self.undo_stack.append(last_command)
                return True

            except Exception as e:
                # Undo failed, put command back in history
                self.executed_commands.append(last_command)
                print(f"Error undoing command: {e}")
                return False

        return False

    async def redo_last_command(self) -> bool:
        """Redo the last undone command."""
        if not self.undo_stack:
            return False

        command = self.undo_stack.pop()

        try:
            await command.execute()
            self.executed_commands.append(command)
            return True

        except Exception as e:
            # Redo failed, put command back in undo stack
            self.undo_stack.append(command)
            print(f"Error redoing command: {e}")
            return False

    def get_command_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent command history."""
        recent_commands = (
            self.executed_commands[-limit:] if limit else self.executed_commands
        )
        return [cmd.get_metadata() for cmd in recent_commands]

    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return bool(self.executed_commands) and self.executed_commands[-1].can_undo()

    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return bool(self.undo_stack)

    def clear_history(self) -> None:
        """Clear command history."""
        self.executed_commands.clear()
        self.undo_stack.clear()


# Command Factory for easy creation
class CommandFactory:
    """Factory for creating commands."""

    @staticmethod
    def create_client_command(
        client_data: Dict[str, Any],
        repositories: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> CreateClientCommand:
        """Create a client creation command."""
        return CreateClientCommand(
            client_data=client_data,
            client_repository=repositories["client_repository"],
            event_bus=event_bus,
        )

    @staticmethod
    def update_client_command(
        client_id: int,
        update_data: Dict[str, Any],
        repositories: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> UpdateClientCommand:
        """Create a client update command."""
        return UpdateClientCommand(
            client_id=client_id,
            update_data=update_data,
            client_repository=repositories["client_repository"],
            event_bus=event_bus,
        )

    @staticmethod
    def generate_workout_command(
        client_id: int,
        workout_preferences: Dict[str, Any],
        repositories: Dict[str, Any],
        strategy_context,
        event_bus: Optional[EventBus] = None,
    ) -> GenerateWorkoutCommand:
        """Create a workout generation command."""
        return GenerateWorkoutCommand(
            client_id=client_id,
            workout_preferences=workout_preferences,
            client_repository=repositories["client_repository"],
            exercise_repository=repositories["exercise_repository"],
            session_repository=repositories["session_repository"],
            strategy_context=strategy_context,
            event_bus=event_bus,
        )

    @staticmethod
    def complete_session_command(
        session_id: int,
        completion_data: Dict[str, Any],
        repositories: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> CompleteSessionCommand:
        """Create a session completion command."""
        return CompleteSessionCommand(
            session_id=session_id,
            completion_data=completion_data,
            session_repository=repositories["session_repository"],
            event_bus=event_bus,
        )

    @staticmethod
    def composite_command(commands: List[ICommand]) -> CompositeCommand:
        """Create a composite command."""
        return CompositeCommand(commands)
