"""Tests for Client domain entity and value objects."""

import pytest
from datetime import date, datetime

from models.client import (
    Client,
    PersonalInfo,
    PhysicalMetrics,
    HealthProfile,
    ActivityLevel,
    Gender,
)


class TestPersonalInfo:
    """Test PersonalInfo value object."""

    def test_valid_personal_info(self):
        """Test creating valid personal info."""
        info = PersonalInfo(
            first_name="Jean",
            last_name="Dupont",
            email="jean.dupont@example.com",
            birth_date=date(1990, 5, 15),
            gender=Gender.MALE
        )

        assert info.first_name == "Jean"
        assert info.last_name == "Dupont"
        assert info.full_name == "Jean Dupont"
        assert info.age is not None
        assert info.age > 30  # Approximate age

    def test_invalid_email(self):
        """Test validation of invalid email."""
        with pytest.raises(ValueError, match="Format d'email invalide"):
            PersonalInfo(
                first_name="Jean",
                last_name="Dupont",
                email="invalid-email"
            )

    def test_empty_names(self):
        """Test validation of empty names."""
        with pytest.raises(ValueError, match="Le prénom est obligatoire"):
            PersonalInfo(
                first_name="",
                last_name="Dupont"
            )

        with pytest.raises(ValueError, match="Le nom est obligatoire"):
            PersonalInfo(
                first_name="Jean",
                last_name=""
            )

    def test_future_birth_date(self):
        """Test validation of future birth date."""
        future_date = date(2050, 1, 1)
        with pytest.raises(ValueError, match="La date de naissance ne peut pas être future"):
            PersonalInfo(
                first_name="Jean",
                last_name="Dupont",
                birth_date=future_date
            )

    def test_age_calculation(self):
        """Test age calculation."""
        birth_date = date(1990, 1, 1)
        info = PersonalInfo(
            first_name="Jean",
            last_name="Dupont",
            birth_date=birth_date
        )

        expected_age = date.today().year - 1990
        if date.today() < date(date.today().year, 1, 1):
            expected_age -= 1

        assert info.age == expected_age


class TestPhysicalMetrics:
    """Test PhysicalMetrics value object."""

    def test_valid_physical_metrics(self):
        """Test creating valid physical metrics."""
        metrics = PhysicalMetrics(
            weight_kg=75.0,
            height_cm=180.0
        )

        assert metrics.weight_kg == 75.0
        assert metrics.height_cm == 180.0
        assert metrics.bmi is not None
        assert 22 < metrics.bmi < 24  # Normal BMI range
        assert metrics.bmi_category == "Poids normal"
        assert metrics.is_complete is True

    def test_bmi_calculation(self):
        """Test BMI calculation."""
        metrics = PhysicalMetrics(
            weight_kg=80.0,
            height_cm=180.0
        )

        expected_bmi = 80.0 / (1.8 ** 2)
        assert abs(metrics.bmi - expected_bmi) < 0.1

    def test_invalid_weight(self):
        """Test validation of invalid weight."""
        with pytest.raises(ValueError, match="Poids invalide"):
            PhysicalMetrics(weight_kg=-10.0)

        with pytest.raises(ValueError, match="Poids invalide"):
            PhysicalMetrics(weight_kg=600.0)

    def test_invalid_height(self):
        """Test validation of invalid height."""
        with pytest.raises(ValueError, match="Taille invalide"):
            PhysicalMetrics(height_cm=-10.0)

        with pytest.raises(ValueError, match="Taille invalide"):
            PhysicalMetrics(height_cm=400.0)

    def test_bmi_categories(self):
        """Test BMI category classification."""
        # Underweight
        metrics = PhysicalMetrics(weight_kg=50.0, height_cm=180.0)
        assert metrics.bmi_category == "Sous-poids"

        # Normal weight
        metrics = PhysicalMetrics(weight_kg=70.0, height_cm=180.0)
        assert metrics.bmi_category == "Poids normal"

        # Overweight
        metrics = PhysicalMetrics(weight_kg=85.0, height_cm=180.0)
        assert metrics.bmi_category == "Surpoids"

        # Obese
        metrics = PhysicalMetrics(weight_kg=100.0, height_cm=180.0)
        assert metrics.bmi_category == "Obésité"


class TestHealthProfile:
    """Test HealthProfile value object."""

    def test_health_profile(self):
        """Test health profile creation."""
        profile = HealthProfile(
            objectives="Perdre du poids",
            medical_history="Aucun antécédent",
            activity_level=ActivityLevel.MODERATELY_ACTIVE,
            exercise_exclusions=[1, 2, 3],
            allergies=["Arachides"],
            medications=["Aspirine"]
        )

        assert profile.objectives == "Perdre du poids"
        assert profile.activity_level == ActivityLevel.MODERATELY_ACTIVE
        assert profile.has_medical_restrictions is True
        assert len(profile.exercise_exclusions) == 3

    def test_exercise_exclusions(self):
        """Test exercise exclusion management."""
        profile = HealthProfile()

        # Add exclusions
        profile.add_exercise_exclusion(1)
        profile.add_exercise_exclusion(2)
        assert len(profile.exercise_exclusions) == 2

        # Remove exclusion
        profile.remove_exercise_exclusion(1)
        assert len(profile.exercise_exclusions) == 1
        assert 1 not in profile.exercise_exclusions

    def test_update_exclusions(self):
        """Test updating exercise exclusions."""
        profile = HealthProfile(exercise_exclusions=[1, 2, 3])

        # Update with different list
        changed = profile.update_exclusions([2, 3, 4])
        assert changed is True
        assert profile.exercise_exclusions == [2, 3, 4]

        # Update with same list
        changed = profile.update_exclusions([2, 3, 4])
        assert changed is False


