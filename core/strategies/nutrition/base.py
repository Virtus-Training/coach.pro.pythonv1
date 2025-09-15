"""
Base classes for nutrition calculation strategies
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from ..base import StrategyContext, StrategyResult


class Gender(Enum):
    """Gender for nutrition calculations"""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(Enum):
    """Physical activity levels"""

    SEDENTARY = "sedentary"  # Little to no exercise
    LIGHT = "light"  # Light exercise 1-3 days/week
    MODERATE = "moderate"  # Moderate exercise 3-5 days/week
    ACTIVE = "active"  # Heavy exercise 6-7 days/week
    VERY_ACTIVE = "very_active"  # Very heavy exercise, physical job
    EXTRA_ACTIVE = "extra_active"  # Extremely active, training twice a day


class NutritionGoal(Enum):
    """Nutrition goals"""

    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    CUTTING = "cutting"  # Body fat reduction while preserving muscle
    BULKING = "bulking"  # Muscle gain with some fat gain
    RECOMPOSITION = "recomposition"  # Simultaneous fat loss and muscle gain


class MacronutrientDistribution(Enum):
    """Standard macronutrient distributions"""

    BALANCED = "balanced"  # 30% protein, 40% carbs, 30% fat
    HIGH_PROTEIN = "high_protein"  # 40% protein, 35% carbs, 25% fat
    LOW_CARB = "low_carb"  # 35% protein, 20% carbs, 45% fat
    KETOGENIC = "ketogenic"  # 20% protein, 5% carbs, 75% fat
    HIGH_CARB = "high_carb"  # 25% protein, 55% carbs, 20% fat
    MEDITERRANEAN = "mediterranean"  # 20% protein, 45% carbs, 35% fat


@dataclass
class PersonalMetrics:
    """Personal metrics for nutrition calculations"""

    age: int
    gender: Gender
    height_cm: float
    weight_kg: float
    body_fat_percentage: Optional[float] = None
    lean_body_mass_kg: Optional[float] = None

    def __post_init__(self):
        """Calculate derived metrics"""
        if self.lean_body_mass_kg is None and self.body_fat_percentage is not None:
            self.lean_body_mass_kg = self.weight_kg * (
                1 - self.body_fat_percentage / 100
            )

    @property
    def bmi(self) -> float:
        """Calculate BMI"""
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m**2)

    @property
    def bmi_category(self) -> str:
        """Get BMI category"""
        bmi = self.bmi
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"


@dataclass
class NutritionPreferences:
    """Nutrition preferences and restrictions"""

    dietary_restrictions: List[str] = field(
        default_factory=list
    )  # vegetarian, vegan, gluten-free, etc.
    food_allergies: List[str] = field(default_factory=list)
    preferred_macro_distribution: MacronutrientDistribution = (
        MacronutrientDistribution.BALANCED
    )
    meal_frequency: int = 3  # Number of meals per day
    snack_frequency: int = 1  # Number of snacks per day
    hydration_goal_liters: float = 2.5
    supplement_preferences: Dict[str, bool] = field(default_factory=dict)


@dataclass
class NutritionContext:
    """Context for nutrition calculations"""

    personal_metrics: PersonalMetrics
    activity_level: ActivityLevel
    nutrition_goal: NutritionGoal
    preferences: NutritionPreferences = field(default_factory=NutritionPreferences)

    # Optional context
    training_days_per_week: int = 3
    training_duration_minutes: int = 60
    training_intensity: str = "moderate"  # low, moderate, high, very_high

    # Medical considerations
    medical_conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)

    # Tracking data (if available)
    recent_weight_trend: Optional[List[float]] = None
    recent_energy_levels: Optional[List[int]] = None  # 1-10 scale
    recent_hunger_levels: Optional[List[int]] = None  # 1-10 scale


@dataclass
class MacronutrientTargets:
    """Calculated macronutrient targets"""

    calories: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float
    fiber_g: float

    # Derived values
    protein_calories: float = field(init=False)
    carbs_calories: float = field(init=False)
    fat_calories: float = field(init=False)

    # Percentages
    protein_percentage: float = field(init=False)
    carbs_percentage: float = field(init=False)
    fat_percentage: float = field(init=False)

    def __post_init__(self):
        """Calculate derived values"""
        self.protein_calories = self.protein_g * 4
        self.carbs_calories = self.carbohydrates_g * 4
        self.fat_calories = self.fat_g * 9

        if self.calories > 0:
            self.protein_percentage = (self.protein_calories / self.calories) * 100
            self.carbs_percentage = (self.carbs_calories / self.calories) * 100
            self.fat_percentage = (self.fat_calories / self.calories) * 100


@dataclass
class NutritionTiming:
    """Nutrition timing recommendations"""

    pre_workout_carbs_g: float = 0
    post_workout_protein_g: float = 0
    post_workout_carbs_g: float = 0
    bedtime_casein_g: float = 0
    morning_protein_g: float = 0

    # Meal timing
    meal_times: List[str] = field(default_factory=list)
    meal_calorie_distribution: List[float] = field(default_factory=list)


@dataclass
class SupplementRecommendations:
    """Supplement recommendations"""

    creatine_g: float = 0
    whey_protein_g: float = 0
    vitamin_d_iu: float = 0
    omega3_g: float = 0
    multivitamin: bool = False
    probiotics: bool = False

    notes: List[str] = field(default_factory=list)


@dataclass
class NutritionResult:
    """Result of nutrition calculations"""

    bmr: float  # Basal Metabolic Rate
    tdee: float  # Total Daily Energy Expenditure
    target_calories: float  # Adjusted for goal
    macronutrient_targets: MacronutrientTargets

    # Additional recommendations
    nutrition_timing: Optional[NutritionTiming] = None
    supplements: Optional[SupplementRecommendations] = None
    hydration_target_liters: float = 2.5

    # Calculation metadata
    calculation_method: str = ""
    confidence_score: float = 0.0  # 0-100
    accuracy_factors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Adaptive recommendations
    weekly_weight_change_target_kg: float = 0.0
    calorie_cycling_enabled: bool = False
    refeed_day_frequency: int = 0  # Days between refeed days (0 = none)

    def get_daily_calorie_range(self) -> tuple:
        """Get acceptable daily calorie range (±10%)"""
        variation = self.target_calories * 0.1
        return (self.target_calories - variation, self.target_calories + variation)

    def get_macro_ranges(self) -> Dict[str, tuple]:
        """Get acceptable macronutrient ranges"""
        return {
            "protein": (
                self.macronutrient_targets.protein_g * 0.9,
                self.macronutrient_targets.protein_g * 1.1,
            ),
            "carbohydrates": (
                self.macronutrient_targets.carbohydrates_g * 0.8,
                self.macronutrient_targets.carbohydrates_g * 1.2,
            ),
            "fat": (
                self.macronutrient_targets.fat_g * 0.85,
                self.macronutrient_targets.fat_g * 1.15,
            ),
        }


# Type aliases for strategy framework integration
NutritionStrategyContext = StrategyContext[NutritionContext]
NutritionStrategyResult = StrategyResult[NutritionResult]


# Constants for calculations
ACTIVITY_MULTIPLIERS = {
    ActivityLevel.SEDENTARY: 1.2,
    ActivityLevel.LIGHT: 1.375,
    ActivityLevel.MODERATE: 1.55,
    ActivityLevel.ACTIVE: 1.725,
    ActivityLevel.VERY_ACTIVE: 1.9,
    ActivityLevel.EXTRA_ACTIVE: 2.2,
}

GOAL_CALORIE_ADJUSTMENTS = {
    NutritionGoal.WEIGHT_LOSS: -0.20,  # 20% deficit
    NutritionGoal.WEIGHT_GAIN: 0.15,  # 15% surplus
    NutritionGoal.MUSCLE_GAIN: 0.10,  # 10% surplus
    NutritionGoal.MAINTENANCE: 0.0,  # No adjustment
    NutritionGoal.CUTTING: -0.25,  # 25% deficit
    NutritionGoal.BULKING: 0.20,  # 20% surplus
    NutritionGoal.RECOMPOSITION: -0.10,  # Small deficit
}

MACRO_DISTRIBUTIONS = {
    MacronutrientDistribution.BALANCED: {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
    MacronutrientDistribution.HIGH_PROTEIN: {
        "protein": 0.40,
        "carbs": 0.35,
        "fat": 0.25,
    },
    MacronutrientDistribution.LOW_CARB: {"protein": 0.35, "carbs": 0.20, "fat": 0.45},
    MacronutrientDistribution.KETOGENIC: {"protein": 0.20, "carbs": 0.05, "fat": 0.75},
    MacronutrientDistribution.HIGH_CARB: {"protein": 0.25, "carbs": 0.55, "fat": 0.20},
    MacronutrientDistribution.MEDITERRANEAN: {
        "protein": 0.20,
        "carbs": 0.45,
        "fat": 0.35,
    },
}
