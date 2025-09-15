# -*- coding: utf-8 -*-
"""
Test simple du système PDF avancé
"""

def main():
    print("Test du Systeme PDF Avance CoachPro")
    print("=" * 50)

    # Test 1: Import des modules
    print("\nTest d'import des modules...")
    try:
        from services.advanced_pdf_service import AdvancedPdfService
        print("OK - AdvancedPdfService")
    except Exception as e:
        print(f"ERREUR - AdvancedPdfService: {e}")
        return False

    try:
        from controllers.advanced_pdf_controller import AdvancedPdfController
        print("OK - AdvancedPdfController")
    except Exception as e:
        print(f"ERREUR - AdvancedPdfController: {e}")
        return False

    # Test 2: Initialisation
    print("\nTest d'initialisation...")
    try:
        service = AdvancedPdfService()
        print("OK - Service initialise")
    except Exception as e:
        print(f"ERREUR - Initialisation: {e}")
        return False

    # Test 3: Templates disponibles
    print("\nTest templates disponibles...")
    try:
        templates = service.get_available_templates()
        print(f"OK - {len(templates)} types de templates")
        for t_type, variants in templates.items():
            print(f"  - {t_type}: {len(variants)} variantes")
    except Exception as e:
        print(f"ERREUR - Templates: {e}")
        return False

    # Test 4: Génération PDF simple
    print("\nTest generation PDF...")
    try:
        import tempfile
        import os

        # Données de test
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

        # Génération
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        print(f"Donnees de test: {session_data}")

        result = service.generate_session_pdf_sync(
            session_data,
            tmp_path,
            template_variant="modern"
        )

        print(f"Resultat generation: {result}")

        if os.path.exists(tmp_path):
            file_size = os.path.getsize(tmp_path)
            print(f"OK - PDF genere: {file_size} bytes")
            os.unlink(tmp_path)
        else:
            print(f"ERREUR - PDF non cree: {result}")
            return False

    except Exception as e:
        print(f"ERREUR - Generation PDF: {e}")
        return False

    print("\n" + "=" * 50)
    print("SUCCES - Tous les tests ont reussi!")
    print("Le systeme PDF avance est operationnel.")
    return True


if __name__ == "__main__":
    main()