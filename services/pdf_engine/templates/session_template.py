"""
Session Template - Professional workout session PDF generation
Enhanced version with modern design and flexible layouts
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from .base_template import BaseTemplate


class SessionTemplate(BaseTemplate):
    """
    Professional session template with modern design
    Supports multiple workout formats: AMRAP, EMOM, TABATA, Sets x Reps
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "header": {
                "enabled": True,
                "show_logo": True,
                "show_metadata": True,
                "show_separator": True,
            },
            "footer": {
                "enabled": True,
                "show_branding": True,
                "show_page_numbers": True,
                "text": "Séance générée avec CoachPro - Votre partenaire fitness",
            },
            "colors": {
                "primary": "#FF6B35",
                "secondary": "#F7931E",
                "accent": "#2E86AB",
                "background": "#FFFFFF",
                "surface": "#FFF3CD",
                "text_primary": "#2C3E50",
                "text_secondary": "#7F8C8D",
                "border": "#E8E8E8",
                "success": "#28A745",
                "warning": "#FFC107",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 24},
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "subheading": {"name": "Helvetica-Bold", "size": 14},
                "body": {"name": "Helvetica", "size": 11},
                "caption": {"name": "Helvetica", "size": 9},
            },
            "layout": {
                "margins": {"top": 60, "bottom": 60, "left": 50, "right": 50},
                "block_spacing": 20,
                "exercise_spacing": 8,
            },
            "blocks": {
                "show_icons": True,
                "show_duration": True,
                "show_format": True,
                "formats": {
                    "AMRAP": {"icon": "A", "color": "#DC3545"},
                    "EMOM": {"icon": "E", "color": "#FF6B35"},
                    "TABATA": {"icon": "T", "color": "#E83E8C"},
                    "SETSxREPS": {"icon": "S", "color": "#28A745"},
                    "FOR_TIME": {"icon": "F", "color": "#FFC107"},
                    "LIBRE": {"icon": "L", "color": "#6F42C1"},
                },
            },
        }

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "date": {"type": "string"},
                "duration": {"type": "number"},
                "type": {"type": "string"},
                "blocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "format": {"type": "string"},
                            "duration": {"type": "number"},
                            "exercises": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "reps": {"type": "string"},
                                        "weight": {"type": "string"},
                                        "rest": {"type": "string"},
                                        "notes": {"type": "string"},
                                    },
                                    "required": ["name"],
                                },
                            },
                        },
                        "required": ["title", "format", "exercises"],
                    },
                },
            },
            "required": ["title", "blocks"],
        }

    def _build_content(self) -> List[Any]:
        """Build main session content"""
        elements = []

        # Session info box
        elements.extend(self._build_session_info())
        elements.append(Spacer(1, 0.5 * cm))

        # Workout blocks
        blocks = self.data.get("blocks", [])
        for i, block in enumerate(blocks):
            if self.preview_mode and i >= 2:  # Limit blocks in preview
                break

            elements.extend(self._build_workout_block(block))
            elements.append(Spacer(1, 0.4 * cm))

        # Notes section
        notes = self.data.get("notes")
        if notes and not self.preview_mode:
            elements.extend(self._build_notes_section(notes))

        return elements

    def _build_session_info(self) -> List[Any]:
        """Build session information box"""
        elements = []

        # Create info table data
        info_data = []

        # Session metadata
        duration = self.data.get("duration")
        session_type = self.data.get("type", "Individuel")
        participants = self.data.get("participants")

        row_data = []
        if duration:
            row_data.append(f"T Duree: {duration} min")  # Removed emoji
        if session_type:
            row_data.append(f"Type: {session_type}")  # Removed emoji
        if participants:
            row_data.append(f"Participants: {participants}")  # Removed emoji

        if row_data:
            info_data.append(row_data)

        if info_data:
            # Handle case where configs are strings (theme names)
            colors_config = self.merged_config.get("colors", {})
            fonts_config = self.merged_config.get("fonts", {})

            if isinstance(colors_config, str):
                colors_config = {
                    "surface": "#FFF3CD",
                    "border": "#E8E8E8",
                    "text_primary": "#2C3E50",
                }
            if isinstance(fonts_config, str):
                fonts_config = {"body": {"name": "Helvetica", "size": 11}}

            # Calculate column widths
            col_count = len(info_data[0])
            col_width = 18 * cm / col_count

            info_table = Table(info_data, colWidths=[col_width] * col_count)
            info_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(colors_config.get("surface", "#FFF3CD")),
                        ),
                        (
                            "BORDER",
                            (0, 0),
                            (-1, -1),
                            1,
                            colors.HexColor(colors_config.get("border", "#E8E8E8")),
                        ),
                        ("PADDING", (0, 0), (-1, -1), 12),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            fonts_config.get("body", {}).get("name", "Helvetica"),
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            fonts_config.get("body", {}).get("size", 11),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(
                                colors_config.get("text_primary", "#2C3E50")
                            ),
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ]
                )
            )

            elements.append(info_table)

        return elements

    def _build_workout_block(self, block: Dict[str, Any]) -> List[Any]:
        """Build individual workout block"""
        elements = []

        # Block header
        elements.extend(self._build_block_header(block))

        # Exercises table
        exercises = block.get("exercises", [])
        if exercises:
            elements.append(self._build_exercises_table(block, exercises))

        return elements

    def _build_block_header(self, block: Dict[str, Any]) -> List[Any]:
        """Build block header with title and format info"""
        elements = []

        block_title = block.get("title", "Bloc d'exercices")
        block_format = block.get("format", "LIBRE")
        block_duration = block.get("duration")

        # Handle case where configs are strings (theme names)
        blocks_config = self.merged_config.get("blocks", {})
        colors_config = self.merged_config.get("colors", {})

        if isinstance(blocks_config, str):
            blocks_config = {"formats": {"LIBRE": {"icon": "L", "color": "#6F42C1"}}}
        if isinstance(colors_config, str):
            colors_config = {"primary": "#FF6B35"}

        # Get format styling
        format_config = blocks_config.get("formats", {}).get(block_format, {})
        format_icon = format_config.get("icon", "L")  # Removed emoji
        format_color = format_config.get(
            "color", colors_config.get("primary", "#FF6B35")
        )

        # Build header content
        header_parts = [f"{format_icon} {block_title}"]

        if blocks_config.get("show_format", True):
            header_parts.append(f"Format: {block_format}")

        if block_duration and blocks_config.get("show_duration", True):
            header_parts.append(f"T {block_duration} min")  # Removed emoji

        header_text = " • ".join(header_parts)

        # Handle fonts config
        fonts_config = self.merged_config.get("fonts", {})
        if isinstance(fonts_config, str):
            fonts_config = {"heading": {"name": "Helvetica-Bold", "size": 16}}

        # Create header paragraph
        header_style = f"""
        <font name="{fonts_config.get("heading", {}).get("name", "Helvetica-Bold")}"
              size="{fonts_config.get("heading", {}).get("size", 16)}"
              color="{format_color}">
        <b>{header_text}</b></font>
        """

        header_paragraph = Paragraph(header_style, self.styles["heading"])
        elements.append(header_paragraph)
        elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_exercises_table(
        self, block: Dict[str, Any], exercises: List[Dict[str, Any]]
    ) -> Any:
        """Build exercises table"""
        block_format = block.get("format", "LIBRE")

        # Determine table structure based on format
        if block_format in ["AMRAP", "FOR_TIME"]:
            return self._build_timed_exercises_table(exercises)
        elif block_format == "EMOM":
            return self._build_emom_table(exercises)
        elif block_format == "TABATA":
            return self._build_tabata_table(exercises)
        else:
            return self._build_standard_exercises_table(exercises)

    def _build_standard_exercises_table(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build standard exercises table (Sets x Reps)"""
        # Table headers
        headers = ["Exercice", "Répétitions", "Poids", "Repos"]
        table_data = [headers]

        # Exercise rows
        for exercise in exercises:
            row = [
                exercise.get("name", ""),
                exercise.get("reps", ""),
                exercise.get("weight", ""),
                exercise.get("rest", ""),
            ]
            table_data.append(row)

        # Column widths
        col_widths = [8 * cm, 4 * cm, 3 * cm, 3 * cm]

        return self._create_styled_table(table_data, col_widths)

    def _build_timed_exercises_table(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build exercises table for AMRAP/FOR TIME formats"""
        headers = ["Exercice", "Répétitions"]
        table_data = [headers]

        for exercise in exercises:
            row = [
                exercise.get("name", ""),
                exercise.get("reps", ""),
            ]
            table_data.append(row)

        col_widths = [12 * cm, 6 * cm]
        return self._create_styled_table(table_data, col_widths)

    def _build_emom_table(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build EMOM format table"""
        headers = ["Minute", "Exercice", "Répétitions"]
        table_data = [headers]

        for i, exercise in enumerate(exercises, 1):
            row = [
                f"Min {i}",
                exercise.get("name", ""),
                exercise.get("reps", ""),
            ]
            table_data.append(row)

        col_widths = [3 * cm, 9 * cm, 6 * cm]
        return self._create_styled_table(table_data, col_widths)

    def _build_tabata_table(self, exercises: List[Dict[str, Any]]) -> Any:
        """Build TABATA format table"""
        headers = ["Exercice", "Travail: 20s", "Repos: 10s"]
        table_data = [headers]

        for exercise in exercises:
            row = [
                exercise.get("name", ""),
                "20 secondes",
                "10 secondes",
            ]
            table_data.append(row)

        col_widths = [10 * cm, 4 * cm, 4 * cm]
        return self._create_styled_table(table_data, col_widths)

    def _create_styled_table(
        self, data: List[List[str]], col_widths: List[float]
    ) -> Any:
        """Create professionally styled table"""
        table = Table(data, colWidths=col_widths, repeatRows=1)

        # Handle case where configs are strings (theme names)
        colors_config = self.merged_config.get("colors", {})
        fonts_config = self.merged_config.get("fonts", {})

        if isinstance(colors_config, str):
            colors_config = {
                "primary": "#FF6B35",
                "text_primary": "#2C3E50",
                "surface": "#FFF3CD",
                "border": "#E8E8E8",
            }
        if isinstance(fonts_config, str):
            fonts_config = {
                "subheading": {"name": "Helvetica-Bold", "size": 14},
                "body": {"name": "Helvetica", "size": 11},
            }

        # Table styling
        style = TableStyle(
            [
                # Header styling
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(colors_config.get("primary", "#FF6B35")),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    fonts_config.get("subheading", {}).get("name", "Helvetica-Bold"),
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    fonts_config.get("subheading", {}).get("size", 14),
                ),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                # Body styling
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    fonts_config.get("body", {}).get("name", "Helvetica"),
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    fonts_config.get("body", {}).get("size", 11),
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor(colors_config.get("text_primary", "#2C3E50")),
                ),
                # Alternating row colors
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(colors_config.get("surface", "#FFF3CD")),
                    ],
                ),
                # Grid and padding
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor(colors_config.get("border", "#E8E8E8")),
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )

        table.setStyle(style)
        return table

    def _build_notes_section(self, notes: str) -> List[Any]:
        """Build notes section"""
        elements = []

        # Handle case where configs are strings (theme names)
        colors_config = self.merged_config.get("colors", {})
        fonts_config = self.merged_config.get("fonts", {})

        if isinstance(colors_config, str):
            colors_config = {"text_primary": "#2C3E50"}
        if isinstance(fonts_config, str):
            fonts_config = {
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "body": {"name": "Helvetica", "size": 11},
            }

        # Notes header
        notes_header = Paragraph(
            f'<font name="{fonts_config.get("heading", {}).get("name", "Helvetica-Bold")}" '
            f'size="{fonts_config.get("heading", {}).get("size", 16)}" '
            f'color="{colors_config.get("text_primary", "#2C3E50")}"><b>N Notes</b></font>',  # Removed emoji
            self.styles["heading"],
        )
        elements.append(notes_header)
        elements.append(Spacer(1, 0.3 * cm))

        # Notes content
        notes_content = Paragraph(
            f'<font name="{fonts_config.get("body", {}).get("name", "Helvetica")}" '
            f'size="{fonts_config.get("body", {}).get("size", 11)}" '
            f'color="{colors_config.get("text_primary", "#2C3E50")}">{notes}</font>',
            self.styles["body"],
        )
        elements.append(notes_content)

        return elements
