"""
Session Home Template - Professional template for home training and remote fitness
Practical format optimized for home workouts with minimal equipment requirements
"""

from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch, mm
from reportlab.platypus import (
    Flowable,
    FrameBreak,
    Image,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from ..base_template import BaseTemplate
from ...components.professional_components import (
    ProgressBarComponent,
    WorkoutBlockComponent,
    DataVisualizationComponent,
    QRCodeComponent,
)


class SessionHomeTemplate(BaseTemplate):
    """
    Session Home Template

    Perfect for:
    - Home training sessions
    - Remote coaching programs
    - Quarantine/lockdown workouts
    - Travel fitness routines
    - Equipment-minimal training
    - Space-constrained environments

    Features:
    - Minimal equipment focus
    - Space optimization guidance
    - Setup photos and diagrams
    - Equipment substitutions
    - Safety considerations for home
    - Efficient workout design
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Home training configuration
        self.home_config = {
            "equipment_level": "minimal",
            "space_requirements": "small",
            "safety_focus": True,
            "efficiency_priority": "maximum",
            "substitution_options": True,
            **self.config.get("home_config", {})
        }

        # Practical home color palette - Calm and focused
        self.colors = {
            "primary": colors.Color(0.25, 0.40, 0.58),        # Home blue
            "secondary": colors.Color(0.45, 0.60, 0.40),      # Calm green
            "accent": colors.Color(0.85, 0.65, 0.13),         # Warm orange
            "background": colors.Color(0.96, 0.96, 0.94),     # Off-white
            "text": colors.Color(0.15, 0.15, 0.15),            # Soft black
            "equipment": colors.Color(0.60, 0.40, 0.80),      # Equipment purple
            "safety": colors.Color(0.80, 0.20, 0.20),         # Safety red
            "efficiency": colors.Color(0.20, 0.70, 0.50),     # Efficiency teal
            "home": colors.Color(0.70, 0.50, 0.30),           # Home brown
            **self.config.get("colors", {})
        }

        # Clear and practical typography
        self.fonts = {
            "title": ("Helvetica-Bold", 18),
            "subtitle": ("Helvetica-Bold", 15),
            "heading": ("Helvetica-Bold", 13),
            "body": ("Helvetica", 11),
            "caption": ("Helvetica", 9),
            "emphasis": ("Helvetica-Bold", 11),
            "practical": ("Helvetica", 10),
            **self.config.get("fonts", {})
        }

        # Content validation
        self._validate_home_data()

    def _validate_home_data(self) -> None:
        """Validate that home training data is present"""
        required_fields = [
            "title", "participant_name", "session_date", "space_required",
            "equipment_needed", "exercises", "safety_notes"
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_home_content(field)

    def _get_default_home_content(self, field: str) -> Any:
        """Provide default home training content"""
        defaults = {
            "title": "Séance Home Training Efficace",
            "participant_name": "Participant",
            "session_date": "Date",
            "space_required": "2m x 2m minimum",
            "equipment_needed": [
                {"item": "Tapis de sol", "essential": True, "substitution": "Serviette épaisse"},
                {"item": "Bouteilles d'eau (2x1L)", "essential": False, "substitution": "Sacs de riz"},
                {"item": "Chaise stable", "essential": True, "substitution": "Bord de canapé"},
                {"item": "Mur libre", "essential": True, "substitution": "Porte fermée"}
            ],
            "exercises": [
                {
                    "name": "Échauffement Dynamique",
                    "duration": "5 min",
                    "space": "Sur place",
                    "equipment": "Aucun",
                    "setup_notes": "Dégager l'espace autour de soi",
                    "safety_tips": ["Commencer doucement", "Vérifier l'espace libre"],
                    "substitutions": {},
                    "home_adaptations": "Musique douce recommandée"
                },
                {
                    "name": "Circuit Fonctionnel",
                    "duration": "20 min",
                    "space": "2m x 2m",
                    "equipment": "Tapis + bouteilles d'eau",
                    "setup_notes": "Tapis au centre, bouteilles à portée",
                    "safety_tips": ["Sol non glissant", "Bouteilles bien fermées"],
                    "substitutions": {
                        "bouteilles": "Sacs de riz ou conserves",
                        "tapis": "Serviette anti-dérapante"
                    },
                    "home_adaptations": "Adapter selon mobilier disponible"
                },
                {
                    "name": "Renforcement Mural",
                    "duration": "10 min",
                    "space": "Contre un mur",
                    "equipment": "Mur + chaise",
                    "setup_notes": "Chaise à 1m du mur, stable",
                    "safety_tips": ["Mur solide", "Chaise bien posée"],
                    "substitutions": {
                        "chaise": "Marche d'escalier ou banc",
                        "mur": "Porte fermée très solide"
                    },
                    "home_adaptations": "Vérifier stabilité avant utilisation"
                },
                {
                    "name": "Stretching Final",
                    "duration": "5 min",
                    "space": "Sur le tapis",
                    "equipment": "Tapis",
                    "setup_notes": "Position confortable au sol",
                    "safety_tips": ["Mouvements lents", "Pas de douleur"],
                    "substitutions": {"tapis": "Lit ou canapé moelleux"},
                    "home_adaptations": "Ambiance relaxante, lumière tamisée"
                }
            ],
            "safety_notes": [
                "Vérifier la stabilité du sol et des équipements",
                "Maintenir un espace libre autour de soi",
                "Éviter les exercices près d'objets fragiles",
                "S'hydrater régulièrement",
                "Arrêter en cas de douleur inhabituelle"
            ]
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete home training session content"""
        content = []

        # Practical home header
        content.append(self._build_home_header())
        content.append(Spacer(1, 10*mm))

        # Home setup requirements
        content.append(self._build_setup_requirements())
        content.append(Spacer(1, 8*mm))

        # Equipment checklist with substitutions
        content.append(self._build_equipment_checklist())
        content.append(Spacer(1, 8*mm))

        # Exercise program with home adaptations
        content.extend(self._build_home_exercises())
        content.append(Spacer(1, 8*mm))

        # Safety guidelines for home training
        content.append(self._build_safety_section())
        content.append(Spacer(1, 6*mm))

        # Efficiency tips and home optimization
        content.append(self._build_efficiency_tips())

        return content

    def _build_home_header(self) -> Table:
        """Build practical home training header"""
        title = self.data.get("title", "Séance Home Training Efficace")
        participant = self.data.get("participant_name", "Participant")
        session_date = self.data.get("session_date", "Date")
        duration = self.data.get("total_duration", "40 min")
        space_required = self.data.get("space_required", "2m x 2m minimum")

        header_data = [
            [
                Paragraph(f"<b>🏠 {title}</b>", ParagraphStyle(
                    'HomeTitle',
                    fontSize=self.fonts["title"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER,
                    spaceAfter=5
                )),
                ""
            ],
            [
                Paragraph("💪 EFFICACE • PRATIQUE • ACCESSIBLE 💪", ParagraphStyle(
                    'HomeTagline',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["efficiency"],
                    alignment=TA_CENTER,
                    spaceAfter=8
                )),
                ""
            ],
            [
                Paragraph(f"<b>👤 Participant:</b> {participant}<br/><b>📅 Date:</b> {session_date}", ParagraphStyle(
                    'ParticipantInfo',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(f"<b>⏱️ Durée totale:</b> {duration}<br/><b>📏 Espace requis:</b> {space_required}", ParagraphStyle(
                    'SessionSpecs',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_RIGHT
                ))
            ]
        ]

        header_table = Table(header_data, colWidths=[9*cm, 9*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.colors["background"]),
            ('BACKGROUND', (0, 2), (-1, 2), self.colors["background"]),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["home"]),
            ('LINEABOVE', (0, 0), (-1, 0), 3, self.colors["primary"]),
            ('LINEBELOW', (0, -1), (-1, -1), 3, self.colors["primary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        return header_table

    def _build_setup_requirements(self) -> Table:
        """Build home setup requirements"""
        room_type = self.data.get("recommended_room", "Salon ou chambre")
        lighting = self.data.get("lighting_needs", "Éclairage naturel ou bon éclairage")
        ventilation = self.data.get("ventilation", "Fenêtre ouverte ou ventilateur")
        floor_type = self.data.get("floor_requirements", "Sol stable, non glissant")

        setup_data = [
            [
                Paragraph("<b>🏠 PRÉPARATION DE L'ESPACE - CONFIGURATION OPTIMALE</b>", ParagraphStyle(
                    'SetupTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph(f"<b>🏠 Pièce recommandée:</b> {room_type}<br/>"
                         f"<b>💡 Éclairage:</b> {lighting}<br/>"
                         f"<b>🌬️ Ventilation:</b> {ventilation}<br/>"
                         f"<b>🏢 Type de sol:</b> {floor_type}", ParagraphStyle(
                    'SetupDetails',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=8
                ))
            ],
            [
                Paragraph("<b>✅ Checklist de préparation:</b><br/>"
                         "☐ Dégager l'espace d'entraînement<br/>"
                         "☐ Éloigner les objets fragiles<br/>"
                         "☐ Vérifier la stabilité du sol<br/>"
                         "☐ Préparer une bouteille d'eau<br/>"
                         "☐ Mettre des vêtements confortables<br/>"
                         "☐ Prévenir les autres occupants", ParagraphStyle(
                    'Checklist',
                    fontSize=self.fonts["practical"][1],
                    textColor=self.colors["home"],
                    alignment=TA_LEFT,
                    leftIndent=10
                ))
            ]
        ]

        setup_table = Table(setup_data, colWidths=[18*cm])
        setup_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["secondary"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["background"]),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["accent"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return setup_table

    def _build_equipment_checklist(self) -> Table:
        """Build equipment checklist with substitutions"""
        equipment = self.data.get("equipment_needed", [])

        equipment_data = [
            [
                Paragraph("<b>🔧 ÉQUIPEMENT REQUIS - ALTERNATIVES INCLUSES</b>", ParagraphStyle(
                    'EquipmentTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph("<b>Équipement</b>", ParagraphStyle(
                    'EquipHeader',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["equipment"],
                    alignment=TA_LEFT
                )),
                Paragraph("<b>Essentiel</b>", ParagraphStyle(
                    'EquipHeader',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["equipment"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Alternative maison</b>", ParagraphStyle(
                    'EquipHeader',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["equipment"],
                    alignment=TA_LEFT
                ))
            ]
        ]

        for item in equipment:
            item_name = item.get("item", "")
            essential = "✅" if item.get("essential", False) else "🔄"
            substitution = item.get("substitution", "Non nécessaire")

            equipment_data.append([
                Paragraph(f"🔧 {item_name}", ParagraphStyle(
                    'EquipItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(essential, ParagraphStyle(
                    'Essential',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["efficiency"],
                    alignment=TA_CENTER
                )),
                Paragraph(f"➡️ {substitution}", ParagraphStyle(
                    'Substitution',
                    fontSize=self.fonts["practical"][1],
                    textColor=self.colors["home"],
                    alignment=TA_LEFT
                ))
            ])

        equipment_table = Table(equipment_data, colWidths=[6*cm, 3*cm, 9*cm])
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["equipment"]),
            ('BACKGROUND', (0, 1), (-1, 1), self.colors["background"]),
            ('BACKGROUND', (0, 2), (-1, -1), self.colors["background"]),
            ('SPAN', (0, 0), (-1, 0)),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return equipment_table

    def _build_home_exercises(self) -> List[Flowable]:
        """Build exercise program with home-specific adaptations"""
        exercises = self.data.get("exercises", [])
        content = []

        # Exercise program header
        content.append(
            Paragraph("<b>💪 PROGRAMME HOME TRAINING - ADAPTATIONS INCLUSES</b>", ParagraphStyle(
                'ExerciseTitle',
                fontSize=self.fonts["heading"][1],
                textColor=self.colors["primary"],
                alignment=TA_CENTER,
                spaceAfter=8
            ))
        )

        for i, exercise in enumerate(exercises):
            exercise_name = exercise.get("name", f"Exercice {i+1}")
            duration = exercise.get("duration", "")
            space = exercise.get("space", "")
            equipment = exercise.get("equipment", "")
            setup_notes = exercise.get("setup_notes", "")
            safety_tips = exercise.get("safety_tips", [])
            substitutions = exercise.get("substitutions", {})
            home_adaptations = exercise.get("home_adaptations", "")

            # Exercise card with home focus
            exercise_data = [
                [
                    Paragraph(f"<b>{i+1}. {exercise_name}</b>", ParagraphStyle(
                        'ExerciseName',
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_LEFT
                    )),
                    Paragraph(f"<b>⏱️ {duration}</b><br/>📏 {space}", ParagraphStyle(
                        'ExerciseSpecs',
                        fontSize=self.fonts["practical"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER
                    ))
                ],
                [
                    Paragraph(f"<b>🔧 Équipement:</b> {equipment}<br/><b>🎯 Installation:</b> {setup_notes}", ParagraphStyle(
                        'ExerciseSetup',
                        fontSize=self.fonts["practical"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                        spaceAfter=5
                    )),
                    ""
                ]
            ]

            # Safety tips
            if safety_tips:
                safety_text = "<b>⚠️ Sécurité:</b> " + " • ".join(safety_tips)
                exercise_data.append([
                    Paragraph(safety_text, ParagraphStyle(
                        'SafetyTips',
                        fontSize=self.fonts["caption"][1],
                        textColor=self.colors["safety"],
                        alignment=TA_LEFT,
                        leftIndent=5,
                        spaceAfter=5
                    )),
                    ""
                ])

            # Equipment substitutions
            if substitutions:
                subs_text = "<b>🔄 Alternatives:</b><br/>"
                for original, substitute in substitutions.items():
                    subs_text += f"• {original} ➡️ {substitute}<br/>"

                exercise_data.append([
                    Paragraph(subs_text, ParagraphStyle(
                        'Substitutions',
                        fontSize=self.fonts["caption"][1],
                        textColor=self.colors["home"],
                        alignment=TA_LEFT,
                        leftIndent=5,
                        spaceAfter=5
                    )),
                    ""
                ])

            # Home adaptations
            if home_adaptations:
                exercise_data.append([
                    Paragraph(f"<b>🏠 Adaptation maison:</b> {home_adaptations}", ParagraphStyle(
                        'HomeAdaptations',
                        fontSize=self.fonts["caption"][1],
                        textColor=self.colors["efficiency"],
                        alignment=TA_LEFT,
                        leftIndent=5
                    )),
                    ""
                ])

            exercise_table = Table(exercise_data, colWidths=[14*cm, 4*cm])

            # Alternate colors for visual separation
            header_color = [self.colors["primary"], self.colors["secondary"], self.colors["accent"]][i % 3]

            exercise_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), header_color),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors["background"]),
                ('SPAN', (0, 1), (1, 1)),  # Span setup info
                ('SPAN', (0, 2), (1, 2)) if len(exercise_data) > 2 else None,  # Span safety if present
                ('SPAN', (0, 3), (1, 3)) if len(exercise_data) > 3 else None,  # Span substitutions if present
                ('SPAN', (0, 4), (1, 4)) if len(exercise_data) > 4 else None,  # Span adaptations if present
                ('BORDER', (0, 0), (-1, -1), 1, header_color),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))

            # Remove None values from style
            table_style = [style for style in exercise_table._tablestyle._cmds if style is not None]
            exercise_table.setStyle(TableStyle(table_style))

            content.append(exercise_table)
            if i < len(exercises) - 1:
                content.append(Spacer(1, 6*mm))

        return content

    def _build_safety_section(self) -> Table:
        """Build safety guidelines for home training"""
        safety_notes = self.data.get("safety_notes", [])

        safety_data = [
            [
                Paragraph("<b>⚠️ CONSIGNES DE SÉCURITÉ À DOMICILE ⚠️</b>", ParagraphStyle(
                    'SafetyTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ]
        ]

        for note in safety_notes:
            safety_data.append([
                Paragraph(f"⚠️ {note}", ParagraphStyle(
                    'SafetyNote',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    leftIndent=10,
                    spaceAfter=4
                ))
            ])

        # Add emergency contact info
        safety_data.append([
            Paragraph("<b>🚨 En cas de problème:</b> Arrêter immédiatement l'exercice et consulter un professionnel si nécessaire", ParagraphStyle(
                'Emergency',
                fontSize=self.fonts["emphasis"][1],
                textColor=self.colors["safety"],
                alignment=TA_CENTER,
                spaceAfter=5
            ))
        ])

        safety_table = Table(safety_data, colWidths=[18*cm])
        safety_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["safety"]),
            ('BACKGROUND', (0, 1), (0, -2), self.colors["background"]),
            ('BACKGROUND', (0, -1), (0, -1), colors.Color(1.0, 0.9, 0.9)),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["safety"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return safety_table

    def _build_efficiency_tips(self) -> Table:
        """Build efficiency tips for home training optimization"""
        efficiency_tips = self.data.get("efficiency_tips", [
            "Préparer tout l'équipement avant de commencer",
            "Utiliser un timer pour respecter les temps de travail",
            "Créer une playlist énergisante adaptée à la durée",
            "Aérer la pièce 10 minutes avant l'entraînement",
            "Planifier l'entraînement aux heures les plus fraîches",
            "Prévoir une serviette et une bouteille d'eau à proximité"
        ])

        tips_data = [
            [
                Paragraph("<b>🚀 CONSEILS D'EFFICACITÉ - OPTIMISATION HOME TRAINING</b>", ParagraphStyle(
                    'TipsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph("<b>⏰ Avant l'entraînement</b>", ParagraphStyle(
                    'CategoryTitle',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["efficiency"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                )),
                Paragraph("<b>💡 Pendant l'entraînement</b>", ParagraphStyle(
                    'CategoryTitle',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["efficiency"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ]
        ]

        # Split tips into before/during categories
        before_tips = efficiency_tips[:3]
        during_tips = efficiency_tips[3:]

        max_tips = max(len(before_tips), len(during_tips))
        for i in range(max_tips):
            before_tip = before_tips[i] if i < len(before_tips) else ""
            during_tip = during_tips[i] if i < len(during_tips) else ""

            tips_data.append([
                Paragraph(f"✓ {before_tip}" if before_tip else "", ParagraphStyle(
                    'Tip',
                    fontSize=self.fonts["practical"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                )),
                Paragraph(f"✓ {during_tip}" if during_tip else "", ParagraphStyle(
                    'Tip',
                    fontSize=self.fonts["practical"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ])

        # Final motivation message
        tips_data.append([
            Paragraph("🏠 <b>L'entraînement à domicile peut être aussi efficace qu'en salle !</b> 💪", ParagraphStyle(
                'Motivation',
                fontSize=self.fonts["emphasis"][1],
                textColor=self.colors["primary"],
                alignment=TA_CENTER
            )),
            ""
        ])

        tips_table = Table(tips_data, colWidths=[9*cm, 9*cm])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["efficiency"]),
            ('BACKGROUND', (0, 1), (-1, 1), self.colors["background"]),
            ('BACKGROUND', (0, 2), (-1, -2), self.colors["background"]),
            ('BACKGROUND', (0, -1), (-1, -1), self.colors["background"]),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, -1), (1, -1)),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["home"]),
            ('LINEABOVE', (0, -1), (-1, -1), 1, self.colors["efficiency"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return tips_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Home Efficient",
            "category": "single_sessions",
            "description": "Format pratique pour home training avec équipement minimal",
            "target_audience": "Home training, confinements, déplacements, espaces restreints",
            "features": [
                "Focus équipement minimal",
                "Guide d'optimisation d'espace",
                "Photos et schémas de setup",
                "Alternatives d'équipement",
                "Consignes de sécurité à domicile",
                "Conseils d'efficacité maximale"
            ],
            "color_scheme": "Practical home colors (blue, green, orange, brown)",
            "typography": "Clear Helvetica for practical reading",
            "layout_style": "Practical home-focused format",
            "complexity": "Beginner to Intermediate",
            "page_count": "2-3 pages",
            "data_requirements": [
                "title", "participant_name", "session_date", "space_required",
                "equipment_needed", "exercises", "safety_notes"
            ],
            "customization_options": [
                "Equipment availability level",
                "Space requirements adaptation",
                "Safety detail level",
                "Substitution complexity"
            ]
        }