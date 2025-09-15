"""
Service de gestion des configurations de génération de séances.
Gère la persistance et l'application des préférences du coach.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from models.workout_config import SessionFeedback, WorkoutGenerationConfig


class WorkoutConfigService:
    """Service de gestion des configurations de workout."""

    def __init__(self, config_dir: str = "data/config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "workout_generation.json"
        self.logger = logging.getLogger(__name__)

        # Charger ou créer la configuration
        self._config = self._load_config()

    def _load_config(self) -> WorkoutGenerationConfig:
        """Charge la configuration depuis le fichier ou crée une par défaut."""
        try:
            if self.config_file.exists():
                return WorkoutGenerationConfig.load_from_file(str(self.config_file))
            else:
                # Première utilisation - créer config par défaut
                config = WorkoutGenerationConfig()
                self._apply_smart_defaults(config)
                self.save_config(config)
                return config
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la config: {e}")
            return WorkoutGenerationConfig()

    def _apply_smart_defaults(self, config: WorkoutGenerationConfig):
        """Applique des defaults intelligents basés sur les meilleures pratiques."""

        # Équilibrage musculaire optimisé pour CrossFit
        config.muscle_balance_rules.update(
            {
                "push_pull_ratio": 0.65,  # Légèrement plus de push (CrossFit style)
                "upper_lower_ratio": 0.6,  # Plus de travail bas du corps
                "max_consecutive_same_muscle": 1,  # Éviter répétition
                "core_frequency": 0.4,  # Important dans CrossFit
            }
        )

        # Exercices favoris par contexte (standards CrossFit/Hyrox)
        config.favorite_exercises.update(
            {
                "warmup": [
                    "Air Squat",
                    "Jumping Jacks",
                    "Arm Circles",
                    "Leg Swings",
                    "Inchworms",
                    "Hip Circles",
                    "Shoulder Shrugs",
                ],
                "strength": [
                    "Back Squat",
                    "Deadlift",
                    "Bench Press",
                    "Overhead Press",
                    "Front Squat",
                    "Romanian Deadlift",
                    "Pull-ups",
                ],
                "conditioning": [
                    "Burpees",
                    "Kettlebell Swings",
                    "Box Jumps",
                    "Mountain Climbers",
                    "Thrusters",
                    "Wall Balls",
                    "Battle Ropes",
                ],
                "finisher": [
                    "Plank Hold",
                    "Burpee Finisher",
                    "Sprint",
                    "Max Effort Row",
                    "Farmer's Walk",
                    "Bear Crawl",
                ],
            }
        )

        # Restrictions basées sur l'expérience coaching
        config.exercise_restrictions.update(
            {
                "limited_frequency": {
                    "Burpees": 0.4,  # Pas plus de 40% des séances
                    "Wall Balls": 0.3,
                    "Turkish Get-ups": 0.2,  # Exercice très technique
                },
                "progression_exercises": {
                    "Muscle-ups": {"min_level": "advanced"},
                    "Handstand Push-ups": {"min_level": "intermediate"},
                    "Pistol Squats": {"min_level": "intermediate"},
                    "Olympic Lifts": {"min_level": "advanced"},
                },
            }
        )

    def get_config(self) -> WorkoutGenerationConfig:
        """Retourne la configuration actuelle."""
        return self._config

    def save_config(self, config: Optional[WorkoutGenerationConfig] = None):
        """Sauvegarde la configuration."""
        if config:
            self._config = config

        try:
            self._config.save_to_file(str(self.config_file))
            self.logger.info("Configuration sauvegardée avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")

    def update_muscle_balance_rules(self, rules: Dict[str, float]):
        """Met à jour les règles d'équilibrage musculaire."""
        self._config.muscle_balance_rules.update(rules)
        self.save_config()

    def update_format_rules(self, format_name: str, rules: Dict[str, Any]):
        """Met à jour les règles pour un format spécifique."""
        self._config.format_rules[format_name] = rules
        self.save_config()

    def add_favorite_exercise(self, context: str, exercise_name: str):
        """Ajoute un exercice aux favoris pour un contexte donné."""
        if context not in self._config.favorite_exercises:
            self._config.favorite_exercises[context] = []

        if exercise_name not in self._config.favorite_exercises[context]:
            self._config.favorite_exercises[context].append(exercise_name)
            self.save_config()

    def remove_favorite_exercise(self, context: str, exercise_name: str):
        """Retire un exercice des favoris."""
        if context in self._config.favorite_exercises:
            try:
                self._config.favorite_exercises[context].remove(exercise_name)
                self.save_config()
            except ValueError:
                pass  # Exercice pas dans la liste

    def ban_exercise(self, exercise_name: str, reason: Optional[str] = None):
        """Interdit un exercice."""
        if exercise_name not in self._config.exercise_restrictions["banned_exercises"]:
            self._config.exercise_restrictions["banned_exercises"].append(exercise_name)
            self.save_config()
            self.logger.info(f"Exercice banni: {exercise_name} - Raison: {reason}")

    def unban_exercise(self, exercise_name: str):
        """Retire un exercice de la liste noire."""
        try:
            self._config.exercise_restrictions["banned_exercises"].remove(exercise_name)
            self.save_config()
        except ValueError:
            pass

    def record_session_feedback(self, feedback: SessionFeedback):
        """Enregistre le feedback d'une séance pour apprentissage."""
        try:
            # Convertir le feedback en format d'apprentissage
            session_data = {
                "session_id": feedback.session_id,
                "format": getattr(feedback, "format", "unknown"),
                "exercises_used": getattr(feedback, "exercises_used", []),
            }

            # Calculer score composite (coach + client + engagement)
            composite_score = (
                feedback.coach_rating * 0.5
                + (feedback.difficulty_perceived / 10) * 0.2
                + (feedback.engagement_level / 10) * 0.3
            ) / 10  # Normaliser sur 0-1

            self._config.update_learning_from_session(session_data, composite_score)
            self.save_config()

            self.logger.info(f"Feedback enregistré pour session {feedback.session_id}")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'enregistrement du feedback: {e}")

    def get_smart_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Retourne des recommandations intelligentes pour la génération."""
        return self._config.get_smart_recommendations(context)

    def export_config(self, filepath: str) -> bool:
        """Exporte la configuration vers un fichier."""
        try:
            self._config.save_to_file(filepath)
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export: {e}")
            return False

    def import_config(self, filepath: str) -> bool:
        """Importe une configuration depuis un fichier."""
        try:
            self._config = WorkoutGenerationConfig.load_from_file(filepath)
            self.save_config()
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de l'import: {e}")
            return False

    def reset_to_defaults(self):
        """Remet la configuration aux valeurs par défaut."""
        self._config = WorkoutGenerationConfig()
        self._apply_smart_defaults(self._config)
        self.save_config()
        self.logger.info("Configuration remise aux valeurs par défaut")

    def get_exercise_restrictions_for_generation(self) -> Dict[str, Any]:
        """Retourne les restrictions d'exercices formatées pour le générateur."""
        return {
            "banned_exercises": set(
                self._config.exercise_restrictions.get("banned_exercises", [])
            ),
            "limited_frequency": self._config.exercise_restrictions.get(
                "limited_frequency", {}
            ),
            "progression_requirements": self._config.exercise_restrictions.get(
                "progression_exercises", {}
            ),
        }

    def validate_exercise_for_context(
        self, exercise_name: str, context: str, user_level: str = "beginner"
    ) -> bool:
        """Valide si un exercice est approprié pour un contexte donné."""
        restrictions = self.get_exercise_restrictions_for_generation()

        # Vérifier si exercice banni
        if exercise_name in restrictions["banned_exercises"]:
            return False

        # Vérifier niveau requis
        progression_req = restrictions["progression_requirements"].get(exercise_name)
        if progression_req:
            required_level = progression_req.get("min_level", "beginner")
            level_hierarchy = {"beginner": 1, "intermediate": 2, "advanced": 3}

            user_level_num = level_hierarchy.get(user_level, 1)
            required_level_num = level_hierarchy.get(required_level, 1)

            if user_level_num < required_level_num:
                return False

        return True

    def get_optimal_rep_range(
        self, format_type: str, exercise_complexity: str = "moderate"
    ) -> tuple:
        """Retourne la fourchette de répétitions optimale pour un format et niveau de complexité."""
        format_rules = self._config.format_rules.get(format_type, {})
        base_range = format_rules.get("rep_range", (8, 12))

        # Ajuster selon complexité
        if exercise_complexity == "complex":
            # Moins de reps pour exercices complexes
            return (max(3, base_range[0] - 3), max(base_range[0], base_range[1] - 3))
        elif exercise_complexity == "simple":
            # Plus de reps pour exercices simples
            return (base_range[0] + 2, base_range[1] + 5)

        return base_range
