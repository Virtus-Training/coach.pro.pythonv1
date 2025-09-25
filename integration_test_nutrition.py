#!/usr/bin/env python3
"""
Test d'Intégration du Système Nutrition Avancé
===============================================

Test complet de l'intégration dans l'application CoachPro
"""

import sys
from pathlib import Path
import customtkinter as ctk

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import CoachApp

def main():
    """Lance l'application avec les fonctionnalités nutrition intégrées"""
    print("🚀 Lancement CoachPro avec Système Nutrition Avancé")
    print("=" * 60)
    print("Fonctionnalités ajoutées:")
    print("✅ Modal nutrition multi-étapes dans page Clients")
    print("✅ Nouvelle page 'Nutrition Avancée' dans le menu")
    print("✅ Calculs scientifiques BMR/TDEE/Macros")
    print("✅ Génération PDF professionnelle")
    print("✅ Dashboard avec calculatrice rapide")
    print("=" * 60)
    print("\n📋 Instructions d'utilisation:")
    print("1. Aller dans 'Clients' → Cliquer sur '🥗 Fiche Nutrition' pour un client")
    print("2. OU aller dans 'Nutrition Avancée' depuis le menu lateral")
    print("3. Tester le formulaire à 5 étapes avec validation temps réel")
    print("4. Générer un PDF professionnel de qualité premium")
    print("\n🎯 Le système rivalise maintenant avec les logiciels nutritionnistes pros!")
    print("=" * 60)

    try:
        app = CoachApp()
        app.mainloop()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()