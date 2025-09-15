"""
Nutrition Template - Professional nutrition assessment and planning PDF
Enhanced version with macro visualization and personalized recommendations
"""

from __future__ import annotations

import io
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

from .base_template import BaseTemplate


class NutritionTemplate(BaseTemplate):
    """
    Professional nutrition template with macro visualization
    Supports detailed nutrition assessments and meal planning
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "header": {
                "enabled": True,
                "show_logo": True,
                "show_metadata": True,
            },
            "footer": {
                "enabled": True,
                "show_branding": True,
                "show_page_numbers": True,
                "text": "Plan nutritionnel générée avec CoachPro",
            },
            "colors": {
                "primary": "#2E86AB",
                "secondary": "#A23B72",
                "accent": "#F18F01",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#2C3E50",
                "text_secondary": "#6C757D",
                "border": "#DEE2E6",
                "success": "#28A745",
                "warning": "#FFC107",
                "protein": "#3C91E6",
                "carbs": "#FFAD05",
                "fat": "#E4572E",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 22},
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "subheading": {"name": "Helvetica-Bold", "size": 13},
                "body": {"name": "Helvetica", "size": 11},
                "caption": {"name": "Helvetica", "size": 9},
            },
            "show_macro_chart": True,
            "show_recommendations": True,
            "show_meal_timeline": True,
        }

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string"},
                "title": {"type": "string"},
                "date": {"type": "string"},
                "personal_info": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "number"},
                        "weight": {"type": "number"},
                        "height": {"type": "number"},
                        "gender": {"type": "string"},
                        "activity_level": {"type": "string"},
                        "goal": {"type": "string"},
                    },
                },
                "nutrition_data": {
                    "type": "object",
                    "properties": {
                        "maintenance_calories": {"type": "number"},
                        "target_calories": {"type": "number"},
                        "protein_g": {"type": "number"},
                        "carbs_g": {"type": "number"},
                        "fat_g": {"type": "number"},
                    },
                    "required": ["maintenance_calories", "target_calories"],
                },
                "meal_plan": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "meal": {"type": "string"},
                            "time": {"type": "string"},
                            "foods": {"type": "array"},
                            "calories": {"type": "number"},
                        },
                    },
                },
                "recommendations": {"type": "array"},
            },
            "required": ["client_name", "title", "nutrition_data"],
        }

    def _build_content(self) -> List[Any]:
        """Build nutrition assessment content"""
        elements = []

        # Personal information section
        elements.extend(self._build_personal_info())
        elements.append(Spacer(1, 0.5 * cm))

        # Nutrition targets section
        elements.extend(self._build_nutrition_targets())
        elements.append(Spacer(1, 0.5 * cm))

        # Macro breakdown with chart
        if self.merged_config.get("show_macro_chart", True):
            elements.extend(self._build_macro_breakdown())
            elements.append(Spacer(1, 0.5 * cm))

        # Meal plan section
        meal_plan = self.data.get("meal_plan", [])
        if meal_plan and not self.preview_mode:
            elements.extend(self._build_meal_plan(meal_plan))
            elements.append(Spacer(1, 0.5 * cm))

        # Recommendations section
        if self.merged_config.get("show_recommendations", True):
            elements.extend(self._build_recommendations())

        return elements

    def _build_personal_info(self) -> List[Any]:
        """Build personal information section"""
        elements = []
        personal_info = self.data.get("personal_info", {})

        if not personal_info:
            return elements

        # Section header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>👤 Informations personnelles</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Create info table
        info_data = []

        # First row
        row1 = []
        age = personal_info.get("age")
        if age:
            row1.append(f"Âge: {age} ans")

        weight = personal_info.get("weight")
        if weight:
            row1.append(f"Poids: {weight} kg")

        height = personal_info.get("height")
        if height:
            row1.append(f"Taille: {height} cm")

        if row1:
            info_data.append(row1)

        # Second row
        row2 = []
        gender = personal_info.get("gender")
        if gender:
            row2.append(f"Sexe: {gender}")

        activity_level = personal_info.get("activity_level")
        if activity_level:
            row2.append(f"Niveau d'activité: {activity_level}")

        goal = personal_info.get("goal")
        if goal:
            row2.append(f"Objectif: {goal}")

        if row2:
            info_data.append(row2)

        if info_data:
            # Calculate column widths
            max_cols = max(len(row) for row in info_data)
            col_width = 18 * cm / max_cols

            # Fill shorter rows
            for row in info_data:
                while len(row) < max_cols:
                    row.append("")

            info_table = Table(info_data, colWidths=[col_width] * max_cols)
            info_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(self.merged_config["colors"]["surface"]),
                        ),
                        (
                            "BORDER",
                            (0, 0),
                            (-1, -1),
                            1,
                            colors.HexColor(self.merged_config["colors"]["border"]),
                        ),
                        ("PADDING", (0, 0), (-1, -1), 10),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            self.merged_config["fonts"]["body"]["name"],
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            self.merged_config["fonts"]["body"]["size"],
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(
                                self.merged_config["colors"]["text_primary"]
                            ),
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )

            elements.append(info_table)

        return elements

    def _build_nutrition_targets(self) -> List[Any]:
        """Build nutrition targets section"""
        elements = []
        nutrition_data = self.data.get("nutrition_data", {})

        # Section header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🎯 Objectifs nutritionnels</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Calories section
        maintenance_cal = nutrition_data.get("maintenance_calories", 0)
        target_cal = nutrition_data.get("target_calories", 0)

        calories_data = [
            ["Type", "Calories", "Différence"],
            ["Maintenance", f"{maintenance_cal} kcal", "—"],
            [
                "Objectif",
                f"{target_cal} kcal",
                f"{target_cal - maintenance_cal:+d} kcal",
            ],
        ]

        calories_table = Table(calories_data, colWidths=[6 * cm, 6 * cm, 6 * cm])
        calories_table.setStyle(self._get_standard_table_style())

        elements.append(calories_table)
        elements.append(Spacer(1, 0.3 * cm))

        # Calculate estimated monthly change
        if maintenance_cal and target_cal:
            delta_cal = target_cal - maintenance_cal
            estimated_change = round((delta_cal * 30) / 7700, 1)  # 1kg ≈ 7700 kcal
            sign = "+" if estimated_change > 0 else ""

            estimation_text = (
                f"📊 <b>Estimation mensuelle:</b> {sign}{estimated_change} kg"
            )
            estimation_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{estimation_text}</font>',
                self.styles["body"],
            )
            elements.append(estimation_paragraph)

        return elements

    def _build_macro_breakdown(self) -> List[Any]:
        """Build macronutrient breakdown with visualization"""
        elements = []
        nutrition_data = self.data.get("nutrition_data", {})

        protein_g = nutrition_data.get("protein_g", 0)
        carbs_g = nutrition_data.get("carbs_g", 0)
        fat_g = nutrition_data.get("fat_g", 0)

        if not any([protein_g, carbs_g, fat_g]):
            return elements

        # Section header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🥗 Répartition des macronutriments</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Calculate calories from macros
        protein_cal = protein_g * 4
        carbs_cal = carbs_g * 4
        fat_cal = fat_g * 9
        total_cal = protein_cal + carbs_cal + fat_cal

        # Macro table
        macro_data = [
            ["Macronutriment", "Grammes", "Calories", "Pourcentage"],
            [
                "🔵 Protéines",
                f"{protein_g} g",
                f"{protein_cal} kcal",
                f"{(protein_cal / total_cal) * 100:.0f}%" if total_cal > 0 else "0%",
            ],
            [
                "🟡 Glucides",
                f"{carbs_g} g",
                f"{carbs_cal} kcal",
                f"{(carbs_cal / total_cal) * 100:.0f}%" if total_cal > 0 else "0%",
            ],
            [
                "🔴 Lipides",
                f"{fat_g} g",
                f"{fat_cal} kcal",
                f"{(fat_cal / total_cal) * 100:.0f}%" if total_cal > 0 else "0%",
            ],
        ]

        macro_table = Table(
            macro_data, colWidths=[4.5 * cm, 4.5 * cm, 4.5 * cm, 4.5 * cm]
        )

        # Custom styling for macro table
        macro_style = TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(self.merged_config["colors"]["primary"]),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["size"],
                ),
                # Protein row
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E3F2FD")),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, 1),
                    colors.HexColor(self.merged_config["colors"]["protein"]),
                ),
                # Carbs row
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#FFF8E1")),
                (
                    "TEXTCOLOR",
                    (0, 2),
                    (-1, 2),
                    colors.HexColor(self.merged_config["colors"]["carbs"]),
                ),
                # Fat row
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FFEBEE")),
                (
                    "TEXTCOLOR",
                    (0, 3),
                    (-1, 3),
                    colors.HexColor(self.merged_config["colors"]["fat"]),
                ),
                # General styling
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["size"],
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor(self.merged_config["colors"]["border"]),
                ),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )

        macro_table.setStyle(macro_style)
        elements.append(macro_table)

        # Add macro chart if enabled
        if total_cal > 0:
            elements.append(Spacer(1, 0.3 * cm))
            chart = self._create_macro_chart(protein_cal, carbs_cal, fat_cal)
            if chart:
                elements.append(chart)

        return elements

    def _create_macro_chart(
        self, protein_cal: float, carbs_cal: float, fat_cal: float
    ) -> Any:
        """Create macro distribution pie chart"""
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_agg import FigureCanvasAgg

            matplotlib.use("Agg")

            # Create figure
            fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
            fig.patch.set_facecolor("white")

            # Data for pie chart
            sizes = [protein_cal, carbs_cal, fat_cal]
            labels = ["Protéines", "Glucides", "Lipides"]
            colors_chart = [
                self.merged_config["colors"]["protein"],
                self.merged_config["colors"]["carbs"],
                self.merged_config["colors"]["fat"],
            ]

            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                colors=colors_chart,
                autopct="%1.0f%%",
                startangle=90,
                wedgeprops={"linewidth": 2, "edgecolor": "white"},
            )

            # Styling
            for text in texts:
                text.set_fontsize(10)
                text.set_fontweight("bold")

            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(10)
                autotext.set_fontweight("bold")

            ax.set_title(
                "Répartition des macronutriments",
                fontsize=12,
                fontweight="bold",
                pad=20,
            )

            # Save to bytes
            canvas = FigureCanvasAgg(fig)
            buffer = io.BytesIO()
            canvas.print_png(buffer)
            buffer.seek(0)

            plt.close(fig)

            # Create ReportLab Image
            chart_image = Image(buffer, width=6 * cm, height=6 * cm)
            return chart_image

        except ImportError:
            # Matplotlib not available - create simple text representation
            total = protein_cal + carbs_cal + fat_cal
            if total > 0:
                prot_pct = (protein_cal / total) * 100
                carbs_pct = (carbs_cal / total) * 100
                fat_pct = (fat_cal / total) * 100

                chart_text = f"""
                🔵 Protéines: {prot_pct:.0f}%
                🟡 Glucides: {carbs_pct:.0f}%
                🔴 Lipides: {fat_pct:.0f}%
                """

                chart_paragraph = Paragraph(
                    f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                    f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                    f'color="{self.merged_config["colors"]["text_primary"]}">{chart_text}</font>',
                    self.styles["body"],
                )
                return chart_paragraph
            return None
        except Exception:
            # Return None if chart creation fails
            return None

    def _build_meal_plan(self, meal_plan: List[Dict[str, Any]]) -> List[Any]:
        """Build meal plan section"""
        elements = []

        # Section header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🍽️ Plan alimentaire</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Build meal table
        meal_data = [["Repas", "Horaire", "Aliments", "Calories"]]

        for meal in meal_plan:
            meal_name = meal.get("meal", "")
            meal_time = meal.get("time", "")
            foods = meal.get("foods", [])
            calories = meal.get("calories", "")

            # Format foods list
            foods_text = ", ".join(foods) if isinstance(foods, list) else str(foods)
            if len(foods_text) > 40:  # Truncate long lists
                foods_text = foods_text[:37] + "..."

            calories_text = f"{calories} kcal" if calories else ""

            meal_data.append([meal_name, meal_time, foods_text, calories_text])

        meal_table = Table(meal_data, colWidths=[3 * cm, 3 * cm, 9 * cm, 3 * cm])
        meal_table.setStyle(self._get_standard_table_style())

        elements.append(meal_table)
        return elements

    def _build_recommendations(self) -> List[Any]:
        """Build personalized recommendations section"""
        elements = []

        recommendations = self.data.get("recommendations", [])

        # Generate default recommendations if none provided
        if not recommendations:
            recommendations = self._generate_default_recommendations()

        if not recommendations:
            return elements

        # Section header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>💡 Recommandations personnalisées</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Create recommendations box
        rec_text = []
        for i, rec in enumerate(recommendations, 1):
            rec_text.append(f"• {rec}")

        rec_content = "<br/>".join(rec_text)

        rec_paragraph = Paragraph(
            f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
            f'size="{self.merged_config["fonts"]["body"]["size"]}" '
            f'color="{self.merged_config["colors"]["text_primary"]}">{rec_content}</font>',
            self.styles["body"],
        )

        # Create background box
        rec_data = [[rec_paragraph]]
        rec_table = Table(rec_data, colWidths=[18 * cm])
        rec_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    (
                        "BORDER",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.HexColor(self.merged_config["colors"]["border"]),
                    ),
                    ("PADDING", (0, 0), (-1, -1), 15),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        elements.append(rec_table)
        return elements

    def _generate_default_recommendations(self) -> List[str]:
        """Generate default recommendations based on client data"""
        recommendations = []
        personal_info = self.data.get("personal_info", {})
        self.data.get("nutrition_data", {})

        # General recommendations
        recommendations.extend(
            [
                "Boire au moins 2-3 litres d'eau par jour",
                "Répartir les repas sur 3-4 prises principales",
                "Privilégier les aliments non transformés",
                "Manger lentement et dans le calme",
            ]
        )

        # Goal-specific recommendations
        goal = personal_info.get("goal", "").lower()
        if "perte" in goal or "minceur" in goal:
            recommendations.extend(
                [
                    "Augmenter la consommation de légumes pour la satiété",
                    "Privilégier les protéines maigres à chaque repas",
                    "Limiter les collations sucrées en soirée",
                ]
            )
        elif "prise" in goal or "masse" in goal:
            recommendations.extend(
                [
                    "Ajouter des collations riches en protéines",
                    "Inclure des glucides complexes autour de l'entraînement",
                    "Ne pas sauter de repas",
                ]
            )

        # Activity-specific recommendations
        activity = personal_info.get("activity_level", "").lower()
        if "élevé" in activity or "intense" in activity:
            recommendations.append(
                "Ajuster l'hydratation selon l'intensité d'entraînement"
            )

        return recommendations

    def _get_standard_table_style(self) -> TableStyle:
        """Get standard table styling"""
        return TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(self.merged_config["colors"]["primary"]),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["size"],
                ),
                # Body
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["size"],
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor(self.merged_config["colors"]["text_primary"]),
                ),
                # Alternating backgrounds
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(self.merged_config["colors"]["surface"]),
                    ],
                ),
                # General styling
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor(self.merged_config["colors"]["border"]),
                ),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
