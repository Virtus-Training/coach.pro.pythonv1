"""
Simple integration test for professional PDF templates
Tests basic functionality without emojis
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

print("TESTING PROFESSIONAL PDF TEMPLATES")
print("=" * 50)

try:
    from controllers.advanced_pdf_controller import AdvancedPdfController

    print("SUCCESS: Controller imported successfully")

    controller = AdvancedPdfController()
    print("SUCCESS: Controller instantiated")

    # Test getting professional templates
    try:
        templates = controller.get_professional_templates()
        print(f"SUCCESS: Found {len(templates)} template categories")

        for category, template_dict in templates.items():
            print(f"  Category: {category}")
            for template_id, info in template_dict.items():
                name = info.get("name", template_id)
                print(f"    - {template_id}: {name}")

    except Exception as e:
        print(f"ERROR: Failed to get templates: {e}")

    # Test performance stats
    try:
        stats = controller.get_performance_stats()
        print("SUCCESS: Performance stats retrieved")
        print(f"  Total documents: {stats.get('total_documents', 0)}")
    except Exception as e:
        print(f"ERROR: Failed to get stats: {e}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback

    traceback.print_exc()

print("\nINTEGRATION TEST COMPLETED")
print("=" * 50)
