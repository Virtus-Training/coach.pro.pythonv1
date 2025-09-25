"""Client domain entity with rich domain logic and business rules."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from core.events import DomainEvent
from domain.events import (
    ClientCreatedEvent,
    ClientUpdatedEvent,
    ExerciseExclusionUpdatedEvent,
)


class ActivityLevel(Enum):
    """Client activity level classification."""

    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

    @property
    def label(self) -> str:
        """Get French label for activity level."""
        labels = {
            ActivityLevel.SEDENTARY: "Sédentaire",
            ActivityLevel.LIGHTLY_ACTIVE: "Peu actif",
            ActivityLevel.MODERATELY_ACTIVE: "Modérément actif",
            ActivityLevel.VERY_ACTIVE: "Très actif",
            ActivityLevel.EXTREMELY_ACTIVE: "Extrêmement actif",
        }
        return labels[self]

    @property
    def multiplier(self) -> float:
        """Get activity multiplier for TDEE calculation."""
        multipliers = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHTLY_ACTIVE: 1.375,
            ActivityLevel.MODERATELY_ACTIVE: 1.55,
            ActivityLevel.VERY_ACTIVE: 1.725,
            ActivityLevel.EXTREMELY_ACTIVE: 1.9,
        }
        return multipliers[self]


class Gender(Enum):
    """Client gender classification."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    @property
    def label(self) -> str:
        """Get French label for gender."""
        labels = {
            Gender.MALE: "Homme",
            Gender.FEMALE: "Femme",
            Gender.OTHER: "Autre",
        }
        return labels[self]


