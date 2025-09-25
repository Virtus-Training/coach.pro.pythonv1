"""
Comprehensive Testing Suite for Advanced Nutrition System
=========================================================

Tests covering:
- BMR calculations (Mifflin-St Jeor, Harris-Benedict)
- TDEE calculations with activity factors
- Macronutrient distribution algorithms
- Edge cases and validation
- Scientific accuracy verification
- Performance benchmarks
"""

import unittest
import pytest
from typing import Dict, Any
import math

from services.advanced_nutrition_calculator import (
    AdvancedNutritionCalculator,
    PersonalData,
    MacroTargets,
    ActivityLevel,
    NutritionGoal,
    BMRMethod,
    NutritionResults
)


class TestBMRCalculations(unittest.TestCase):
    """Test BMR calculation accuracy"""

    def setUp(self):
        """Setup test data"""
        self.calculator = AdvancedNutritionCalculator()

    def test_mifflin_st_jeor_male(self):
        """Test Mifflin-St Jeor for male subjects"""
        # Test case: 30-year-old male, 80kg, 180cm
        bmr = self.calculator.calculate_bmr(
            age=30,
            sexe="Homme",
            taille_cm=180,
            poids_kg=80,
            method=BMRMethod.MIFFLIN_ST_JEOR
        )

        # Expected: 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780
        expected_bmr = 10 * 80 + 6.25 * 180 - 5 * 30 + 5
        self.assertAlmostEqual(bmr, expected_bmr, places=1)
        self.assertGreater(bmr, 1700)  # Reasonable range
        self.assertLess(bmr, 1900)

    def test_mifflin_st_jeor_female(self):
        """Test Mifflin-St Jeor for female subjects"""
        # Test case: 25-year-old female, 60kg, 165cm
        bmr = self.calculator.calculate_bmr(
            age=25,
            sexe="Femme",
            taille_cm=165,
            poids_kg=60,
            method=BMRMethod.MIFFLIN_ST_JEOR
        )

        # Expected: 10*60 + 6.25*165 - 5*25 - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
        expected_bmr = 10 * 60 + 6.25 * 165 - 5 * 25 - 161
        self.assertAlmostEqual(bmr, expected_bmr, places=1)
        self.assertGreater(bmr, 1200)
        self.assertLess(bmr, 1500)

    def test_harris_benedict_male(self):
        """Test Harris-Benedict for male subjects"""
        bmr = self.calculator.calculate_bmr(
            age=35,
            sexe="Homme",
            taille_cm=175,
            poids_kg=75,
            method=BMRMethod.HARRIS_BENEDICT
        )

        # Expected: 88.362 + (13.397 * 75) + (4.799 * 175) - (5.677 * 35)
        expected_bmr = 88.362 + (13.397 * 75) + (4.799 * 175) - (5.677 * 35)
        self.assertAlmostEqual(bmr, expected_bmr, places=1)

    def test_harris_benedict_female(self):
        """Test Harris-Benedict for female subjects"""
        bmr = self.calculator.calculate_bmr(
            age=28,
            sexe="Femme",
            taille_cm=160,
            poids_kg=55,
            method=BMRMethod.HARRIS_BENEDICT
        )

        # Expected: 447.593 + (9.247 * 55) + (3.098 * 160) - (4.330 * 28)
        expected_bmr = 447.593 + (9.247 * 55) + (3.098 * 160) - (4.330 * 28)
        self.assertAlmostEqual(bmr, expected_bmr, places=1)

    def test_body_fat_adjustment(self):
        """Test BMR with body fat percentage adjustment"""
        # Same person with different body fat percentages
        bmr_no_bf = self.calculator.calculate_bmr(
            age=30, sexe="Homme", taille_cm=180, poids_kg=80
        )

        bmr_low_bf = self.calculator.calculate_bmr(
            age=30, sexe="Homme", taille_cm=180, poids_kg=80,
            masse_grasse_pct=10  # Very lean
        )

        bmr_high_bf = self.calculator.calculate_bmr(
            age=30, sexe="Homme", taille_cm=180, poids_kg=80,
            masse_grasse_pct=25  # Higher body fat
        )

        # Low body fat should have higher BMR than high body fat
        self.assertGreater(bmr_low_bf, bmr_high_bf)
        # All should be within reasonable range
        self.assertGreater(bmr_low_bf, 1700)
        self.assertLess(bmr_high_bf, 1900)

    def test_bmr_edge_cases(self):
        """Test BMR calculation edge cases"""
        # Very young person
        bmr_young = self.calculator.calculate_bmr(
            age=18, sexe="Homme", taille_cm=175, poids_kg=70
        )

        # Older person
        bmr_old = self.calculator.calculate_bmr(
            age=65, sexe="Homme", taille_cm=175, poids_kg=70
        )

        # Young should have higher BMR than old
        self.assertGreater(bmr_young, bmr_old)

        # All results should be above minimum threshold
        self.assertGreaterEqual(bmr_young, 800)
        self.assertGreaterEqual(bmr_old, 800)


