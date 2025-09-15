"""
Test Controller PDF Generation
"""

import sys
import tempfile
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

print("TESTING CONTROLLER PDF GENERATION")
print("=" * 50)

try:
    from controllers.advanced_pdf_controller import AdvancedPdfController

    print("SUCCESS: Controller imported")

    controller = AdvancedPdfController()
    print("SUCCESS: Controller instantiated")

    # Better test data matching expected structure
    workout_data = {
        "title": "Entraînement Elite Test",
        "client_name": "John Doe",
        "coach_name": "Coach Pro",
        "session_date": "2024-01-15",
        "session_duration": "45 min",
        "exercises": [
            {
                "name": "Push-ups",
                "sets": 3,
                "reps": 15,
                "rest": "60s",
                "notes": "Maintenir la forme correcte",
            },
            {
                "name": "Squats",
                "sets": 4,
                "reps": 12,
                "rest": "90s",
                "notes": "Descendre à 90 degrés",
            },
            {
                "name": "Plank",
                "sets": 3,
                "reps": "30s",
                "rest": "45s",
                "notes": "Gainage complet",
            },
        ],
    }

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    print(f"Generating PDF to: {output_path}")

    try:
        result = controller.generate_professional_workout_pdf(
            workout_data=workout_data,
            output_path=output_path,
            template_style="elite",
            async_mode=False,
        )

        print(f"Result: {result}")

        if result.get("success"):
            print("SUCCESS: PDF generated successfully!")
            if Path(output_path).exists():
                size = Path(output_path).stat().st_size
                print(f"  File size: {size} bytes")
                print(f"  File location: {output_path}")
            else:
                print("WARNING: File not found after generation")
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"ERROR: PDF generation failed: {error_msg}")

    except Exception as e:
        print(f"EXCEPTION during PDF generation: {e}")
        traceback.print_exc()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    traceback.print_exc()

print("\nCONTROLLER TEST COMPLETED")
print("=" * 50)
