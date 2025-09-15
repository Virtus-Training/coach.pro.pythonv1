"""
Test simple du système PDF avancé
Vérification que les modules s'importent et fonctionnent
"""

def test_import_modules():
    """Test l'import des modules principaux"""
    print("Test d'import des modules...")

    try:
        from services.advanced_pdf_service import AdvancedPdfService
        print("OK - AdvancedPdfService importe avec succes")
    except ImportError as e:
        print(f"ERREUR import AdvancedPdfService: {e}")
        return False

    try:
        from controllers.advanced_pdf_controller import AdvancedPdfController
        print("OK - AdvancedPdfController importe avec succes")
    except ImportError as e:
        print(f"ERREUR import AdvancedPdfController: {e}")
        return False

    try:
        from ui.pages.advanced_pdf_templates_page import AdvancedPdfTemplatesPage
        print("OK - AdvancedPdfTemplatesPage importe avec succes")
    except ImportError as e:
        print(f"ERREUR import AdvancedPdfTemplatesPage: {e}")
        return False

    return True


def test_service_initialization():
    """Test l'initialisation du service"""
    print("\n🧪 Test d'initialisation du service...")

    try:
        from services.advanced_pdf_service import AdvancedPdfService
        service = AdvancedPdfService()
        print("✅ Service initialisé avec succès")

        # Test templates disponibles
        templates = service.get_available_templates()
        print(f"✅ Templates disponibles: {list(templates.keys())}")

        # Test thèmes
        themes = service.get_template_themes()
        print(f"✅ Thèmes disponibles: {list(themes.keys())}")

        return True
    except Exception as e:
        print(f"❌ Erreur initialisation service: {e}")
        return False


def test_sample_data():
    """Test la génération de données d'exemple"""
    print("\n🧪 Test des données d'exemple...")

    try:
        from services.advanced_pdf_service import AdvancedPdfService
        service = AdvancedPdfService()

        # Test données session
        session_data = service.get_sample_data("session")
        print(f"✅ Données session: {len(str(session_data))} caractères")

        # Test données nutrition
        nutrition_data = service.get_sample_data("nutrition")
        print(f"✅ Données nutrition: {len(str(nutrition_data))} caractères")

        return True
    except Exception as e:
        print(f"❌ Erreur données d'exemple: {e}")
        return False


def test_simple_pdf_generation():
    """Test génération PDF simple"""
    print("\n🧪 Test génération PDF simple...")

    try:
        from services.advanced_pdf_service import AdvancedPdfService
        import tempfile
        import os

        service = AdvancedPdfService()

        # Créer fichier temporaire
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        # Données de test simples
        session_data = {
            "title": "Test Session",
            "client_name": "Test Client",
            "date": "2025-01-20",
            "blocks": [
                {
                    "title": "Test Block",
                    "format": "LIBRE",
                    "exercises": [
                        {"name": "Test Exercise", "reps": "10"}
                    ]
                }
            ]
        }

        # Génération synchrone
        result = service.generate_session_pdf_sync(
            session_data,
            tmp_path,
            template_variant="modern"
        )

        if os.path.exists(tmp_path):
            file_size = os.path.getsize(tmp_path)
            print(f"✅ PDF généré avec succès: {file_size} bytes")

            # Nettoyage
            os.unlink(tmp_path)
            return True
        else:
            print(f"❌ Fichier PDF non créé: {result}")
            return False

    except Exception as e:
        print(f"❌ Erreur génération PDF: {e}")
        # Cleanup if needed
        try:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except:
            pass
        return False


def main():
    """Test principal"""
    print("🚀 Test du Système PDF Avancé CoachPro")
    print("=" * 50)

    tests_passed = 0
    total_tests = 4

    # Test 1: Import des modules
    if test_import_modules():
        tests_passed += 1

    # Test 2: Initialisation du service
    if test_service_initialization():
        tests_passed += 1

    # Test 3: Données d'exemple
    if test_sample_data():
        tests_passed += 1

    # Test 4: Génération PDF simple
    if test_simple_pdf_generation():
        tests_passed += 1

    # Résultats
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")

    if tests_passed == total_tests:
        print("🎉 Tous les tests ont réussi ! Le système PDF avancé est opérationnel.")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)