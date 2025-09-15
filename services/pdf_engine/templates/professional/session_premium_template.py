"""
Session Premium Template - Professional template for high-end personal training
Luxury personalized format for VIP clients and premium coaching services
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
    PremiumHeaderComponent,
    MotivationalBadgeComponent,
)


class SessionPremiumTemplate(BaseTemplate):
    """
    Session Premium Template

    Perfect for:
    - High-end personal training sessions
    - VIP client exclusive programs
    - Premium coaching services
    - Luxury fitness facilities
    - Celebrity and executive training

    Features:
    - Luxurious design and typography
    - Extensive personalization options
    - Detailed coaching notes sections
    - Real-time adaptation tracking
    - Premium branding elements
    - Executive summary format
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Premium session configuration
        self.premium_config = {
            "luxury_level": "maximum",
            "personalization": "comprehensive",
            "detail_depth": "extensive",
            "coach_notes": "detailed",
            "branding": "premium",
            **self.config.get("premium_config", {})
        }

        # Luxury color palette - Sophisticated and elegant
        self.colors = {
            "primary": colors.Color(0.07, 0.07, 0.07),        # Deep charcoal
            "secondary": colors.Color(0.68, 0.56, 0.35),      # Elegant gold
            "accent": colors.Color(0.85, 0.85, 0.85),         # Platinum silver
            "background": colors.Color(0.98, 0.97, 0.95),     # Cream white
            "text": colors.Color(0.13, 0.13, 0.13),            # Rich black
            "luxury": colors.Color(0.58, 0.48, 0.28),         # Bronze luxury
            "premium": colors.Color(0.20, 0.20, 0.20),        # Premium black
            "highlight": colors.Color(0.95, 0.90, 0.75),      # Champagne highlight
            **self.config.get("colors", {})
        }

        # Premium typography - Elegant and refined
        self.fonts = {
            "title": ("Times-Bold", 24),
            "subtitle": ("Times-Bold", 18),
            "heading": ("Times-Bold", 16),
            "body": ("Times-Roman", 12),
            "caption": ("Times-Italic", 10),
            "emphasis": ("Times-Bold", 14),
            "signature": ("Times-Italic", 14),
            **self.config.get("fonts", {})
        }

        # Content validation
        self._validate_premium_data()

    def _validate_premium_data(self) -> None:
        """Validate that premium session data is present"""
        required_fields = [
            "title", "client_name", "coach_name", "session_date",
            "session_goals", "exercises", "coach_notes"
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_premium_content(field)

    def _get_default_premium_content(self, field: str) -> Any:
        """Provide default premium content"""
        defaults = {
            "title": "Séance Premium Personnalisée",
            "client_name": "Client VIP",
            "coach_name": "Coach Expert",
            "session_date": "Date",
            "session_goals": [
                "Optimisation des performances individuelles",
                "Progression technique personnalisée",
                "Atteinte des objectifs spécifiques"
            ],
            "exercises": [
                {
                    "name": "Échauffement Personnalisé",
                    "duration": "10 min",
                    "intensity": "Progressive",
                    "notes": "Adapté aux besoins spécifiques du client",
                    "coaching_points": ["Mobilité ciblée", "Activation neuromusculaire"],
                    "adaptations": []
                },
                {
                    "name": "Entraînement Principal",
                    "duration": "35 min",
                    "intensity": "Haute",
                    "notes": "Focus sur les objectifs prioritaires",
                    "coaching_points": ["Technique parfaite", "Progression mesurée"],
                    "adaptations": []
                },
                {
                    "name": "Récupération Active",
                    "duration": "5 min",
                    "intensity": "Faible",
                    "notes": "Retour au calme personnalisé",
                    "coaching_points": ["Relaxation", "Étirements ciblés"],
                    "adaptations": []
                }
            ],
            "coach_notes": {
                "pre_session": "Évaluation de l'état du client",
                "during_session": "Adaptations en temps réel",
                "post_session": "Bilan et recommandations",
                "next_session": "Objectifs pour la prochaine séance"
            }
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete premium session content"""
        content = []

        # Luxury header with premium branding
        content.append(self._build_premium_header())
        content.append(Spacer(1, 12*mm))

        # Client profile and session overview
        content.append(self._build_client_profile())
        content.append(Spacer(1, 10*mm))

        # Session goals and objectives
        content.append(self._build_session_goals())
        content.append(Spacer(1, 10*mm))

        # Detailed exercise program
        content.extend(self._build_exercise_program())
        content.append(Spacer(1, 10*mm))

        # Coach notes and observations
        content.append(self._build_coach_notes_section())
        content.append(Spacer(1, 10*mm))

        # Real-time adaptations tracking
        content.append(self._build_adaptations_section())
        content.append(Spacer(1, 8*mm))

        # Premium session summary and signature
        content.append(self._build_premium_summary())

        return content

    def _build_premium_header(self) -> Table:
        """Build luxury header with premium branding"""
        title = self.data.get("title", "Séance Premium Personnalisée")
        client_name = self.data.get("client_name", "Client VIP")
        coach_name = self.data.get("coach_name", "Coach Expert")
        session_date = self.data.get("session_date", "Date")
        session_time = self.data.get("session_time", "Heure")

        # Premium header with luxury styling
        header_data = [
            [
                Paragraph(f"<b>{title}</b>", ParagraphStyle(
                    'LuxuryTitle',
                    fontSize=self.fonts["title"][1],
                    textColor=self.colors["premium"],
                    alignment=TA_CENTER,
                    spaceAfter=5
                )),
                ""
            ],
            [
                Paragraph("EXCELLENCE • PERSONNALISATION • PERFORMANCE", ParagraphStyle(
                    'Tagline',
                    fontSize=self.fonts["caption"][1],
                    textColor=self.colors["luxury"],
                    alignment=TA_CENTER,
                    spaceAfter=8
                )),
                ""
            ],
            [
                Paragraph(f"<b>Client:</b> {client_name}<br/><b>Coach:</b> {coach_name}", ParagraphStyle(
                    'ClientInfo',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(f"<b>Date:</b> {session_date}<br/><b>Heure:</b> {session_time}", ParagraphStyle(
                    'SessionInfo',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_RIGHT
                ))
            ]
        ]

        header_table = Table(header_data, colWidths=[9*cm, 9*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), self.colors["background"]),
            ('BACKGROUND', (0, 2), (-1, 2), self.colors["highlight"]),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["secondary"]),
            ('LINEABOVE', (0, 0), (-1, 0), 3, self.colors["primary"]),
            ('LINEBELOW', (0, -1), (-1, -1), 3, self.colors["primary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        return header_table

    def _build_client_profile(self) -> Table:
        """Build detailed client profile for personalization"""
        profile = self.data.get("client_profile", {})

        # Default profile data if not provided
        if not profile:
            profile = {
                "fitness_level": "Avancé",
                "preferences": ["Entraînement fonctionnel", "Haute intensité"],
                "limitations": ["Aucune restriction majeure"],
                "goals": ["Performance", "Bien-être"],
                "experience": "5+ ans d'entraînement régulier"
            }

        profile_data = [
            [
                Paragraph("<b>PROFIL CLIENT - PERSONNALISATION PREMIUM</b>", ParagraphStyle(
                    'ProfileTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph(f"<b>Niveau:</b> {profile.get('fitness_level', 'Non défini')}", ParagraphStyle(
                    'ProfileItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ],
            [
                Paragraph(f"<b>Préférences:</b> {', '.join(profile.get('preferences', []))}", ParagraphStyle(
                    'ProfileItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ],
            [
                Paragraph(f"<b>Limitations:</b> {', '.join(profile.get('limitations', []))}", ParagraphStyle(
                    'ProfileItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ],
            [
                Paragraph(f"<b>Expérience:</b> {profile.get('experience', 'Non définie')}", ParagraphStyle(
                    'ProfileItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ]
        ]

        profile_table = Table(profile_data, colWidths=[18*cm])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["luxury"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["highlight"]),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        return profile_table

    def _build_session_goals(self) -> Table:
        """Build session goals with luxury presentation"""
        goals = self.data.get("session_goals", [])

        goals_data = [
            [
                Paragraph("<b>OBJECTIFS DE SÉANCE - EXCELLENCE CIBLÉE</b>", ParagraphStyle(
                    'GoalsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                ""
            ]
        ]

        for i, goal in enumerate(goals):
            goals_data.append([
                Paragraph(f"<b>{i+1}.</b>", ParagraphStyle(
                    'GoalNumber',
                    fontSize=self.fonts["emphasis"][1],
                    textColor=self.colors["secondary"],
                    alignment=TA_CENTER
                )),
                Paragraph(goal, ParagraphStyle(
                    'Goal',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=4
                ))
            ])

        goals_table = Table(goals_data, colWidths=[2*cm, 16*cm])
        goals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["primary"]),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors["background"]),
            ('SPAN', (0, 0), (1, 0)),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return goals_table

    def _build_exercise_program(self) -> List[Flowable]:
        """Build detailed exercise program with premium formatting"""
        exercises = self.data.get("exercises", [])
        content = []

        # Program header
        content.append(
            Paragraph("<b>PROGRAMME D'ENTRAÎNEMENT - CONCEPTION PREMIUM</b>", ParagraphStyle(
                'ProgramTitle',
                fontSize=self.fonts["heading"][1],
                textColor=self.colors["primary"],
                alignment=TA_CENTER,
                spaceAfter=10
            ))
        )

        # Each exercise as a luxury card
        for i, exercise in enumerate(exercises):
            exercise_name = exercise.get("name", f"Exercice {i+1}")
            duration = exercise.get("duration", "")
            intensity = exercise.get("intensity", "")
            notes = exercise.get("notes", "")
            coaching_points = exercise.get("coaching_points", [])
            adaptations = exercise.get("adaptations", [])

            # Exercise card
            exercise_data = [
                [
                    Paragraph(f"<b>{exercise_name}</b>", ParagraphStyle(
                        'ExerciseName',
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_LEFT
                    )),
                    Paragraph(f"<b>{duration}</b><br/><i>{intensity}</i>", ParagraphStyle(
                        'ExerciseSpecs',
                        fontSize=self.fonts["body"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER
                    ))
                ],
                [
                    Paragraph(f"<b>Notes du Coach:</b><br/>{notes}", ParagraphStyle(
                        'ExerciseNotes',
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                        spaceAfter=5
                    )),
                    ""
                ]
            ]

            # Add coaching points if present
            if coaching_points:
                points_text = "<b>Points Clés:</b><br/>"
                for point in coaching_points:
                    points_text += f"• {point}<br/>"

                exercise_data.append([
                    Paragraph(points_text, ParagraphStyle(
                        'CoachingPoints',
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["luxury"],
                        alignment=TA_LEFT,
                        leftIndent=10
                    )),
                    ""
                ])

            exercise_table = Table(exercise_data, colWidths=[12*cm, 6*cm])
            exercise_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors["secondary"]),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors["highlight"]),
                ('SPAN', (0, 1), (1, 1)),  # Span notes across both columns
                ('BORDER', (0, 0), (-1, -1), 2, self.colors["luxury"]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))

            content.append(exercise_table)
            if i < len(exercises) - 1:
                content.append(Spacer(1, 8*mm))

        return content

    def _build_coach_notes_section(self) -> Table:
        """Build comprehensive coach notes section"""
        coach_notes = self.data.get("coach_notes", {})

        notes_data = [
            [
                Paragraph("<b>NOTES PROFESSIONNELLES DU COACH</b>", ParagraphStyle(
                    'NotesTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ]
        ]

        # Pre-session notes
        pre_session = coach_notes.get("pre_session", "")
        if pre_session:
            notes_data.append([
                Paragraph(f"<b>🎯 Pré-Séance:</b><br/>{pre_session}", ParagraphStyle(
                    'PreSession',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=6
                ))
            ])

        # During session notes
        during_session = coach_notes.get("during_session", "")
        if during_session:
            notes_data.append([
                Paragraph(f"<b>⚡ Pendant la Séance:</b><br/>{during_session}", ParagraphStyle(
                    'DuringSession',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=6
                ))
            ])

        # Post-session notes
        post_session = coach_notes.get("post_session", "")
        if post_session:
            notes_data.append([
                Paragraph(f"<b>📝 Post-Séance:</b><br/>{post_session}", ParagraphStyle(
                    'PostSession',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=6
                ))
            ])

        # Next session preparation
        next_session = coach_notes.get("next_session", "")
        if next_session:
            notes_data.append([
                Paragraph(f"<b>🎪 Prochaine Séance:</b><br/>{next_session}", ParagraphStyle(
                    'NextSession',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["luxury"],
                    alignment=TA_LEFT
                ))
            ])

        notes_table = Table(notes_data, colWidths=[18*cm])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["primary"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["background"]),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        return notes_table

    def _build_adaptations_section(self) -> Table:
        """Build real-time adaptations tracking"""
        adaptations = self.data.get("real_time_adaptations", [
            {
                "time": "15min",
                "observation": "Client montre des signes de fatigue",
                "adaptation": "Réduction de l'intensité de 20%",
                "result": "Récupération rapide, bonne forme maintenue"
            },
            {
                "time": "30min",
                "observation": "Excellent état de forme",
                "adaptation": "Ajout d'une série bonus",
                "result": "Performance exceptionnelle"
            }
        ])

        adaptations_data = [
            [
                Paragraph("<b>ADAPTATIONS TEMPS RÉEL - COACHING RÉACTIF</b>", ParagraphStyle(
                    'AdaptationsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph("<b>Temps</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Observation</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Adaptation</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Résultat</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER
                ))
            ]
        ]

        for adaptation in adaptations:
            time = adaptation.get("time", "")
            observation = adaptation.get("observation", "")
            adaptation_made = adaptation.get("adaptation", "")
            result = adaptation.get("result", "")

            adaptations_data.append([
                Paragraph(f"<b>{time}</b>", ParagraphStyle(
                    'AdaptTime',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["luxury"],
                    alignment=TA_CENTER
                )),
                Paragraph(observation, ParagraphStyle(
                    'AdaptItem',
                    fontSize=self.fonts["caption"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(adaptation_made, ParagraphStyle(
                    'AdaptItem',
                    fontSize=self.fonts["caption"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(result, ParagraphStyle(
                    'AdaptItem',
                    fontSize=self.fonts["caption"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                ))
            ])

        adaptations_table = Table(adaptations_data, colWidths=[2*cm, 5*cm, 5*cm, 6*cm])
        adaptations_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["accent"]),
            ('BACKGROUND', (0, 1), (-1, 1), self.colors["highlight"]),
            ('BACKGROUND', (0, 2), (-1, -1), self.colors["background"]),
            ('SPAN', (0, 0), (-1, 0)),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return adaptations_table

    def _build_premium_summary(self) -> Table:
        """Build premium session summary with signature area"""
        session_rating = self.data.get("session_rating", "Excellent")
        client_feedback = self.data.get("client_feedback", "Séance parfaitement adaptée à mes besoins")
        next_appointment = self.data.get("next_appointment", "À définir")

        summary_data = [
            [
                Paragraph("<b>BILAN DE SÉANCE PREMIUM</b>", ParagraphStyle(
                    'SummaryTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ],
            [
                Paragraph(f"<b>Évaluation Globale:</b> {session_rating}", ParagraphStyle(
                    'Rating',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["luxury"],
                    alignment=TA_LEFT,
                    spaceAfter=5
                ))
            ],
            [
                Paragraph(f"<b>Retour Client:</b><br/><i>\"{client_feedback}\"</i>", ParagraphStyle(
                    'Feedback',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=8
                ))
            ],
            [
                Paragraph(f"<b>Prochain RDV:</b> {next_appointment}", ParagraphStyle(
                    'NextAppt',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=10
                ))
            ],
            [
                Paragraph("Signature Coach: ___________________", ParagraphStyle(
                    'CoachSignature',
                    fontSize=self.fonts["signature"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph("Signature Client: ___________________", ParagraphStyle(
                    'ClientSignature',
                    fontSize=self.fonts["signature"][1],
                    textColor=self.colors["text"],
                    alignment=TA_RIGHT
                ))
            ]
        ]

        summary_table = Table(summary_data, colWidths=[9*cm, 9*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["secondary"]),
            ('BACKGROUND', (0, 1), (-1, -2), self.colors["highlight"]),
            ('BACKGROUND', (0, -1), (-1, -1), self.colors["background"]),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["luxury"]),
            ('LINEABOVE', (0, -1), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        return summary_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Workout Premium",
            "category": "single_sessions",
            "description": "Format luxe personnalisé pour personal training haut de gamme",
            "target_audience": "Personal training haut de gamme, séances privées VIP",
            "features": [
                "Design luxueux et sophisticated",
                "Personnalisation extensive",
                "Notes de coaching détaillées",
                "Suivi des adaptations temps réel",
                "Éléments de branding premium",
                "Section signatures professionnelles"
            ],
            "color_scheme": "Luxury palette (charcoal, gold, platinum, cream)",
            "typography": "Elegant Times Roman family",
            "layout_style": "Executive luxury format",
            "complexity": "Advanced",
            "page_count": "2-3 pages",
            "data_requirements": [
                "title", "client_name", "coach_name", "session_date",
                "session_goals", "exercises", "coach_notes"
            ],
            "customization_options": [
                "Luxury level intensity",
                "Personalization depth",
                "Coaching detail level",
                "Premium branding elements"
            ]
        }