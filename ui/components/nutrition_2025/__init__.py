"""🚀 CoachPro Nutrition 2025 - Advanced Component Library

Version simplifiée pour intégration immédiate.
Les composants avancés avec animations seront intégrés progressivement.
"""

# Utiliser uniquement les stubs pour l'intégration initiale
from .stubs import (
    AnimatedCard,
    ProgressBar,
    ScoreIndicator,
    StreakTracker,
    MacroProgressRings,
    AdvancedFoodLogger,
    QuickActionBar,
    AnalyticsDashboard,
    IntelligentMealPlanner
)

from .meal_plan_generator import MealPlanGenerator

# Alias pour compatibilité
SmartNutritionDashboard = None

__all__ = [
    "AnimatedCard",
    "ProgressBar",
    "ScoreIndicator",
    "StreakTracker",
    "MacroProgressRings",
    "AdvancedFoodLogger",
    "QuickActionBar",
    "AnalyticsDashboard",
    "IntelligentMealPlanner",
    "MealPlanGenerator"
]