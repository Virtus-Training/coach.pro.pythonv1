# -*- coding: utf-8 -*-
"""
Debug du problème PDF
"""

def test_step_by_step():
    print("Debug step by step...")

    # Test 1: Template Factory
    print("\n1. Test Template Factory")
    try:
        from services.pdf_engine.core.template_factory import TemplateFactory
        factory = TemplateFactory()
        print("OK - TemplateFactory initialise")
    except Exception as e:
        print(f"ERREUR - TemplateFactory: {e}")
        return

    # Test 2: Session Template directement
    print("\n2. Test Session Template direct")
    try:
        from services.pdf_engine.templates.session_template import SessionTemplate

        session_data = {
            "title": "Test Session",
            "client_name": "Test Client",
            "date": "2025-01-20",
            "blocks": []
        }

        template = SessionTemplate(session_data)
        print("OK - SessionTemplate cree")
    except Exception as e:
        print(f"ERREUR - SessionTemplate: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 3: Template Factory create_template
    print("\n3. Test Factory create_template")
    try:
        template = factory.create_template("session", session_data)
        print("OK - Template cree via factory")
    except Exception as e:
        print(f"ERREUR - Factory create: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nDEBUG termine - pas d'erreur detectee au niveau templates")


if __name__ == "__main__":
    test_step_by_step()