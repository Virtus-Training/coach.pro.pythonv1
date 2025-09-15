"""
Program Template - Professional training program PDF generation
Multi-week program layouts with progression tracking
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

from .base_template import BaseTemplate


class ProgramTemplate(BaseTemplate):
    """
    Professional program template for multi-week training programs
    Supports weekly/daily layouts with progression visualization
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
                "text": "Programme d'entraînement généré avec CoachPro",
            },
            "colors": {
                "primary": "#6F42C1",
                "secondary": "#E83E8C",
                "accent": "#20C997",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#212529",
                "text_secondary": "#6C757D",
                "border": "#DEE2E6",
                "week_bg": "#F1F3F4",
                "day_bg": "#FFFFFF",
                "progression_up": "#28A745",
                "progression_down": "#DC3545",
                "progression_maintain": "#FFC107",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 24},
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "subheading": {"name": "Helvetica-Bold", "size": 13},
                "body": {"name": "Helvetica", "size": 10},
                "caption": {"name": "Helvetica", "size": 8},
            },
            "layout": "weekly",  # weekly, daily, compact
            "show_progression": True,
            "show_rest_days": True,
            "page_break_per_week": False,
        }

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "duration_weeks": {"type": "number"},
                "goal": {"type": "string"},
                "weeks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "week_number": {"type": "number"},
                            "focus": {"type": "string"},
                            "days": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "day": {"type": "string"},
                                        "type": {"type": "string"},
                                        "exercises": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "sets": {"type": "string"},
                                                    "reps": {"type": "string"},
                                                    "weight": {"type": "string"},
                                                    "rest": {"type": "string"},
                                                    "progression": {"type": "string"},
                                                },
                                                "required": ["name"]
                                            }
                                        }
                                    },
                                    "required": ["day", "type"]
                                }
                            }
                        },
                        "required": ["week_number", "days"]
                    }
                }
            },
            "required": ["title", "weeks"]
        }

    def _build_content(self) -> List[Any]:
        """Build program content"""
        elements = []

        # Program overview
        elements.extend(self._build_program_overview())
        elements.append(Spacer(1, 0.5 * cm))

        # Weekly breakdown
        weeks = self.data.get("weeks", [])
        layout = self.merged_config.get("layout", "weekly")

        for i, week in enumerate(weeks):
            if self.preview_mode and i >= 2:  # Limit weeks in preview
                break

            if layout == "weekly":
                elements.extend(self._build_weekly_layout(week))
            elif layout == "daily":
                elements.extend(self._build_daily_layout(week))
            else:  # compact
                elements.extend(self._build_compact_layout(week))

            # Page break between weeks if configured
            if (self.merged_config.get("page_break_per_week", False) and
                i < len(weeks) - 1 and not self.preview_mode):
                elements.append(PageBreak())
            else:
                elements.append(Spacer(1, 0.6 * cm))

        # Program notes
        notes = self.data.get("notes")
        if notes and not self.preview_mode:
            elements.extend(self._build_notes_section(notes))

        return elements

    def _build_program_overview(self) -> List[Any]:
        """Build program overview section"""
        elements = []

        # Overview header
        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📋 Vue d\'ensemble du programme</b></font>',
            self.styles["heading"]
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Program details
        overview_data = []

        duration = self.data.get("duration_weeks")
        if duration:
            overview_data.append(f"⏱️ Durée: {duration} semaines")

        goal = self.data.get("goal")
        if goal:
            overview_data.append(f"🎯 Objectif: {goal}")

        frequency = self._calculate_weekly_frequency()
        if frequency:
            overview_data.append(f"📅 Fréquence: {frequency} séances/semaine")

        if overview_data:
            overview_text = " • ".join(overview_data)
            overview_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{overview_text}</font>',
                self.styles["body"]
            )

            # Create background box
            overview_table_data = [[overview_paragraph]]
            overview_table = Table(overview_table_data, colWidths=[18 * cm])
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.merged_config["colors"]["surface"])),
                ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor(self.merged_config["colors"]["border"])),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(overview_table)

        return elements

    def _build_weekly_layout(self, week: Dict[str, Any]) -> List[Any]:
        """Build weekly layout format"""
        elements = []

        week_number = week.get("week_number", 1)
        focus = week.get("focus", "")

        # Week header
        week_title = f"Semaine {week_number}"
        if focus:
            week_title += f" - {focus}"

        week_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>{week_title}</b></font>',
            self.styles["heading"]
        )
        elements.append(week_header)
        elements.append(Spacer(1, 0.3 * cm))

        # Days in this week
        days = week.get("days", [])
        for day in days:
            elements.extend(self._build_day_section(day))
            elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_daily_layout(self, week: Dict[str, Any]) -> List[Any]:
        """Build daily layout format (more detailed)"""
        elements = []

        week_number = week.get("week_number", 1)
        focus = week.get("focus", "")

        # Week header
        week_title = f"📅 Semaine {week_number}"
        if focus:
            week_title += f" - Focus: {focus}"

        week_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>{week_title}</b></font>',
            self.styles["heading"]
        )
        elements.append(week_header)
        elements.append(Spacer(1, 0.4 * cm))

        # Build detailed day cards
        days = week.get("days", [])
        for day in days:
            elements.extend(self._build_detailed_day_card(day))
            elements.append(Spacer(1, 0.4 * cm))

        return elements

    def _build_compact_layout(self, week: Dict[str, Any]) -> List[Any]:
        """Build compact layout format (table format)"""
        elements = []

        week_number = week.get("week_number", 1)
        focus = week.get("focus", "")

        # Week header
        week_title = f"Semaine {week_number}"
        if focus:
            week_title += f" ({focus})"

        week_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>{week_title}</b></font>',
            self.styles["heading"]
        )
        elements.append(week_header)
        elements.append(Spacer(1, 0.2 * cm))

        # Build compact table
        table_data = [["Jour", "Type", "Exercices Principaux"]]

        days = week.get("days", [])
        for day in days:
            day_name = day.get("day", "")
            day_type = day.get("type", "")

            # Get main exercises (first 3)
            exercises = day.get("exercises", [])
            main_exercises = [ex.get("name", "") for ex in exercises[:3]]
            exercises_text = ", ".join(main_exercises)
            if len(exercises) > 3:
                exercises_text += f" +{len(exercises) - 3} autres"

            table_data.append([day_name, day_type, exercises_text])

        compact_table = Table(table_data, colWidths=[3 * cm, 4 * cm, 11 * cm])
        compact_table.setStyle(self._get_compact_table_style())

        elements.append(compact_table)
        return elements

    def _build_day_section(self, day: Dict[str, Any]) -> List[Any]:
        """Build individual day section"""
        elements = []

        day_name = day.get("day", "")
        day_type = day.get("type", "")
        exercises = day.get("exercises", [])

        # Day header
        day_header_text = f"🗓️ {day_name}"
        if day_type:
            day_header_text += f" - {day_type}"

        day_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
            f'color="{self.merged_config["colors"]["text_primary"]}"><b>{day_header_text}</b></font>',
            self.styles["heading"]
        )
        elements.append(day_header)

        # Rest day handling
        if day_type.lower() in ["repos", "rest"] and self.merged_config.get("show_rest_days", True):
            rest_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_secondary"]}"><i>🛌 Jour de repos - Récupération active recommandée</i></font>',
                self.styles["body"]
            )
            elements.append(rest_paragraph)
            return elements

        # Exercises table
        if exercises:
            elements.append(Spacer(1, 0.2 * cm))
            exercises_table = self._build_exercises_table(exercises)
            elements.append(exercises_table)

        return elements

    def _build_detailed_day_card(self, day: Dict[str, Any]) -> List[Any]:
        """Build detailed day card for daily layout"""
        elements = []

        day_name = day.get("day", "")
        day_type = day.get("type", "")
        exercises = day.get("exercises", [])

        # Day card container
        card_data = []

        # Day header row
        day_title = f"🗓️ {day_name} - {day_type}" if day_type else f"🗓️ {day_name}"
        header_paragraph = Paragraph(
            f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
            f'color="white"><b>{day_title}</b></font>',
            self.styles["heading"]
        )
        card_data.append([header_paragraph])

        # Exercises content
        if exercises:
            exercises_content = self._build_day_exercises_content(exercises)
            card_data.append([exercises_content])

        # Create card table
        card_table = Table(card_data, colWidths=[18 * cm])
        card_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.merged_config["colors"]["primary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('PADDING', (0, 0), (-1, 0), 12),

            # Content styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.merged_config["colors"]["day_bg"])),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor(self.merged_config["colors"]["border"])),
            ('PADDING', (0, 1), (-1, -1), 15),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(card_table)
        return elements

    def _build_day_exercises_content(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build exercises content for day card"""
        content_parts = []

        for i, exercise in enumerate(exercises, 1):
            name = exercise.get("name", "")
            sets = exercise.get("sets", "")
            reps = exercise.get("reps", "")
            weight = exercise.get("weight", "")
            rest = exercise.get("rest", "")
            progression = exercise.get("progression", "")

            # Format exercise line
            exercise_line = f"{i}. <b>{name}</b>"

            details = []
            if sets:
                details.append(f"{sets} séries")
            if reps:
                details.append(f"{reps} rép")
            if weight:
                details.append(f"{weight}")
            if rest:
                details.append(f"repos {rest}")

            if details:
                exercise_line += f" • {' • '.join(details)}"

            if progression and self.merged_config.get("show_progression", True):
                prog_color = self._get_progression_color(progression)
                exercise_line += f' <font color="{prog_color}">({progression})</font>'

            content_parts.append(exercise_line)

        content_text = "<br/>".join(content_parts)

        return Paragraph(
            f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
            f'size="{self.merged_config["fonts"]["body"]["size"]}" '
            f'color="{self.merged_config["colors"]["text_primary"]}">{content_text}</font>',
            self.styles["body"]
        )

    def _build_exercises_table(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build exercises table"""
        # Table headers
        headers = ["Exercice", "Séries", "Répétitions", "Poids", "Repos"]
        if self.merged_config.get("show_progression", True):
            headers.append("Progression")

        table_data = [headers]

        # Exercise rows
        for exercise in exercises:
            row = [
                exercise.get("name", ""),
                exercise.get("sets", ""),
                exercise.get("reps", ""),
                exercise.get("weight", ""),
                exercise.get("rest", ""),
            ]

            if self.merged_config.get("show_progression", True):
                progression = exercise.get("progression", "")
                row.append(progression)

            table_data.append(row)

        # Column widths
        if self.merged_config.get("show_progression", True):
            col_widths = [6 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2 * cm]
        else:
            col_widths = [7 * cm, 3 * cm, 3 * cm, 3 * cm, 2 * cm]

        return self._create_styled_table(table_data, col_widths)

    def _create_styled_table(self, data: List[List[str]], col_widths: List[float]) -> Any:
        """Create professionally styled table"""
        table = Table(data, colWidths=col_widths, repeatRows=1)

        style = TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.merged_config["colors"]["primary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["name"]),
            ('FONTSIZE', (0, 0), (-1, 0), self.merged_config["fonts"]["subheading"]["size"]),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Body styling
            ('FONTNAME', (0, 1), (-1, -1), self.merged_config["fonts"]["body"]["name"]),
            ('FONTSIZE', (0, 1), (-1, -1), self.merged_config["fonts"]["body"]["size"]),
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

        table.setStyle(style)
        return table

    def _get_compact_table_style(self) -> TableStyle:
        """Get styling for compact table"""
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

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(self.merged_config["colors"]["border"])),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

    def _build_notes_section(self, notes: str) -> List[Any]:
        """Build notes section"""
        elements = []

        notes_header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📝 Notes du programme</b></font>',
            self.styles["heading"]
        )
        elements.append(notes_header)
        elements.append(Spacer(1, 0.3 * cm))

        notes_content = Paragraph(
            f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
            f'size="{self.merged_config["fonts"]["body"]["size"]}" '
            f'color="{self.merged_config["colors"]["text_primary"]}">{notes}</font>',
            self.styles["body"]
        )
        elements.append(notes_content)

        return elements

    def _calculate_weekly_frequency(self) -> str:
        """Calculate average weekly training frequency"""
        weeks = self.data.get("weeks", [])
        if not weeks:
            return ""

        total_sessions = 0
        week_count = len(weeks)

        for week in weeks:
            days = week.get("days", [])
            sessions = sum(1 for day in days if day.get("type", "").lower() not in ["repos", "rest"])
            total_sessions += sessions

        if week_count > 0:
            avg_frequency = total_sessions / week_count
            return f"{avg_frequency:.1f}"

        return ""

    def _get_progression_color(self, progression: str) -> str:
        """Get color for progression indicator"""
        progression_lower = progression.lower()

        if any(word in progression_lower for word in ["+", "augment", "plus", "lourd"]):
            return self.merged_config["colors"]["progression_up"]
        elif any(word in progression_lower for word in ["-", "diminue", "moins", "léger"]):
            return self.merged_config["colors"]["progression_down"]
        else:
            return self.merged_config["colors"]["progression_maintain"]