class TestTDEECalculations(unittest.TestCase):
    """Test TDEE calculation with activity factors"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()
        self.base_bmr = 1800  # Typical male BMR

    def test_activity_factors(self):
        """Test all activity level multipliers"""
        activity_tests = [
            (ActivityLevel.SEDENTARY, 1.2),
            (ActivityLevel.LIGHTLY_ACTIVE, 1.375),
            (ActivityLevel.MODERATELY_ACTIVE, 1.55),
            (ActivityLevel.VERY_ACTIVE, 1.725),
            (ActivityLevel.EXTREMELY_ACTIVE, 1.9)
        ]

        for activity_level, expected_factor in activity_tests:
            tdee = self.calculator.calculate_tdee(self.base_bmr, activity_level)
            expected_tdee = self.base_bmr * expected_factor

            self.assertAlmostEqual(tdee, expected_tdee, places=1)
            self.assertEqual(activity_level.factor, expected_factor)

    def test_tdee_progression(self):
        """Test that TDEE increases with activity level"""
        activity_levels = [
            ActivityLevel.SEDENTARY,
            ActivityLevel.LIGHTLY_ACTIVE,
            ActivityLevel.MODERATELY_ACTIVE,
            ActivityLevel.VERY_ACTIVE,
            ActivityLevel.EXTREMELY_ACTIVE
        ]

        tdees = []
        for level in activity_levels:
            tdee = self.calculator.calculate_tdee(self.base_bmr, level)
            tdees.append(tdee)

        # Each level should be higher than the previous
        for i in range(1, len(tdees)):
            self.assertGreater(tdees[i], tdees[i-1])


class TestMacroDistribution(unittest.TestCase):
    """Test macronutrient distribution calculations"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_macro_calculation_balance(self):
        """Test that macro calculations balance correctly"""
        target_calories = 2200
        poids_kg = 75

        macro_targets = MacroTargets(
            proteines_g_par_kg=1.6,
            glucides_pct=50.0,
            lipides_pct=50.0
        )

        prot_g, carb_g, fat_g, prot_kcal, carb_kcal, fat_kcal = \
            self.calculator.calculate_macro_distribution(
                target_calories, poids_kg, macro_targets
            )

        # Check protein calculation
        expected_protein_g = poids_kg * 1.6
        self.assertEqual(prot_g, int(expected_protein_g))
        self.assertEqual(prot_kcal, prot_g * 4)

        # Check total calories approximately match target
        total_kcal = prot_kcal + carb_kcal + fat_kcal
        self.assertAlmostEqual(total_kcal, target_calories, delta=50)

        # Check macro ratios
        remaining_kcal = target_calories - prot_kcal
        expected_carb_kcal = remaining_kcal * 0.5
        expected_fat_kcal = remaining_kcal * 0.5

        self.assertAlmostEqual(carb_kcal, expected_carb_kcal, delta=20)
        self.assertAlmostEqual(fat_kcal, expected_fat_kcal, delta=20)

    def test_minimum_macros(self):
        """Test minimum macro requirements are enforced"""
        # Very low calorie scenario
        target_calories = 1000
        poids_kg = 60

        macro_targets = MacroTargets(
            proteines_g_par_kg=0.8,  # Minimum protein
            glucides_pct=30.0,
            lipides_pct=70.0
        )

        prot_g, carb_g, fat_g, prot_kcal, carb_kcal, fat_kcal = \
            self.calculator.calculate_macro_distribution(
                target_calories, poids_kg, macro_targets
            )

        # Check minimums are enforced
        self.assertGreaterEqual(carb_g, 50)  # Minimum 50g carbs
        self.assertGreaterEqual(fat_g, 20)   # Minimum 20g fats

    def test_high_protein_scenario(self):
        """Test high protein distribution"""
        target_calories = 2000
        poids_kg = 80

        macro_targets = MacroTargets(
            proteines_g_par_kg=2.5,  # High protein
            glucides_pct=40.0,
            lipides_pct=60.0
        )

        prot_g, carb_g, fat_g, prot_kcal, carb_kcal, fat_kcal = \
            self.calculator.calculate_macro_distribution(
                target_calories, poids_kg, macro_targets
            )

        # Protein should be 200g (80kg * 2.5)
        self.assertEqual(prot_g, 200)
        self.assertEqual(prot_kcal, 800)  # 200g * 4 kcal/g

        # Remaining calories should be distributed correctly
        remaining_kcal = target_calories - prot_kcal  # 1200 kcal
        expected_carb_kcal = remaining_kcal * 0.4  # 480 kcal
        expected_fat_kcal = remaining_kcal * 0.6   # 720 kcal

        self.assertAlmostEqual(carb_kcal, expected_carb_kcal, delta=20)
        self.assertAlmostEqual(fat_kcal, expected_fat_kcal, delta=20)


