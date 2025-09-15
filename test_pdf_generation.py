"""
Test PDF Generation - Diagnose PDF creation issues
"""

import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

print("TESTING PDF GENERATION")
print("=" * 50)

try:
    from controllers.advanced_pdf_controller import AdvancedPdfController

    print("SUCCESS: Controller imported")

    controller = AdvancedPdfController()
    print("SUCCESS: Controller instantiated")

    # Test data for workout PDF
    workout_data = {
        "title": "Test Workout",
        "client_name": "Client Test",
        "coach_name": "Coach Test",
        "session_date": "2024-01-15",
        "session_duration": "45 min",
        "exercises": [
            {
                "name": "Push-ups",
                "sets": 3,
                "reps": 15,
                "rest": "60s",
                "notes": "Maintenir la forme",
            },
            {
                "name": "Squats",
                "sets": 4,
                "reps": 12,
                "rest": "90s",
                "notes": "Descendre à 90 degrés",
            },
        ],
    }

    # Create temporary output file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    print(f"Testing PDF generation to: {output_path}")

    # Test Elite template
    try:
        result = controller.generate_professional_workout_pdf(
            workout_data=workout_data, output_path=output_path, template_style="elite"
        )

        if result.get("success"):
            print("SUCCESS: Elite template PDF generated")
            if Path(output_path).exists():
                size = Path(output_path).stat().st_size
                print(f"  File size: {size} bytes")
            else:
                print("WARNING: File not found after generation")
        else:
            print(
                f"ERROR: Elite template failed: {result.get('error', 'Unknown error')}"
            )

    except Exception as e:
        print(f"CRITICAL ERROR in Elite template: {e}")
        import traceback

        traceback.print_exc()

    # Test templates list
    try:
        templates = controller.get_professional_templates()
        print(f"SUCCESS: Found {len(templates)} template categories")

        for category, template_dict in templates.items():
            print(f"  Category '{category}': {len(template_dict)} templates")

    except Exception as e:
        print(f"ERROR: Failed to get templates: {e}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback

    traceback.print_exc()

print("\nPDF GENERATION TEST COMPLETED")
print("=" * 50)
