#!/usr/bin/env python3
"""
Test Simple d'Intégration Nutrition
===================================

Test minimal pour vérifier l'intégration sans lancer l'UI complète
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test que tous les imports fonctionnent"""
    print("Test des imports...")

    try:
        # Test advanced nutrition calculator
        from services.advanced_nutrition_calculator import (
            AdvancedNutritionCalculator,
            PersonalData,
            MacroTargets,
            ActivityLevel,
            NutritionGoal
        )
        print("OK - Advanced nutrition calculator")

        # Test professional PDF
        from services.professional_nutrition_pdf import generate_professional_nutrition_pdf
        print("OK - Professional PDF generator")

        # Test controller
        from controllers.advanced_nutrition_controller import AdvancedNutritionController
        print("OK - Advanced nutrition controller")

        # Test modal
        from ui.modals.nutrition_form_modal import AdvancedNutritionFormModal
        print("OK - Advanced nutrition modal")

        # Test dashboard
        from ui.components.nutrition_dashboard import AdvancedNutritionDashboard
        print("OK - Advanced nutrition dashboard")

        return True

    except Exception as e:
        print(f"ERREUR import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calculations():
    """Test des calculs nutrition de base"""
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

        # Test BMR calculation
        bmr = calculator.calculate_bmr(
            age=30,
            sexe="Homme",
            taille_cm=175,
            poids_kg=75
        )
        print(f"✅ BMR calculé: {bmr:.1f} kcal/jour")

        # Test complete calculation
        personal_data = PersonalData(
            nom="Test", prenom="User",
            age=30, sexe="Homme",
            taille_cm=175, poids_kg=75,
            niveau_activite=ActivityLevel.MODERATELY_ACTIVE,
            objectif=NutritionGoal.MAINTENANCE
        )

        results = calculator.calculate_complete_nutrition(personal_data, MacroTargets())
        print(f"✅ Calcul complet:")
        print(f"   - TDEE: {results.tdee_kcal} kcal")
        print(f"   - Objectif: {results.objectif_kcal} kcal")
        print(f"   - Protéines: {results.proteines_g}g")
        print(f"   - Glucides: {results.glucides_g}g")
        print(f"   - Lipides: {results.lipides_g}g")

        return True

    except Exception as e:
        print(f"❌ Erreur calculs: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_integration():
    """Test intégration base de données"""
    print("\n💾 Test base de données...")

    try:
        from repositories.fiche_nutrition_repo import FicheNutritionRepository
        from models.fiche_nutrition import FicheNutrition

        repo = FicheNutritionRepository()
        print("✅ Repository nutrition - OK")

        # Test création fiche
        fiche = FicheNutrition(
            id=None,
            client_id=1,
            date_creation=None,
            poids_kg_mesure=75.0,
            objectif="Maintenance",
            proteines_cible_g_par_kg=1.6,
            ratio_glucides_lipides_cible=50.0,
            maintenance_kcal=2200,
            objectif_kcal=2200,
            proteines_g=120,
            glucides_g=275,
            lipides_g=97
        )

        print("✅ Modèle fiche nutrition - OK")
        return True

    except Exception as e:
        print(f"❌ Erreur database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test complet d'intégration"""
    print("🚀 Test d'Intégration Système Nutrition Avancé")
    print("=" * 50)

    success = True

    # Test imports
    if not test_imports():
        success = False

    # Test calculations
    if not test_calculations():
        success = False

    # Test database
    if not test_database_integration():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("✅ TOUS LES TESTS PASSENT - Intégration réussie!")
        print("\n📋 Fonctionnalités disponibles:")
        print("• Calculs nutrition scientifiques")
        print("• Formulaire modal multi-étapes")
        print("• Dashboard nutrition avancé")
        print("• Génération PDF professionnelle")
        print("• Intégration complète dans l'app")
        print("\n🚀 Lancez 'python main.py' pour utiliser l'application!")
    else:
        print("❌ ÉCHEC - Problèmes d'intégration détectés")

    return success

if __name__ == "__main__":
    main()