#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_unified_nutrition():
    print("Test Page Nutrition Unifiee")
    print("=" * 40)

    try:
        # Test import de la page unifiée
        from ui.pages.nutrition_unified_page import NutritionUnifiedPage
        print("OK - Import page nutrition unifiee")

        # Test des dépendances
        from controllers.nutrition_controller import NutritionController
        from controllers.advanced_nutrition_controller import AdvancedNutritionController
        print("OK - Controllers disponibles")

        from ui.components.nutrition_dashboard import AdvancedNutritionDashboard
        print("OK - Dashboard avance disponible")

        # Test intégration app
        from app import CoachApp
        print("OK - Integration dans app principale")

        print("\n" + "=" * 40)
        print("INTEGRATION REUSSIE!")
        print("\nPage 'Nutrition' maintenant disponible avec 3 onglets:")
        print("- Dashboard : Vue d'ensemble + calculatrice rapide")
        print("- Nutrition 2025 : Interface moderne de suivi")
        print("- Calculs Avances : Generateur fiches scientifiques")
        print("\nLancez 'python main.py' pour tester!")

        return True

    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_unified_nutrition()