class TestCompleteNutritionCalculation(unittest.TestCase):
    """Test complete nutrition calculation pipeline"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_complete_calculation_male_maintenance(self):
        """Test complete calculation for male maintenance"""
        personal_data = PersonalData(
            nom="Test",
            prenom="User",
            age=30,
            sexe="Homme",
            taille_cm=180,
            poids_kg=80,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=NutritionGoal.MAINTENANCE
        )

        macro_targets = MacroTargets(
            proteines_g_par_kg=1.6,
            glucides_pct=50.0,
            lipides_pct=50.0
        )

        results = self.calculator.calculate_complete_nutrition(
            personal_data, macro_targets
        )

        # Validate results structure
        self.assertIsInstance(results, NutritionResults)
        self.assertGreater(results.bmr_kcal, 1600)
        self.assertLess(results.bmr_kcal, 2000)
        self.assertGreater(results.tdee_kcal, 2000)
        self.assertLess(results.tdee_kcal, 3000)

        # Maintenance should have no deficit/surplus
        self.assertEqual(results.deficit_surplus, 0)
        self.assertEqual(results.objectif_kcal, results.tdee_kcal)

        # Check macros
        self.assertGreater(results.proteines_g, 100)
        self.assertGreater(results.glucides_g, 200)
        self.assertGreater(results.lipides_g, 60)

        # Check percentages sum to ~100%
        total_pct = results.proteines_pct + results.glucides_pct + results.lipides_pct
        self.assertAlmostEqual(total_pct, 100.0, delta=1.0)

    def test_complete_calculation_female_fat_loss(self):
        """Test complete calculation for female fat loss"""
        personal_data = PersonalData(
            nom="Test",
            prenom="User",
            age=28,
            sexe="Femme",
            taille_cm=165,
            poids_kg=60,
            niveau_activite=ActivityLevel.LIGHTLY_ACTIVE,
            objectif=NutritionGoal.FAT_LOSS_MODERATE
        )

        macro_targets = MacroTargets(
            proteines_g_par_kg=1.8,  # Higher protein for fat loss
            glucides_pct=40.0,
            lipides_pct=60.0
        )

        results = self.calculator.calculate_complete_nutrition(
            personal_data, macro_targets
        )

        # Fat loss should have negative deficit
        self.assertEqual(results.deficit_surplus, -400)
        self.assertLess(results.objectif_kcal, results.tdee_kcal)

        # Should never go below 110% of BMR
        min_calories = results.bmr_kcal * 1.1
        self.assertGreaterEqual(results.objectif_kcal, min_calories)

        # Protein should be high for muscle preservation
        expected_protein = 60 * 1.8  # 108g
        self.assertEqual(results.proteines_g, int(expected_protein))

    def test_complete_calculation_lean_gain(self):
        """Test complete calculation for lean gain"""
        personal_data = PersonalData(
            nom="Test",
            prenom="User",
            age=25,
            sexe="Homme",
            taille_cm=175,
            poids_kg=70,
            niveau_activite=ActivityLevel.VERY_ACTIVE,
            objectif=NutritionGoal.LEAN_GAIN_MODERATE
        )

        macro_targets = MacroTargets(
            proteines_g_par_kg=2.0,
            glucides_pct=60.0,  # Higher carbs for gain
            lipides_pct=40.0
        )

        results = self.calculator.calculate_complete_nutrition(
            personal_data, macro_targets
        )

        # Lean gain should have positive surplus
        self.assertEqual(results.deficit_surplus, 400)
        self.assertGreater(results.objectif_kcal, results.tdee_kcal)

        # Higher activity should result in higher TDEE
        self.assertGreater(results.tdee_kcal, 2500)


class TestValidationAndEdgeCases(unittest.TestCase):
    """Test validation and edge cases"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_age_validation(self):
        """Test age validation"""
        personal_data = PersonalData(
            nom="Test", prenom="User",
            age=5,  # Too young
            sexe="Homme", taille_cm=175, poids_kg=70,
            niveau_activite=ActivityLevel.SEDENTARY,
            objectif=NutritionGoal.MAINTENANCE
        )

        with self.assertRaises(ValueError):
            self.calculator.calculate_complete_nutrition(personal_data, MacroTargets())

    def test_weight_validation(self):
        """Test weight validation"""
        personal_data = PersonalData(
            nom="Test", prenom="User",
            age=30, sexe="Homme", taille_cm=175,
            poids_kg=25,  # Too light
            niveau_activite=ActivityLevel.SEDENTARY,
            objectif=NutritionGoal.MAINTENANCE
        )

        with self.assertRaises(ValueError):
            self.calculator.calculate_complete_nutrition(personal_data, MacroTargets())

    def test_height_validation(self):
        """Test height validation"""
        personal_data = PersonalData(
            nom="Test", prenom="User",
            age=30, sexe="Homme",
            taille_cm=90,  # Too short
            poids_kg=70, niveau_activite=ActivityLevel.SEDENTARY,
            objectif=NutritionGoal.MAINTENANCE
        )

        with self.assertRaises(ValueError):
            self.calculator.calculate_complete_nutrition(personal_data, MacroTargets())


