"""
Education Focus Nutrition Sheet Template - Professional template for nutritional education
Pedagogical design with accessible infographics for education and prevention
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
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


class NutritionSheetEducationTemplate(BaseTemplate):
    """
    Education Focus Nutrition Sheet Template

    Perfect for:
    - Nutritional education sessions
    - Prevention and awareness campaigns
    - Educational materials for clients
    - School and community programs
    - Health promotion initiatives

    Features:
    - Accessible infographics
    - Step-by-step guidance
    - Comparison charts
    - Practical tips and checklists
    - Evidence-based information
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Education-specific configuration
        self.education_config = {
            "visual_emphasis": True,
            "infographic_style": True,
            "accessibility_level": "high",
            "pedagogical_approach": "progressive",
            "target_audience": "general_public",
            **self.config.get("education_config", {}),
        }

        # Educational color scheme - Accessible and professional
        self.colors = {
            "primary": colors.Color(0.11, 0.37, 0.58),  # Professional blue
            "secondary": colors.Color(0.25, 0.59, 0.29),  # Educational green
            "accent": colors.Color(0.95, 0.61, 0.11),  # Attention orange
            "background": colors.Color(0.98, 0.98, 0.98),  # Light background
            "text": colors.Color(0.13, 0.13, 0.13),  # Dark text
            "info": colors.Color(0.20, 0.60, 0.86),  # Info blue
            "warning": colors.Color(1.0, 0.76, 0.03),  # Warning yellow
            "success": colors.Color(0.30, 0.69, 0.31),  # Success green
            **self.config.get("colors", {}),
        }

        # Educational typography
        self.fonts = {
            "title": ("Helvetica-Bold", 22),
            "subtitle": ("Helvetica-Bold", 16),
            "heading": ("Helvetica-Bold", 14),
            "body": ("Helvetica", 12),
            "caption": ("Helvetica", 10),
            "emphasis": ("Helvetica-Bold", 12),
            **self.config.get("fonts", {}),
        }

        # Content validation
        self._validate_education_data()

    def _validate_education_data(self) -> None:
        """Validate that education-specific data is present"""
        required_fields = [
            "title",
            "topic",
            "learning_objectives",
            "key_concepts",
            "practical_tips",
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_education_content(field)

    def _get_default_education_content(self, field: str) -> Any:
        """Provide default educational content"""
        defaults = {
            "title": "Guide Nutritionnel Éducatif",
            "topic": "Fondamentaux de la Nutrition",
            "learning_objectives": [
                "Comprendre les bases de l'équilibre nutritionnel",
                "Identifier les groupes d'aliments essentiels",
                "Adopter des habitudes alimentaires saines",
            ],
            "key_concepts": [
                {
                    "concept": "Équilibre Alimentaire",
                    "description": "Répartition optimale des nutriments",
                    "examples": ["Assiette équilibrée", "Portions recommandées"],
                },
                {
                    "concept": "Nutriments Essentiels",
                    "description": "Macronutriments et micronutriments",
                    "examples": ["Protéines", "Glucides", "Lipides", "Vitamines"],
                },
            ],
            "practical_tips": [
                "Planifier ses repas à l'avance",
                "Lire les étiquettes alimentaires",
                "Privilégier les aliments non transformés",
                "Maintenir une hydratation adéquate",
            ],
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete education sheet content"""
        content = []

        # Header with educational branding
        content.append(self._build_education_header())
        content.append(Spacer(1, 15 * mm))

        # Learning objectives section
        content.append(self._build_learning_objectives())
        content.append(Spacer(1, 10 * mm))

        # Key concepts with infographics
        content.extend(self._build_key_concepts())
        content.append(Spacer(1, 10 * mm))

        # Nutritional comparison chart
        content.append(self._build_comparison_section())
        content.append(Spacer(1, 10 * mm))

        # Practical application section
        content.append(self._build_practical_section())
        content.append(Spacer(1, 10 * mm))

        # Progress tracking checklist
        content.append(self._build_progress_checklist())
        content.append(Spacer(1, 10 * mm))

        # Educational resources and next steps
        content.append(self._build_resources_section())

        return content

    def _build_education_header(self) -> Table:
        """Build educational header with visual identity"""
        title = self.data.get("title", "Guide Nutritionnel Éducatif")
        topic = self.data.get("topic", "Fondamentaux de la Nutrition")
        date = self.data.get("date", "Date")
        educator = self.data.get("educator_name", "Éducateur Nutrition")

        # Create header data with educational styling
        header_data = [
            [
                Paragraph(
                    f"<b>{title}</b>",
                    ParagraphStyle(
                        "Title",
                        fontSize=self.fonts["title"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                ),
                Paragraph(
                    "<b>📚 FORMATION</b>",
                    ParagraphStyle(
                        "Badge",
                        fontSize=12,
                        textColor=self.colors["accent"],
                        alignment=TA_CENTER,
                        borderWidth=1,
                        borderColor=self.colors["accent"],
                    ),
                ),
            ],
            [
                Paragraph(
                    f"<i>{topic}</i>",
                    ParagraphStyle(
                        "Subtitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=self.colors["text"],
                        alignment=TA_LEFT,
                    ),
                ),
                Paragraph(
                    f"<b>{date}</b><br/>{educator}",
                    ParagraphStyle(
                        "Info",
                        fontSize=self.fonts["caption"][1],
                        textColor=self.colors["text"],
                        alignment=TA_CENTER,
                    ),
                ),
            ],
        ]

        header_table = Table(header_data, colWidths=[13 * cm, 5 * cm])
        header_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["background"]),
                    ("BACKGROUND", (1, 0), (1, 0), colors.white),
                    ("BORDER", (1, 0), (1, 0), 2, self.colors["accent"]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return header_table

    def _build_learning_objectives(self) -> Table:
        """Build learning objectives section with visual checkboxes"""
        objectives = self.data.get("learning_objectives", [])

        # Create objectives with checkboxes
        objective_data = [
            [
                Paragraph(
                    "<b>🎯 OBJECTIFS D'APPRENTISSAGE</b>",
                    ParagraphStyle(
                        "SectionTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                )
            ]
        ]

        for i, objective in enumerate(objectives):
            objective_data.append(
                [
                    Paragraph(
                        f"☐ {objective}",
                        ParagraphStyle(
                            "Objective",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=20,
                            spaceAfter=3,
                        ),
                    )
                ]
            )

        objectives_table = Table(objective_data, colWidths=[18 * cm])
        objectives_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["info"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (0, 0), 8),
                    ("BOTTOMPADDING", (0, 0), (0, 0), 8),
                    ("TOPPADDING", (0, 1), (0, -1), 4),
                    ("BOTTOMPADDING", (0, 1), (0, -1), 4),
                ]
            )
        )

        return objectives_table

    def _build_key_concepts(self) -> List[Flowable]:
        """Build key concepts section with infographic-style presentation"""
        concepts = self.data.get("key_concepts", [])
        content = []

        # Section header
        content.append(
            Paragraph(
                "<b>🧠 CONCEPTS CLÉS</b>",
                ParagraphStyle(
                    "SectionHeader",
                    fontSize=self.fonts["heading"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_LEFT,
                    spaceAfter=8,
                ),
            )
        )

        # Create concept cards
        for i, concept in enumerate(concepts):
            concept_name = concept.get("concept", "Concept")
            description = concept.get("description", "")
            examples = concept.get("examples", [])

            # Concept card data
            card_data = [
                [
                    Paragraph(
                        f"<b>{i + 1}. {concept_name}</b>",
                        ParagraphStyle(
                            "ConceptTitle",
                            fontSize=self.fonts["subtitle"][1],
                            textColor=colors.white,
                            alignment=TA_LEFT,
                        ),
                    )
                ],
                [
                    Paragraph(
                        description,
                        ParagraphStyle(
                            "ConceptDesc",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_JUSTIFY,
                            spaceAfter=5,
                        ),
                    )
                ],
            ]

            # Add examples if present
            if examples:
                examples_text = " • ".join(examples)
                card_data.append(
                    [
                        Paragraph(
                            f"<b>Exemples:</b> {examples_text}",
                            ParagraphStyle(
                                "Examples",
                                fontSize=self.fonts["caption"][1],
                                textColor=self.colors["secondary"],
                                alignment=TA_LEFT,
                                leftIndent=10,
                            ),
                        )
                    ]
                )

            concept_table = Table(card_data, colWidths=[18 * cm])
            concept_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (0, 0), self.colors["secondary"]),
                        ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                        ("BORDER", (0, 0), (-1, -1), 1, self.colors["secondary"]),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )

            content.append(concept_table)
            if i < len(concepts) - 1:
                content.append(Spacer(1, 8 * mm))

        return content

    def _build_comparison_section(self) -> Table:
        """Build nutritional comparison with visual emphasis"""
        comparisons = self.data.get("nutritional_comparisons", [])

        if not comparisons:
            # Default comparison example
            comparisons = [
                {
                    "category": "Sources de Protéines",
                    "items": [
                        {
                            "name": "Viande rouge",
                            "value": 25,
                            "unit": "g/100g",
                            "note": "Riche en fer",
                        },
                        {
                            "name": "Poisson",
                            "value": 22,
                            "unit": "g/100g",
                            "note": "Oméga-3",
                        },
                        {
                            "name": "Légumineuses",
                            "value": 8,
                            "unit": "g/100g",
                            "note": "Fibres",
                        },
                    ],
                }
            ]

        # Build comparison table
        comparison_data = [
            [
                Paragraph(
                    "<b>📊 COMPARAISONS NUTRITIONNELLES</b>",
                    ParagraphStyle(
                        "ComparisonTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for comparison in comparisons:
            category = comparison.get("category", "Catégorie")
            items = comparison.get("items", [])

            comparison_data.append(
                [
                    Paragraph(
                        f"<b>{category}</b>",
                        ParagraphStyle(
                            "Category",
                            fontSize=self.fonts["subtitle"][1],
                            textColor=self.colors["primary"],
                            alignment=TA_LEFT,
                            spaceAfter=5,
                        ),
                    )
                ]
            )

            # Items comparison
            for item in items:
                name = item.get("name", "")
                value = item.get("value", 0)
                unit = item.get("unit", "")
                note = item.get("note", "")

                # Create progress bar for visual comparison
                max_value = max([i.get("value", 0) for i in items]) if items else 100
                min(200, (value / max_value) * 200) if max_value > 0 else 0

                item_text = f"• <b>{name}</b>: {value} {unit}"
                if note:
                    item_text += f" <i>({note})</i>"

                comparison_data.append(
                    [
                        Paragraph(
                            item_text,
                            ParagraphStyle(
                                "ComparisonItem",
                                fontSize=self.fonts["body"][1],
                                textColor=self.colors["text"],
                                alignment=TA_LEFT,
                                leftIndent=15,
                                spaceAfter=3,
                            ),
                        )
                    ]
                )

        comparison_table = Table(comparison_data, colWidths=[18 * cm])
        comparison_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["accent"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return comparison_table

    def _build_practical_section(self) -> Table:
        """Build practical tips and applications"""
        tips = self.data.get("practical_tips", [])

        # Create practical tips section
        practical_data = [
            [
                Paragraph(
                    "<b>💡 CONSEILS PRATIQUES</b>",
                    ParagraphStyle(
                        "PracticalTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for i, tip in enumerate(tips):
            tip_icon = ["🥗", "📖", "🍎", "💧", "⏰", "🏃"][i % 6]
            practical_data.append(
                [
                    Paragraph(
                        f"{tip_icon} {tip}",
                        ParagraphStyle(
                            "Tip",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=10,
                            spaceAfter=4,
                        ),
                    )
                ]
            )

        practical_table = Table(practical_data, colWidths=[18 * cm])
        practical_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["success"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return practical_table

    def _build_progress_checklist(self) -> Table:
        """Build progress tracking checklist for self-assessment"""
        checklist_items = self.data.get(
            "progress_checklist",
            [
                "J'ai identifié mes objectifs nutritionnels",
                "Je connais les groupes d'aliments essentiels",
                "Je sais lire les étiquettes nutritionnelles",
                "J'ai planifié mes repas pour la semaine",
                "Je maintiens une hydratation adéquate",
                "J'évalue régulièrement mes habitudes alimentaires",
            ],
        )

        checklist_data = [
            [
                Paragraph(
                    "<b>✅ AUTO-ÉVALUATION DES PROGRÈS</b>",
                    ParagraphStyle(
                        "ChecklistTitle",
                        fontSize=self.fonts["heading"][1],
                        textColor=colors.white,
                        alignment=TA_CENTER,
                    ),
                )
            ]
        ]

        for item in checklist_items:
            checklist_data.append(
                [
                    Paragraph(
                        f"☐ {item}",
                        ParagraphStyle(
                            "ChecklistItem",
                            fontSize=self.fonts["body"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            leftIndent=15,
                            spaceAfter=4,
                        ),
                    )
                ]
            )

        checklist_table = Table(checklist_data, colWidths=[18 * cm])
        checklist_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), self.colors["primary"]),
                    ("BACKGROUND", (0, 1), (0, -1), self.colors["background"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return checklist_table

    def _build_resources_section(self) -> Table:
        """Build additional resources and next steps"""
        resources = self.data.get(
            "additional_resources",
            [
                "Guide alimentaire officiel de votre région",
                "Applications mobiles de suivi nutritionnel",
                "Consultation avec un nutritionniste agréé",
                "Ateliers de cuisine santé dans votre communauté",
            ],
        )

        next_steps = self.data.get(
            "next_steps",
            [
                "Tenir un journal alimentaire pendant 1 semaine",
                "Planifier 3 repas équilibrés",
                "Identifier 1 habitude à améliorer",
                "Fixer un rendez-vous de suivi",
            ],
        )

        resources_data = [
            [
                Paragraph(
                    "<b>📚 RESSOURCES COMPLÉMENTAIRES</b>",
                    ParagraphStyle(
                        "ResourcesTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                ),
                Paragraph(
                    "<b>🎯 PROCHAINES ÉTAPES</b>",
                    ParagraphStyle(
                        "NextStepsTitle",
                        fontSize=self.fonts["subtitle"][1],
                        textColor=self.colors["primary"],
                        alignment=TA_LEFT,
                        spaceAfter=5,
                    ),
                ),
            ]
        ]

        max_rows = max(len(resources), len(next_steps))
        for i in range(max_rows):
            resource = resources[i] if i < len(resources) else ""
            next_step = next_steps[i] if i < len(next_steps) else ""

            resources_data.append(
                [
                    Paragraph(
                        f"• {resource}" if resource else "",
                        ParagraphStyle(
                            "Resource",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["text"],
                            alignment=TA_LEFT,
                            spaceAfter=3,
                        ),
                    ),
                    Paragraph(
                        f"→ {next_step}" if next_step else "",
                        ParagraphStyle(
                            "NextStep",
                            fontSize=self.fonts["caption"][1],
                            textColor=self.colors["secondary"],
                            alignment=TA_LEFT,
                            spaceAfter=3,
                        ),
                    ),
                ]
            )

        resources_table = Table(resources_data, colWidths=[9 * cm, 9 * cm])
        resources_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.colors["background"]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("BORDER", (0, 0), (-1, -1), 1, self.colors["background"]),
                ]
            )
        )

        return resources_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Education Focus",
            "category": "nutrition_sheets",
            "description": "Template pédagogique avec infographies accessibles",
            "target_audience": "Éducation nutritionnelle, prévention, sensibilisation",
            "features": [
                "Infographies accessibles",
                "Objectifs d'apprentissage clairs",
                "Comparaisons visuelles",
                "Conseils pratiques actionnables",
                "Auto-évaluation des progrès",
                "Ressources complémentaires",
            ],
            "color_scheme": "Professional blue with educational green accents",
            "typography": "Clear and accessible Helvetica family",
            "layout_style": "Educational cards with visual emphasis",
            "complexity": "Intermediate",
            "page_count": "1-2 pages",
            "data_requirements": [
                "title",
                "topic",
                "learning_objectives",
                "key_concepts",
                "practical_tips",
            ],
            "customization_options": [
                "Visual emphasis level",
                "Accessibility settings",
                "Target audience adaptation",
                "Infographic complexity",
            ],
        }
