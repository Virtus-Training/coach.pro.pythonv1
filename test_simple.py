#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    print("Test des imports...")

    try:
        from services.advanced_nutrition_calculator import (
            AdvancedNutritionCalculator,
            PersonalData,
            MacroTargets,
            ActivityLevel,
            NutritionGoal
        )
        print("OK - Advanced nutrition calculator")

        from services.professional_nutrition_pdf import generate_professional_nutrition_pdf
        print("OK - Professional PDF generator")

        from controllers.advanced_nutrition_controller import AdvancedNutritionController
        print("OK - Advanced nutrition controller")

        from ui.modals.nutrition_form_modal import AdvancedNutritionFormModal
        print("OK - Advanced nutrition modal")

        from ui.components.nutrition_dashboard import AdvancedNutritionDashboard
        print("OK - Advanced nutrition dashboard")

        return True

    except Exception as e:
        print(f"ERREUR import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calculations():
    print("\nTest des calculs...")

    try:
        from services.advanced_nutrition_calculator import (
            AdvancedNutritionCalculator,
            PersonalData,
            MacroTargets,
            ActivityLevel,
            NutritionGoal
        )

        calculator = AdvancedNutritionCalculator()

        bmr = calculator.calculate_bmr(
            age=30,
            sexe="Homme",
            taille_cm=175,
            poids_kg=75
        )
        print(f"OK - BMR calcule: {bmr:.1f} kcal/jour")

        personal_data = PersonalData(
            nom="Test", prenom="User",
            age=30, sexe="Homme",
            taille_cm=175, poids_kg=75,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=NutritionGoal.MAINTENANCE
        )

        results = calculator.calculate_complete_nutrition(personal_data, MacroTargets())
        print(f"OK - Calcul complet:")
        print(f"   - TDEE: {results.tdee_kcal} kcal")
        print(f"   - Objectif: {results.objectif_kcal} kcal")
        print(f"   - Proteines: {results.proteines_g}g")
        print(f"   - Glucides: {results.glucides_g}g")
        print(f"   - Lipides: {results.lipides_g}g")

        return True

    except Exception as e:
        print(f"ERREUR calculs: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Test d'Integration Systeme Nutrition Avance")
    print("=" * 50)

    success = True

    if not test_imports():
        success = False

    if not test_calculations():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("TOUS LES TESTS PASSENT - Integration reussie!")
        print("\nFonctionnalites disponibles:")
        print("- Calculs nutrition scientifiques")
        print("- Formulaire modal multi-etapes")
        print("- Dashboard nutrition avance")
        print("- Generation PDF professionnelle")
        print("- Integration complete dans l'app")
        print("\nLancez 'python main.py' pour utiliser l'application!")
    else:
        print("ECHEC - Problemes d'integration detectes")

    return success

if __name__ == "__main__":
    main()