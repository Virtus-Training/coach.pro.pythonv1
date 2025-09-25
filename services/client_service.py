"""Client Service with Unit of Work pattern and domain events."""

from __future__ import annotations

import re
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from core.events import IEventBus
from core.exceptions import BusinessRuleViolationError, ValidationError
from core.unit_of_work import IAsyncUnitOfWork, create_unit_of_work
from domain.events import (
    ClientCreatedEvent,
    ClientUpdatedEvent,
    ClientDeactivatedEvent,
)
from models.client import (
    Client,
    PersonalInfo,
    PhysicalMetrics,
    HealthProfile,
    ActivityLevel,
    Gender,
)
from repositories.interfaces import ISpecification, QueryOptions, QueryResult


class ClientByEmailSpecification(ISpecification[Client]):
    """Specification to find client by email."""

    def __init__(self, email: str):
        self.email = email.lower().strip()

    def is_satisfied_by(self, entity: Client) -> bool:
        return (
            entity.personal_info.email
            and entity.personal_info.email.lower().strip() == self.email
        )

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "LOWER(TRIM(email)) = ?", (self.email,)


class ActiveClientsSpecification(ISpecification[Client]):
    """Specification for active clients with high readiness scores."""

    def __init__(self, min_readiness_score: float = 70.0):
        self.min_readiness_score = min_readiness_score

    def is_satisfied_by(self, entity: Client) -> bool:
        return entity.get_fitness_readiness_score() >= self.min_readiness_score

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        # This would require complex SQL for readiness score calculation
        # For now, return a placeholder
        return "1=1", ()


