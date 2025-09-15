"""
Detailed PDF Generation Test - Find exact error location
"""

import sys
import tempfile
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print("DETAILED PDF GENERATION TEST")
print("=" * 50)

try:
    # Test factory directly
    from services.pdf_engine.core.professional_template_factory import ProfessionalTemplateFactory
    print("SUCCESS: Factory imported")

    factory = ProfessionalTemplateFactory()
    print("SUCCESS: Factory instantiated")

    # Test template creation
    test_data = {
        "title": "Test Workout",
        "client_name": "Client Test",
        "coach_name": "Coach Test",
        "session_date": "2024-01-15"
    }

    try:
        template = factory.create_template("workout_elite", test_data)
        print(f"SUCCESS: Template created: {type(template)}")

        # Test if template has required methods
        if hasattr(template, 'build_content'):
            print("SUCCESS: Template has build_content method")
        else:
            print("ERROR: Template missing build_content method")

        if hasattr(template, 'build'):
            print("SUCCESS: Template has build method")
        else:
            print("ERROR: Template missing build method")

        # Try to build content
        try:
            content = template.build_content()
            print(f"SUCCESS: build_content returned {len(content)} items")
        except Exception as e:
            print(f"ERROR in build_content: {e}")
            traceback.print_exc()

    except Exception as e:
        print(f"ERROR creating template: {e}")
        traceback.print_exc()

    # Test PDFEngine directly
    print("\nTesting PDFEngine...")
    from services.pdf_engine.core.pdf_engine import PDFEngine
    engine = PDFEngine()
    engine.template_factory = factory
    print("SUCCESS: PDFEngine with professional factory")

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        output_path = tmp.name

    try:
        result = engine.generate_sync(
            template_type="workout_elite",
            data=test_data,
            output_path=output_path
        )
        print(f"SUCCESS: PDF generated: {result}")
    except Exception as e:
        print(f"ERROR in PDFEngine.generate_sync: {e}")
        traceback.print_exc()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    traceback.print_exc()

print("\nDETAILED TEST COMPLETED")
print("=" * 50)