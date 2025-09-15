"""
Nutrition Calculation Strategy Engine

Scientific algorithms for precise nutrition calculations with
multiple methodologies and ML-based personalization.
"""

from .base import NutritionContext, NutritionResult, NutritionGoal, ActivityLevel
from .harris_benedict_strategy import HarrisBenedictStrategy
from .mifflin_st_jeor_strategy import MifflinStJeorStrategy
from .katch_mcardle_strategy import KatchMcArdleStrategy
from .ml_nutrition_strategy import MLNutritionStrategy
from .manager import NutritionStrategyManager

__all__ = [
    "NutritionContext",
    "NutritionResult",
    "NutritionGoal",
    "ActivityLevel",
    "HarrisBenedictStrategy",
    "MifflinStJeorStrategy",
    "KatchMcArdleStrategy",
    "MLNutritionStrategy",
    "NutritionStrategyManager"
]