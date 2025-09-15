"""
Démonstration du Système PDF Avancé CoachPro
Exemple d'utilisation des nouvelles capacités de génération PDF
"""

import asyncio
import json
from pathlib import Path

from services.advanced_pdf_service import AdvancedPdfService


async def demo_advanced_pdf_system():
    """
    Démonstration complète du système PDF avancé
    """
    print("🚀 Démonstration du Système PDF Avancé CoachPro")
    print("=" * 60)

    # Initialize service
    pdf_service = AdvancedPdfService()

    # Create output directory
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    # 1. Session PDF with modern template
    print("\n📋 1. Génération PDF Séance (Template Moderne)")
    session_data = {
        "title": "HIIT Cardio Intense",
        "client_name": "Marie Dupont",
        "date": "2025-01-20",
        "duration": 45,
        "type": "Individuel",
        "blocks": [
            {
                "title": "Échauffement",
                "format": "LIBRE",
                "duration": 10,
                "exercises": [
                    {"name": "Marche rapide", "reps": "5 min", "notes": "Intensité progressive"},
                    {"name": "Mobilisations articulaires", "reps": "10x", "notes": "Épaules, hanches"},
                ]
            },
            {
                "title": "Corps principal",
                "format": "TABATA",
                "duration": 20,
                "exercises": [
                    {"name": "Burpees", "reps": "Maximum", "notes": "Technique parfaite"},
                    {"name": "Mountain Climbers", "reps": "Maximum", "notes": "Gainage serré"},
                    {"name": "Jump Squats", "reps": "Maximum", "notes": "Réception souple"},
                ]
            },
            {
                "title": "Retour au calme",
                "format": "LIBRE",
                "duration": 15,
                "exercises": [
                    {"name": "Étirements", "reps": "30s chaque", "notes": "Respiration profonde"},
                    {"name": "Relaxation", "reps": "5 min", "notes": "Position allongée"},
                ]
            }
        ],
        "notes": "Hydratation régulière. Adapter l'intensité selon la forme du jour."
    }

    result = await pdf_service.generate_session_pdf_async(
        session_data,
        str(output_dir / "session_hiit_moderne.pdf"),
        template_variant="modern"
    )
    print(f"   ✅ Session PDF généré en {result['generation_time']:.2f}s")
    print(f"   📄 Taille: {result['file_size'] // 1024} KB, {result['pages']} pages")

    # 2. Nutrition PDF with detailed template
    print("\n🥗 2. Génération PDF Nutrition (Template Détaillé)")
    nutrition_data = {
        "title": "Bilan Nutritionnel Personnalisé",
        "client_name": "Pierre Martin",
        "date": "2025-01-20",
        "personal_info": {
            "age": 35,
            "weight": 78.5,
            "height": 175,
            "gender": "Homme",
            "activity_level": "Modéré (3-4 séances/semaine)",
            "goal": "Perte de poids progressive"
        },
        "nutrition_data": {
            "maintenance_calories": 2200,
            "target_calories": 1800,
            "protein_g": 140,
            "carbs_g": 180,
            "fat_g": 60
        },
        "meal_plan": [
            {
                "meal": "Petit-déjeuner",
                "time": "7h30",
                "foods": ["Avoine 60g", "Protéines 30g", "Banane", "Amandes 20g"],
                "calories": 420
            },
            {
                "meal": "Collation",
                "time": "10h00",
                "foods": ["Yaourt grec", "Myrtilles"],
                "calories": 150
            },
            {
                "meal": "Déjeuner",
                "time": "12h30",
                "foods": ["Blanc de poulet 150g", "Quinoa 80g", "Légumes verts", "Huile olive 10ml"],
                "calories": 580
            }
        ],
        "recommendations": [
            "Boire au moins 2.5L d'eau par jour",
            "Privilégier les légumes à chaque repas principal",
            "Collations riches en protéines (yaourt, noix)",
            "Éviter les sucres rapides en soirée",
            "Peser les aliments au début pour calibrer les portions"
        ]
    }

    result = await pdf_service.generate_nutrition_pdf_async(
        nutrition_data,
        str(output_dir / "nutrition_detaillee.pdf"),
        template_variant="detailed"
    )
    print(f"   ✅ Nutrition PDF généré en {result['generation_time']:.2f}s")
    print(f"   📄 Taille: {result['file_size'] // 1024} KB, {result['pages']} pages")

    # 3. Program PDF with weekly layout
    print("\n📅 3. Génération PDF Programme (Layout Hebdomadaire)")
    program_data = {
        "title": "Programme Force & Masse - 4 Semaines",
        "client_name": "Sophie Leblanc",
        "duration_weeks": 4,
        "goal": "Développement de la force et hypertrophie musculaire",
        "weeks": [
            {
                "week_number": 1,
                "focus": "Adaptation - Volume modéré",
                "days": [
                    {
                        "day": "Lundi",
                        "type": "Force Haut du corps",
                        "exercises": [
                            {"name": "Développé couché", "sets": "4", "reps": "8-10", "weight": "65kg", "rest": "2min", "progression": "+2.5kg semaine 2"},
                            {"name": "Tractions assistées", "sets": "3", "reps": "6-8", "rest": "2min", "progression": "Moins d'assistance"},
                            {"name": "Dips", "sets": "3", "reps": "10-12", "rest": "90s", "progression": "+1 rep"},
                            {"name": "Rowing haltères", "sets": "4", "reps": "10", "weight": "20kg", "rest": "90s", "progression": "+2kg"},
                        ]
                    },
                    {
                        "day": "Mardi",
                        "type": "Repos actif",
                        "exercises": []
                    },
                    {
                        "day": "Mercredi",
                        "type": "Force Bas du corps",
                        "exercises": [
                            {"name": "Squat", "sets": "4", "reps": "8-10", "weight": "50kg", "rest": "3min", "progression": "+5kg semaine 2"},
                            {"name": "Soulevé de terre", "sets": "3", "reps": "6", "weight": "70kg", "rest": "3min", "progression": "+5kg"},
                            {"name": "Fentes bulgares", "sets": "3", "reps": "12/jambe", "weight": "15kg", "rest": "2min", "progression": "+2kg"},
                            {"name": "Hip thrust", "sets": "3", "reps": "15", "weight": "60kg", "rest": "90s", "progression": "+5kg"},
                        ]
                    },
                    {
                        "day": "Jeudi",
                        "type": "Repos",
                        "exercises": []
                    },
                    {
                        "day": "Vendredi",
                        "type": "Force Complet",
                        "exercises": [
                            {"name": "Développé militaire", "sets": "4", "reps": "8", "weight": "35kg", "rest": "2min", "progression": "+1-2kg"},
                            {"name": "Squat goblet", "sets": "3", "reps": "15", "weight": "20kg", "rest": "90s", "progression": "+2.5kg"},
                            {"name": "Pompes", "sets": "3", "reps": "Maximum", "rest": "90s", "progression": "+2 reps"},
                        ]
                    },
                    {
                        "day": "Weekend",
                        "type": "Repos ou activité libre",
                        "exercises": []
                    }
                ]
            },
            {
                "week_number": 2,
                "focus": "Intensification - Volume maintenu",
                "days": [
                    {
                        "day": "Lundi",
                        "type": "Force Haut du corps",
                        "exercises": [
                            {"name": "Développé couché", "sets": "4", "reps": "6-8", "weight": "67.5kg", "rest": "2min"},
                            {"name": "Tractions", "sets": "3", "reps": "5-7", "rest": "2min"},
                            {"name": "Dips", "sets": "3", "reps": "11-13", "rest": "90s"},
                            {"name": "Rowing haltères", "sets": "4", "reps": "8-10", "weight": "22kg", "rest": "90s"},
                        ]
                    }
                ]
            }
        ],
        "notes": "Programme progressif sur 4 semaines. Échauffement obligatoire de 10min avant chaque séance. Hydratation et récupération prioritaires."
    }

    result = await pdf_service.generate_program_pdf_async(
        program_data,
        str(output_dir / "programme_force_hebdomadaire.pdf"),
        template_variant="weekly"
    )
    print(f"   ✅ Programme PDF généré en {result['generation_time']:.2f}s")
    print(f"   📄 Taille: {result['file_size'] // 1024} KB, {result['pages']} pages")

    # 4. Meal Plan PDF with detailed recipes
    print("\n🍽️ 4. Génération PDF Plan Alimentaire (avec recettes)")
    meal_plan_data = {
        "title": "Plan Alimentaire Semaine - Prise de Masse",
        "client_name": "Antoine Rousseau",
        "week_start_date": "2025-01-20",
        "daily_meals": [
            {
                "day": "Lundi",
                "date": "20/01/2025",
                "meals": [
                    {
                        "type": "Petit-déjeuner",
                        "time": "7h30",
                        "name": "Bowl protéiné complet",
                        "ingredients": ["Avoine 80g", "Protéines vanille 30g", "Banane", "Beurre d'amande 20g", "Myrtilles 50g"],
                        "calories": 520,
                        "macros": {"protein": 30, "carbs": 45, "fat": 18}
                    },
                    {
                        "type": "Collation",
                        "time": "10h30",
                        "name": "Smoothie post-entraînement",
                        "ingredients": ["Lait 250ml", "Banane", "Protéines 25g", "Miel 15g"],
                        "calories": 320,
                        "macros": {"protein": 28, "carbs": 35, "fat": 6}
                    },
                    {
                        "type": "Déjeuner",
                        "time": "13h00",
                        "name": "Poulet grillé quinoa légumes",
                        "ingredients": ["Blanc de poulet 180g", "Quinoa cuit 150g", "Brocolis 200g", "Huile olive 15ml", "Avocat 1/2"],
                        "calories": 680,
                        "macros": {"protein": 50, "carbs": 35, "fat": 22}
                    },
                    {
                        "type": "Collation",
                        "time": "16h30",
                        "name": "Mix énergétique",
                        "ingredients": ["Yaourt grec 150g", "Granola 30g", "Noix 20g"],
                        "calories": 280,
                        "macros": {"protein": 18, "carbs": 20, "fat": 15}
                    },
                    {
                        "type": "Dîner",
                        "time": "19h30",
                        "name": "Saumon patate douce",
                        "ingredients": ["Filet de saumon 150g", "Patate douce 200g", "Épinards 150g", "Huile olive 10ml"],
                        "calories": 520,
                        "macros": {"protein": 35, "carbs": 30, "fat": 20}
                    }
                ]
            },
            {
                "day": "Mardi",
                "date": "21/01/2025",
                "meals": [
                    {
                        "type": "Petit-déjeuner",
                        "time": "7h30",
                        "name": "Œufs brouillés toast avocat",
                        "ingredients": ["Œufs 3", "Pain complet 2 tranches", "Avocat 1", "Beurre 10g"],
                        "calories": 580,
                        "macros": {"protein": 28, "carbs": 35, "fat": 32}
                    }
                ]
            }
        ],
        "shopping_list": [
            {
                "category": "Protéines",
                "items": ["Blanc de poulet 1kg", "Filet de saumon 500g", "Œufs x12", "Yaourt grec nature", "Protéines en poudre vanille"]
            },
            {
                "category": "Glucides",
                "items": ["Avoine 1kg", "Quinoa 500g", "Pain complet", "Patates douces 1kg", "Bananes"]
            },
            {
                "category": "Légumes",
                "items": ["Brocolis", "Épinards frais", "Avocat x3", "Myrtilles 250g"]
            },
            {
                "category": "Matières grasses",
                "items": ["Huile olive vierge", "Beurre d'amande", "Noix mélangées", "Beurre fermier"]
            }
        ],
        "recipes": [
            {
                "name": "Bowl protéiné complet",
                "ingredients": ["80g d'avoine", "30g de protéines vanille", "1 banane", "20g de beurre d'amande", "50g de myrtilles", "250ml de lait d'amande"],
                "instructions": [
                    "Faire cuire l'avoine avec le lait d'amande 5min",
                    "Mélanger les protéines en poudre avec un peu d'eau",
                    "Incorporer les protéines à l'avoine tiède",
                    "Garnir avec la banane, myrtilles et beurre d'amande"
                ],
                "prep_time": 8,
                "servings": 1
            },
            {
                "name": "Poulet grillé quinoa légumes",
                "ingredients": ["180g de blanc de poulet", "150g de quinoa cuit", "200g de brocolis", "15ml d'huile olive", "1/2 avocat", "Herbes de Provence"],
                "instructions": [
                    "Cuire le quinoa selon les instructions (15min)",
                    "Faire griller le poulet avec herbes 6min de chaque côté",
                    "Cuire les brocolis à la vapeur 5min",
                    "Assaisonner avec huile olive et servir avec avocat"
                ],
                "prep_time": 20,
                "servings": 1
            }
        ]
    }

    result = await pdf_service.generate_meal_plan_pdf_async(
        meal_plan_data,
        str(output_dir / "plan_alimentaire_detaille.pdf"),
        template_variant="detailed"
    )
    print(f"   ✅ Plan alimentaire PDF généré en {result['generation_time']:.2f}s")
    print(f"   📄 Taille: {result['file_size'] // 1024} KB, {result['pages']} pages")

    # 5. Progress Report PDF
    print("\n📊 5. Génération PDF Rapport de Progression")
    progress_data = {
        "title": "Rapport de Progression Trimestriel",
        "client_name": "Isabelle Moreau",
        "report_period": "Octobre 2024 - Janvier 2025",
        "start_date": "2024-10-01",
        "end_date": "2025-01-20",
        "summary": {
            "total_sessions": 48,
            "weight_change": -6.2,
            "body_fat_change": -4.8,
            "muscle_gain": 2.1,
            "achievements": [
                "Objectif de poids atteint (-6kg)",
                "Amélioration significative de la force (+25%)",
                "Endurance cardiovasculaire développée",
                "Habitudes alimentaires stabilisées",
                "Confiance en soi retrouvée"
            ]
        },
        "measurements": [
            {
                "date": "2024-10-01",
                "weight": 72.3,
                "body_fat": 32.1,
                "muscle_mass": 22.8,
                "measurements": {
                    "chest": 94,
                    "waist": 82,
                    "hips": 102,
                    "arms": 28,
                    "thighs": 58
                }
            },
            {
                "date": "2024-11-01",
                "weight": 70.1,
                "body_fat": 30.2,
                "muscle_mass": 23.4,
                "measurements": {
                    "chest": 92,
                    "waist": 78,
                    "hips": 99,
                    "arms": 29,
                    "thighs": 57
                }
            },
            {
                "date": "2024-12-01",
                "weight": 68.5,
                "body_fat": 28.8,
                "muscle_mass": 24.2,
                "measurements": {
                    "chest": 91,
                    "waist": 75,
                    "hips": 97,
                    "arms": 29,
                    "thighs": 56
                }
            },
            {
                "date": "2025-01-20",
                "weight": 66.1,
                "body_fat": 27.3,
                "muscle_mass": 24.9,
                "measurements": {
                    "chest": 90,
                    "waist": 72,
                    "hips": 95,
                    "arms": 30,
                    "thighs": 55
                }
            }
        ],
        "performance_data": [
            {
                "exercise": "Développé couché",
                "data_points": [
                    {"date": "2024-10-01", "weight": 40, "reps": 8, "volume": 320},
                    {"date": "2025-01-20", "weight": 50, "reps": 10, "volume": 500}
                ]
            },
            {
                "exercise": "Squat",
                "data_points": [
                    {"date": "2024-10-01", "weight": 50, "reps": 6, "volume": 300},
                    {"date": "2025-01-20", "weight": 65, "reps": 8, "volume": 520}
                ]
            }
        ],
        "goals": [
            {
                "description": "Atteindre 65kg",
                "target_date": "2025-01-31",
                "status": "Atteint",
                "progress_percentage": 100
            },
            {
                "description": "Développé couché 50kg",
                "target_date": "2025-02-15",
                "status": "Atteint",
                "progress_percentage": 100
            },
            {
                "description": "10% de masse grasse",
                "target_date": "2025-06-01",
                "status": "En cours",
                "progress_percentage": 65
            }
        ]
    }

    result = await pdf_service.generate_progress_report_pdf_async(
        progress_data,
        str(output_dir / "rapport_progression_complet.pdf"),
        template_variant="comprehensive"
    )
    print(f"   ✅ Rapport de progression PDF généré en {result['generation_time']:.2f}s")
    print(f"   📄 Taille: {result['file_size'] // 1024} KB, {result['pages']} pages")

    # 6. Batch Generation Demo
    print("\n🚀 6. Génération par Lot (Batch Processing)")
    batch_jobs = [
        {
            "template_type": "session",
            "data": session_data,
            "filename": "session_batch_1",
            "template_config": {"variant": "classic"}
        },
        {
            "template_type": "nutrition",
            "data": nutrition_data,
            "filename": "nutrition_batch_1",
            "template_config": {"variant": "summary"}
        },
        {
            "template_type": "program",
            "data": program_data,
            "filename": "program_batch_1",
            "template_config": {"variant": "compact", "layout": "compact"}
        }
    ]

    batch_results = pdf_service.batch_generate_pdfs(batch_jobs, str(output_dir / "batch"))
    print(f"   ✅ Génération par lot: {batch_results['successful']}/{batch_results['total_jobs']} réussies")

    # 7. Performance Statistics
    print("\n📈 7. Statistiques de Performance")
    stats = pdf_service.get_performance_stats()
    print(f"   📊 Documents générés: {stats['total_documents']}")
    print(f"   ⏱️ Temps total: {stats['total_time']:.2f}s")
    print(f"   🚀 Temps moyen: {stats['average_time']:.2f}s par document")

    if stats.get('cache_stats'):
        cache_stats = stats['cache_stats']
        print(f"   🗄️ Cache: {cache_stats['hits']} hits, {cache_stats['misses']} misses")
        print(f"   📈 Taux de cache: {cache_stats['hit_rate']:.1%}")
        print(f"   💾 Taille cache: {cache_stats['total_size_mb']:.1f} MB")

    # 8. Template Information
    print("\n🏗️ 8. Templates Disponibles")
    available_templates = pdf_service.get_available_templates()
    for template_type, variants in available_templates.items():
        print(f"   📋 {template_type.title()}: {', '.join(variants)}")

    print("\n✨ 9. Thèmes Disponibles")
    themes = pdf_service.get_template_themes()
    for theme_name, colors in themes.items():
        print(f"   🎨 {theme_name.title()}: {colors.get('primary', 'N/A')} (primaire)")

    print("\n" + "=" * 60)
    print("🎉 Démonstration terminée avec succès!")
    print(f"📁 Fichiers générés dans: {output_dir.absolute()}")
    print("\n✨ Fonctionnalités démontrées:")
    print("   • 5 types de templates professionnels")
    print("   • Génération asynchrone haute performance")
    print("   • Templates variants et thèmes personnalisables")
    print("   • Système de cache intelligent")
    print("   • Génération par lot")
    print("   • Statistiques de performance")
    print("   • Architecture modulaire et extensible")


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_advanced_pdf_system())