"""
Test AdvancedPdfService directly
"""

import sys
import tempfile
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

print("TESTING ADVANCED PDF SERVICE DIRECTLY")
print("=" * 50)

try:
    from services.advanced_pdf_service import AdvancedPdfService

    print("SUCCESS: Service imported")

    service = AdvancedPdfService()
    print("SUCCESS: Service instantiated")

    # Test data
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
            }
        ],
    }

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    print(f"Generating PDF via service to: {output_path}")

    try:
        result = service.generate_professional_workout_pdf_sync(
            workout_data=workout_data, output_path=output_path, template_style="elite"
        )

        print(f"Service result: {result}")

        if result.get("success", True):  # Assume success if no success key
            print("SUCCESS: PDF generated via service!")
            if Path(output_path).exists():
                size = Path(output_path).stat().st_size
                print(f"  File size: {size} bytes")
            else:
                print("WARNING: File not found")
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"EXCEPTION in service: {e}")
        traceback.print_exc()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    traceback.print_exc()

print("\nSERVICE TEST COMPLETED")
print("=" * 50)
