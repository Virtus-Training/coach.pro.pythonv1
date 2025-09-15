"""
Session Group Template - Professional template for group fitness and team training
Dynamic format designed for collective energy and team motivation
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Flowable,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from ..base_template import BaseTemplate


class SessionGroupTemplate(BaseTemplate):
    """
    Session Group Template

    Perfect for:
    - Group fitness classes
    - Team training sessions
    - Corporate wellness programs
    - Community fitness events
    - Boot camp style workouts
    - Team building activities

    Features:
    - High-energy dynamic design
    - Team motivation elements
    - Group progress tracking
    - Playlist integration
    - Level variations for participants
    - Team building components
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Group session configuration
        self.group_config = {
            "energy_level": "high",
            "team_focus": True,
            "motivation_elements": True,
            "level_variations": True,
            "group_dynamics": "collaborative",
            **self.config.get("group_config", {}),
        }

        # Dynamic group color palette - Energetic and motivating
        self.colors = {
            "primary": colors.Color(0.85, 0.11, 0.39),  # Dynamic magenta
            "secondary": colors.Color(0.11, 0.73, 0.95),  # Electric blue
            "accent": colors.Color(0.97, 0.61, 0.07),  # Energetic orange
            "background": colors.Color(0.97, 0.97, 0.97),  # Light background
            "text": colors.Color(0.13, 0.13, 0.13),  # Dark text
            "energy": colors.Color(0.89, 0.22, 0.11),  # Energy red
            "team": colors.Color(0.31, 0.78, 0.47),  # Team green
            "motivation": colors.Color(0.67, 0.12, 0.94),  # Motivation purple
            "highlight": colors.Color(1.0, 0.95, 0.0),  # Bright yellow
            **self.config.get("colors", {}),
        }

        # Dynamic typography - Bold and energetic
        self.fonts = {
            "title": ("Helvetica-Bold", 20),
            "subtitle": ("Helvetica-Bold", 16),
            "heading": ("Helvetica-Bold", 14),
            "body": ("Helvetica", 11),
            "caption": ("Helvetica", 9),
            "emphasis": ("Helvetica-Bold", 12),
            "energy": ("Helvetica-Bold", 18),
            **self.config.get("fonts", {}),
        }

        # Content validation
        self._validate_group_data()

    def _validate_group_data(self) -> None:
        """Validate that group session data is present"""
        required_fields = [
            "title",
            "instructor_name",
            "session_date",
            "group_size",
            "exercises",
            "playlist",
            "team_goals",
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_group_content(field)

    def _get_default_group_content(self, field: str) -> Any:
        """Provide default group content"""
        defaults = {
            "title": "Séance Collective Énergique",
            "instructor_name": "Coach Groupe",
            "session_date": "Date",
            "group_size": "12 participants",
            "exercises": [
                {
                    "name": "Échauffement Collectif",
                    "duration": "8 min",
                    "energy_level": "Montée en puissance",
                    "team_element": "Synchronisation groupe",
                    "variations": {
                        "débutant": "Amplitude réduite",
                        "intermédiaire": "Tempo normal",
                        "avancé": "Amplitude maximale",
                    },
                    "motivation": "Créer l'énergie de groupe",
                },
                {
                    "name": "Circuit Training Équipe",
                    "duration": "25 min",
                    "energy_level": "Haute intensité",
                    "team_element": "Rotation par équipes",
                    "variations": {
                        "débutant": "30s effort / 30s repos",
                        "intermédiaire": "40s effort / 20s repos",
                        "avancé": "50s effort / 10s repos",
                    },
                    "motivation": "Dépassement collectif",
                },
                {
                    "name": "Défi Équipe Final",
                    "duration": "12 min",
                    "energy_level": "Maximum",
                    "team_element": "Challenge collaboratif",
                    "variations": {
                        "débutant": "Objectif adapté",
                        "intermédiaire": "Objectif standard",
                        "avancé": "Objectif défi",
                    },
                    "motivation": "Victoire collective",
                },
                {
                    "name": "Récupération Groupe",
                    "duration": "5 min",
                    "energy_level": "Relaxation",
                    "team_element": "Cohésion et bilan",
                    "variations": {"tous": "Étirements synchronisés"},
                    "motivation": "Célébration des efforts",
                },
            ],
            "playlist": [
                {
                    "song": "Warm Up Energy",
                    "artist": "Motivation Mix",
                    "bpm": "120",
                    "phase": "Échauffement",
                },
                {
                    "song": "Beast Mode",
                    "artist": "Workout Heroes",
                    "bpm": "140",
                    "phase": "Circuit",
                },
                {
                    "song": "Team Power",
                    "artist": "Group Energy",
                    "bpm": "145",
                    "phase": "Défi",
                },
                {
                    "song": "Cool Victory",
                    "artist": "Relaxation",
                    "bpm": "90",
                    "phase": "Récupération",
                },
            ],
            "team_goals": [
                "Créer une synergie de groupe positive",
                "Encourager le dépassement mutuel",
                "Développer l'esprit d'équipe",
                "Maintenir l'énergie collective",
            ],
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete group session content"""
        content = []

        # Dynamic group header
        content.append(self._build_group_header())
        content.append(Spacer(1, 10 * mm))

        # Team composition and energy meter
        content.append(self._build_team_composition())
        content.append(Spacer(1, 8 * mm))

        # Group goals and team spirit
        content.append(self._build_team_goals())
        content.append(Spacer(1, 8 * mm))

        # Exercise program with variations
        content.extend(self._build_group_exercises())
        content.append(Spacer(1, 8 * mm))

        # Playlist and music integration
        content.append(self._build_playlist_section())
        content.append(Spacer(1, 8 * mm))

        # Team challenges and motivation
        content.append(self._build_team_challenges())
        content.append(Spacer(1, 6 * mm))

        # Group energy summary
        content.append(self._build_energy_summary())

        return content

    def _build_group_header(self) -> Table:
        """Build dynamic group session header"""
        title = self.data.get("title", "Séance Collective Énergique")
        instructor = self.data.get("instructor_name", "Coach Groupe")
        session_date = self.data.get("session_date", "Date")
        session_time = self.data.get("session_time", "Heure")
        group_size = self.data.get("group_size", "12 participants")
        location = self.data.get("location", "Salle de sport")

        header_data = [
            [
                Paragraph(
                    f"<b>🔥 {title.upper()} 🔥</b>",
                    ParagraphStyle(
                        "GroupTitle",
                        fontSize=self.fonts["title"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_CENTER,
                        spaceAfter=5,
                    ),
                ),
                "",
            ],
            [
                Paragraph(
                    "⚡ ÉNERGIE • ÉQUIPE • EXCELLENCE ⚡",
                    ParagraphStyle(
                        "Motto",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["energy"],
                        alignment=TA_CENTER,
                        spaceAfter=8,
                    ),
                ),
                "",
            ],
            [
                Paragraph(
                    f"<b>👨‍🏫 Instructeur:</b> {instructor}<br/><b>👥 Groupe:</b> {group_size}",
                    ParagraphStyle(
                        "InstructorInfo",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                    ),
                ),
                Paragraph(
                    f"<b>📅 Date:</b> {session_date}<br/><b>⏰ Heure:</b> {session_time}<br/><b>📍 Lieu:</b> {location}",
                    ParagraphStyle(
                        "SessionDetails",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["text"],
                        alignment=TA_RIGHT,
                    ),
                ),
            ],
        ]

        header_table = Table(header_data, colWidths=[9 * cm, 9 * cm])
        header_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 1), self.colors["highlight"]),
                    ("BACKGROUND", (0, 2), (-1, 2), self.colors["background"]),
                    ("SPAN", (0, 0), (1, 0)),
                    ("SPAN", (0, 1), (1, 1)),
                    ("BORDER", (0, 0), (-1, -1), 3, self.colors["primary"]),
                    ("LINEABOVE", (0, 0), (-1, 0), 4, self.colors["energy"]),
                    ("LINEBELOW", (0, -1), (-1, -1), 4, self.colors["energy"]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return header_table

    def _build_team_composition(self) -> Table:
        """Build team composition and energy level"""
        team_data = self.data.get(
            "team_composition",
            {"beginners": 4, "intermediate": 6, "advanced": 2, "total": 12},
        )

        energy_level = self.data.get("target_energy", "🔥🔥🔥🔥 MAXIMUM")

        composition_data = [
            [
                Paragraph(
                    "<b>🎯 COMPOSITION ÉQUIPE</b>",
                    ParagraphStyle(
                        "TeamTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                ),
                Paragraph(
                    "<b>⚡ NIVEAU D'ÉNERGIE CIBLE</b>",
                    ParagraphStyle(
                        "EnergyTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                ),
            ],
            [
                Paragraph(
                    f"🟢 <b>Débutants:</b> {team_data.get('beginners', 0)}<br/>"
                    f"🟡 <b>Intermédiaires:</b> {team_data.get('intermediate', 0)}<br/>"
                    f"🔴 <b>Avancés:</b> {team_data.get('advanced', 0)}<br/>"
                    f"👥 <b>Total:</b> {team_data.get('total', 0)}",
                    ParagraphStyle(
                        "TeamBreakdown",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                ),
                Paragraph(
                    f"<b>{energy_level}</b><br/><br/>🎵 Musique énergisante<br/>🏆 Défis collectifs<br/>🤝 Entraide obligatoire",
                    ParagraphStyle(
                        "EnergyDescription",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["energy"],
                        alignment=TA_CENTER,
                    ),
                ),
            ],
        ]

        composition_table = Table(composition_data, colWidths=[9 * cm, 9 * cm])
        composition_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["team"]),
                    ("BACKGROUND", (0, 1), (-1, 1), self.colors["background"]),
                    ("BORDER", (0, 0), (-1, -1), 2, self.colors["secondary"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return composition_table

    def _build_team_goals(self) -> Table:
        """Build team goals and collective objectives"""
        team_goals = self.data.get("team_goals", [])

        goals_data = [
            [
                Paragraph(
                    "<b>🎯 OBJECTIFS COLLECTIFS - ENSEMBLE VERS LA VICTOIRE</b>",
                    ParagraphStyle(
                        "TeamGoalsTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        team_icons = ["🤝", "💪", "🏆", "⚡", "🔥", "🎯"]
        for i, goal in enumerate(team_goals):
            icon = team_icons[i % len(team_icons)]
            goals_data.append(
                [
                    Paragraph(
                        f"{icon} {goal}",
                        ParagraphStyle(
                            "TeamGoal",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=10,
                            spaceAfter=4,
                        ),
                    )
                ]
            )

        goals_table = Table(goals_data, colWidths=[18 * cm])
        goals_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["motivation"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("BORDER", (0, 0), (-1, -1), 2, self.colors["accent"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return goals_table

    def _build_group_exercises(self) -> List[Flowable]:
        """Build group exercises with level variations"""
        exercises = self.data.get("exercises", [])
        content = []

        # Exercises header
        content.append(
            Paragraph(
                "<b>💪 PROGRAMME COLLECTIF - ADAPTATION POUR TOUS 💪</b>",
                ParagraphStyle(
                    "ExercisesTitle",
                    fontSize=self.fonts["heading"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER,
                    spaceAfter=8,
                ),
            )
        )

        for i, exercise in enumerate(exercises):
            exercise_name = exercise.get("name", f"Exercice {i + 1}")
            duration = exercise.get("duration", "")
            energy_level = exercise.get("energy_level", "")
            team_element = exercise.get("team_element", "")
            variations = exercise.get("variations", {})
            motivation = exercise.get("motivation", "")

            # Exercise card with dynamic styling
            exercise_data = [
                [
                    Paragraph(
                        f"<b>{i + 1}. {exercise_name}</b>",
                        ParagraphStyle(
                            "ExerciseName",
                            fontSize=self.fonts["subtitle"][1],
                            textColor=colors.white,
                            alignment=TA_LEFT,
                        ),
                    ),
                    Paragraph(
                        f"<b>⏱️ {duration}</b><br/>⚡ {energy_level}",
                        ParagraphStyle(
                            "ExerciseSpecs",
                            fontSize=self.fonts["body"][1],
                            textColor=colors.white,
                            alignment=TA_CENTER,
                        ),
                    ),
                ],
                [
                    Paragraph(
                        f"<b>🤝 Élément d'équipe:</b> {team_element}",
                        ParagraphStyle(
                            "TeamElement",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["team"],
                            alignment=TA_LEFT,
                            spaceAfter=5,
                        ),
                    ),
                    "",
                ],
                [
                    Paragraph(
                        f"<b>🎯 Motivation:</b> <i>{motivation}</i>",
                        ParagraphStyle(
                            "Motivation",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["motivation"],
                            alignment=TA_LEFT,
                            spaceAfter=5,
                        ),
                    ),
                    "",
                ],
            ]

            # Add variations section
            if variations:
                variations_text = "<b>📊 Variations par niveau:</b><br/>"
                level_colors = {
                    "débutant": "🟢",
                    "intermédiaire": "🟡",
                    "avancé": "🔴",
                    "tous": "🟦",
                }

                for level, variation in variations.items():
                    icon = level_colors.get(level, "•")
                    variations_text += (
                        f"{icon} <b>{level.title()}:</b> {variation}<br/>"
                    )

                exercise_data.append(
                    [
                        Paragraph(
                            variations_text,
                            ParagraphStyle(
                                "Variations",
                                fontSize=self.fonts["caption"][1],
                                textColor=self.colors["text"],
                                alignment=TA_LEFT,
                                leftIndent=10,
                            ),
                        ),
                        "",
                    ]
                )

            exercise_table = Table(exercise_data, colWidths=[12 * cm, 6 * cm])

            # Dynamic color based on exercise position
            header_color = [
                self.colors["primary"],
                self.colors["secondary"],
                self.colors["accent"],
                self.colors["energy"],
            ][i % 4]

            exercise_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), header_color),
                        ("BACKGROUND", (0, 1), (-1, -1), self.colors["background"]),
                        ("SPAN", (0, 1), (1, 1)),
                        ("SPAN", (0, 2), (1, 2)),
                        ("SPAN", (0, 3), (1, 3))
                        if len(exercise_data) > 3
                        else ("SPAN", (0, 2), (1, 2)),
                        ("BORDER", (0, 0), (-1, -1), 2, header_color),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )

            content.append(exercise_table)
            if i < len(exercises) - 1:
                content.append(Spacer(1, 6 * mm))

        return content

    def _build_playlist_section(self) -> Table:
        """Build playlist integration section"""
        playlist = self.data.get("playlist", [])

        playlist_data = [
            [
                Paragraph(
                    "<b>🎵 PLAYLIST ÉNERGIQUE - MUSIQUE = MOTIVATION</b>",
                    ParagraphStyle(
                        "PlaylistTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ],
            [
                Paragraph(
                    "<b>Titre</b>",
                    ParagraphStyle(
                        "PlaylistHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                    ),
                ),
                Paragraph(
                    "<b>Artiste</b>",
                    ParagraphStyle(
                        "PlaylistHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                    ),
                ),
                Paragraph(
                    "<b>BPM</b>",
                    ParagraphStyle(
                        "PlaylistHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_CENTER,
                    ),
                ),
                Paragraph(
                    "<b>Phase</b>",
                    ParagraphStyle(
                        "PlaylistHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_CENTER,
                    ),
                ),
            ],
        ]

        for song in playlist:
            song_title = song.get("song", "")
            artist = song.get("artist", "")
            bpm = song.get("bpm", "")
            phase = song.get("phase", "")

            playlist_data.append(
                [
                    Paragraph(
                        f"🎵 {song_title}",
                        ParagraphStyle(
                            "SongTitle",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                        ),
                    ),
                    Paragraph(
                        artist,
                        ParagraphStyle(
                            "Artist",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                        ),
                    ),
                    Paragraph(
                        f"<b>{bpm}</b>",
                        ParagraphStyle(
                            "BPM",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["energy"],
                            alignment=TA_CENTER,
                        ),
                    ),
                    Paragraph(
                        phase,
                        ParagraphStyle(
                            "Phase",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["secondary"],
                            alignment=TA_CENTER,
                        ),
                    ),
                ]
            )

        playlist_table = Table(
            playlist_data, colWidths=[6 * cm, 5 * cm, 3 * cm, 4 * cm]
        )
        playlist_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["accent"]),
                    ("BACKGROUND", (0, 1), (-1, 1), self.colors["highlight"]),
                    ("BACKGROUND", (0, 2), (-1, -1), self.colors["background"]),
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["secondary"]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return playlist_table

    def _build_team_challenges(self) -> Table:
        """Build team challenges and group motivation"""
        challenges = self.data.get(
            "team_challenges",
            [
                {
                    "challenge": "Synchronisation parfaite",
                    "points": "50",
                    "difficulty": "🟡",
                },
                {
                    "challenge": "Encouragements continus",
                    "points": "30",
                    "difficulty": "🟢",
                },
                {
                    "challenge": "Dépassement collectif",
                    "points": "100",
                    "difficulty": "🔴",
                },
                {"challenge": "Esprit d'équipe", "points": "40", "difficulty": "🟢"},
            ],
        )

        challenges_data = [
            [
                Paragraph(
                    "<b>🏆 DÉFIS ÉQUIPE - POINTS DE MOTIVATION 🏆</b>",
                    ParagraphStyle(
                        "ChallengesTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ],
            [
                Paragraph(
                    "<b>Défi</b>",
                    ParagraphStyle(
                        "ChallengeHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["team"],
                        alignment=TA_LEFT,
                    ),
                ),
                Paragraph(
                    "<b>Points</b>",
                    ParagraphStyle(
                        "ChallengeHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["team"],
                        alignment=TA_CENTER,
                    ),
                ),
                Paragraph(
                    "<b>Difficulté</b>",
                    ParagraphStyle(
                        "ChallengeHeader",
                        fontSize=self.fonts["emphasis"][1],
                        textColor=self.colors["team"],
                        alignment=TA_CENTER,
                    ),
                ),
            ],
        ]

        for challenge in challenges:
            challenge_name = challenge.get("challenge", "")
            points = challenge.get("points", "0")
            difficulty = challenge.get("difficulty", "🟢")

            challenges_data.append(
                [
                    Paragraph(
                        f"🎯 {challenge_name}",
                        ParagraphStyle(
                            "Challenge",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                        ),
                    ),
                    Paragraph(
                        f"<b>{points}</b>",
                        ParagraphStyle(
                            "Points",
                            fontSize=self.fonts["emphasis"][1],
                            textColor=self.colors["energy"],
                            alignment=TA_CENTER,
                        ),
                    ),
                    Paragraph(
                        difficulty,
                        ParagraphStyle(
                            "Difficulty",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_CENTER,
                        ),
                    ),
                ]
            )

        challenges_table = Table(challenges_data, colWidths=[10 * cm, 4 * cm, 4 * cm])
        challenges_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["motivation"]),
                    ("BACKGROUND", (0, 1), (-1, 1), self.colors["highlight"]),
                    ("BACKGROUND", (0, 2), (-1, -1), self.colors["background"]),
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BORDER", (0, 0), (-1, -1), 2, self.colors["team"]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return challenges_table

    def _build_energy_summary(self) -> Table:
        """Build group energy summary and team celebration"""
        total_energy = self.data.get("total_energy_achieved", "🔥🔥🔥🔥 95%")
        team_spirit = self.data.get("team_spirit_rating", "Excellent")
        group_feedback = self.data.get(
            "group_feedback", "Énergie incroyable ! On recommence quand ?"
        )
        next_session = self.data.get(
            "next_group_session", "Même jour, semaine prochaine"
        )

        summary_data = [
            [
                Paragraph(
                    "<b>⚡ BILAN ÉNERGÉTIQUE DU GROUPE ⚡</b>",
                    ParagraphStyle(
                        "SummaryTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ],
            [
                Paragraph(
                    f"<b>🔥 Énergie Totale Atteinte:</b> {total_energy}",
                    ParagraphStyle(
                        "EnergyTotal",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["energy"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                )
            ],
            [
                Paragraph(
                    f"<b>🤝 Esprit d'équipe:</b> {team_spirit}",
                    ParagraphStyle(
                        "TeamSpirit",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["team"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                )
            ],
            [
                Paragraph(
                    f'<b>💬 Retour du groupe:</b><br/><i>"{group_feedback}"</i>',
                    ParagraphStyle(
                        "GroupFeedback",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                        spaceAfter=8,
                    ),
                )
            ],
            [
                Paragraph(
                    f"<b>🗓️ Prochaine séance collective:</b> {next_session}",
                    ParagraphStyle(
                        "NextSession",
                        fontSize=self.fonts["body"][1],
                        textColor=self.colors["motivation"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                )
            ],
            [
                Paragraph(
                    "🏆 <b>BRAVO À TOUTE L'ÉQUIPE !</b> 🏆",
                    ParagraphStyle(
                        "Celebration",
                        fontSize=self.fonts["energy"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_CENTER,
                    ),
                )
            ],
        ]

        summary_table = Table(summary_data, colWidths=[18 * cm])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["secondary"]),
                    ("BACKGROUND", (0, 1), (0, -2), self.colors["background"]),
                    ("BACKGROUND", (0, -1), (0, -1), self.colors["highlight"]),
                    ("BORDER", (0, 0), (-1, -1), 3, self.colors["primary"]),
                    ("LINEABOVE", (0, -1), (-1, -1), 2, self.colors["energy"]),
                    ("LINEBELOW", (0, -1), (-1, -1), 2, self.colors["energy"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 15),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return summary_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Group Energy",
            "category": "single_sessions",
            "description": "Format dynamique pour cours collectifs et team training",
            "target_audience": "Cours collectifs, team training, événements fitness",
            "features": [
                "Design haute énergie",
                "Éléments de motivation d'équipe",
                "Suivi des progrès collectifs",
                "Intégration playlist musicale",
                "Variations par niveau",
                "Défis et challenges collaboratifs",
            ],
            "color_scheme": "Dynamic energetic colors (magenta, electric blue, orange)",
            "typography": "Bold Helvetica for high impact",
            "layout_style": "High-energy group format",
            "complexity": "Intermediate",
            "page_count": "2-3 pages",
            "data_requirements": [
                "title",
                "instructor_name",
                "session_date",
                "group_size",
                "exercises",
                "playlist",
                "team_goals",
            ],
            "customization_options": [
                "Energy level intensity",
                "Group size adaptation",
                "Team challenge difficulty",
                "Musical integration level",
            ],
        }
