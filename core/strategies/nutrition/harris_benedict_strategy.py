"""
Harris-Benedict BMR Calculation Strategy

Classic metabolic rate calculation using the Harris-Benedict equation.
Widely accepted and validated for general population use.
"""

import time
from typing import List, Dict, Any, Optional

from ..base import BaseStrategy, StrategyConfig, StrategyPriority
from .base import (
    NutritionStrategyContext, NutritionStrategyResult, NutritionContext,
    NutritionResult, MacronutrientTargets, Gender, ActivityLevel, NutritionGoal,
    ACTIVITY_MULTIPLIERS, GOAL_CALORIE_ADJUSTMENTS, MACRO_DISTRIBUTIONS
)


class HarrisBenedictStrategy(BaseStrategy[NutritionContext]):
    """
    Harris-Benedict equation for BMR calculation.

    Features:
    - Classic, widely validated equation
    - Gender-specific calculations
    - Conservative but reliable estimates
    - Suitable for general population
    - Medical/research grade accuracy
    """

    def __init__(self):
        config = StrategyConfig(
            name="harris_benedict_nutrition",
            version="1.0.0",
            priority=StrategyPriority.HIGH,
            timeout_seconds=5.0,
            cache_enabled=True,
            cache_ttl_seconds=3600  # 1 hour
        )
        super().__init__(config)

        # Strategy metadata
        self._strategy_category = "nutrition_calculation"
        self._strategy_tags = {"classic", "validated", "medical_grade", "conservative"}

    async def execute_async(self, context: NutritionStrategyContext) -> NutritionStrategyResult:
        """Execute Harris-Benedict nutrition calculation"""
        start_time = time.time()

        try:
            nutrition_context = context.data

            # Calculate BMR using Harris-Benedict equation
            bmr = self._calculate_bmr_harris_benedict(nutrition_context)

            # Calculate TDEE
            tdee = self._calculate_tdee(bmr, nutrition_context)

            # Adjust for nutrition goal
            target_calories = self._adjust_calories_for_goal(tdee, nutrition_context)

            # Calculate macronutrient targets
            macro_targets = self._calculate_macronutrient_targets(target_calories, nutrition_context)

            # Create result
            nutrition_result = NutritionResult(
                bmr=bmr,
                tdee=tdee,
                target_calories=target_calories,
                macronutrient_targets=macro_targets,
                calculation_method="Harris-Benedict",
                confidence_score=85.0,  # Well-validated equation
                accuracy_factors=[
                    "Classic equation with extensive validation",
                    "Suitable for general population",
                    "Conservative estimates"
                ]
            )

            # Add warnings and recommendations
            self._add_warnings_and_recommendations(nutrition_result, nutrition_context)

            execution_time = (time.time() - start_time) * 1000

            return NutritionStrategyResult(
                data=nutrition_result,
                success=True,
                execution_time_ms=execution_time,
                strategy_name=self.name,
                strategy_version=self.version
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return NutritionStrategyResult(
                data=None,
                success=False,
                execution_time_ms=execution_time,
                strategy_name=self.name,
                error_message=f"Harris-Benedict calculation failed: {str(e)}"
            )

    def _calculate_bmr_harris_benedict(self, context: NutritionContext) -> float:
        """Calculate BMR using Harris-Benedict equation (revised version)"""
        metrics = context.personal_metrics

        if metrics.gender == Gender.MALE:
            # Male: BMR = 88.362 + (13.397 × weight in kg) + (4.799 × height in cm) - (5.677 × age in years)
            bmr = 88.362 + (13.397 * metrics.weight_kg) + (4.799 * metrics.height_cm) - (5.677 * metrics.age)
        else:
            # Female: BMR = 447.593 + (9.247 × weight in kg) + (3.098 × height in cm) - (4.330 × age in years)
            bmr = 447.593 + (9.247 * metrics.weight_kg) + (3.098 * metrics.height_cm) - (4.330 * metrics.age)

        return max(bmr, 800)  # Minimum safe BMR

    def _calculate_tdee(self, bmr: float, context: NutritionContext) -> float:
        """Calculate Total Daily Energy Expenditure"""
        activity_multiplier = ACTIVITY_MULTIPLIERS.get(context.activity_level, 1.2)

        # Base TDEE
        tdee = bmr * activity_multiplier

        # Adjust for training specifics
        if context.training_days_per_week > 0:
            # Additional calories for training
            training_calories_per_session = self._estimate_training_calories(context)
            weekly_training_calories = training_calories_per_session * context.training_days_per_week
            daily_training_calories = weekly_training_calories / 7

            tdee += daily_training_calories

        return tdee

    def _estimate_training_calories(self, context: NutritionContext) -> float:
        """Estimate calories burned per training session"""
        base_calories_per_minute = {
            "low": 5,
            "moderate": 8,
            "high": 12,
            "very_high": 15
        }

        calories_per_minute = base_calories_per_minute.get(context.training_intensity, 8)
        session_calories = calories_per_minute * context.training_duration_minutes

        # Adjust for body weight (heavier people burn more calories)
        weight_factor = context.personal_metrics.weight_kg / 70  # Normalize to 70kg
        session_calories *= weight_factor

        return session_calories

    def _adjust_calories_for_goal(self, tdee: float, context: NutritionContext) -> float:
        """Adjust TDEE based on nutrition goal"""
        adjustment = GOAL_CALORIE_ADJUSTMENTS.get(context.nutrition_goal, 0.0)
        target_calories = tdee * (1 + adjustment)

        # Ensure minimum safe calories
        min_calories = context.personal_metrics.weight_kg * 22  # 22 cal/kg minimum
        target_calories = max(target_calories, min_calories)

        # Cap maximum calories for weight loss
        if context.nutrition_goal in [NutritionGoal.WEIGHT_LOSS, NutritionGoal.CUTTING]:
            max_deficit = tdee * 0.3  # Maximum 30% deficit
            target_calories = max(target_calories, tdee - max_deficit)

        return target_calories

    def _calculate_macronutrient_targets(self, target_calories: float, context: NutritionContext) -> MacronutrientTargets:
        """Calculate macronutrient targets"""
        # Get base distribution
        distribution = MACRO_DISTRIBUTIONS.get(
            context.preferences.preferred_macro_distribution,
            MACRO_DISTRIBUTIONS["balanced"]
        )

        # Adjust for goal and activity
        distribution = self._adjust_macro_distribution(distribution, context)

        # Calculate macros
        protein_calories = target_calories * distribution["protein"]
        carbs_calories = target_calories * distribution["carbs"]
        fat_calories = target_calories * distribution["fat"]

        protein_g = protein_calories / 4
        carbs_g = carbs_calories / 4
        fat_g = fat_calories / 9

        # Calculate fiber target (14g per 1000 calories)
        fiber_g = (target_calories / 1000) * 14

        return MacronutrientTargets(
            calories=target_calories,
            protein_g=protein_g,
            carbohydrates_g=carbs_g,
            fat_g=fat_g,
            fiber_g=fiber_g
        )

    def _adjust_macro_distribution(self, base_distribution: Dict[str, float], context: NutritionContext) -> Dict[str, float]:
        """Adjust macro distribution based on goals and activity"""
        distribution = base_distribution.copy()

        # Adjust for muscle gain goals
        if context.nutrition_goal in [NutritionGoal.MUSCLE_GAIN, NutritionGoal.BULKING]:
            # Increase protein slightly
            distribution["protein"] = min(0.35, distribution["protein"] + 0.05)
            # Adjust others proportionally
            remaining = 1.0 - distribution["protein"]
            carbs_fat_ratio = distribution["carbs"] / (distribution["carbs"] + distribution["fat"])
            distribution["carbs"] = remaining * carbs_fat_ratio
            distribution["fat"] = remaining * (1 - carbs_fat_ratio)

        # Adjust for high training volume
        if context.training_days_per_week >= 5:
            # Increase carbs for recovery
            distribution["carbs"] = min(0.50, distribution["carbs"] + 0.05)
            # Decrease fat proportionally
            distribution["fat"] = max(0.20, distribution["fat"] - 0.05)

        # Ensure protein minimums
        min_protein_per_kg = 1.6  # grams per kg body weight
        min_protein_calories = (min_protein_per_kg * context.personal_metrics.weight_kg * 4)
        min_protein_percentage = min_protein_calories / (context.personal_metrics.weight_kg * 25 * 4)  # Estimate daily calories

        if distribution["protein"] < min_protein_percentage:
            distribution["protein"] = min(0.40, min_protein_percentage)
            # Adjust others proportionally
            remaining = 1.0 - distribution["protein"]
            carbs_fat_ratio = distribution["carbs"] / (distribution["carbs"] + distribution["fat"])
            distribution["carbs"] = remaining * carbs_fat_ratio
            distribution["fat"] = remaining * (1 - carbs_fat_ratio)

        return distribution

    def _add_warnings_and_recommendations(self, result: NutritionResult, context: NutritionContext):
        """Add warnings and specific recommendations"""
        # Age-related warnings
        if context.personal_metrics.age > 65:
            result.warnings.append("Consider consulting healthcare provider for seniors-specific nutrition needs")
            result.accuracy_factors.append("Age-adjusted calculations may need medical supervision")

        # BMI warnings
        bmi = context.personal_metrics.bmi
        if bmi < 18.5:
            result.warnings.append("Underweight BMI detected - focus on healthy weight gain")
        elif bmi > 30:
            result.warnings.append("Obesity BMI detected - consider gradual, sustainable approach")

        # Goal-specific recommendations
        if context.nutrition_goal == NutritionGoal.WEIGHT_LOSS:
            result.accuracy_factors.append("Conservative approach recommended for sustainable weight loss")
            if result.target_calories < result.bmr * 1.1:
                result.warnings.append("Very low calorie target - consider less aggressive deficit")

        # Activity level considerations
        if context.activity_level == ActivityLevel.VERY_ACTIVE and context.training_days_per_week < 6:
            result.warnings.append("Activity level may not match training frequency")

        # Hydration recommendations
        base_hydration = 35 * context.personal_metrics.weight_kg / 1000  # 35ml per kg
        training_hydration = context.training_days_per_week * 0.5  # Extra 500ml per training day
        result.hydration_target_liters = base_hydration + (training_hydration / 7)

        # Set weekly weight change target
        if context.nutrition_goal == NutritionGoal.WEIGHT_LOSS:
            result.weekly_weight_change_target_kg = -0.5  # 0.5kg per week
        elif context.nutrition_goal == NutritionGoal.WEIGHT_GAIN:
            result.weekly_weight_change_target_kg = 0.3  # 0.3kg per week
        elif context.nutrition_goal == NutritionGoal.MUSCLE_GAIN:
            result.weekly_weight_change_target_kg = 0.2  # 0.2kg per week

    def validate_context(self, context: NutritionStrategyContext) -> List[str]:
        """Validate nutrition calculation context"""
        errors = []
        nutrition_context = context.data

        # Validate personal metrics
        metrics = nutrition_context.personal_metrics
        if metrics.age < 18 or metrics.age > 100:
            errors.append("Age must be between 18 and 100 years")

        if metrics.height_cm < 120 or metrics.height_cm > 250:
            errors.append("Height must be between 120 and 250 cm")

        if metrics.weight_kg < 30 or metrics.weight_kg > 300:
            errors.append("Weight must be between 30 and 300 kg")

        if metrics.body_fat_percentage is not None:
            if metrics.body_fat_percentage < 3 or metrics.body_fat_percentage > 50:
                errors.append("Body fat percentage must be between 3% and 50%")

        # Validate training parameters
        if nutrition_context.training_days_per_week < 0 or nutrition_context.training_days_per_week > 7:
            errors.append("Training days per week must be between 0 and 7")

        if nutrition_context.training_duration_minutes < 0 or nutrition_context.training_duration_minutes > 300:
            errors.append("Training duration must be between 0 and 300 minutes")

        return errors

    def get_supported_context_types(self) -> List[type]:
        """Get supported context types"""
        return [NutritionContext]

    @property
    def preferred_contexts(self) -> List[type]:
        """Contexts where this strategy performs best"""
        return [NutritionContext]