class TestRecommendations(unittest.TestCase):
    """Test personalized recommendations"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_general_recommendations(self):
        """Test general recommendations generation"""
        results = self._create_test_results()
        recommendations = self.calculator.get_personalized_recommendations(results)

        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 5)

        # Should contain hydration recommendation
        hydration_found = any("💧" in rec for rec in recommendations)
        self.assertTrue(hydration_found)

        # Should contain sleep recommendation
        sleep_found = any("😴" in rec for rec in recommendations)
        self.assertTrue(sleep_found)

    def test_fat_loss_recommendations(self):
        """Test fat loss specific recommendations"""
        results = self._create_test_results(goal=NutritionGoal.FAT_LOSS_MODERATE)
        recommendations = self.calculator.get_personalized_recommendations(results)

        # Should contain fat loss specific advice
        fat_loss_found = any("légumes" in rec.lower() for rec in recommendations)
        self.assertTrue(fat_loss_found)

    def test_lean_gain_recommendations(self):
        """Test lean gain specific recommendations"""
        results = self._create_test_results(goal=NutritionGoal.LEAN_GAIN_MODERATE)
        recommendations = self.calculator.get_personalized_recommendations(results)

        # Should contain lean gain specific advice
        gain_found = any("glucides" in rec.lower() for rec in recommendations)
        self.assertTrue(gain_found)

    def _create_test_results(self, goal=NutritionGoal.MAINTENANCE) -> NutritionResults:
        """Create test results object"""
        personal_data = PersonalData(
            nom="Test", prenom="User", age=30, sexe="Homme",
            taille_cm=175, poids_kg=75,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=goal
        )

        return self.calculator.calculate_complete_nutrition(
            personal_data, MacroTargets()
        )


class TestTimelineEstimation(unittest.TestCase):
    """Test timeline estimation functionality"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_maintenance_timeline(self):
        """Test maintenance timeline"""
        results = self._create_test_results(NutritionGoal.MAINTENANCE)
        timeline = self.calculator.estimate_timeline(results)

        self.assertEqual(timeline["rate"], "0 kg/mois")
        self.assertEqual(timeline["timeline"], "Maintenance continue")

    def test_fat_loss_timeline(self):
        """Test fat loss timeline"""
        results = self._create_test_results(NutritionGoal.FAT_LOSS_MODERATE)
        timeline = self.calculator.estimate_timeline(results)

        self.assertIn("kg/mois", timeline["rate"])
        self.assertIn("-", timeline["rate"])  # Should be negative

    def test_lean_gain_timeline(self):
        """Test lean gain timeline"""
        results = self._create_test_results(NutritionGoal.LEAN_GAIN_MODERATE)
        timeline = self.calculator.estimate_timeline(results)

        self.assertIn("kg/mois", timeline["rate"])
        self.assertIn("+", timeline["rate"])  # Should be positive

    def _create_test_results(self, goal: NutritionGoal) -> NutritionResults:
        """Create test results"""
        personal_data = PersonalData(
            nom="Test", prenom="User", age=30, sexe="Homme",
            taille_cm=175, poids_kg=75,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=goal
        )

        return self.calculator.calculate_complete_nutrition(
            personal_data, MacroTargets()
        )


class TestPerformance(unittest.TestCase):
    """Performance tests for nutrition calculations"""

    def setUp(self):
        self.calculator = AdvancedNutritionCalculator()

    def test_calculation_performance(self):
        """Test that calculations are performant"""
        import time

        personal_data = PersonalData(
            nom="Test", prenom="User", age=30, sexe="Homme",
            taille_cm=175, poids_kg=75,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=NutritionGoal.MAINTENANCE
        )

        # Time 100 calculations
        start_time = time.time()
        for _ in range(100):
            results = self.calculator.calculate_complete_nutrition(
                personal_data, MacroTargets()
            )
        end_time = time.time()

        avg_time = (end_time - start_time) / 100

        # Should complete in less than 10ms per calculation
        self.assertLess(avg_time, 0.01)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)