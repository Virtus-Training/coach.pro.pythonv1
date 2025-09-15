"""
Test script for professional PDF templates
Validates the integration and functionality of commercial-grade templates
"""

import os
import tempfile

from controllers.advanced_pdf_controller import AdvancedPdfController


def test_professional_templates():
    """Test all professional templates with sample data"""
    print("🏆 TESTING PROFESSIONAL PDF TEMPLATES")
    print("=" * 50)

    controller = AdvancedPdfController()

    # Test workout templates
    print("\n💪 TESTING WORKOUT TEMPLATES:")
    workout_data = {
        "title": "Programme Elite Performance",
        "client_name": "Alexandre Martin",
        "program_overview": {
            "primary_goal": "Force maximale",
            "duration_weeks": 8,
            "sessions_per_week": 4,
            "intensity_level": "Élevé",
            "target_areas": ["Poitrine", "Dos", "Jambes"],
        },
        "performance_metrics": {
            "strength_progress": 85,
            "endurance_progress": 70,
            "flexibility_progress": 60,
        },
        "target_muscle_groups": ["chest", "shoulders", "legs"],
        "workout_blocks": [
            {
                "title": "Force Maximale",
                "duration": 45,
                "format": "PRINCIPAL",
                "exercises": [
                    {"name": "Squat", "reps": "5x3", "notes": "90% 1RM"},
                    {"name": "Développé couché", "reps": "5x3", "notes": "85% 1RM"},
                    {"name": "Soulevé de terre", "reps": "4x2", "notes": "95% 1RM"},
                ],
            }
        ],
    }

    workout_styles = ["elite", "motivation", "medical"]
    for style in workout_styles:
        try:
            with tempfile.NamedTemporaryFile(
                suffix=f"_{style}_workout.pdf", delete=False
            ) as temp_file:
                temp_path = temp_file.name

            print(f"  🏋️ Testing {style.upper()} template...")
            result = controller.generate_professional_workout_pdf(
                workout_data, temp_path, style
            )

            if result.get("success"):
                print(
                    f"    ✅ SUCCESS - Generated in {result.get('generation_time', 0):.2f}s"
                )
                print(f"    📄 File: {temp_path}")
                print(f"    📊 Size: {os.path.getsize(temp_path) // 1024} KB")
            else:
                print(f"    ❌ FAILED - {result.get('error')}")

        except Exception as e:
            print(f"    💥 EXCEPTION - {str(e)}")

    # Test nutrition templates
    print("\n🥗 TESTING NUTRITION TEMPLATES:")
    nutrition_data = {
        "client_name": "Sophie Leblanc",
        "analysis_date": "2025-01-13",
        "biometrics": {
            "age": 28,
            "weight": 65.5,
            "height": 170,
            "body_fat": 22.5,
            "lean_mass": 50.8,
        },
        "nutrition_analytics": {
            "tdee": 2100,
            "target_calories": 1800,
            "protein_g": 130,
            "carbs_g": 180,
            "fat_g": 70,
            "fiber_target": 28,
            "water_target": 33,
        },
        "micronutrient_analysis": {
            "vit_d": 18,
            "b12": 3.2,
            "iron": 12,
            "magnesium": 280,
            "zinc": 9.5,
            "omega3": 1.8,
        },
    }

    nutrition_styles = ["science"]  # Start with one that we've implemented
    for style in nutrition_styles:
        try:
            with tempfile.NamedTemporaryFile(
                suffix=f"_{style}_nutrition.pdf", delete=False
            ) as temp_file:
                temp_path = temp_file.name

            print(f"  🔬 Testing {style.upper()} template...")
            result = controller.generate_professional_nutrition_pdf(
                nutrition_data, temp_path, style
            )

            if result.get("success"):
                print(
                    f"    ✅ SUCCESS - Generated in {result.get('generation_time', 0):.2f}s"
                )
                print(f"    📄 File: {temp_path}")
                print(f"    📊 Size: {os.path.getsize(temp_path) // 1024} KB")
            else:
                print(f"    ❌ FAILED - {result.get('error')}")

        except Exception as e:
            print(f"    💥 EXCEPTION - {str(e)}")

    # Test template information
    print("\n📋 TESTING TEMPLATE INFORMATION:")
    try:
        templates_info = controller.get_professional_templates()
        print(f"  📊 Found {len(templates_info)} template categories")

        for category, templates in templates_info.items():
            print(f"  📁 {category}: {len(templates)} templates")
            for template_id, template_info in templates.items():
                print(
                    f"    • {template_info.get('name', template_id)}: {template_info.get('style', 'No style')}"
                )
    except Exception as e:
        print(f"  💥 Template info failed: {str(e)}")

    # Performance stats
    print("\n📈 PERFORMANCE STATISTICS:")
    try:
        stats = controller.get_performance_stats()
        print(f"  📊 Total documents: {stats.get('total_documents', 0)}")
        print(f"  ⏱️ Average time: {stats.get('average_time', 0):.2f}s")

        cache_stats = stats.get("cache_stats")
        if cache_stats:
            print(f"  💾 Cache hits: {cache_stats.get('hits', 0)}")
            print(f"  🎯 Hit rate: {cache_stats.get('hit_rate', 0):.1%}")
    except Exception as e:
        print(f"  💥 Stats failed: {str(e)}")

    print("\n🏁 PROFESSIONAL TEMPLATES TEST COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    test_professional_templates()
