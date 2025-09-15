"""
Nutrition Wellness Template - Lifestyle photography and inspirational design
Wellness-focused nutrition planning with visual emphasis
Target: Coaching wellness, perte de poids, grand public
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import Spacer, Table, TableStyle

from ...components.professional_components import (
    MacronutrientWheelComponent,
)
from ..base_template import BaseTemplate


class NutritionWellnessTemplate(BaseTemplate):
    """
    Nutrition Wellness Template - Lifestyle focused with visual emphasis
    Instagram-style grid layout with HD photography and wellness tips
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "lifestyle_photography",
            "layout": "instagram_grid",
            "visual_emphasis": "photography",
            "wellness_focus": True,
            "colors": {
                "primary": "#744210",
                "secondary": "#9c7346",
                "accent": "#68d391",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text_primary": "#2d3748",
                "text_secondary": "#4a5568",
                "success": "#38a169",
                "warning": "#d69e2e",
                "wellness": "#68d391",
                "lifestyle": "#9c7346",
            },
            "fonts": {
                "title": {"name": "Georgia-Bold", "size": 24},
                "subtitle": {"name": "Georgia-Bold", "size": 18},
                "heading": {"name": "Georgia-Bold", "size": 15},
                "body": {"name": "Georgia", "size": 11},
                "caption": {"name": "Georgia-Italic", "size": 9},
                "lifestyle": {"name": "Georgia-Italic", "size": 12},
            },
            "layout": {
                "margins": {"top": 50, "bottom": 50, "left": 40, "right": 40},
                "header_height": 100,
                "footer_height": 40,
                "block_spacing": 20,
                "grid_style": True,
            },
            "wellness": {
                "show_lifestyle_tips": True,
                "show_meal_prep": True,
                "show_shopping_guide": True,
                "show_wellness_quotes": True,
                "photo_emphasis": True,
            },
        }

    def _build_content(self) -> List[Any]:
        """Build wellness nutrition content with lifestyle photography style"""
        elements = []

        # Lifestyle header with wellness branding
        elements.append(self._build_lifestyle_header())
        elements.append(Spacer(1, 15))

        # Wellness journey overview
        elements.append(self._build_wellness_journey())
        elements.append(Spacer(1, 20))

        # Instagram-style nutrition grid
        elements.append(self._build_nutrition_grid())
        elements.append(Spacer(1, 15))

        # Meal prep planning section
        elements.append(self._build_meal_prep_section())
        elements.append(Spacer(1, 20))

        # Lifestyle tips and habits
        elements.append(self._build_lifestyle_tips())
        elements.append(Spacer(1, 15))

        # Shopping guide with seasonal focus
        elements.append(self._build_shopping_guide())
        elements.append(Spacer(1, 15))

        # Wellness quotes and motivation
        elements.append(self._build_wellness_inspiration())

        return elements

    def _build_lifestyle_header(self) -> Table:
        """Build lifestyle-focused header with wellness branding"""
        client_name = self.data.get("client_name", "Client")
        plan_title = self.data.get("plan_title", "Plan Wellness Lifestyle")
        wellness_goal = self.data.get("wellness_goal", "Équilibre et bien-être")

        header_data = [
            [f"🌿 {plan_title.upper()} 🌿"],
            [f"Parcours Wellness de {client_name}"],
            [f"🎯 Objectif: {wellness_goal}"],
            ["✨ Nourrir son corps, cultiver son bien-être ✨"],
        ]

        header_table = Table(header_data, colWidths=[6 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    # Main title
                    ("FONTNAME", (0, 0), (0, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (0, 0), 22),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#f0f9ff")),
                    # Client name
                    ("FONTNAME", (0, 1), (0, 1), "Georgia-Bold"),
                    ("FONTSIZE", (0, 1), (0, 1), 16),
                    (
                        "TEXTCOLOR",
                        (0, 1),
                        (0, 1),
                        HexColor(self.merged_config["colors"]["text_primary"]),
                    ),
                    # Goal
                    ("FONTNAME", (0, 2), (0, 2), "Georgia"),
                    ("FONTSIZE", (0, 2), (0, 2), 14),
                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (0, 2),
                        HexColor(self.merged_config["colors"]["wellness"]),
                    ),
                    # Inspiration
                    ("FONTNAME", (0, 3), (0, 3), "Georgia-Italic"),
                    ("FONTSIZE", (0, 3), (0, 3), 12),
                    (
                        "TEXTCOLOR",
                        (0, 3),
                        (0, 3),
                        HexColor(self.merged_config["colors"]["lifestyle"]),
                    ),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        2,
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        return header_table

    def _build_wellness_journey(self) -> Table:
        """Build wellness journey overview with progress tracking"""
        journey_data = self.data.get("wellness_journey", {})

        journey_info = [
            ["🌱 VOTRE PARCOURS WELLNESS", "", ""],
            ["Aspect", "Situation Actuelle", "Objectif"],
            [
                "💪 Énergie",
                journey_data.get("current_energy", "Variable"),
                journey_data.get("target_energy", "Stable et élevée"),
            ],
            [
                "😴 Sommeil",
                journey_data.get("current_sleep", "6-7h"),
                journey_data.get("target_sleep", "7-8h réparateur"),
            ],
            [
                "🧘 Stress",
                journey_data.get("current_stress", "Modéré"),
                journey_data.get("target_stress", "Gestion optimale"),
            ],
            [
                "⚖️ Poids",
                journey_data.get("current_weight", "N/A"),
                journey_data.get("target_weight", "Équilibre naturel"),
            ],
            [
                "💝 Relation nourriture",
                journey_data.get("current_relationship", "Perfectible"),
                journey_data.get("target_relationship", "Intuitive et sereine"),
            ],
        ]

        journey_table = Table(journey_info, colWidths=[2 * inch, 2 * inch, 2 * inch])
        journey_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["wellness"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Georgia-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#f0fff4")),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["wellness"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return journey_table

    def _build_nutrition_grid(self) -> Table:
        """Build Instagram-style nutrition information grid"""
        nutrition_data = self.data.get("nutrition_overview", {})

        # Macronutrient wheel
        protein_g = nutrition_data.get("protein_g", 100)
        carbs_g = nutrition_data.get("carbs_g", 150)
        fat_g = nutrition_data.get("fat_g", 60)
        macro_wheel = MacronutrientWheelComponent(
            protein_g, carbs_g, fat_g, width=120, height=120
        )

        # Key nutrition metrics
        metrics_data = [
            ["📊 VOS BESOINS NUTRITION"],
            [f"🔥 Calories: {nutrition_data.get('target_calories', 1800)} kcal"],
            [f"💧 Hydratation: {nutrition_data.get('water_target', 2.5)}L"],
            [f"🌾 Fibres: {nutrition_data.get('fiber_target', 25)}g"],
            [f"🥗 Portions légumes: {nutrition_data.get('veggie_portions', 5)}"],
            [f"🍎 Portions fruits: {nutrition_data.get('fruit_portions', 3)}"],
        ]

        # Wellness habits
        habits_data = [
            ["🌟 HABITUDES WELLNESS"],
            ["🌅 Petit-déjeuner équilibré"],
            ["🍽️ Repas mindful (sans écrans)"],
            ["🥤 Eau citronnée au réveil"],
            ["🌙 Dîner 3h avant coucher"],
            ["🧘 5min méditation/repas"],
        ]

        # Layout grid
        grid_layout = [[macro_wheel, metrics_data, habits_data]]

        grid_table = Table(grid_layout, colWidths=[2 * inch, 2 * inch, 2 * inch])
        grid_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f8fffe")),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["wellness"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 15),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
                ]
            )
        )

        return grid_table

    def _build_meal_prep_section(self) -> Table:
        """Build meal prep planning with visual guide"""
        meal_prep = self.data.get("meal_prep_guide", {})

        prep_data = [
            ["🍱 GUIDE MEAL PREP WELLNESS", "", ""],
            ["Jour", "Préparation", "Tips Lifestyle"],
            [
                "Dimanche",
                meal_prep.get("sunday_prep", "Batch cooking légumes, céréales"),
                "🎵 Musique relaxante pendant la prep",
            ],
            [
                "Lundi",
                meal_prep.get("monday_prep", "Assemblage bowls petit-déjeuner"),
                "☀️ Réveil en douceur avec routine",
            ],
            [
                "Mercredi",
                meal_prep.get("wednesday_prep", "Préparation collations saines"),
                "🌿 Intégrer des herbes fraîches",
            ],
            [
                "Vendredi",
                meal_prep.get("friday_prep", "Planning weekend gourmand"),
                "🎉 Se faire plaisir consciemment",
            ],
        ]

        prep_table = Table(prep_data, colWidths=[1.5 * inch, 2.5 * inch, 2 * inch])
        prep_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["lifestyle"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Georgia-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#fef7ed")),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["lifestyle"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return prep_table

    def _build_lifestyle_tips(self) -> Table:
        """Build lifestyle tips and wellness habits"""
        tips = self.data.get(
            "lifestyle_tips",
            [
                "🌅 Commencer la journée par 5 minutes de gratitude",
                "🌊 Boire un verre d'eau avant chaque repas",
                "🍃 Intégrer 10 min de marche après le déjeuner",
                "🧘 Pratiquer la respiration consciente avant de manger",
                "🌙 Créer un rituel du soir apaisant",
                "📱 Déconnecter 1h avant le coucher",
                "🎨 Cultiver une activité créative relaxante",
                "🤝 Partager un repas en conscience chaque semaine",
            ],
        )

        tips_data = [["🌟 LIFESTYLE TIPS POUR VOTRE BIEN-ÊTRE"]]

        # Organiser les tips en 2 colonnes
        for i in range(0, len(tips), 2):
            row = [tips[i]]
            if i + 1 < len(tips):
                row.append(tips[i + 1])
            else:
                row.append("")
            tips_data.append(row)

        tips_table = Table(tips_data, colWidths=[3 * inch, 3 * inch])
        tips_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Tips content
                    ("FONTNAME", (0, 1), (-1, -1), "Georgia"),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 1), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f0fff4")),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return tips_table

    def _build_shopping_guide(self) -> Table:
        """Build seasonal shopping guide"""
        shopping_data = self.data.get("shopping_guide", {})

        shopping_categories = [
            ["🛒 GUIDE SHOPPING WELLNESS SAISONNIER", "", ""],
            ["Catégorie", "Aliments Privilégiés", "Astuce Wellness"],
            [
                "🥬 Légumes de saison",
                shopping_data.get("seasonal_veggies", "Épinards, courges, choux"),
                "🌱 Choisir bio quand possible",
            ],
            [
                "🍎 Fruits frais",
                shopping_data.get("seasonal_fruits", "Pommes, poires, agrumes"),
                "🍯 Privilégier les saveurs naturelles",
            ],
            [
                "🌾 Céréales complètes",
                shopping_data.get("whole_grains", "Quinoa, avoine, riz complet"),
                "💪 Source d'énergie durable",
            ],
            [
                "🥜 Protéines végétales",
                shopping_data.get("plant_proteins", "Légumineuses, noix, graines"),
                "🌍 Impact environnemental réduit",
            ],
            [
                "🐟 Protéines animales",
                shopping_data.get("animal_proteins", "Poissons gras, œufs bio"),
                "⭐ Qualité plutôt que quantité",
            ],
            [
                "🧈 Bons gras",
                shopping_data.get("healthy_fats", "Huile olive, avocat, oléagineux"),
                "💡 Essentiels pour l'absorption vitamines",
            ],
        ]

        shopping_table = Table(
            shopping_categories, colWidths=[1.8 * inch, 2.2 * inch, 2 * inch]
        )
        shopping_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 13),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Georgia-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#fef7ed")),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return shopping_table

    def _build_wellness_inspiration(self) -> Table:
        """Build wellness quotes and inspiration section"""
        wellness_quotes = self.data.get(
            "wellness_quotes",
            [
                "💫 « Votre corps est votre temple. Gardez-le pur et propre pour que l'âme y habite. »",
                "🌱 « Chaque petit pas vers une alimentation consciente est une victoire. »",
                "✨ « La santé n'est pas tout, mais sans la santé, tout n'est rien. »",
                "🌈 « Nourrissez votre corps avec gratitude et bienveillance. »",
            ],
        )

        inspiration_data = [
            ["💖 INSPIRATION WELLNESS"],
            [wellness_quotes[0] if len(wellness_quotes) > 0 else ""],
            [wellness_quotes[1] if len(wellness_quotes) > 1 else ""],
            [wellness_quotes[2] if len(wellness_quotes) > 2 else ""],
            [wellness_quotes[3] if len(wellness_quotes) > 3 else ""],
            ["🌟 Célébrez chaque jour votre engagement envers votre bien-être ! 🌟"],
        ]

        inspiration_table = Table(inspiration_data, colWidths=[6 * inch])
        inspiration_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("FONTNAME", (0, 0), (0, 0), "Georgia-Bold"),
                    ("FONTSIZE", (0, 0), (0, 0), 16),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Quotes
                    ("FONTNAME", (0, 1), (-1, -2), "Georgia-Italic"),
                    ("FONTSIZE", (0, 1), (-1, -2), 11),
                    (
                        "TEXTCOLOR",
                        (0, 1),
                        (-1, -2),
                        HexColor(self.merged_config["colors"]["text_primary"]),
                    ),
                    # Final message
                    ("FONTNAME", (0, -1), (0, -1), "Georgia-Bold"),
                    ("FONTSIZE", (0, -1), (0, -1), 12),
                    (
                        "TEXTCOLOR",
                        (0, -1),
                        (0, -1),
                        HexColor(self.merged_config["colors"]["wellness"]),
                    ),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f0fff4")),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return inspiration_table

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Nutrition Wellness template data requirements"""
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string"},
                "plan_title": {"type": "string"},
                "wellness_goal": {"type": "string"},
                "wellness_journey": {
                    "type": "object",
                    "properties": {
                        "current_energy": {"type": "string"},
                        "target_energy": {"type": "string"},
                        "current_sleep": {"type": "string"},
                        "target_sleep": {"type": "string"},
                        "current_stress": {"type": "string"},
                        "target_stress": {"type": "string"},
                        "current_weight": {"type": "string"},
                        "target_weight": {"type": "string"},
                        "current_relationship": {"type": "string"},
                        "target_relationship": {"type": "string"},
                    },
                },
                "nutrition_overview": {
                    "type": "object",
                    "properties": {
                        "target_calories": {"type": "integer"},
                        "protein_g": {"type": "integer"},
                        "carbs_g": {"type": "integer"},
                        "fat_g": {"type": "integer"},
                        "water_target": {"type": "number"},
                        "fiber_target": {"type": "integer"},
                        "veggie_portions": {"type": "integer"},
                        "fruit_portions": {"type": "integer"},
                    },
                },
                "meal_prep_guide": {
                    "type": "object",
                    "properties": {
                        "sunday_prep": {"type": "string"},
                        "monday_prep": {"type": "string"},
                        "wednesday_prep": {"type": "string"},
                        "friday_prep": {"type": "string"},
                    },
                },
                "lifestyle_tips": {"type": "array", "items": {"type": "string"}},
                "shopping_guide": {
                    "type": "object",
                    "properties": {
                        "seasonal_veggies": {"type": "string"},
                        "seasonal_fruits": {"type": "string"},
                        "whole_grains": {"type": "string"},
                        "plant_proteins": {"type": "string"},
                        "animal_proteins": {"type": "string"},
                        "healthy_fats": {"type": "string"},
                    },
                },
                "wellness_quotes": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["client_name"],
        }