class TestClient:
    """Test Client aggregate root."""

    def create_test_client(self) -> Client:
        """Create a test client."""
        personal_info = PersonalInfo(
            first_name="Jean",
            last_name="Dupont",
            email="jean.dupont@example.com",
            birth_date=date(1990, 5, 15),
            gender=Gender.MALE
        )

        physical_metrics = PhysicalMetrics(
            weight_kg=75.0,
            height_cm=180.0
        )

        health_profile = HealthProfile(
            objectives="Musculation",
            activity_level=ActivityLevel.MODERATELY_ACTIVE
        )

        return Client(
            client_id=1,
            personal_info=personal_info,
            physical_metrics=physical_metrics,
            health_profile=health_profile
        )

    def test_client_creation(self):
        """Test client creation."""
        client = self.create_test_client()

        assert client.id == 1
        assert client.display_name == "Jean Dupont"
        assert client.personal_info.first_name == "Jean"
        assert client.physical_metrics.weight_kg == 75.0

    def test_fitness_readiness_score(self):
        """Test fitness readiness score calculation."""
        client = self.create_test_client()
        score = client.get_fitness_readiness_score()

        assert isinstance(score, float)
        assert 0 <= score <= 100
        assert score > 70  # Should be high for complete profile

    def test_is_ready_for_nutrition_plan(self):
        """Test nutrition plan readiness check."""
        client = self.create_test_client()
        assert client.is_ready_for_nutrition_plan() is True

    def test_update_personal_info(self):
        """Test updating personal information."""
        client = self.create_test_client()

        client.update_personal_info(
            first_name="Pierre",
            email="pierre.dupont@example.com"
        )

        assert client.personal_info.first_name == "Pierre"
        assert client.personal_info.email == "pierre.dupont@example.com"
        assert client.personal_info.last_name == "Dupont"  # Unchanged

    def test_update_physical_metrics(self):
        """Test updating physical metrics."""
        client = self.create_test_client()

        client.update_physical_metrics(
            weight_kg=80.0,
            height_cm=185.0
        )

        assert client.physical_metrics.weight_kg == 80.0
        assert client.physical_metrics.height_cm == 185.0

    def test_update_exercise_exclusions(self):
        """Test updating exercise exclusions."""
        client = self.create_test_client()

        client.update_exercise_exclusions([1, 2, 3])

        assert client.health_profile.exercise_exclusions == [1, 2, 3]

    def test_can_perform_exercise(self):
        """Test exercise performance check."""
        client = self.create_test_client()
        client.update_exercise_exclusions([1, 2, 3])

        assert client.can_perform_exercise(1) is False
        assert client.can_perform_exercise(4) is True

    def test_domain_events(self):
        """Test domain event generation."""
        personal_info = PersonalInfo(
            first_name="Jean",
            last_name="Dupont"
        )

        # Creating a new client should generate domain events
        client = Client(
            client_id=None,  # New client
            personal_info=personal_info
        )

        events = client.get_domain_events()
        assert len(events) > 0

        # Getting events again should return empty list
        events_again = client.get_domain_events()
        assert len(events_again) == 0

    def test_complete_profile_check(self):
        """Test complete profile assessment."""
        # Incomplete profile
        client = Client(
            client_id=1,
            personal_info=PersonalInfo(
                first_name="Jean",
                last_name="Dupont"
            )
        )

        assert client.is_complete_profile is False

        # Complete profile
        complete_client = self.create_test_client()
        assert complete_client.is_complete_profile is True


class TestActivityLevel:
    """Test ActivityLevel enum."""

    def test_activity_level_labels(self):
        """Test activity level labels."""
        assert ActivityLevel.SEDENTARY.label == "Sédentaire"
        assert ActivityLevel.MODERATELY_ACTIVE.label == "Modérément actif"

    def test_activity_level_multipliers(self):
        """Test activity level multipliers."""
        assert ActivityLevel.SEDENTARY.multiplier == 1.2
        assert ActivityLevel.MODERATELY_ACTIVE.multiplier == 1.55
        assert ActivityLevel.VERY_ACTIVE.multiplier == 1.725


class TestGender:
    """Test Gender enum."""

    def test_gender_labels(self):
        """Test gender labels."""
        assert Gender.MALE.label == "Homme"
        assert Gender.FEMALE.label == "Femme"
        assert Gender.OTHER.label == "Autre"