@dataclass
class PersonalInfo:
    """Client personal information value object."""

    first_name: str
    last_name: str
    email: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None

    def __post_init__(self):
        """Validate personal info after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate personal information."""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("Le prénom est obligatoire")

        if not self.last_name or not self.last_name.strip():
            raise ValueError("Le nom est obligatoire")

        if self.email and not self._is_valid_email(self.email):
            raise ValueError("Format d'email invalide")

        if self.birth_date and self.birth_date > date.today():
            raise ValueError("La date de naissance ne peut pas être future")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email.strip()))

    @property
    def full_name(self) -> str:
        """Get formatted full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> Optional[int]:
        """Calculate age from birth date."""
        if not self.birth_date:
            return None

        today = date.today()
        age = today.year - self.birth_date.year

        # Adjust if birthday hasn't occurred this year
        if today.month < self.birth_date.month or (
            today.month == self.birth_date.month and today.day < self.birth_date.day
        ):
            age -= 1

        return max(0, age)


@dataclass
class PhysicalMetrics:
    """Client physical measurements value object."""

    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None

    def __post_init__(self):
        """Validate physical metrics after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate physical measurements."""
        if self.weight_kg is not None and (self.weight_kg <= 0 or self.weight_kg > 500):
            raise ValueError("Poids invalide (doit être entre 0 et 500 kg)")

        if self.height_cm is not None and (self.height_cm <= 0 or self.height_cm > 300):
            raise ValueError("Taille invalide (doit être entre 0 et 300 cm)")

        if self.body_fat_percentage is not None and (
            self.body_fat_percentage < 0 or self.body_fat_percentage > 100
        ):
            raise ValueError("Pourcentage de graisse corporelle invalide (0-100%)")

        if self.muscle_mass_kg is not None and (
            self.muscle_mass_kg <= 0 or self.muscle_mass_kg > 200
        ):
            raise ValueError("Masse musculaire invalide (doit être positive)")

    @property
    def bmi(self) -> Optional[float]:
        """Calculate Body Mass Index."""
        if not self.weight_kg or not self.height_cm:
            return None

        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m**2), 1)

    @property
    def bmi_category(self) -> Optional[str]:
        """Get BMI category classification."""
        bmi = self.bmi
        if not bmi:
            return None

        if bmi < 18.5:
            return "Sous-poids"
        elif bmi < 25:
            return "Poids normal"
        elif bmi < 30:
            return "Surpoids"
        else:
            return "Obésité"

    @property
    def is_complete(self) -> bool:
        """Check if basic metrics are available for calculations."""
        return self.weight_kg is not None and self.height_cm is not None


@dataclass
class HealthProfile:
    """Client health and fitness profile value object."""

    objectives: Optional[str] = None
    medical_history: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    exercise_exclusions: List[int] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)

    @property
    def has_medical_restrictions(self) -> bool:
        """Check if client has any medical restrictions."""
        return bool(
            self.exercise_exclusions
            or self.medical_history
            or self.allergies
            or self.medications
        )

    def add_exercise_exclusion(self, exercise_id: int) -> None:
        """Add exercise exclusion."""
        if exercise_id not in self.exercise_exclusions:
            self.exercise_exclusions.append(exercise_id)

    def remove_exercise_exclusion(self, exercise_id: int) -> None:
        """Remove exercise exclusion."""
        if exercise_id in self.exercise_exclusions:
            self.exercise_exclusions.remove(exercise_id)

    def update_exclusions(self, exclusion_ids: List[int]) -> bool:
        """Update exercise exclusions and return if changed."""
        old_exclusions = set(self.exercise_exclusions)
        new_exclusions = set(exclusion_ids)

        if old_exclusions != new_exclusions:
            self.exercise_exclusions = exclusion_ids.copy()
            return True
        return False


class Client:
    """Client aggregate root with rich domain logic and business rules."""

    def __init__(
        self,
        client_id: Optional[int],
        personal_info: PersonalInfo,
        physical_metrics: Optional[PhysicalMetrics] = None,
        health_profile: Optional[HealthProfile] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = client_id
        self.personal_info = personal_info
        self.physical_metrics = physical_metrics or PhysicalMetrics()
        self.health_profile = health_profile or HealthProfile()
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        # Domain events tracking
        self._domain_events: List[DomainEvent] = []

        # Raise creation event for new clients
        if client_id is None:
            self._add_domain_event(
                ClientCreatedEvent(
                    client_id=str(self.id or 0),
                    email=self.personal_info.email or "",
                    full_name=self.personal_info.full_name,
                )
            )

    def _add_domain_event(self, event: DomainEvent) -> None:
        """Add domain event to be published."""
        self._domain_events.append(event)

    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events and clear the list."""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    def update_personal_info(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[date] = None,
        gender: Optional[Gender] = None,
    ) -> None:
        """Update personal information with validation."""
        old_info = self.personal_info
        updated_fields = {}

        # Create new personal info with updates
        new_info = PersonalInfo(
            first_name=first_name or old_info.first_name,
            last_name=last_name or old_info.last_name,
            email=email if email is not None else old_info.email,
            birth_date=birth_date if birth_date is not None else old_info.birth_date,
            gender=gender if gender is not None else old_info.gender,
        )

        # Track changes
        if new_info.first_name != old_info.first_name:
            updated_fields["first_name"] = new_info.first_name
        if new_info.last_name != old_info.last_name:
            updated_fields["last_name"] = new_info.last_name
        if new_info.email != old_info.email:
            updated_fields["email"] = new_info.email
        if new_info.birth_date != old_info.birth_date:
            updated_fields["birth_date"] = new_info.birth_date.isoformat() if new_info.birth_date else None
        if new_info.gender != old_info.gender:
            updated_fields["gender"] = new_info.gender.value if new_info.gender else None

        if updated_fields:
            self.personal_info = new_info
            self.updated_at = datetime.now()

            # Raise domain event
            self._add_domain_event(
                ClientUpdatedEvent(
                    client_id=str(self.id or 0),
                    updated_fields=updated_fields,
                )
            )

    def update_physical_metrics(
        self,
        weight_kg: Optional[float] = None,
        height_cm: Optional[float] = None,
        body_fat_percentage: Optional[float] = None,
        muscle_mass_kg: Optional[float] = None,
    ) -> None:
        """Update physical measurements."""
        old_metrics = self.physical_metrics
        updated_fields = {}

        # Create new metrics with updates
        new_metrics = PhysicalMetrics(
            weight_kg=weight_kg if weight_kg is not None else old_metrics.weight_kg,
            height_cm=height_cm if height_cm is not None else old_metrics.height_cm,
            body_fat_percentage=body_fat_percentage
            if body_fat_percentage is not None
            else old_metrics.body_fat_percentage,
            muscle_mass_kg=muscle_mass_kg
            if muscle_mass_kg is not None
            else old_metrics.muscle_mass_kg,
        )

        # Track changes
        if new_metrics.weight_kg != old_metrics.weight_kg:
            updated_fields["weight_kg"] = new_metrics.weight_kg
        if new_metrics.height_cm != old_metrics.height_cm:
            updated_fields["height_cm"] = new_metrics.height_cm
        if new_metrics.body_fat_percentage != old_metrics.body_fat_percentage:
            updated_fields["body_fat_percentage"] = new_metrics.body_fat_percentage
        if new_metrics.muscle_mass_kg != old_metrics.muscle_mass_kg:
            updated_fields["muscle_mass_kg"] = new_metrics.muscle_mass_kg

        if updated_fields:
            self.physical_metrics = new_metrics
            self.updated_at = datetime.now()

            # Raise domain event
            self._add_domain_event(
                ClientUpdatedEvent(
                    client_id=str(self.id or 0),
                    updated_fields=updated_fields,
                )
            )

    def update_exercise_exclusions(self, exclusion_ids: List[int]) -> None:
        """Update exercise exclusions with domain event."""
        if self.health_profile.update_exclusions(exclusion_ids):
            self.updated_at = datetime.now()

            # Raise domain event
            self._add_domain_event(
                ExerciseExclusionUpdatedEvent(
                    client_id=str(self.id or 0),
                    excluded_exercise_ids=exclusion_ids,
                )
            )

    def can_perform_exercise(self, exercise_id: int) -> bool:
        """Check if client can perform a specific exercise."""
        return exercise_id not in self.health_profile.exercise_exclusions

    def is_ready_for_nutrition_plan(self) -> bool:
        """Check if client has enough data for nutrition planning."""
        return (
            self.physical_metrics.is_complete
            and self.personal_info.age is not None
            and self.personal_info.gender is not None
            and self.health_profile.activity_level is not None
        )

    def get_fitness_readiness_score(self) -> float:
        """Calculate fitness readiness score (0-100)."""
        score = 0.0

        # Personal info completeness (30 points)
        if self.personal_info.first_name and self.personal_info.last_name:
            score += 10
        if self.personal_info.email:
            score += 5
        if self.personal_info.birth_date:
            score += 10
        if self.personal_info.gender:
            score += 5

        # Physical metrics (40 points)
        if self.physical_metrics.weight_kg:
            score += 15
        if self.physical_metrics.height_cm:
            score += 15
        if self.physical_metrics.body_fat_percentage:
            score += 5
        if self.physical_metrics.muscle_mass_kg:
            score += 5

        # Health profile (30 points)
        if self.health_profile.objectives:
            score += 10
        if self.health_profile.activity_level:
            score += 15
        if self.health_profile.medical_history:
            score += 5

        return min(score, 100.0)

    @property
    def display_name(self) -> str:
        """Get display name for UI."""
        return self.personal_info.full_name

    @property
    def is_complete_profile(self) -> bool:
        """Check if profile is complete enough for coaching."""
        return self.get_fitness_readiness_score() >= 70

    def __str__(self) -> str:
        return f"Client({self.id}, {self.display_name})"

    def __repr__(self) -> str:
        return (
            f"Client(id={self.id}, name='{self.display_name}', "
            f"readiness={self.get_fitness_readiness_score():.1f}%)"
        )
