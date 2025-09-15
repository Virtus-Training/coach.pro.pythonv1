"""
Elite Performance Workout Template - Premium minimalist design
Rivals high-end coaching platforms like Trainerize Pro
Target: Coaches haut de gamme, athlètes avancés
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from ...components.professional_components import (
    AnatomyZoneComponent,
    DataVisualizationComponent,
    PremiumHeaderComponent,
    ProgressBarComponent,
    QRCodeComponent,
    WorkoutBlockComponent,
)
from ..base_template import BaseTemplate


class WorkoutEliteTemplate(BaseTemplate):
    """
    Elite Performance Template - Premium minimalist with advanced data visualization
    Designed to impress clients paying 200€/h+ for coaching
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "elite_professional",
            "layout": "grid_structured",
            "show_progress_graphs": True,
            "show_anatomy_zones": True,
            "show_qr_codes": True,
            "data_density": "high",
            "branding": "premium_minimal",
            "colors": {
                "primary": "#1a365d",
                "secondary": "#2d3748",
                "accent": "#3182ce",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text_primary": "#1a202c",
                "text_secondary": "#4a5568",
                "success": "#38a169",
                "warning": "#d69e2e",
                "chart": "#3182ce",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 24},
                "subtitle": {"name": "Helvetica-Bold", "size": 18},
                "heading": {"name": "Helvetica-Bold", "size": 14},
                "body": {"name": "Helvetica", "size": 10},
                "caption": {"name": "Helvetica", "size": 8},
            },
            "layout": {
                "margins": {"top": 50, "bottom": 50, "left": 40, "right": 40},
                "header_height": 100,
                "footer_height": 40,
                "block_spacing": 25,
                "grid_columns": 2,
            },
            "components": {
                "progress_visualization": True,
                "anatomy_highlighting": True,
                "performance_metrics": True,
                "video_integration": True,
            },
        }

    def _to_paragraph(self, text: str, style_name: str = "Body") -> Paragraph:
        """Convert string to Paragraph for table cells"""
        if not text:
            text = ""
        style = ParagraphStyle(
            style_name, fontSize=10, textColor=colors.black, alignment=TA_LEFT
        )
        return Paragraph(str(text), style)

    def _build_content(self) -> List[Any]:
        """Build elite workout content with premium layout and data visualization"""
        elements = []

        # Premium header with branding
        elements.append(self._build_premium_header())
        elements.append(Spacer(1, 20))

        # Executive summary with key metrics
        elements.append(self._build_executive_summary())
        elements.append(Spacer(1, 15))

        # Performance analytics dashboard
        if self.merged_config.get("show_progress_graphs", True):
            elements.append(self._build_performance_dashboard())
            elements.append(Spacer(1, 20))

        # Anatomy zone targeting
        if self.merged_config.get("show_anatomy_zones", True):
            elements.append(self._build_anatomy_section())
            elements.append(Spacer(1, 20))

        # Workout blocks with premium styling
        elements.extend(self._build_elite_workout_blocks())

        # Performance tracking section
        elements.append(self._build_tracking_section())

        # QR codes for video integration
        if self.merged_config.get("show_qr_codes", True):
            elements.append(self._build_video_integration())

        return elements

    def _build_premium_header(self) -> PremiumHeaderComponent:
        """Build luxury header with professional branding"""
        title = self.data.get("title", "Programme d'Entraînement Elite")
        client_name = self.data.get("client_name", "Client")
        subtitle = f"Programme personnalisé - {client_name}"

        return PremiumHeaderComponent(
            title=title,
            subtitle=subtitle,
            logo_path=self.merged_config.get("logo_path", ""),
            width=500,
            height=100,
        )

    def _build_executive_summary(self) -> Table:
        """Build executive summary with key metrics"""
        program_data = self.data.get("program_overview", {})

        summary_data = [
            [
                self._to_paragraph("RÉSUMÉ EXÉCUTIF", "Header"),
                self._to_paragraph("", "Body"),
                self._to_paragraph("", "Body"),
            ],
            [
                self._to_paragraph("Objectif Principal", "Body"),
                self._to_paragraph(
                    program_data.get("primary_goal", "Performance"), "Body"
                ),
                self._to_paragraph("", "Body"),
            ],
            [
                self._to_paragraph("Durée Programme", "Body"),
                self._to_paragraph(
                    f"{program_data.get('duration_weeks', 12)} semaines", "Body"
                ),
                self._to_paragraph("", "Body"),
            ],
            [
                self._to_paragraph("Fréquence", "Body"),
                self._to_paragraph(
                    f"{program_data.get('sessions_per_week', 4)} séances/semaine",
                    "Body",
                ),
                self._to_paragraph("", "Body"),
            ],
            [
                self._to_paragraph("Niveau Intensité", "Body"),
                self._to_paragraph(
                    program_data.get("intensity_level", "Élevé"), "Body"
                ),
                self._to_paragraph("", "Body"),
            ],
            [
                self._to_paragraph("Focus Anatomique", "Body"),
                self._to_paragraph(
                    ", ".join(program_data.get("target_areas", ["Corps complet"])),
                    "Body",
                ),
                self._to_paragraph("", "Body"),
            ],
        ]

        table = Table(summary_data, colWidths=[3 * inch, 2 * inch, 1 * inch])
        table.setStyle(
            TableStyle(
                [
                    # Header row
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("SPAN", (0, 0), (-1, 0)),
                    # Content rows
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f8fafc")),
                ]
            )
        )

        return table

    def _build_performance_dashboard(self) -> Table:
        """Build performance analytics dashboard"""
        performance_data = self.data.get("performance_metrics", {})

        # Create dashboard with multiple visualizations

        # Progress bars for key metrics
        strength_progress = performance_data.get("strength_progress", 0)
        endurance_progress = performance_data.get("endurance_progress", 0)
        flexibility_progress = performance_data.get("flexibility_progress", 0)

        progress_bars = [
            ["TABLEAU DE BORD PERFORMANCE"],
            [
                ProgressBarComponent(
                    strength_progress, 100, 150, 15, "#e53e3e", "#fc8181"
                )
            ],
            ["Force: {}%".format(strength_progress)],
            [
                ProgressBarComponent(
                    endurance_progress, 100, 150, 15, "#3182ce", "#63b3ed"
                )
            ],
            ["Endurance: {}%".format(endurance_progress)],
            [
                ProgressBarComponent(
                    flexibility_progress, 100, 150, 15, "#38a169", "#68d391"
                )
            ],
            ["Flexibilité: {}%".format(flexibility_progress)],
        ]

        # Performance trend visualization
        if "performance_trend" in performance_data:
            trend_chart = DataVisualizationComponent(
                performance_data["performance_trend"],
                chart_type="line",
                width=250,
                height=120,
            )
            progress_bars.append([trend_chart])

        dashboard = Table([[progress_bars]], colWidths=[6 * inch])
        dashboard.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f7fafc")),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                ]
            )
        )

        return dashboard

    def _build_anatomy_section(self) -> Table:
        """Build anatomy zone targeting visualization"""
        target_muscles = self.data.get(
            "target_muscle_groups", ["chest", "shoulders", "arms"]
        )

        anatomy_viz = AnatomyZoneComponent(target_muscles, width=150, height=200)

        muscle_focus = [
            ["CIBLAGE ANATOMIQUE", "GROUPES MUSCULAIRES"],
            [
                anatomy_viz,
                "\n".join([f"• {muscle.title()}" for muscle in target_muscles]),
            ],
        ]

        anatomy_table = Table(muscle_focus, colWidths=[2.5 * inch, 3.5 * inch])
        anatomy_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 1, HexColor("#e2e8f0")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#ffffff")),
                ]
            )
        )

        return anatomy_table

    def _build_elite_workout_blocks(self) -> List[Any]:
        """Build workout blocks with elite styling and data integration"""
        elements = []
        blocks = self.data.get("workout_blocks", [])

        if not blocks:
            # Generate default elite structure if no blocks provided
            blocks = self._generate_default_elite_blocks()

        for i, block in enumerate(blocks):
            # Section header
            block_title = Paragraph(
                f"<b>BLOC {i + 1}: {block.get('title', 'Entraînement').upper()}</b>",
                self.styles["heading"],
            )
            elements.append(block_title)
            elements.append(Spacer(1, 10))

            # Elite workout block component
            elite_block = WorkoutBlockComponent(block, width=500, theme="elite")
            elements.append(elite_block)
            elements.append(Spacer(1, 15))

            # Performance metrics for this block
            if block.get("performance_data"):
                elements.append(self._build_block_metrics(block["performance_data"]))
                elements.append(Spacer(1, 15))

        return elements

    def _build_block_metrics(self, metrics_data: Dict[str, Any]) -> Table:
        """Build detailed metrics table for workout block"""
        metrics = [
            ["Métrique", "Valeur", "Objectif"],
            [
                "Volume (kg)",
                metrics_data.get("volume", "N/A"),
                metrics_data.get("target_volume", "N/A"),
            ],
            [
                "Intensité (%1RM)",
                metrics_data.get("intensity", "N/A"),
                metrics_data.get("target_intensity", "N/A"),
            ],
            [
                "Densité (ex/min)",
                metrics_data.get("density", "N/A"),
                metrics_data.get("target_density", "N/A"),
            ],
            [
                "RPE moyen",
                metrics_data.get("rpe", "N/A"),
                metrics_data.get("target_rpe", "N/A"),
            ],
        ]

        metrics_table = Table(metrics, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        metrics_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]
            )
        )

        return metrics_table

    def _build_tracking_section(self) -> Table:
        """Build performance tracking section with data inputs"""
        tracking_data = [
            ["SUIVI PERFORMANCE", "", ""],
            ["Date", "Métrique", "Valeur"],
            ["____", "Volume Total (kg)", "________"],
            ["____", "RPE Moyen", "________"],
            ["____", "Temps Total", "________"],
            ["____", "Fréquence Cardiaque Max", "________"],
            ["____", "Notes Subjectives", "________"],
        ]

        tracking_table = Table(
            tracking_data, colWidths=[1.5 * inch, 2 * inch, 2 * inch]
        )
        tracking_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    # Content
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 2), (-1, -1), 10),
                ]
            )
        )

        return tracking_table

    def _build_video_integration(self) -> Table:
        """Build video integration section with QR codes"""
        videos = self.data.get("video_links", [])
        if not videos:
            return Spacer(1, 0)  # Return empty spacer if no videos

        qr_elements = []
        for video in videos[:4]:  # Limit to 4 videos for layout
            qr_code = QRCodeComponent(video.get("url", ""), width=50, height=50)
            video_title = video.get("title", "Démonstration")
            qr_elements.append([qr_code, video_title])

        # Arrange QR codes in 2x2 grid
        if len(qr_elements) >= 2:
            video_table = Table(
                [
                    ["VIDÉOS DÉMONSTRATION", ""],
                    qr_elements[0] if len(qr_elements) > 0 else ["", ""],
                    qr_elements[1] if len(qr_elements) > 1 else ["", ""],
                ],
                colWidths=[2.5 * inch, 2.5 * inch],
            )
        else:
            video_table = Table(
                [["VIDÉOS DÉMONSTRATION"], qr_elements[0] if qr_elements else [""]]
            )

        video_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                ]
            )
        )

        return video_table

    def _generate_default_elite_blocks(self) -> List[Dict[str, Any]]:
        """Generate default elite workout structure if not provided"""
        return [
            {
                "title": "Activation Neuromusculaire",
                "duration": 10,
                "format": "PRÉPARATOIRE",
                "exercises": [
                    {
                        "name": "Mobilisation articulaire dynamique",
                        "reps": "2x8",
                        "notes": "Amplitude maximale",
                    },
                    {
                        "name": "Activation glute",
                        "reps": "2x12",
                        "notes": "Contrôle moteur",
                    },
                    {"name": "Potentialisation", "reps": "3x3", "notes": "70% 1RM"},
                ],
                "performance_data": {
                    "volume": 450,
                    "target_volume": 500,
                    "intensity": 70,
                    "target_intensity": 75,
                    "rpe": 6,
                    "target_rpe": 6,
                },
            },
            {
                "title": "Force Maximale",
                "duration": 35,
                "format": "PRINCIPAL",
                "exercises": [
                    {
                        "name": "Squat Back",
                        "reps": "5x3",
                        "notes": "85-90% 1RM, 3min repos",
                    },
                    {
                        "name": "Développé Couché",
                        "reps": "5x3",
                        "notes": "85-90% 1RM, 3min repos",
                    },
                    {
                        "name": "Soulevé de Terre",
                        "reps": "4x2",
                        "notes": "90-95% 1RM, 4min repos",
                    },
                ],
                "performance_data": {
                    "volume": 2800,
                    "target_volume": 3000,
                    "intensity": 88,
                    "target_intensity": 90,
                    "rpe": 9,
                    "target_rpe": 9,
                },
            },
            {
                "title": "Récupération Active",
                "duration": 15,
                "format": "FINITION",
                "exercises": [
                    {
                        "name": "Étirements statiques",
                        "reps": "5x30s",
                        "notes": "Groupes travaillés",
                    },
                    {
                        "name": "Respiration diaphragmatique",
                        "reps": "3x10",
                        "notes": "Parasympathique",
                    },
                    {
                        "name": "Foam rolling",
                        "reps": "5min",
                        "notes": "Points de tension",
                    },
                ],
                "performance_data": {
                    "volume": 0,
                    "target_volume": 0,
                    "intensity": 30,
                    "target_intensity": 30,
                    "rpe": 3,
                    "target_rpe": 3,
                },
            },
        ]

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Elite template data requirements"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "program_overview": {
                    "type": "object",
                    "properties": {
                        "primary_goal": {"type": "string"},
                        "duration_weeks": {"type": "integer"},
                        "sessions_per_week": {"type": "integer"},
                        "intensity_level": {"type": "string"},
                        "target_areas": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "performance_metrics": {
                    "type": "object",
                    "properties": {
                        "strength_progress": {"type": "number"},
                        "endurance_progress": {"type": "number"},
                        "flexibility_progress": {"type": "number"},
                        "performance_trend": {"type": "object"},
                    },
                },
                "target_muscle_groups": {"type": "array", "items": {"type": "string"}},
                "workout_blocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "duration": {"type": "integer"},
                            "format": {"type": "string"},
                            "exercises": {"type": "array"},
                            "performance_data": {"type": "object"},
                        },
                    },
                },
                "video_links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                        },
                    },
                },
            },
            "required": ["title", "client_name"],
        }
