"""
Scientific Report Nutrition Sheet Template - Professional template for academic and research use
Evidence-based format with detailed analysis, bibliography, and scientific methodology
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
    DataVisualizationComponent,
    MacronutrientWheelComponent,
    NutritionFactsComponent,
    ProgressBarComponent,
)


class NutritionSheetScientificTemplate(BaseTemplate):
    """
    Scientific Report Nutrition Sheet Template

    Perfect for:
    - Academic research publications
    - Healthcare professional documentation
    - Evidence-based practice reports
    - Clinical nutrition studies
    - Professional training materials
    - Peer-reviewed content

    Features:
    - Academic formatting standards
    - Comprehensive bibliography
    - Statistical analysis presentation
    - Evidence grading system
    - Methodological transparency
    - Peer-review ready format
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(data, config or {})

        # Scientific configuration
        self.scientific_config = {
            "citation_style": "apa",  # apa, vancouver, harvard
            "evidence_grading": True,
            "statistical_significance": True,
            "peer_review_format": True,
            "methodology_detail": "comprehensive",
            **self.config.get("scientific_config", {})
        }

        # Academic color scheme - Conservative and professional
        self.colors = {
            "primary": colors.Color(0.13, 0.31, 0.53),       # Academic blue
            "secondary": colors.Color(0.26, 0.26, 0.26),     # Charcoal grey
            "accent": colors.Color(0.58, 0.0, 0.83),         # Scientific purple
            "background": colors.Color(1.0, 1.0, 1.0),       # Pure white
            "text": colors.Color(0.0, 0.0, 0.0),             # Black text
            "table_header": colors.Color(0.90, 0.90, 0.90),  # Light grey
            "citation": colors.Color(0.40, 0.40, 0.40),      # Medium grey
            "evidence_a": colors.Color(0.20, 0.60, 0.20),    # High evidence
            "evidence_b": colors.Color(0.80, 0.80, 0.20),    # Moderate evidence
            "evidence_c": colors.Color(0.80, 0.40, 0.20),    # Low evidence
            **self.config.get("colors", {})
        }

        # Academic typography
        self.fonts = {
            "title": ("Times-Bold", 16),
            "subtitle": ("Times-Bold", 14),
            "heading": ("Times-Bold", 12),
            "body": ("Times-Roman", 11),
            "caption": ("Times-Roman", 9),
            "citation": ("Times-Italic", 10),
            "table": ("Times-Roman", 10),
            **self.config.get("fonts", {})
        }

        # Content validation
        self._validate_scientific_data()

    def _validate_scientific_data(self) -> None:
        """Validate that scientific report data is present"""
        required_fields = [
            "title", "authors", "abstract", "methodology",
            "findings", "references", "evidence_level"
        ]

        for field in required_fields:
            if field not in self.data:
                self.data[field] = self._get_default_scientific_content(field)

    def _get_default_scientific_content(self, field: str) -> Any:
        """Provide default scientific content"""
        defaults = {
            "title": "Analyse Scientifique de l'Intervention Nutritionnelle",
            "authors": [
                {"name": "Dr. Jean Nutrition", "affiliation": "Centre de Recherche Nutritionnelle", "email": "j.nutrition@research.fr"},
                {"name": "Prof. Marie Science", "affiliation": "Université de Nutrition", "email": "m.science@uni.fr"}
            ],
            "abstract": "Cette étude examine l'efficacité des interventions nutritionnelles personnalisées basées sur l'analyse des biomarqueurs individuels. L'approche méthodologique combine l'analyse quantitative des apports nutritionnels avec l'évaluation qualitative des changements comportementaux. Les résultats démontrent une amélioration significative des paramètres métaboliques (p<0.05) chez 85% des participants suivis sur 12 semaines.",
            "methodology": {
                "study_design": "Étude interventionnelle prospective randomisée",
                "participants": "156 adultes en surpoids (BMI 25-35)",
                "intervention": "Plan nutritionnel personnalisé basé sur biomarqueurs",
                "duration": "12 semaines avec suivi à 6 mois",
                "measurements": ["Composition corporelle", "Profil lipidique", "Glycémie", "Marqueurs inflammatoires"],
                "statistical_analysis": "ANOVA à mesures répétées, test de Student, régression logistique"
            },
            "findings": [
                {
                    "finding": "Réduction significative du poids corporel",
                    "value": "-5.2kg ± 2.1",
                    "p_value": "p<0.001",
                    "confidence": "95%",
                    "evidence_level": "A"
                },
                {
                    "finding": "Amélioration du profil lipidique",
                    "value": "LDL -15%, HDL +12%",
                    "p_value": "p<0.01",
                    "confidence": "95%",
                    "evidence_level": "A"
                },
                {
                    "finding": "Stabilisation glycémique",
                    "value": "HbA1c -0.8%",
                    "p_value": "p<0.05",
                    "confidence": "90%",
                    "evidence_level": "B"
                }
            ],
            "references": [
                {
                    "authors": "Smith, J., Brown, M., & Wilson, K.",
                    "year": "2023",
                    "title": "Personalized nutrition interventions: A systematic review",
                    "journal": "Journal of Nutritional Science",
                    "volume": "15",
                    "pages": "234-251",
                    "doi": "10.1016/j.jns.2023.02.015"
                },
                {
                    "authors": "Garcia, A., et al.",
                    "year": "2022",
                    "title": "Biomarker-guided dietary recommendations in metabolic syndrome",
                    "journal": "Clinical Nutrition",
                    "volume": "41",
                    "pages": "1892-1905",
                    "doi": "10.1016/j.clnu.2022.08.023"
                }
            ],
            "evidence_level": "A"
        }

        return defaults.get(field, "")

    def build_content(self) -> List[Flowable]:
        """Build the complete scientific report content"""
        content = []

        # Academic title page
        content.append(self._build_title_page())
        content.append(Spacer(1, 15*mm))

        # Abstract
        content.append(self._build_abstract())
        content.append(Spacer(1, 10*mm))

        # Methodology section
        content.append(self._build_methodology())
        content.append(Spacer(1, 10*mm))

        # Results and findings
        content.append(self._build_results_section())
        content.append(Spacer(1, 10*mm))

        # Statistical analysis
        content.append(self._build_statistical_analysis())
        content.append(Spacer(1, 10*mm))

        # Evidence grading
        content.append(self._build_evidence_grading())
        content.append(Spacer(1, 10*mm))

        # Limitations and considerations
        content.append(self._build_limitations())
        content.append(Spacer(1, 10*mm))

        # References
        content.append(self._build_references())

        return content

    def _build_title_page(self) -> Table:
        """Build academic title page with author information"""
        title = self.data.get("title", "")
        authors = self.data.get("authors", [])
        date = self.data.get("date", "")
        institution = self.data.get("institution", "Centre de Recherche Nutritionnelle")

        title_data = [
            [
                Paragraph(f"<b>{title}</b>", ParagraphStyle(
                    'AcademicTitle',
                    fontSize=self.fonts["title"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_CENTER,
                    spaceAfter=10
                ))
            ],
            [
                Paragraph("<b>RAPPORT SCIENTIFIQUE - NUTRITION CLINIQUE</b>", ParagraphStyle(
                    'ReportType',
                    fontSize=self.fonts["subtitle"][1],
                    textColor=self.colors["secondary"],
                    alignment=TA_CENTER,
                    spaceAfter=15
                ))
            ]
        ]

        # Authors section
        if authors:
            authors_text = ""
            for i, author in enumerate(authors):
                name = author.get("name", "")
                affiliation = author.get("affiliation", "")
                email = author.get("email", "")

                authors_text += f"<b>{name}</b><br/><i>{affiliation}</i><br/>{email}"
                if i < len(authors) - 1:
                    authors_text += "<br/><br/>"

            title_data.append([
                Paragraph(authors_text, ParagraphStyle(
                    'Authors',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER,
                    spaceAfter=10
                ))
            ])

        # Institution and date
        title_data.extend([
            [
                Paragraph(f"<b>{institution}</b>", ParagraphStyle(
                    'Institution',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["secondary"],
                    alignment=TA_CENTER,
                    spaceAfter=5
                ))
            ],
            [
                Paragraph(date, ParagraphStyle(
                    'Date',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                ))
            ]
        ])

        title_table = Table(title_data, colWidths=[18*cm])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors["background"]),
            ('BORDER', (0, 0), (-1, -1), 2, self.colors["primary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))

        return title_table

    def _build_abstract(self) -> Table:
        """Build academic abstract section"""
        abstract = self.data.get("abstract", "")
        keywords = self.data.get("keywords", ["nutrition personnalisée", "biomarqueurs", "intervention", "evidence-based"])

        abstract_data = [
            [
                Paragraph("<b>RÉSUMÉ</b>", ParagraphStyle(
                    'AbstractTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_LEFT,
                    spaceAfter=8
                ))
            ],
            [
                Paragraph(abstract, ParagraphStyle(
                    'AbstractText',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_JUSTIFY,
                    spaceAfter=8
                ))
            ],
            [
                Paragraph(f"<b>Mots-clés:</b> {'; '.join(keywords)}", ParagraphStyle(
                    'Keywords',
                    fontSize=self.fonts["caption"][1],
                    textColor=self.colors["citation"],
                    alignment=TA_LEFT
                ))
            ]
        ]

        abstract_table = Table(abstract_data, colWidths=[18*cm])
        abstract_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors["table_header"]),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        return abstract_table

    def _build_methodology(self) -> Table:
        """Build methodology section with detailed parameters"""
        methodology = self.data.get("methodology", {})

        method_data = [
            [
                Paragraph("<b>MÉTHODOLOGIE</b>", ParagraphStyle(
                    'MethodTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=self.colors["primary"],
                    alignment=TA_LEFT,
                    spaceAfter=8
                ))
            ]
        ]

        # Study design
        study_design = methodology.get("study_design", "")
        method_data.append([
            Paragraph(f"<b>Design de l'étude:</b> {study_design}", ParagraphStyle(
                'MethodItem',
                fontSize=self.fonts["body"][1],
                textColor=self.colors["text"],
                alignment=TA_LEFT,
                spaceAfter=4
            ))
        ])

        # Participants
        participants = methodology.get("participants", "")
        method_data.append([
            Paragraph(f"<b>Participants:</b> {participants}", ParagraphStyle(
                'MethodItem',
                fontSize=self.fonts["body"][1],
                textColor=self.colors["text"],
                alignment=TA_LEFT,
                spaceAfter=4
            ))
        ])

        # Intervention
        intervention = methodology.get("intervention", "")
        method_data.append([
            Paragraph(f"<b>Intervention:</b> {intervention}", ParagraphStyle(
                'MethodItem',
                fontSize=self.fonts["body"][1],
                textColor=self.colors["text"],
                alignment=TA_LEFT,
                spaceAfter=4
            ))
        ])

        # Duration
        duration = methodology.get("duration", "")
        method_data.append([
            Paragraph(f"<b>Durée:</b> {duration}", ParagraphStyle(
                'MethodItem',
                fontSize=self.fonts["body"][1],
                textColor=self.colors["text"],
                alignment=TA_LEFT,
                spaceAfter=4
            ))
        ])

        # Measurements
        measurements = methodology.get("measurements", [])
        if measurements:
            measurements_text = "; ".join(measurements)
            method_data.append([
                Paragraph(f"<b>Mesures:</b> {measurements_text}", ParagraphStyle(
                    'MethodItem',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=4
                ))
            ])

        # Statistical analysis
        stats = methodology.get("statistical_analysis", "")
        method_data.append([
            Paragraph(f"<b>Analyse statistique:</b> {stats}", ParagraphStyle(
                'MethodItem',
                fontSize=self.fonts["body"][1],
                textColor=self.colors["text"],
                alignment=TA_LEFT,
                spaceAfter=4
            ))
        ])

        method_table = Table(method_data, colWidths=[18*cm])
        method_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["primary"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["background"]),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return method_table

    def _build_results_section(self) -> Table:
        """Build results section with statistical presentation"""
        findings = self.data.get("findings", [])

        results_data = [
            [
                Paragraph("<b>RÉSULTATS PRINCIPAUX</b>", ParagraphStyle(
                    'ResultsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                "",
                "",
                ""
            ],
            [
                Paragraph("<b>Mesure</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Résultat</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Significativité</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                )),
                Paragraph("<b>Évidence</b>", ParagraphStyle(
                    'TableHeader',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                ))
            ]
        ]

        for finding in findings:
            finding_name = finding.get("finding", "")
            value = finding.get("value", "")
            p_value = finding.get("p_value", "")
            evidence_level = finding.get("evidence_level", "C")

            # Color code evidence level
            evidence_color = {
                "A": self.colors["evidence_a"],
                "B": self.colors["evidence_b"],
                "C": self.colors["evidence_c"]
            }.get(evidence_level, self.colors["evidence_c"])

            results_data.append([
                Paragraph(finding_name, ParagraphStyle(
                    'ResultItem',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                )),
                Paragraph(f"<b>{value}</b>", ParagraphStyle(
                    'ResultValue',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                )),
                Paragraph(p_value, ParagraphStyle(
                    'PValue',
                    fontSize=self.fonts["table"][1],
                    textColor=self.colors["text"],
                    alignment=TA_CENTER
                )),
                Paragraph(f"<b>{evidence_level}</b>", ParagraphStyle(
                    'Evidence',
                    fontSize=self.fonts["table"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ])

        results_table = Table(results_data, colWidths=[6*cm, 4*cm, 4*cm, 4*cm])

        # Dynamic styling for evidence levels
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["accent"]),
            ('BACKGROUND', (0, 1), (-1, 1), self.colors["table_header"]),
            ('SPAN', (0, 0), (-1, 0)),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]

        # Add evidence level colors
        for i, finding in enumerate(findings):
            evidence_level = finding.get("evidence_level", "C")
            evidence_color = {
                "A": self.colors["evidence_a"],
                "B": self.colors["evidence_b"],
                "C": self.colors["evidence_c"]
            }.get(evidence_level, self.colors["evidence_c"])

            table_style.append(('BACKGROUND', (3, i+2), (3, i+2), evidence_color))

        results_table.setStyle(TableStyle(table_style))

        return results_table

    def _build_statistical_analysis(self) -> Table:
        """Build statistical analysis summary"""
        stats = self.data.get("statistical_summary", {
            "sample_size": "n=156",
            "power": "80%",
            "alpha": "0.05",
            "confidence_interval": "95%",
            "effect_size": "Cohen's d = 0.8",
            "missing_data": "5.2% (intention-to-treat analysis)"
        })

        stats_data = [
            [
                Paragraph("<b>ANALYSE STATISTIQUE - PARAMÈTRES</b>", ParagraphStyle(
                    'StatsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ]
        ]

        for param, value in stats.items():
            param_name = param.replace("_", " ").title()
            stats_data.append([
                Paragraph(f"<b>{param_name}:</b> {value}", ParagraphStyle(
                    'StatParam',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    spaceAfter=3
                ))
            ])

        stats_table = Table(stats_data, colWidths=[18*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["secondary"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["table_header"]),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return stats_table

    def _build_evidence_grading(self) -> Table:
        """Build evidence grading system explanation"""
        evidence_data = [
            [
                Paragraph("<b>CLASSIFICATION DE L'ÉVIDENCE</b>", ParagraphStyle(
                    'EvidenceTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                ""
            ],
            [
                Paragraph("<b>Grade A</b>", ParagraphStyle(
                    'GradeA',
                    fontSize=self.fonts["body"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                Paragraph("Évidence forte - Recommandation basée sur des études randomisées de haute qualité", ParagraphStyle(
                    'GradeDesc',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                ))
            ],
            [
                Paragraph("<b>Grade B</b>", ParagraphStyle(
                    'GradeB',
                    fontSize=self.fonts["body"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                Paragraph("Évidence modérée - Recommandation basée sur des études de qualité acceptable", ParagraphStyle(
                    'GradeDesc',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                ))
            ],
            [
                Paragraph("<b>Grade C</b>", ParagraphStyle(
                    'GradeC',
                    fontSize=self.fonts["body"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                )),
                Paragraph("Évidence faible - Recommandation basée sur l'opinion d'experts ou études limitées", ParagraphStyle(
                    'GradeDesc',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT
                ))
            ]
        ]

        evidence_table = Table(evidence_data, colWidths=[3*cm, 15*cm])
        evidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors["accent"]),
            ('BACKGROUND', (0, 1), (0, 1), self.colors["evidence_a"]),
            ('BACKGROUND', (0, 2), (0, 2), self.colors["evidence_b"]),
            ('BACKGROUND', (0, 3), (0, 3), self.colors["evidence_c"]),
            ('SPAN', (0, 0), (1, 0)),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return evidence_table

    def _build_limitations(self) -> Table:
        """Build limitations and considerations section"""
        limitations = self.data.get("limitations", [
            "Échantillon limité à une population spécifique (adultes en surpoids)",
            "Durée de suivi relativement courte (12 semaines)",
            "Possible biais de sélection des participants volontaires",
            "Variabilité inter-individuelle des réponses métaboliques",
            "Besoin de validation dans des populations plus larges"
        ])

        limitations_data = [
            [
                Paragraph("<b>LIMITATIONS ET CONSIDÉRATIONS</b>", ParagraphStyle(
                    'LimitationsTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ]
        ]

        for limitation in limitations:
            limitations_data.append([
                Paragraph(f"• {limitation}", ParagraphStyle(
                    'Limitation',
                    fontSize=self.fonts["body"][1],
                    textColor=self.colors["text"],
                    alignment=TA_LEFT,
                    leftIndent=10,
                    spaceAfter=3
                ))
            ])

        limitations_table = Table(limitations_data, colWidths=[18*cm])
        limitations_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["accent"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["background"]),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return limitations_table

    def _build_references(self) -> Table:
        """Build academic references section"""
        references = self.data.get("references", [])

        ref_data = [
            [
                Paragraph("<b>RÉFÉRENCES BIBLIOGRAPHIQUES</b>", ParagraphStyle(
                    'ReferencesTitle',
                    fontSize=self.fonts["heading"][1],
                    textColor=colors.white,
                    alignment=TA_CENTER
                ))
            ]
        ]

        for i, ref in enumerate(references):
            authors = ref.get("authors", "")
            year = ref.get("year", "")
            title = ref.get("title", "")
            journal = ref.get("journal", "")
            volume = ref.get("volume", "")
            pages = ref.get("pages", "")
            doi = ref.get("doi", "")

            citation = f"{i+1}. {authors} ({year}). {title}. <i>{journal}</i>, {volume}, {pages}."
            if doi:
                citation += f" DOI: {doi}"

            ref_data.append([
                Paragraph(citation, ParagraphStyle(
                    'Reference',
                    fontSize=self.fonts["citation"][1],
                    textColor=self.colors["text"],
                    alignment=TA_JUSTIFY,
                    leftIndent=15,
                    spaceAfter=5
                ))
            ])

        ref_table = Table(ref_data, colWidths=[18*cm])
        ref_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.colors["primary"]),
            ('BACKGROUND', (0, 1), (0, -1), self.colors["background"]),
            ('BORDER', (0, 0), (-1, -1), 1, self.colors["secondary"]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        return ref_table

    def get_template_info(self) -> Dict[str, Any]:
        """Return template information and capabilities"""
        return {
            "name": "Scientific Report",
            "category": "nutrition_sheets",
            "description": "Format académique avec evidence-based et bibliographie complète",
            "target_audience": "Professionnels santé, recherche, formation académique",
            "features": [
                "Format académique standard",
                "Bibliographie complète",
                "Analyse statistique détaillée",
                "Classification de l'évidence",
                "Méthodologie transparente",
                "Format peer-review ready"
            ],
            "color_scheme": "Conservative academic colors (blue, grey, purple)",
            "typography": "Times Roman family for academic presentation",
            "layout_style": "Academic journal format",
            "complexity": "Advanced",
            "page_count": "3-5 pages",
            "data_requirements": [
                "title", "authors", "abstract", "methodology",
                "findings", "references", "evidence_level"
            ],
            "customization_options": [
                "Citation style (APA, Vancouver, Harvard)",
                "Evidence grading system",
                "Statistical detail level",
                "Academic formatting standard"
            ]
        }