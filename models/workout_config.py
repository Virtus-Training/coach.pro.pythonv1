"""
Configuration des paramètres de génération de séances.
Modèle pour persister les préférences du coach utilisateur.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkoutGenerationConfig:
    """Configuration pour la génération automatique de séances."""

    # === RÈGLES MÉTIER ===
    # Équilibrage des groupes musculaires
    muscle_balance_rules: Dict[str, float] = field(default_factory=lambda: {
        "push_pull_ratio": 0.6,  # Ratio push/pull optimal (0.5 = équilibré, 0.8 = plus push)
        "upper_lower_ratio": 0.7,  # Ratio haut/bas du corps
        "max_consecutive_same_muscle": 2,  # Max exercices consécutifs même muscle
        "core_frequency": 0.3,  # Fréquence minimale d'exercices de gainage
    })

    # Règles par format de WOD
    format_rules: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "AMRAP": {
            "optimal_exercises": 4,  # Nombre d'exercices optimal
            "rep_range": (8, 15),   # Fourchette de répétitions
            "prefer_patterns": ["squat", "push", "pull"],
            "avoid_complex": True,  # Éviter mouvements trop techniques
        },
        "EMOM": {
            "optimal_exercises": 3,
            "rep_range": (6, 12),
            "prefer_patterns": ["hinge", "carry", "jump"],
            "allow_complex": True,
        },
        "For Time": {
            "optimal_exercises": 5,
            "rep_range": (12, 21),  # Nombres CrossFit (3, 6, 9, 12, 15, 18, 21)
            "prefer_patterns": ["squat", "pull", "push"],
            "scale_by_strength": True,
        },
        "Tabata": {
            "optimal_exercises": 1,
            "rep_range": (8, 12),
            "prefer_patterns": ["jump", "carry"],
            "high_intensity_only": True,
        },
        "Skill": {
            "optimal_exercises": 2,  # 1-3 mouvements techniques
            "rep_range": (3, 8),     # Peu de répétitions pour la qualité
            "prefer_patterns": ["complex", "technical", "coordination"],
            "focus_quality": True,   # Privilégier la qualité à la quantité
            "allow_complex": True,   # Mouvements complexes autorisés
        }
    })

    # === PRÉFÉRENCES COACH ===
    # Exercices favoris par contexte
    favorite_exercises: Dict[str, List[str]] = field(default_factory=lambda: {
        "warmup": ["air_squat", "jumping_jacks", "arm_circles"],
        "strength": ["deadlift", "squat", "bench_press"],
        "conditioning": ["burpees", "mountain_climbers", "kettlebell_swings"],
        "finisher": ["plank", "burpees", "sprint"],
    })

    # Exercices à éviter ou limiter
    exercise_restrictions: Dict[str, Any] = field(default_factory=lambda: {
        "banned_exercises": [],  # Exercices interdits
        "limited_frequency": {   # Exercices à fréquence limitée
            "burpees": 0.3,       # Max 30% des séances
            "wall_balls": 0.4,
        },
        "progression_exercises": {  # Exercices nécessitant progression
            "muscle_ups": {"min_level": "advanced"},
            "handstand_pushups": {"min_level": "intermediate"},
        }
    })

    # === INTELLIGENCE ADAPTATIVE ===
    # Patterns d'apprentissage
    learning_preferences: Dict[str, Any] = field(default_factory=lambda: {
        "successful_combinations": {},  # Combinaisons qui ont bien fonctionné
        "client_feedback_weights": {},  # Pondération selon feedback clients
        "seasonal_adjustments": {},     # Ajustements saisonniers
        "equipment_preferences": {},    # Préférences d'équipement par contexte
    })

    # === CONTRAINTES TECHNIQUES ===
    # Gestion de l'équipement
    equipment_management: Dict[str, Any] = field(default_factory=lambda: {
        "available_equipment": [],      # Équipement disponible
        "equipment_rotation": True,     # Rotation équipement dans séance
        "max_equipment_changes": 3,     # Max changements équipement/séance
        "setup_time_factor": 1.2,      # Facteur temps d'installation
    })

    # Gestion temporelle
    timing_rules: Dict[str, Any] = field(default_factory=lambda: {
        "transition_time_sec": 30,      # Temps transition entre exercices
        "equipment_change_sec": 60,     # Temps changement équipement
        "instruction_time_sec": 45,     # Temps explication nouvel exercice
        "rest_calculation_method": "density_based",  # ou "heart_rate_based"
    })

    # === RÈGLES PHYSIOLOGIQUES ===
    physiological_rules: Dict[str, Any] = field(default_factory=lambda: {
        "fatigue_management": {
            "max_consecutive_high_intensity": 2,
            "recovery_exercise_ratio": 0.2,  # 20% d'exercices de récupération
            "muscle_group_recovery_time": 24,  # Heures avant re-sollicitation
        },
        "energy_system_targeting": {
            "phosphocreatine": 0.3,  # 30% exercices système PC (0-15s)
            "glycolytic": 0.5,       # 50% système glycolytique (15s-2min)
            "aerobic": 0.2,          # 20% système aérobie (>2min)
        },
        "movement_complexity": {
            "warmup_complexity": "simple",
            "main_complexity": "varied",
            "finisher_complexity": "simple_to_moderate",
        }
    })

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire pour sauvegarde."""
        return {
            'muscle_balance_rules': self.muscle_balance_rules,
            'format_rules': self.format_rules,
            'favorite_exercises': self.favorite_exercises,
            'exercise_restrictions': self.exercise_restrictions,
            'learning_preferences': self.learning_preferences,
            'equipment_management': self.equipment_management,
            'timing_rules': self.timing_rules,
            'physiological_rules': self.physiological_rules,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkoutGenerationConfig':
        """Charge la configuration depuis un dictionnaire."""
        return cls(**data)

    def save_to_file(self, filepath: str):
        """Sauvegarde la configuration dans un fichier JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'WorkoutGenerationConfig':
        """Charge la configuration depuis un fichier JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Retourner configuration par défaut si fichier introuvable/corrompu
            return cls()

    def update_learning_from_session(self, session_data: Dict[str, Any], feedback_score: float):
        """Met à jour les préférences d'apprentissage basées sur le feedback."""
        session_id = session_data.get('session_id', 'unknown')

        # Enregistrer les combinaisons réussies (score > 7/10)
        if feedback_score >= 0.7:
            exercises_used = session_data.get('exercises_used', [])
            format_used = session_data.get('format', 'unknown')

            key = f"{format_used}_{len(exercises_used)}"
            if key not in self.learning_preferences['successful_combinations']:
                self.learning_preferences['successful_combinations'][key] = []

            self.learning_preferences['successful_combinations'][key].append({
                'exercises': exercises_used,
                'score': feedback_score,
                'session_id': session_id,
            })

    def get_smart_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Retourne des recommandations intelligentes basées sur le contexte et l'historique."""
        course_type = context.get('course_type', 'Cross-Training')
        format_type = context.get('format', 'AMRAP')

        recommendations = {
            'suggested_exercises': [],
            'optimal_rep_ranges': {},
            'timing_suggestions': {},
            'equipment_sequence': [],
        }

        # Recommandations basées sur les règles de format
        if format_type in self.format_rules:
            format_rule = self.format_rules[format_type]
            recommendations['optimal_rep_ranges'] = {
                'min_reps': format_rule['rep_range'][0],
                'max_reps': format_rule['rep_range'][1],
            }
            recommendations['preferred_patterns'] = format_rule.get('prefer_patterns', [])

        # Recommandations basées sur l'apprentissage
        successful_combos = self.learning_preferences.get('successful_combinations', {})
        if successful_combos:
            # Trouver les combinaisons les plus réussies pour ce format
            best_combos = []
            for key, combos in successful_combos.items():
                if key.startswith(format_type):
                    sorted_combos = sorted(combos, key=lambda x: x['score'], reverse=True)
                    best_combos.extend(sorted_combos[:3])  # Top 3

            if best_combos:
                recommendations['suggested_exercises'] = [
                    combo['exercises'] for combo in best_combos[:2]
                ]

        return recommendations


@dataclass
class SessionFeedback:
    """Modèle pour collecter le feedback des séances."""
    session_id: str
    coach_rating: float  # 0-10
    client_feedback: Optional[str] = None
    difficulty_perceived: float = 5.0  # 1-10
    engagement_level: float = 5.0     # 1-10
    technical_issues: List[str] = field(default_factory=list)
    suggested_improvements: Optional[str] = None
    would_repeat: bool = True
