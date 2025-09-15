"""
Nutrition Calculation Strategy Engine

Scientific algorithms for precise nutrition calculations with
multiple methodologies and ML-based personalization.
"""

from .base import ActivityLevel, NutritionContext, NutritionGoal, NutritionResult
from .harris_benedict_strategy import HarrisBenedictStrategy
from .katch_mcardle_strategy import KatchMcArdleStrategy
from .manager import NutritionStrategyManager
from .mifflin_st_jeor_strategy import MifflinStJeorStrategy
from .ml_nutrition_strategy import MLNutritionStrategy

__all__ = [
    "NutritionContext",
    "NutritionResult",
    "NutritionGoal",
    "ActivityLevel",
    "HarrisBenedictStrategy",
    "MifflinStJeorStrategy",
    "KatchMcArdleStrategy",
    "MLNutritionStrategy",
    "NutritionStrategyManager",
]
