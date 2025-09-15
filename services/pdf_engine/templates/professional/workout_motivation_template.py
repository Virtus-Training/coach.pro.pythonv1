"""
Motivation+ Workout Template - Energetic gamified design
High-engagement template for fitness enthusiasts and beginners
Target: Fitness grand public, débutants, groupe classes
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from ...components.professional_components import (
    MotivationalBadgeComponent,
    ProgressBarComponent,
)
from ..base_template import BaseTemplate


class WorkoutMotivationTemplate(BaseTemplate):
    """
    Motivation+ Template - Energetic design with gamification elements
    Designed to maximize engagement and motivation for fitness journey
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "energetic_vibrant",
            "layout": "card_dynamic",
            "gamification": True,
            "motivation_level": "high",
            "color_intensity": "vibrant",
            "colors": {
                "primary": "#e53e3e",
                "secondary": "#fd7e14",
                "accent": "#38d9a9",
                "background": "#ffffff",
                "surface": "#fff5f5",
                "text_primary": "#2d3748",
                "text_secondary": "#718096",
                "success": "#48bb78",
                "warning": "#ed8936",
                "energy": "#ff6b35",
                "achievement": "#ffd700",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 26},
                "subtitle": {"name": "Helvetica-Bold", "size": 20},
                "heading": {"name": "Helvetica-Bold", "size": 15},
                "body": {"name": "Helvetica", "size": 11},
                "caption": {"name": "Helvetica", "size": 9},
                "motivational": {"name": "Helvetica-Bold", "size": 13},
            },
            "layout": {
                "margins": {"top": 50, "bottom": 50, "left": 40, "right": 40},
                "header_height": 120,
                "footer_height": 50,
                "block_spacing": 20,
                "card_style": True,
            },
            "gamification": {
                "show_badges": True,
                "show_progress_bars": True,
                "show_achievements": True,
                "show_motivational_quotes": True,
                "point_system": True,
            },
        }

    def _build_content(self) -> List[Any]:
        """Build motivational workout content with gamification elements"""
        elements = []

        # Energetic header with motivational messaging
        elements.append(self._build_energetic_header())
        elements.append(Spacer(1, 15))

        # Achievement dashboard with badges and progress
        elements.append(self._build_achievement_dashboard())
        elements.append(Spacer(1, 20))

        # Motivational quote section
        elements.append(self._build_motivational_section())
        elements.append(Spacer(1, 15))

        # Goal tracking with visual progress
        elements.append(self._build_goal_tracking())
        elements.append(Spacer(1, 20))

        # Energetic workout blocks with card styling
        elements.extend(self._build_energetic_workout_blocks())

        # Challenge and reward section
        elements.append(self._build_challenge_section())

        # Team motivation (if group workout)
        if self.data.get("is_group_session", False):
            elements.append(self._build_team_motivation())

        return elements

    def _build_energetic_header(self) -> Table:
        """Build high-energy header with dynamic styling"""
        title = self.data.get("title", "💪 PROGRAMME MOTIVATION+ 💪")
        client_name = self.data.get("client_name", "Champion")
        session_number = self.data.get("session_number", 1)

        # Create energetic header with emoji and dynamic text
        header_data = [
            [f"🔥 {title.upper()} 🔥"],
            [f"Salut {client_name} ! Prêt(e) pour ta séance #{session_number} ?"],
            ["🚀 C'EST PARTI POUR DÉCHIRER ! 🚀"],
        ]

        header_table = Table(header_data, colWidths=[6 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    # Main title
                    ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (0, 0), 24),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    # Subtitle
                    ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 1), (0, 1), 16),
                    (
                        "TEXTCOLOR",
                        (0, 1),
                        (0, 1),
                        HexColor(self.merged_config["colors"]["text_primary"]),
                    ),
                    # Energy message
                    ("FONTNAME", (0, 2), (0, 2), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 2), (0, 2), 14),
                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (0, 2),
                        HexColor(self.merged_config["colors"]["energy"]),
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
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return header_table

    def _build_achievement_dashboard(self) -> Table:
        """Build gamified achievement dashboard with badges and progress"""
        achievements = self.data.get("achievements", {})

        # Create achievement badges
        badge_data = [
            ("streak", achievements.get("current_streak", 0), "🔥"),
            ("personal_best", achievements.get("personal_bests", 0), "🏆"),
            ("consistency", achievements.get("consistency_score", 0), "✅"),
            ("achievement", achievements.get("total_achievements", 0), "⭐"),
        ]

        badge_row = []
        for badge_type, value, emoji in badge_data:
            badge = MotivationalBadgeComponent(
                badge_type, str(value), width=70, height=70
            )
            badge_row.append([badge, f"{emoji} {value}"])

        # Progress towards goals
        goal_progress = achievements.get("goal_progress", 65)
        weekly_progress = achievements.get("weekly_progress", 80)

        progress_section = [
            ["🎯 PROGRESSION VERS TES OBJECTIFS 🎯"],
            [ProgressBarComponent(goal_progress, 100, 200, 20, "#48bb78", "#81c784")],
            [f"Objectif principal: {goal_progress}% complété"],
            [ProgressBarComponent(weekly_progress, 100, 200, 20, "#3182ce", "#63b3ed")],
            [f"Objectif hebdomadaire: {weekly_progress}% complété"],
        ]

        # Combine badges and progress
        dashboard_data = [
            badge_row[:2],  # First row of badges
            badge_row[2:],  # Second row of badges
            progress_section,
        ]

        dashboard = Table(dashboard_data, colWidths=[3 * inch, 3 * inch])
        dashboard.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        2,
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f0fff4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return dashboard

    def _build_motivational_section(self) -> Table:
        """Build motivational quotes and affirmations section"""
        quotes = self.data.get(
            "motivational_quotes",
            [
                "💪 Tu es plus fort(e) que tes excuses !",
                "🚀 Chaque répétition te rapproche de ton objectif !",
                "🔥 Ton seul concurrent, c'est toi d'hier !",
            ],
        )

        quote_of_day = quotes[0] if quotes else "💪 Tu vas y arriver !"

        motivation_data = [
            ["🌟 MOTIVATION DU JOUR 🌟"],
            [quote_of_day],
            ["🎯 Aujourd'hui, tu deviens une meilleure version de toi-même ! 🎯"],
        ]

        motivation_table = Table(motivation_data, colWidths=[6 * inch])
        motivation_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (0, 0), 16),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, 0),
                        HexColor(self.merged_config["colors"]["achievement"]),
                    ),
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#fffbeb")),
                    # Quote
                    ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 1), (0, 1), 14),
                    (
                        "TEXTCOLOR",
                        (0, 1),
                        (0, 1),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    # Affirmation
                    ("FONTNAME", (0, 2), (0, 2), "Helvetica-Oblique"),
                    ("FONTSIZE", (0, 2), (0, 2), 12),
                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (0, 2),
                        HexColor(self.merged_config["colors"]["text_secondary"]),
                    ),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["achievement"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return motivation_table

    def _build_goal_tracking(self) -> Table:
        """Build visual goal tracking with progress indicators"""
        goals = self.data.get("session_goals", {})

        goal_data = [
            ["📊 TES OBJECTIFS POUR CETTE SÉANCE 📊", "", ""],
            ["Objectif", "Cible", "Progression"],
            [
                "💪 Force",
                goals.get("strength_target", "Maintenir niveau"),
                ProgressBarComponent(goals.get("strength_progress", 50), 100, 100, 15),
            ],
            [
                "❤️ Cardio",
                goals.get("cardio_target", "Zone 2-3"),
                ProgressBarComponent(goals.get("cardio_progress", 70), 100, 100, 15),
            ],
            [
                "🎯 Technique",
                goals.get("technique_target", "Parfaire mouvement"),
                ProgressBarComponent(goals.get("technique_progress", 85), 100, 100, 15),
            ],
            [
                "🧘 Mental",
                goals.get("mental_target", "Concentration"),
                ProgressBarComponent(goals.get("mental_progress", 60), 100, 100, 15),
            ],
        ]

        goal_table = Table(goal_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        goal_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["secondary"]),
                    ),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return goal_table

    def _build_energetic_workout_blocks(self) -> List[Any]:
        """Build workout blocks with high-energy card styling"""
        elements = []
        blocks = self.data.get("workout_blocks", [])

        if not blocks:
            blocks = self._generate_default_motivation_blocks()

        for i, block in enumerate(blocks):
            # Energetic block header with emoji and color
            block_emoji = ["🔥", "💪", "⚡", "🚀", "💥"][i % 5]
            header_color = [
                self.merged_config["colors"]["primary"],
                self.merged_config["colors"]["secondary"],
                self.merged_config["colors"]["accent"],
                self.merged_config["colors"]["energy"],
                self.merged_config["colors"]["success"],
            ][i % 5]

            block_title = Paragraph(
                f"<b>{block_emoji} BLOC {i + 1}: {block.get('title', 'Exercices').upper()} {block_emoji}</b>",
                self.styles["heading"],
            )
            elements.append(block_title)
            elements.append(Spacer(1, 10))

            # Motivation block component with card styling
            motivational_block = self._build_motivational_block_card(
                block, header_color
            )
            elements.append(motivational_block)
            elements.append(Spacer(1, 15))

            # Encouragement after each block
            encouragement = self._get_block_encouragement(i, len(blocks))
            if encouragement:
                elements.append(encouragement)
                elements.append(Spacer(1, 10))

        return elements

    def _build_motivational_block_card(
        self, block: Dict[str, Any], header_color: str
    ) -> Table:
        """Build workout block as motivational card"""
        exercises = block.get("exercises", [])
        duration = block.get("duration", 0)
        format_type = block.get("format", "LIBRE")

        # Block info header
        info_data = [[f"⏱️ Durée: {duration} min", f"📋 Format: {format_type}"]]

        # Exercises with motivational styling
        exercise_data = []
        for i, exercise in enumerate(exercises):
            exercise_emoji = ["🏋️", "🤸", "🏃", "🧘", "💪"][i % 5]
            exercise_row = [
                f"{exercise_emoji} {exercise.get('name', 'Exercise')}",
                exercise.get("reps", ""),
                exercise.get("notes", ""),
            ]
            exercise_data.append(exercise_row)

        # Combine info and exercises
        card_data = info_data + [["Exercice", "Répétitions", "Notes"]] + exercise_data

        card_table = Table(card_data, colWidths=[2.5 * inch, 1.5 * inch, 2 * inch])
        card_table.setStyle(
            TableStyle(
                [
                    # Info header
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor(header_color)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    # Exercise header
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    # Exercise rows - alternating colors
                    ("GRID", (0, 0), (-1, -1), 1, HexColor("#e2e8f0")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        # Add alternating row colors for exercises
        for i in range(2, len(card_data)):
            if i % 2 == 0:
                card_table.setStyle(
                    TableStyle([("BACKGROUND", (0, i), (-1, i), HexColor("#fafafa"))])
                )

        return card_table

    def _get_block_encouragement(
        self, block_index: int, total_blocks: int
    ) -> Optional[Paragraph]:
        """Get motivational encouragement after each block"""
        encouragements = [
            "🎉 Excellent début ! Tu gères comme un(e) champion(ne) !",
            "💪 Tu sens cette énergie ? C'est toi qui deviens plus fort(e) !",
            "🚀 Incroyable ! Tu es en feu ! Continue comme ça !",
            "⭐ Waouh ! Tu dépasses mes attentes ! Garde cette intensité !",
            "🏆 BRAVO ! Tu viens de terminer un entraînement de guerrier(ère) !",
        ]

        if block_index < len(encouragements):
            encouragement_text = encouragements[block_index]
            style = self.styles["body"].clone("encouragement")
            style.textColor = HexColor(self.merged_config["colors"]["success"])
            style.fontSize = 12
            style.fontName = "Helvetica-Bold"
            style.alignment = TA_CENTER

            return Paragraph(encouragement_text, style)

        return None

    def _build_challenge_section(self) -> Table:
        """Build challenge and reward section"""
        challenges = self.data.get("challenges", {})

        challenge_data = [
            ["🏆 DÉFIS ET RÉCOMPENSES 🏆"],
            [
                "💎 Défi Principal",
                challenges.get(
                    "main_challenge",
                    "Complète tous les exercices avec une forme parfaite",
                ),
            ],
            [
                "⚡ Défi Bonus",
                challenges.get(
                    "bonus_challenge", "Améliore d'1 répétition ton record personnel"
                ),
            ],
            [
                "🎁 Récompense",
                challenges.get(
                    "reward", "Tu mérites une boisson protéinée délicieuse ! 🥤"
                ),
            ],
        ]

        challenge_table = Table(challenge_data, colWidths=[1.5 * inch, 4.5 * inch])
        challenge_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 16),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["achievement"]),
                    ),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 11),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, HexColor("#ffd700")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#fffbeb")),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return challenge_table

    def _build_team_motivation(self) -> Table:
        """Build team motivation section for group sessions"""
        team_data = self.data.get("team_data", {})

        team_table_data = [
            ["👥 MOTIVATION D'ÉQUIPE 👥"],
            ["🔥 Énergie Collective", "📈 Progression Groupe", "🏆 Objectif Commun"],
            [
                team_data.get("energy_level", "MAXIMALE ! 💯"),
                team_data.get("group_progress", "En route vers l'excellence !"),
                team_data.get("team_goal", "Dépasser nos limites ensemble !"),
            ],
            ["💪 Ensemble, nous sommes UNSTOPPABLES ! 💪"],
        ]

        team_table = Table(team_table_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        team_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("SPAN", (0, 3), (-1, 3)),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 16),
                    ("FONTSIZE", (0, 3), (-1, 3), 14),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    (
                        "TEXTCOLOR",
                        (0, 3),
                        (-1, 3),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    # Content
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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

        return team_table

    def _generate_default_motivation_blocks(self) -> List[Dict[str, Any]]:
        """Generate default motivational workout structure"""
        return [
            {
                "title": "Réveil Musculaire Explosif",
                "duration": 8,
                "format": "ÉCHAUFFEMENT",
                "exercises": [
                    {
                        "name": "Jumping Jacks Énergiques",
                        "reps": "2x20",
                        "notes": "Réveil complet du corps ! 🔥",
                    },
                    {
                        "name": "High Knees Dynamiques",
                        "reps": "2x15",
                        "notes": "Monte ces genoux ! 💪",
                    },
                    {
                        "name": "Arm Circles Power",
                        "reps": "2x10",
                        "notes": "Prépare tes épaules ! ⚡",
                    },
                ],
            },
            {
                "title": "Zone de Combat Principal",
                "duration": 25,
                "format": "HIIT INTENSIF",
                "exercises": [
                    {
                        "name": "Burpees Warrior",
                        "reps": "4x8",
                        "notes": "Tu es un(e) guerrier(ère) ! 🏹",
                    },
                    {
                        "name": "Push-Ups Explosive",
                        "reps": "4x10",
                        "notes": "Explose vers le haut ! 🚀",
                    },
                    {
                        "name": "Squats Jump Power",
                        "reps": "4x12",
                        "notes": "Saute comme un champion ! 🏆",
                    },
                    {
                        "name": "Mountain Climbers Fury",
                        "reps": "4x20",
                        "notes": "Grimpe cette montagne ! ⛰️",
                    },
                ],
            },
            {
                "title": "Récupération de Champion",
                "duration": 12,
                "format": "COOLDOWN ACTIF",
                "exercises": [
                    {
                        "name": "Étirements Victory",
                        "reps": "5x30s",
                        "notes": "Célèbre ta victoire ! 🎉",
                    },
                    {
                        "name": "Respiration Zen Master",
                        "reps": "3x10",
                        "notes": "Respire ta réussite ! 🧘",
                    },
                    {
                        "name": "Gratitude Stretch",
                        "reps": "5min",
                        "notes": "Remercie ton corps ! 🙏",
                    },
                ],
            },
        ]

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Motivation template data requirements"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "session_number": {"type": "integer"},
                "is_group_session": {"type": "boolean"},
                "achievements": {
                    "type": "object",
                    "properties": {
                        "current_streak": {"type": "integer"},
                        "personal_bests": {"type": "integer"},
                        "consistency_score": {"type": "integer"},
                        "total_achievements": {"type": "integer"},
                        "goal_progress": {"type": "number"},
                        "weekly_progress": {"type": "number"},
                    },
                },
                "motivational_quotes": {"type": "array", "items": {"type": "string"}},
                "session_goals": {
                    "type": "object",
                    "properties": {
                        "strength_target": {"type": "string"},
                        "strength_progress": {"type": "number"},
                        "cardio_target": {"type": "string"},
                        "cardio_progress": {"type": "number"},
                        "technique_target": {"type": "string"},
                        "technique_progress": {"type": "number"},
                        "mental_target": {"type": "string"},
                        "mental_progress": {"type": "number"},
                    },
                },
                "workout_blocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "duration": {"type": "integer"},
                            "format": {"type": "string"},
                            "exercises": {"type": "array"},
                        },
                    },
                },
                "challenges": {
                    "type": "object",
                    "properties": {
                        "main_challenge": {"type": "string"},
                        "bonus_challenge": {"type": "string"},
                        "reward": {"type": "string"},
                    },
                },
                "team_data": {
                    "type": "object",
                    "properties": {
                        "energy_level": {"type": "string"},
                        "group_progress": {"type": "string"},
                        "team_goal": {"type": "string"},
                    },
                },
            },
            "required": ["title", "client_name"],
        }
