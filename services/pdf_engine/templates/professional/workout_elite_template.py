"""
Elite Performance Workout Template - Simplified working version
Premium minimalist design for high-end coaching with working PDF generation
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from ..base_template import BaseTemplate


class WorkoutEliteTemplate(BaseTemplate):
    """
    Elite Performance Workout Template - Simplified Version
    Premium minimalist design focused on data and performance
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Elite colors
        self.colors = {
            "primary": colors.Color(0.1, 0.3, 0.5),
            "secondary": colors.Color(0.6, 0.6, 0.6),
            "accent": colors.Color(0.2, 0.6, 0.8),
        }

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration for Elite template"""
        return {
            "page_size": "A4",
            "margins": {
                "top": 25*mm,
                "bottom": 25*mm,
                "left": 25*mm,
                "right": 25*mm
            },
            "show_header": False,
            "show_footer": False
        }

    def _to_paragraph(self, text: str, style_name: str = "Body") -> Paragraph:
        """Convert string to Paragraph for table cells"""
        if not text:
            text = ""
        style = ParagraphStyle(
            style_name,
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        return Paragraph(str(text), style)

    def _build_content(self) -> List[Any]:
        """Build elite workout content with premium layout"""
        elements = []

        # Title
        title_style = ParagraphStyle(
            'EliteTitle',
            fontSize=24,
            textColor=self.colors["primary"],
            alignment=TA_CENTER,
            spaceAfter=10
        )

        title = self.data.get('title', 'Programme Elite')
        elements.append(Paragraph(f"<b>⭐ {title} ⭐</b>", title_style))
        elements.append(Spacer(1, 15*mm))

        # Client information table
        client_table = self._build_client_info()
        elements.append(client_table)
        elements.append(Spacer(1, 15*mm))

        # Exercises section
        if self.data.get('exercises'):
            exercises_section = self._build_exercises_section()
            elements.extend(exercises_section)

        return elements

    def _build_client_info(self) -> Table:
        """Build client information table"""
        client_name = self.data.get('client_name', 'Client')
        coach_name = self.data.get('coach_name', 'Coach')
        session_date = self.data.get('session_date', 'Date')
        duration = self.data.get('session_duration', '60 min')

        info_data = [
            [self._to_paragraph("<b>INFORMATIONS CLIENT</b>", "Header"), self._to_paragraph("", "Body")],
            [self._to_paragraph("Client:", "Body"), self._to_paragraph(client_name, "Body")],
            [self._to_paragraph("Coach:", "Body"), self._to_paragraph(coach_name, "Body")],
            [self._to_paragraph("Date:", "Body"), self._to_paragraph(session_date, "Body")],
            [self._to_paragraph("Durée:", "Body"), self._to_paragraph(duration, "Body")]
        ]

        info_table = Table(info_data, colWidths=[4*cm, 8*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return info_table

    def _build_exercises_section(self) -> List[Any]:
        """Build exercises section"""
        elements = []

        # Section title
        exercise_title = ParagraphStyle(
            'ExerciseTitle',
            fontSize=18,
            textColor=self.colors["primary"],
            alignment=TA_LEFT,
            spaceAfter=8
        )
        elements.append(Paragraph("<b>💪 PROGRAMME D'EXERCICES</b>", exercise_title))
        elements.append(Spacer(1, 10*mm))

        # Exercise table
        exercises = self.data.get('exercises', [])
        if exercises:
            exercise_table = self._build_exercise_table(exercises)
            elements.append(exercise_table)

        return elements

    def _build_exercise_table(self, exercises: List[Dict[str, Any]]) -> Table:
        """Build exercise table"""
        exercise_data = [
            [
                self._to_paragraph("<b>Exercice</b>", "Header"),
                self._to_paragraph("<b>Séries</b>", "Header"),
                self._to_paragraph("<b>Reps</b>", "Header"),
                self._to_paragraph("<b>Repos</b>", "Header"),
                self._to_paragraph("<b>Notes</b>", "Header")
            ]
        ]

        for i, exercise in enumerate(exercises):
            name = exercise.get('name', f'Exercice {i+1}')
            sets = str(exercise.get('sets', '-'))
            reps = str(exercise.get('reps', '-'))
            rest = str(exercise.get('rest', '-'))
            notes = exercise.get('notes', '')

            exercise_data.append([
                self._to_paragraph(f"{i+1}. {name}", "Body"),
                self._to_paragraph(sets, "Body"),
                self._to_paragraph(reps, "Body"),
                self._to_paragraph(rest, "Body"),
                self._to_paragraph(notes, "Body")
            ])

        exercise_table = Table(exercise_data, colWidths=[5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3*cm])
        exercise_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["accent"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (3, -1), 'CENTER'),  # Center align numbers
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        return exercise_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information"""
        return {
            "name": "Elite Performance (Simple)",
            "category": "workout_programs",
            "description": "Premium minimalist design for high-end coaching",
            "target_audience": "High-end coaches, advanced athletes",
            "features": [
                "Clean professional layout",
                "Client information summary",
                "Structured exercise program",
                "Performance-focused design"
            ],
            "complexity": "Simple",
            "page_count": "1-2 pages"
        }