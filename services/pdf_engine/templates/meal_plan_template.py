"""
Meal Plan Template - Professional meal planning PDF generation
Weekly meal schedules with shopping lists and recipes
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

from .base_template import BaseTemplate


class MealPlanTemplate(BaseTemplate):
    """
    Professional meal plan template with weekly schedules
    Supports detailed meal plans, recipes, and shopping lists
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
                "text": "Plan alimentaire généré avec CoachPro",
            },
            "colors": {
                "primary": "#28A745",
                "secondary": "#20C997",
                "accent": "#FD7E14",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#212529",
                "text_secondary": "#6C757D",
                "border": "#DEE2E6",
                "breakfast": "#FF6B35",
                "lunch": "#2E86AB",
                "dinner": "#7C3AED",
                "snack": "#10B981",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 22},
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "subheading": {"name": "Helvetica-Bold", "size": 13},
                "body": {"name": "Helvetica", "size": 10},
                "caption": {"name": "Helvetica", "size": 8},
            },
            "show_recipes": True,
            "show_shopping_list": True,
            "show_nutrition_summary": True,
            "layout": "detailed",  # detailed, overview, compact
        }

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "week_start_date": {"type": "string"},
                "daily_meals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "string"},
                            "date": {"type": "string"},
                            "meals": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "time": {"type": "string"},
                                        "name": {"type": "string"},
                                        "ingredients": {"type": "array"},
                                        "calories": {"type": "number"},
                                        "macros": {
                                            "type": "object",
                                            "properties": {
                                                "protein": {"type": "number"},
                                                "carbs": {"type": "number"},
                                                "fat": {"type": "number"}
                                            }
                                        }
                                    },
                                    "required": ["type", "name"]
                                }
                            }
                        },
                        "required": ["day", "meals"]
                    }
                },
                "shopping_list": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "items": {"type": "array"}
                        }
                    }
                },
                "recipes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "ingredients": {"type": "array"},
                            "instructions": {"type": "array"},
                            "prep_time": {"type": "number"},
                            "servings": {"type": "number"}
                        }
                    }
                }
            },
            "required": ["title", "daily_meals"]
        }

    def _build_content(self) -> List[Any]:
        """Build meal plan content"""
        elements = []

        # Weekly overview
        elements.extend(self._build_weekly_overview())
        elements.append(Spacer(1, 0.5 * cm))

        # Daily meal plans
        daily_meals = self.data.get("daily_meals", [])
        layout = self.merged_config.get("layout", "detailed")

        for i, day_plan in enumerate(daily_meals):
            if self.preview_mode and i >= 3:
                break

            if layout == "detailed":
                elements.extend(self._build_detailed_day_plan(day_plan))
            else:
                elements.extend(self._build_compact_day_plan(day_plan))

            elements.append(Spacer(1, 0.4 * cm))

        # Shopping list
        if (self.merged_config.get("show_shopping_list", True) and
            not self.preview_mode):
            elements.extend(self._build_shopping_list())
            elements.append(PageBreak())

        # Recipes
        if (self.merged_config.get("show_recipes", True) and
            not self.preview_mode):
            elements.extend(self._build_recipes_section())

        return elements

    def _build_weekly_overview(self) -> List[Any]:
        """Build weekly meal plan overview"""
        elements = []

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🗓️ Aperçu de la semaine</b></font>',
            self.styles["heading"]
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Week summary table
        summary_data = [["Jour", "Petit-déj", "Déjeuner", "Dîner", "Collations"]]

        daily_meals = self.data.get("daily_meals", [])
        for day_plan in daily_meals:
            day_name = day_plan.get("day", "")
            meals = day_plan.get("meals", [])

            # Group meals by type
            meal_types = {"breakfast": "", "lunch": "", "dinner": "", "snack": ""}

            for meal in meals:
                meal_type = meal.get("type", "").lower()
                meal_name = meal.get("name", "")

                if meal_type in ["petit-déjeuner", "breakfast"]:
                    meal_types["breakfast"] = meal_name
                elif meal_type in ["déjeuner", "lunch"]:
                    meal_types["lunch"] = meal_name
                elif meal_type in ["dîner", "dinner"]:
                    meal_types["dinner"] = meal_name
                elif meal_type in ["collation", "snack"]:
                    if meal_types["snack"]:
                        meal_types["snack"] += f", {meal_name}"
                    else:
                        meal_types["snack"] = meal_name

            summary_data.append([
                day_name,
                meal_types["breakfast"][:20] + ("..." if len(meal_types["breakfast"]) > 20 else ""),
                meal_types["lunch"][:20] + ("..." if len(meal_types["lunch"]) > 20 else ""),
                meal_types["dinner"][:20] + ("..." if len(meal_types["dinner"]) > 20 else ""),
                meal_types["snack"][:20] + ("..." if len(meal_types["snack"]) > 20 else ""),
            ])

        summary_table = Table(summary_data, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 4.5*cm])
        summary_table.setStyle(self._get_overview_table_style())

        elements.append(summary_table)
        return elements

    def _build_detailed_day_plan(self, day_plan: Dict[str, Any]) -> List[Any]:
        """Build detailed day meal plan"""
        elements = []

        day_name = day_plan.get("day", "")
        day_date = day_plan.get("date", "")
        meals = day_plan.get("meals", [])

        # Day header
        day_title = day_name
        if day_date:
            day_title += f" - {day_date}"

        day_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📅 {day_title}</b></font>',
            self.styles["heading"]
        )
        elements.append(day_header)
        elements.append(Spacer(1, 0.3 * cm))

        # Meals for this day
        for meal in meals:
            elements.extend(self._build_meal_card(meal))
            elements.append(Spacer(1, 0.2 * cm))

        return elements

    def _build_compact_day_plan(self, day_plan: Dict[str, Any]) -> List[Any]:
        """Build compact day meal plan"""
        elements = []

        day_name = day_plan.get("day", "")
        meals = day_plan.get("meals", [])

        # Compact table for the day
        day_data = [[f"📅 {day_name}", "Repas", "Calories"]]

        daily_calories = 0
        for meal in meals:
            meal_type = meal.get("type", "")
            meal_name = meal.get("name", "")
            calories = meal.get("calories", 0)
            daily_calories += calories

            day_data.append(["", f"{meal_type}: {meal_name}", f"{calories} kcal"])

        # Add total row
        day_data.append(["", "Total journée", f"{daily_calories} kcal"])

        day_table = Table(day_data, colWidths=[4*cm, 10*cm, 4*cm])
        day_table.setStyle(self._get_compact_day_style())

        elements.append(day_table)
        return elements

    def _build_meal_card(self, meal: Dict[str, Any]) -> List[Any]:
        """Build individual meal card"""
        elements = []

        meal_type = meal.get("type", "")
        meal_time = meal.get("time", "")
        meal_name = meal.get("name", "")
        ingredients = meal.get("ingredients", [])
        calories = meal.get("calories", 0)
        macros = meal.get("macros", {})

        # Get meal color
        meal_color = self._get_meal_color(meal_type)

        # Meal header
        meal_title = f"{self._get_meal_icon(meal_type)} {meal_type}"
        if meal_time:
            meal_title += f" ({meal_time})"

        meal_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
            f'size="{self.merged_config["fonts"]["body"]["size"]}" '
            f'color="white"><b>{meal_title}</b></font>',
            self.styles["body"]
        )

        # Meal content
        content_parts = [f"<b>{meal_name}</b>"]

        if ingredients:
            ingredients_text = ", ".join(ingredients) if isinstance(ingredients, list) else str(ingredients)
            content_parts.append(f"Ingrédients: {ingredients_text}")

        if calories:
            content_parts.append(f"Calories: {calories} kcal")

        if macros:
            macro_parts = []
            if macros.get("protein"):
                macro_parts.append(f"P: {macros['protein']}g")
            if macros.get("carbs"):
                macro_parts.append(f"G: {macros['carbs']}g")
            if macros.get("fat"):
                macro_parts.append(f"L: {macros['fat']}g")

            if macro_parts:
                content_parts.append(f"Macros: {' | '.join(macro_parts)}")

        meal_content = Paragraph(
            f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
            f'size="{self.merged_config["fonts"]["body"]["size"]}" '
            f'color="{self.merged_config["colors"]["text_primary"]}">{"<br/>".join(content_parts)}</font>',
            self.styles["body"]
        )

        # Create meal card
        card_data = [[meal_header], [meal_content]]
        card_table = Table(card_data, colWidths=[18*cm])
        card_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(meal_color)),
            ('PADDING', (0, 0), (-1, 0), 8),

            # Content
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor(self.merged_config["colors"]["border"])),
            ('PADDING', (0, 1), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(card_table)
        return elements

    def _build_shopping_list(self) -> List[Any]:
        """Build shopping list section"""
        elements = []
        shopping_list = self.data.get("shopping_list", [])

        if not shopping_list:
            return elements

        # Shopping list header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🛒 Liste de courses</b></font>',
            self.styles["heading"]
        )
        elements.append(header)
        elements.append(Spacer(1, 0.4 * cm))

        # Group items by category
        for category_data in shopping_list:
            category = category_data.get("category", "")
            items = category_data.get("items", [])

            if not items:
                continue

            # Category header
            category_header = Paragraph(
                f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
                f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}"><b>{category}</b></font>',
                self.styles["heading"]
            )
            elements.append(category_header)
            elements.append(Spacer(1, 0.2 * cm))

            # Items list
            items_text = []
            for item in items:
                items_text.append(f"☐ {item}")

            items_content = "<br/>".join(items_text)
            items_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{items_content}</font>',
                self.styles["body"]
            )

            elements.append(items_paragraph)
            elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_recipes_section(self) -> List[Any]:
        """Build recipes section"""
        elements = []
        recipes = self.data.get("recipes", [])

        if not recipes:
            return elements

        # Recipes header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>👨‍🍳 Recettes</b></font>',
            self.styles["heading"]
        )
        elements.append(header)
        elements.append(Spacer(1, 0.4 * cm))

        # Individual recipes
        for recipe in recipes:
            elements.extend(self._build_recipe_card(recipe))
            elements.append(Spacer(1, 0.4 * cm))

        return elements

    def _build_recipe_card(self, recipe: Dict[str, Any]) -> List[Any]:
        """Build individual recipe card"""
        elements = []

        recipe_name = recipe.get("name", "")
        ingredients = recipe.get("ingredients", [])
        instructions = recipe.get("instructions", [])
        prep_time = recipe.get("prep_time")
        servings = recipe.get("servings")

        # Recipe header
        recipe_header_text = f"🍳 {recipe_name}"
        if prep_time:
            recipe_header_text += f" ({prep_time} min)"
        if servings:
            recipe_header_text += f" - {servings} portions"

        recipe_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>{recipe_header_text}</b></font>',
            self.styles["heading"]
        )
        elements.append(recipe_header)
        elements.append(Spacer(1, 0.2 * cm))

        # Ingredients
        if ingredients:
            ingredients_header = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}"><b>Ingrédients:</b></font>',
                self.styles["body"]
            )
            elements.append(ingredients_header)

            ingredients_text = []
            for ingredient in ingredients:
                ingredients_text.append(f"• {ingredient}")

            ingredients_content = "<br/>".join(ingredients_text)
            ingredients_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{ingredients_content}</font>',
                self.styles["body"]
            )
            elements.append(ingredients_paragraph)
            elements.append(Spacer(1, 0.2 * cm))

        # Instructions
        if instructions:
            instructions_header = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}"><b>Préparation:</b></font>',
                self.styles["body"]
            )
            elements.append(instructions_header)

            instructions_text = []
            for i, instruction in enumerate(instructions, 1):
                instructions_text.append(f"{i}. {instruction}")

            instructions_content = "<br/>".join(instructions_text)
            instructions_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{instructions_content}</font>',
                self.styles["body"]
            )
            elements.append(instructions_paragraph)

        return elements

    def _get_meal_color(self, meal_type: str) -> str:
        """Get color for meal type"""
        meal_type_lower = meal_type.lower()

        if "petit-déj" in meal_type_lower or "breakfast" in meal_type_lower:
            return self.merged_config["colors"]["breakfast"]
        elif "déjeuner" in meal_type_lower or "lunch" in meal_type_lower:
            return self.merged_config["colors"]["lunch"]
        elif "dîner" in meal_type_lower or "dinner" in meal_type_lower:
            return self.merged_config["colors"]["dinner"]
        elif "collation" in meal_type_lower or "snack" in meal_type_lower:
            return self.merged_config["colors"]["snack"]
        else:
            return self.merged_config["colors"]["primary"]

    def _get_meal_icon(self, meal_type: str) -> str:
        """Get icon for meal type"""
        meal_type_lower = meal_type.lower()

        if "petit-déj" in meal_type_lower or "breakfast" in meal_type_lower:
            return "🌅"
        elif "déjeuner" in meal_type_lower or "lunch" in meal_type_lower:
            return "🌞"
        elif "dîner" in meal_type_lower or "dinner" in meal_type_lower:
            return "🌙"
        elif "collation" in meal_type_lower or "snack" in meal_type_lower:
            return "🍎"
        else:
            return "🍽️"

    def _get_overview_table_style(self) -> TableStyle:
        """Get styling for overview table"""
        return TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.merged_config["colors"]["primary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["name"]),
            ('FONTSIZE', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["size"]),

            # Body
            ('FONTNAME', (0, 1), (-1, -1), self.merged_config["fonts"]["caption"]["name"]),
            ('FONTSIZE', (0, 1), (-1, -1), self.merged_config["fonts"]["caption"]["size"]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor(self.merged_config["colors"]["text_primary"])),

            # Alternating backgrounds
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, colors.HexColor(self.merged_config["colors"]["surface"])]),

            # Grid and padding
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.merged_config["colors"]["border"])),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

    def _get_compact_day_style(self) -> TableStyle:
        """Get styling for compact day table"""
        return TableStyle([
            # First row (day header)
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.merged_config["colors"]["surface"])),
            ('FONTNAME', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["name"]),
            ('FONTSIZE', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["size"]),
            ('SPAN', (0, 0), (2, 0)),  # Span day name across columns

            # Body rows
            ('FONTNAME', (0, 1), (-1, -2), self.merged_config["fonts"]["body"]["name"]),
            ('FONTSIZE', (0, 1), (-1, -2), self.merged_config["fonts"]["body"]["size"]),

            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor(self.merged_config["colors"]["primary"])),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('FONTNAME', (0, -1), (-1, -1), self.merged_config["fonts"]["subheading"]["name"]),

            # Grid and padding
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.merged_config["colors"]["border"])),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])