class ClientService:
    """Client domain service with enterprise patterns."""

    def __init__(
        self,
        uow_factory = None,  # Callable[[], IAsyncUnitOfWork]
        event_bus: Optional[IEventBus] = None,
    ) -> None:
        self._uow_factory = uow_factory or create_unit_of_work
        self._event_bus = event_bus

    async def get_all_clients(
        self, options: Optional[QueryOptions] = None
    ) -> QueryResult[Client]:
        """Get all clients with pagination and filtering."""
        async with self._uow_factory() as uow:
            return await uow.clients.get_all(options)

    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Get client by ID."""
        async with self._uow_factory() as uow:
            return await uow.clients.get_by_id(client_id)

    async def get_client_with_exclusions(self, client_id: int) -> tuple[Client, List[int]]:
        """Return a client and the list of excluded exercise IDs."""
        async with self._uow_factory() as uow:
            client = await uow.clients.get_by_id(client_id)
            if not client:
                raise ValueError("Client introuvable")
            exclusions = client.health_profile.exercise_exclusions
            return client, exclusions

    def _validate_client_data(self, data: Dict[str, Any]) -> None:
        """Validate client data with comprehensive business rules."""
        errors: Dict[str, str] = {}

        # Required fields validation
        if not data.get("first_name", "").strip():
            errors["first_name"] = "Le prénom est obligatoire."
        if not data.get("last_name", "").strip():
            errors["last_name"] = "Le nom est obligatoire."

        # Email validation
        email = data.get("email", "").strip()
        if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errors["email"] = "Format d'email invalide."

        # Physical metrics validation
        weight = data.get("weight_kg")
        if weight is not None and (not isinstance(weight, (int, float)) or weight <= 0 or weight > 500):
            errors["weight_kg"] = "Poids invalide (doit être entre 0 et 500 kg)."

        height = data.get("height_cm")
        if height is not None and (not isinstance(height, (int, float)) or height <= 0 or height > 300):
            errors["height_cm"] = "Taille invalide (doit être entre 0 et 300 cm)."

        # Birth date validation
        birth_date_str = data.get("birth_date")
        if birth_date_str:
            try:
                birth_date = date.fromisoformat(birth_date_str)
                if birth_date > date.today():
                    errors["birth_date"] = "La date de naissance ne peut pas être future."
                # Check minimum age (optional business rule)
                age = (date.today() - birth_date).days // 365
                if age < 13:  # Minimum age requirement
                    errors["birth_date"] = "L'âge minimum requis est 13 ans."
            except ValueError:
                errors["birth_date"] = "Format de date invalide (YYYY-MM-DD)."

        if errors:
            raise ValidationError("Erreurs de validation", errors)

    async def _validate_unique_email(self, email: str, exclude_client_id: Optional[int] = None) -> None:
        """Validate email uniqueness."""
        if not email:
            return

        async with self._uow_factory() as uow:
            existing_client = await uow.clients.find_by_email(email)
            if existing_client and existing_client.id != exclude_client_id:
                raise BusinessRuleViolationError(f"Un client avec l'email {email} existe déjà.")

    async def create_client(self, client_data: Dict[str, Any]) -> Client:
        """Create new client with full validation and domain events."""
        # Validate input data
        self._validate_client_data(client_data)

        # Check email uniqueness
        email = client_data.get("email", "").strip()
        if email:
            await self._validate_unique_email(email)

        # Parse and validate dates
        birth_date = None
        if client_data.get("birth_date"):
            try:
                birth_date = date.fromisoformat(client_data["birth_date"])
            except ValueError:
                raise ValidationError("Format de date invalide", {"birth_date": "Format attendu: YYYY-MM-DD"})

        # Parse gender
        gender = None
        if client_data.get("gender"):
            try:
                gender = Gender(client_data["gender"])
            except ValueError:
                raise ValidationError("Genre invalide", {"gender": "Valeurs acceptées: male, female, other"})

        # Parse activity level
        activity_level = None
        if client_data.get("activity_level"):
            try:
                activity_level = ActivityLevel(client_data["activity_level"])
            except ValueError:
                raise ValidationError("Niveau d'activité invalide", {"activity_level": "Voir les valeurs acceptées"})

        # Create value objects
        personal_info = PersonalInfo(
            first_name=client_data["first_name"].strip(),
            last_name=client_data["last_name"].strip(),
            email=email or None,
            birth_date=birth_date,
            gender=gender,
        )

        physical_metrics = PhysicalMetrics(
            weight_kg=client_data.get("weight_kg"),
            height_cm=client_data.get("height_cm"),
            body_fat_percentage=client_data.get("body_fat_percentage"),
            muscle_mass_kg=client_data.get("muscle_mass_kg"),
        )

        health_profile = HealthProfile(
            objectives=client_data.get("objectives", "").strip() or None,
            medical_history=client_data.get("medical_history", "").strip() or None,
            activity_level=activity_level,
            exercise_exclusions=client_data.get("exercise_exclusions", []),
            allergies=client_data.get("allergies", []),
            medications=client_data.get("medications", []),
        )

        # Create client entity
        client = Client(
            client_id=None,
            personal_info=personal_info,
            physical_metrics=physical_metrics,
            health_profile=health_profile,
        )

        # Save to database using Unit of Work
        async with self._uow_factory() as uow:
            created_client = await uow.clients.create(client)
            await uow.save_changes()

            # Publish domain events
            if self._event_bus:
                for event in created_client.get_domain_events():
                    await self._event_bus.publish(event)

            return created_client

    async def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Client:
        """Update existing client with validation and domain events."""
        # Validate input data
        self._validate_client_data(client_data)

        # Check email uniqueness (excluding current client)
        email = client_data.get("email", "").strip()
        if email:
            await self._validate_unique_email(email, exclude_client_id=client_id)

        async with self._uow_factory() as uow:
            # Get existing client
            client = await uow.clients.get_by_id(client_id)
            if not client:
                raise ValueError(f"Client {client_id} introuvable")

            # Parse dates and enums
            birth_date = None
            if client_data.get("birth_date"):
                try:
                    birth_date = date.fromisoformat(client_data["birth_date"])
                except ValueError:
                    raise ValidationError("Format de date invalide", {"birth_date": "Format attendu: YYYY-MM-DD"})

            gender = None
            if client_data.get("gender"):
                try:
                    gender = Gender(client_data["gender"])
                except ValueError:
                    raise ValidationError("Genre invalide", {"gender": "Valeurs acceptées: male, female, other"})

            activity_level = None
            if client_data.get("activity_level"):
                try:
                    activity_level = ActivityLevel(client_data["activity_level"])
                except ValueError:
                    raise ValidationError("Niveau d'activité invalide", {"activity_level": "Voir les valeurs acceptées"})

            # Update personal info
            client.update_personal_info(
                first_name=client_data.get("first_name"),
                last_name=client_data.get("last_name"),
                email=email or None,
                birth_date=birth_date,
                gender=gender,
            )

            # Update physical metrics
            client.update_physical_metrics(
                weight_kg=client_data.get("weight_kg"),
                height_cm=client_data.get("height_cm"),
                body_fat_percentage=client_data.get("body_fat_percentage"),
                muscle_mass_kg=client_data.get("muscle_mass_kg"),
            )

            # Update health profile
            if "objectives" in client_data:
                client.health_profile.objectives = client_data["objectives"].strip() or None

            if "medical_history" in client_data:
                client.health_profile.medical_history = client_data["medical_history"].strip() or None

            if "activity_level" in client_data:
                client.health_profile.activity_level = activity_level

            if "exercise_exclusions" in client_data:
                client.update_exercise_exclusions(client_data["exercise_exclusions"])

            # Save changes
            updated_client = await uow.clients.update(client)
            await uow.save_changes()

            # Publish domain events
            if self._event_bus:
                for event in updated_client.get_domain_events():
                    await self._event_bus.publish(event)

            return updated_client

    async def delete_client(self, client_id: int) -> bool:
        """Soft delete client with domain events."""
        async with self._uow_factory() as uow:
            client = await uow.clients.get_by_id(client_id)
            if not client:
                return False

            # Perform soft delete
            success = await uow.clients.soft_delete(client_id)
            if success:
                await uow.save_changes()

                # Publish domain event
                if self._event_bus:
                    await self._event_bus.publish(
                        ClientDeactivatedEvent(
                            client_id=str(client_id),
                            reason="Suppression demandée",
                        )
                    )

            return success

    # Compatibility methods for existing code

    async def get_all_clients_list(self) -> List[Client]:
        """Get all clients as a list (compatibility method)."""
        result = await self.get_all_clients()
        return result.data

    async def add_client(self, client_data: Dict[str, Any]) -> Client:
        """Add client (compatibility method)."""
        return await self.create_client(client_data)

    async def update_client_legacy(self, client: Client, client_data: Dict[str, Any]) -> Client:
        """Update client using legacy signature (compatibility method)."""
        if not client.id:
            raise ValueError("Client ID is required")
        return await self.update_client(client.id, client_data)

    async def update_client_anamnese(self, client_id: int, objectifs: str, antecedents: str) -> Client:
        """Update client anamnesis (compatibility method)."""
        async with self._uow_factory() as uow:
            client = await uow.clients.get_by_id(client_id)
            if not client:
                raise ValueError(f"Client {client_id} introuvable")

            # Update health profile
            client.health_profile.objectives = objectifs.strip() or None
            client.health_profile.medical_history = antecedents.strip() or None
            client.updated_at = datetime.now()

            # Save changes
            updated_client = await uow.clients.update(client)
            await uow.save_changes()

            return updated_client

    async def get_client_exclusions(self, client_id: int) -> List[int]:
        """Get exercise exclusions for client."""
        client = await self.get_client_by_id(client_id)
        return client.health_profile.exercise_exclusions if client else []

    async def update_client_exclusions(self, client_id: int, exercise_ids: List[int]) -> Client:
        """Update client's exercise exclusions."""
        async with self._uow_factory() as uow:
            client = await uow.clients.get_by_id(client_id)
            if not client:
                raise ValueError(f"Client {client_id} introuvable")

            # Update exclusions (this will trigger domain events)
            client.update_exercise_exclusions(exercise_ids)

            # Save changes
            updated_client = await uow.clients.update(client)
            await uow.save_changes()

            # Publish domain events
            if self._event_bus:
                for event in updated_client.get_domain_events():
                    await self._event_bus.publish(event)

            return updated_client
