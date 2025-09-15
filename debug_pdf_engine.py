# -*- coding: utf-8 -*-
"""
Debug du PDFEngine
"""

def test_pdf_engine():
    print("Debug PDFEngine...")

    # Test 1: Import
    try:
        from services.pdf_engine.core.pdf_engine import PDFEngine
        print("OK - PDFEngine importe")
    except Exception as e:
        print(f"ERREUR - Import PDFEngine: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 2: Initialisation
    try:
        engine = PDFEngine(cache_enabled=False)  # Disable cache for debugging
        print("OK - PDFEngine initialise")
    except Exception as e:
        print(f"ERREUR - Init PDFEngine: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 3: generate_sync
    try:
        import tempfile

        session_data = {
            "title": "Test Session",
            "client_name": "Test Client",
            "date": "2025-01-20",
            "blocks": []
        }

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        print(f"Test avec donnees: {session_data}")
        print(f"Chemin sortie: {tmp_path}")

        result = engine.generate_sync(
            "session",
            session_data,
            tmp_path,
            {"variant": "modern"}
        )

        print(f"Resultat: {result}")

    except Exception as e:
        print(f"ERREUR - generate_sync: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pdf_engine()