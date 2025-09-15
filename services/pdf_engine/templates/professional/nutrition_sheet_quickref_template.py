"""
Quick Reference Nutrition Sheet Template - Professional template for rapid consultation
Concise and actionable format for quick reference and daily use
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


class NutritionSheetQuickRefTemplate(BaseTemplate):
    """
    Quick Reference Nutrition Sheet Template

    Perfect for:
    - Quick consultation during busy days
    - Pocket guides for clients
    - Emergency nutrition reference
    - Daily habit reminders
    - On-the-go decision making

    Features:
    - Ultra-concise format
    - Action-oriented content
    - Visual quick-scan elements
    - Memorable formatting
    - Essential information only
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Quick reference specific configuration
        self.quickref_config = {
            "density": "ultra_high",
            "action_focused": True,
            "visual_shortcuts": True,
            "memorable_format": True,
            "emergency_info": True,
            **self.config.get("quickref_config", {}),
        }

        # Quick reference color scheme - High contrast and memorable
        self.colors = {
            "primary": colors.Color(0.85, 0.11, 0.14),  # Emergency red
            "secondary": colors.Color(0.11, 0.56, 0.25),  # Action green
            "accent": colors.Color(1.0, 0.65, 0.0),  # Warning orange
            "background": colors.Color(0.95, 0.95, 0.95),  # Light grey
            "text": colors.Color(0.1, 0.1, 0.1),  # Nearly black
            "highlight": colors.Color(1.0, 1.0, 0.7),  # Yellow highlight
            "urgent": colors.Color(0.8, 0.0, 0.0),  # Urgent red
            "good": colors.Color(0.0, 0.6, 0.0),  # Good green
            **self.config.get("colors", {}),
        }

        # Quick reference typography - Bold and scannable
        self.fonts = {
            "title": ("Helvetica-Bold", 18),
            "subtitle": ("Helvetica-Bold", 14),
            "heading": ("Helvetica-Bold", 12),
            "body": ("Helvetica-Bold", 11),
            "caption": ("Helvetica", 9),
            "emphasis": ("Helvetica-Bold", 11),
            "large": ("Helvetica-Bold", 16),
            **self.config.get("fonts", {}),
        }

        # Content validation
        self._validate_quickref_data()

    def _validate_quickref_data(self) -> None:
        """Validate that quick reference specific data is present"""
        required_fields = [
            "title",
            "quick_actions",
            "emergency_tips",
            "daily_reminders",
            "key_numbers",
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_quickref_content(field)

    def _get_default_quickref_content(self, field: str) -> Any:
        """Provide default quick reference content"""
        defaults = {
            "title": "Aide-Mémoire Nutrition",
            "quick_actions": [
                {
                    "action": "Boire 1 verre d'eau",
                    "trigger": "Avant chaque repas",
                    "benefit": "Satiété",
                },
                {
                    "action": "Manger 1 fruit",
                    "trigger": "Entre les repas",
                    "benefit": "Vitamines",
                },
                {
                    "action": "Prendre 10 respirations",
                    "trigger": "Avant de manger",
                    "benefit": "Mindfulness",
                },
                {
                    "action": "Mastiquer 20 fois",
                    "trigger": "Chaque bouchée",
                    "benefit": "Digestion",
                },
            ],
            "emergency_tips": [
                {
                    "situation": "Fringale sucrée",
                    "solution": "Pomme + 10 amandes",
                    "why": "Fibres + protéines",
                },
                {
                    "situation": "Fatigue après-midi",
                    "solution": "Thé vert + carré chocolat",
                    "why": "Théine + antioxydants",
                },
                {
                    "situation": "Repas manqué",
                    "solution": "Smoothie protéiné",
                    "why": "Récupération rapide",
                },
                {
                    "situation": "Restaurant",
                    "solution": "Légumes d'abord",
                    "why": "Contrôle portions",
                },
            ],
            "daily_reminders": [
                "💧 8 verres d'eau minimum",
                "🥬 5 portions fruits/légumes",
                "🥗 Légumes à chaque repas",
                "🍎 Collation si > 4h entre repas",
                "⏰ Arrêter de manger 3h avant coucher",
            ],
            "key_numbers": [
                {
                    "metric": "Eau",
                    "value": "35ml",
                    "unit": "par kg de poids",
                    "note": "Base hydratation",
                },
                {
                    "metric": "Protéines",
                    "value": "1.2g",
                    "unit": "par kg de poids",
                    "note": "Sédentaires",
                },
                {
                    "metric": "Fibres",
                    "value": "25-30g",
                    "unit": "par jour",
                    "note": "Digestif",
                },
                {
                    "metric": "Omega-3",
                    "value": "2-3g",
                    "unit": "par semaine",
                    "note": "Poissons gras",
                },
            ],
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete quick reference sheet content"""
        content = []

        # Compact header with emergency contact style
        content.append(self._build_quickref_header())
        content.append(Spacer(1, 8 * mm))

        # Quick actions in emergency card format
        content.append(self._build_quick_actions_section())
        content.append(Spacer(1, 6 * mm))

        # Emergency situations and solutions
        content.append(self._build_emergency_section())
        content.append(Spacer(1, 6 * mm))

        # Daily reminders checklist
        content.append(self._build_daily_reminders())
        content.append(Spacer(1, 6 * mm))

        # Key numbers reference table
        content.append(self._build_key_numbers_section())
        content.append(Spacer(1, 6 * mm))

        # Quick decision flowchart
        content.append(self._build_decision_flowchart())

        return content

    def _build_quickref_header(self) -> Table:
        """Build emergency-style header for quick identification"""
        title = self.data.get("title", "Aide-Mémoire Nutrition")
        subtitle = self.data.get("subtitle", "GUIDE RAPIDE - CONSULTEZ EN CAS DE DOUTE")
        date = self.data.get("date", "")

        # Emergency contact card style header
        header_data = [
            [
                Paragraph(
                    f"<b>🆘 {title.upper()}</b>",
                    ParagraphStyle(
                        "EmergencyTitle",
                        fontSize=self.fonts["title"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                        spaceAfter=3,
                    ),
                )
            ],
            [
                Paragraph(
                    subtitle,
                    ParagraphStyle(
                        "EmergencySubtitle",
                        fontSize=self.fonts["caption"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ],
        ]

        if date:
            header_data.append(
                [
                    Paragraph(
                        f"Édition: {date}",
                        ParagraphStyle(
                            "Date",
                            fontSize=self.fonts["caption"][1],
                            textColor=colors.white,
                            alignment=TA_CENTER,
                        ),
                    )
                ]
            )

        header_table = Table(header_data, colWidths=[18 * cm])
        header_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), self.colors["primary"]),
                    ("BORDER", (0, 0), (-1, -1), 3, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return header_table

    def _build_quick_actions_section(self) -> Table:
        """Build quick actions in emergency response format"""
        actions = self.data.get("quick_actions", [])

        action_data = [
            [
                Paragraph(
                    "<b>⚡ ACTIONS RAPIDES - EN CAS DE BESOIN</b>",
                    ParagraphStyle(
                        "ActionTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                ),
                "",
            ]
        ]

        # Split actions into two columns for space efficiency
        for i in range(0, len(actions), 2):
            left_action = actions[i] if i < len(actions) else None
            right_action = actions[i + 1] if i + 1 < len(actions) else None

            left_text = ""
            right_text = ""

            if left_action:
                action_text = left_action.get("action", "")
                trigger = left_action.get("trigger", "")
                benefit = left_action.get("benefit", "")
                left_text = f"<b>🎯 {action_text}</b><br/><i>Quand:</i> {trigger}<br/><i>Bénéfice:</i> {benefit}"

            if right_action:
                action_text = right_action.get("action", "")
                trigger = right_action.get("trigger", "")
                benefit = right_action.get("benefit", "")
                right_text = f"<b>🎯 {action_text}</b><br/><i>Quand:</i> {trigger}<br/><i>Bénéfice:</i> {benefit}"

            action_data.append(
                [
                    Paragraph(
                        left_text,
                        ParagraphStyle(
                            "QuickAction",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            spaceAfter=4,
                        ),
                    ),
                    Paragraph(
                        right_text,
                        ParagraphStyle(
                            "QuickAction",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            spaceAfter=4,
                        ),
                    ),
                ]
            )

        action_table = Table(action_data, colWidths=[9 * cm, 9 * cm])
        action_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["secondary"]),
                    ("BACKGROUND", (0, 1), (-1, -1), self.colors["background"]),
                    ("SPAN", (0, 0), (1, 0)),  # Span header across both columns
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["secondary"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return action_table

    def _build_emergency_section(self) -> Table:
        """Build emergency situations with immediate solutions"""
        emergencies = self.data.get("emergency_tips", [])

        emergency_data = [
            [
                Paragraph(
                    "<b>🚨 SITUATIONS D'URGENCE - SOLUTIONS IMMÉDIATES</b>",
                    ParagraphStyle(
                        "EmergencyHeader",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for emergency in emergencies:
            situation = emergency.get("situation", "")
            solution = emergency.get("solution", "")
            why = emergency.get("why", "")

            emergency_text = (
                f"<b>⚠️ {situation.upper()}</b><br/>→ <b>{solution}</b> <i>({why})</i>"
            )

            emergency_data.append(
                [
                    Paragraph(
                        emergency_text,
                        ParagraphStyle(
                            "Emergency",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=10,
                            spaceAfter=4,
                        ),
                    )
                ]
            )

        emergency_table = Table(emergency_data, colWidths=[18 * cm])
        emergency_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["urgent"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["highlight"]),
                    ("BORDER", (0, 0), (-1, -1), 2, self.colors["urgent"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return emergency_table

    def _build_daily_reminders(self) -> Table:
        """Build daily reminders checklist"""
        reminders = self.data.get("daily_reminders", [])

        reminder_data = [
            [
                Paragraph(
                    "<b>✅ RAPPELS QUOTIDIENS - COCHEZ VOS PROGRÈS</b>",
                    ParagraphStyle(
                        "ReminderTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                ),
                "",
            ]
        ]

        # Split reminders into two columns
        for i in range(0, len(reminders), 2):
            left_reminder = reminders[i] if i < len(reminders) else ""
            right_reminder = reminders[i + 1] if i + 1 < len(reminders) else ""

            reminder_data.append(
                [
                    Paragraph(
                        f"☐ {left_reminder}",
                        ParagraphStyle(
                            "Reminder",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            spaceAfter=3,
                        ),
                    ),
                    Paragraph(
                        f"☐ {right_reminder}" if right_reminder else "",
                        ParagraphStyle(
                            "Reminder",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            spaceAfter=3,
                        ),
                    ),
                ]
            )

        reminder_table = Table(reminder_data, colWidths=[9 * cm, 9 * cm])
        reminder_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["good"]),
                    ("BACKGROUND", (0, 1), (-1, -1), self.colors["background"]),
                    ("SPAN", (0, 0), (1, 0)),
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["good"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return reminder_table

    def _build_key_numbers_section(self) -> Table:
        """Build key nutritional numbers reference"""
        key_numbers = self.data.get("key_numbers", [])

        numbers_data = [
            [
                Paragraph(
                    "<b>📊 CHIFFRES CLÉS - MÉMORISER</b>",
                    ParagraphStyle(
                        "NumbersTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for number in key_numbers:
            metric = number.get("metric", "")
            value = number.get("value", "")
            unit = number.get("unit", "")
            note = number.get("note", "")

            number_text = f"<b>{metric}:</b> <b style='color: red'>{value}</b> {unit} <i>({note})</i>"

            numbers_data.append(
                [
                    Paragraph(
                        number_text,
                        ParagraphStyle(
                            "KeyNumber",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=15,
                            spaceAfter=3,
                        ),
                    )
                ]
            )

        numbers_table = Table(numbers_data, colWidths=[18 * cm])
        numbers_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["accent"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["accent"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return numbers_table

    def _build_decision_flowchart(self) -> Table:
        """Build quick decision making flowchart"""
        decision_flow = self.data.get(
            "decision_flow",
            [
                {
                    "question": "J'ai faim",
                    "yes": "Depuis >3h?",
                    "no": "Boire eau + attendre 20min",
                },
                {
                    "question": "Depuis >3h?",
                    "yes": "Collation saine",
                    "no": "Activité ou distraction",
                },
                {
                    "question": "Envie sucrée",
                    "yes": "Fruit disponible?",
                    "no": "Identifier émotion",
                },
                {
                    "question": "Fruit disponible?",
                    "yes": "Prendre le fruit",
                    "no": "Carré chocolat noir",
                },
            ],
        )

        flowchart_data = [
            [
                Paragraph(
                    "<b>🤔 ARBRE DE DÉCISION - QUE FAIRE?</b>",
                    ParagraphStyle(
                        "FlowchartTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for flow in decision_flow:
            question = flow.get("question", "")
            yes_path = flow.get("yes", "")
            no_path = flow.get("no", "")

            flow_text = (
                f"<b>❓ {question}</b><br/>✅ OUI → {yes_path}<br/>❌ NON → {no_path}"
            )

            flowchart_data.append(
                [
                    Paragraph(
                        flow_text,
                        ParagraphStyle(
                            "DecisionFlow",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=10,
                            spaceAfter=5,
                        ),
                    )
                ]
            )

        flowchart_table = Table(flowchart_data, colWidths=[18 * cm])
        flowchart_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["primary"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["highlight"]),
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["primary"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return flowchart_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Quick Reference",
            "category": "nutrition_sheets",
            "description": "Guide rapide concis et actionnable pour usage quotidien",
            "target_audience": "Aide-mémoires, consultations rapides, urgences nutritionnelles",
            "features": [
                "Format ultra-concis",
                "Actions immédiates",
                "Solutions d'urgence",
                "Rappels quotidiens",
                "Chiffres clés mémorisables",
                "Arbre de décision rapide",
            ],
            "color_scheme": "High contrast emergency colors (red, green, orange)",
            "typography": "Bold Helvetica for quick scanning",
            "layout_style": "Emergency contact card format",
            "complexity": "Simple",
            "page_count": "1 page maximum",
            "data_requirements": [
                "title",
                "quick_actions",
                "emergency_tips",
                "daily_reminders",
                "key_numbers",
            ],
            "customization_options": [
                "Emergency color intensity",
                "Content density level",
                "Action prioritization",
                "Decision flow complexity",
            ],
        }
