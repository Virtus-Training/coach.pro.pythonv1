"""
Medical Pro Workout Template - Clinical professional design
Designed for medical professionals, rehabilitation, and therapeutic coaching
Target: Kinésithérapie, rééducation, coaching thérapeutique
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from ..base_template import BaseTemplate


class WorkoutMedicalTemplate(BaseTemplate):
    """
    Medical Pro Template - Clinical design with medical compliance
    Designed for healthcare professionals and therapeutic interventions
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "medical_clinical",
            "layout": "medical_structured",
            "compliance": True,
            "documentation_level": "complete",
            "medical_standards": True,
            "colors": {
                "primary": "#2b6cb0",
                "secondary": "#4a5568",
                "accent": "#48bb78",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text_primary": "#1a202c",
                "text_secondary": "#4a5568",
                "success": "#38a169",
                "warning": "#d69e2e",
                "error": "#e53e3e",
                "medical": "#2b6cb0",
                "caution": "#ed8936",
            },
            "fonts": {
                "title": {"name": "Times-Bold", "size": 20},
                "subtitle": {"name": "Times-Bold", "size": 16},
                "heading": {"name": "Times-Bold", "size": 13},
                "subheading": {"name": "Times-Roman", "size": 11},
                "body": {"name": "Times-Roman", "size": 10},
                "caption": {"name": "Times-Italic", "size": 8},
                "medical": {"name": "Times-Roman", "size": 9},
            },
            "layout": {
                "margins": {"top": 60, "bottom": 60, "left": 50, "right": 50},
                "header_height": 80,
                "footer_height": 50,
                "block_spacing": 20,
                "medical_format": True,
            },
            "medical_compliance": {
                "show_contraindications": True,
                "show_precautions": True,
                "show_monitoring": True,
                "show_adaptations": True,
                "documentation_required": True,
            },
        }

    def _build_content(self) -> List[Any]:
        """Build medical workout content with clinical documentation"""
        elements = []

        # Medical header with professional credentials
        elements.append(self._build_medical_header())
        elements.append(Spacer(1, 15))

        # Patient/Client information section
        elements.append(self._build_patient_information())
        elements.append(Spacer(1, 15))

        # Medical assessment and contraindications
        elements.append(self._build_medical_assessment())
        elements.append(Spacer(1, 15))

        # Treatment objectives and plan
        elements.append(self._build_treatment_objectives())
        elements.append(Spacer(1, 15))

        # Exercise prescription with medical detail
        elements.extend(self._build_medical_exercise_blocks())

        # Monitoring and evaluation section
        elements.append(self._build_monitoring_section())

        # Medical notes and adaptations
        elements.append(self._build_medical_notes())

        # Professional signatures and compliance
        elements.append(self._build_compliance_section())

        return elements

    def _build_medical_header(self) -> Table:
        """Build professional medical header"""
        facility = self.data.get("facility_name", "Centre de Rééducation")
        practitioner = self.data.get("practitioner_name", "Dr. Professionnel")
        credentials = self.data.get("practitioner_credentials", "Kinésithérapeute D.E.")
        date = self.data.get("prescription_date", "Date non spécifiée")

        header_data = [
            [f"{facility}", f"Date: {date}"],
            [
                f"{practitioner}, {credentials}",
                "PRESCRIPTION D'EXERCICES THÉRAPEUTIQUES",
            ],
            ["Licence professionnelle: " + self.data.get("license_number", "N/A"), ""],
        ]

        header_table = Table(header_data, colWidths=[3 * inch, 3 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    # Facility and date
                    ("FONTNAME", (0, 0), (0, 0), "Times-Bold"),
                    ("FONTNAME", (1, 0), (1, 0), "Times-Roman"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    # Practitioner and title
                    ("FONTNAME", (0, 1), (0, 1), "Times-Roman"),
                    ("FONTNAME", (1, 1), (1, 1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (0, 1), 11),
                    ("FONTSIZE", (1, 1), (1, 1), 14),
                    (
                        "TEXTCOLOR",
                        (1, 1),
                        (1, 1),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    # License
                    ("FONTNAME", (0, 2), (0, 2), "Times-Italic"),
                    ("FONTSIZE", (0, 2), (0, 2), 9),
                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (0, 2),
                        HexColor(self.merged_config["colors"]["text_secondary"]),
                    ),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return header_table

    def _build_patient_information(self) -> Table:
        """Build comprehensive patient information section"""
        patient = self.data.get("patient_info", {})

        patient_data = [
            ["INFORMATIONS PATIENT", "", ""],
            [
                "Nom:",
                patient.get("name", "Non spécifié"),
                "Âge: " + str(patient.get("age", "N/A")),
            ],
            [
                "Diagnostic principal:",
                patient.get("primary_diagnosis", "Non spécifié"),
                "",
            ],
            ["Diagnostic secondaire:", patient.get("secondary_diagnosis", "Aucun"), ""],
            [
                "Date début traitement:",
                patient.get("treatment_start", "Non spécifiée"),
                "Nombre de séances: " + str(patient.get("session_count", "N/A")),
            ],
            [
                "Médecin prescripteur:",
                patient.get("prescribing_physician", "Non spécifié"),
                "Objectif thérapeutique: "
                + patient.get("therapeutic_goal", "Récupération fonctionnelle"),
            ],
        ]

        patient_table = Table(
            patient_data, colWidths=[2 * inch, 2.5 * inch, 1.5 * inch]
        )
        patient_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f8fafc")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return patient_table

    def _build_medical_assessment(self) -> Table:
        """Build medical assessment with contraindications and precautions"""
        assessment = self.data.get("medical_assessment", {})

        assessment_data = [
            ["ÉVALUATION MÉDICALE ET CONTRE-INDICATIONS", ""],
            ["État général:", assessment.get("general_condition", "Stable")],
            [
                "Limitations fonctionnelles:",
                assessment.get("functional_limitations", "Voir évaluation initiale"),
            ],
            [
                "Contre-indications absolues:",
                assessment.get("absolute_contraindications", "Aucune identifiée"),
            ],
            [
                "Contre-indications relatives:",
                assessment.get("relative_contraindications", "Douleur aiguë > 7/10"),
            ],
            [
                "Précautions particulières:",
                assessment.get("special_precautions", "Éviter mouvements brusques"),
            ],
            [
                "Médications affectant l'exercice:",
                assessment.get("medications", "Aucune interférence connue"),
            ],
            [
                "Dernière évaluation:",
                assessment.get("last_evaluation", "Date non spécifiée"),
            ],
        ]

        assessment_table = Table(assessment_data, colWidths=[2.5 * inch, 3.5 * inch])
        assessment_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["caution"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Labels
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    # Content styling for contraindications
                    (
                        "TEXTCOLOR",
                        (0, 3),
                        (-1, 3),
                        HexColor(self.merged_config["colors"]["error"]),
                    ),  # Absolute contraindications
                    (
                        "TEXTCOLOR",
                        (0, 4),
                        (-1, 4),
                        HexColor(self.merged_config["colors"]["warning"]),
                    ),  # Relative contraindications
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#d69e2e")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#fffbeb")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return assessment_table

    def _build_treatment_objectives(self) -> Table:
        """Build treatment objectives and therapeutic plan"""
        objectives = self.data.get("treatment_objectives", {})

        objectives_data = [
            ["OBJECTIFS THÉRAPEUTIQUES ET PLAN DE TRAITEMENT", ""],
            [
                "Objectif principal:",
                objectives.get("primary_objective", "Restauration fonction"),
            ],
            [
                "Objectifs secondaires:",
                objectives.get(
                    "secondary_objectives", "Réduction douleur, amélioration mobilité"
                ),
            ],
            [
                "Critères de progression:",
                objectives.get(
                    "progression_criteria", "Échelle EVA, amplitude articulaire"
                ),
            ],
            [
                "Durée estimée du traitement:",
                objectives.get("estimated_duration", "6-8 semaines"),
            ],
            [
                "Fréquence des séances:",
                objectives.get("session_frequency", "3x/semaine"),
            ],
            [
                "Réévaluation prévue:",
                objectives.get("reevaluation_date", "Dans 2 semaines"),
            ],
            [
                "Critères d'arrêt:",
                objectives.get("stop_criteria", "Douleur > 7/10, inflammation aiguë"),
            ],
        ]

        objectives_table = Table(objectives_data, colWidths=[2.5 * inch, 3.5 * inch])
        objectives_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["success"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#38a169")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f0fff4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return objectives_table

    def _build_medical_exercise_blocks(self) -> List[Any]:
        """Build exercise prescription with medical detail"""
        elements = []
        exercise_blocks = self.data.get("exercise_prescription", [])

        if not exercise_blocks:
            exercise_blocks = self._generate_default_medical_blocks()

        for i, block in enumerate(exercise_blocks):
            # Medical block header
            block_title = Paragraph(
                f"<b>PHASE {i + 1}: {block.get('phase_name', 'Exercices thérapeutiques').upper()}</b>",
                self.styles["heading"],
            )
            elements.append(block_title)
            elements.append(Spacer(1, 8))

            # Medical exercise table
            medical_table = self._build_medical_exercise_table(block)
            elements.append(medical_table)
            elements.append(Spacer(1, 12))

            # Progress tracking for this phase
            if block.get("tracking_parameters"):
                tracking_table = self._build_phase_tracking(
                    block["tracking_parameters"]
                )
                elements.append(tracking_table)
                elements.append(Spacer(1, 10))

        return elements

    def _build_medical_exercise_table(self, block: Dict[str, Any]) -> Table:
        """Build detailed medical exercise prescription table"""
        exercises = block.get("exercises", [])
        phase_info = block.get("phase_info", {})

        # Phase information header
        phase_data = [
            ["Phase:", phase_info.get("description", "Phase thérapeutique")],
            ["Durée:", phase_info.get("duration", "2-3 semaines")],
            ["Objectif:", phase_info.get("objective", "Progression fonctionnelle")],
        ]

        # Exercise prescription table
        exercise_headers = [
            "Exercice",
            "Prescription",
            "Paramètres",
            "Précautions",
            "Progression",
        ]
        exercise_data = [exercise_headers]

        for exercise in exercises:
            exercise_row = [
                exercise.get("name", "Exercice"),
                exercise.get("prescription", "Selon tolérance"),
                exercise.get("parameters", "ROM complet"),
                exercise.get("precautions", "Arrêt si douleur"),
                exercise.get("progression", "Augmentation graduelle"),
            ]
            exercise_data.append(exercise_row)

        # Combine phase info and exercises
        combined_data = (
            phase_data + [["PRESCRIPTION DÉTAILLÉE", "", "", "", ""]] + exercise_data
        )

        exercise_table = Table(
            combined_data,
            colWidths=[1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch],
        )
        exercise_table.setStyle(
            TableStyle(
                [
                    # Phase info
                    ("FONTNAME", (0, 0), (0, 2), "Times-Bold"),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 2),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    ("SPAN", (1, 0), (-1, 0)),
                    ("SPAN", (1, 1), (-1, 1)),
                    ("SPAN", (1, 2), (-1, 2)),
                    # Exercise header
                    ("SPAN", (0, 3), (-1, 3)),
                    ("FONTNAME", (0, 3), (-1, 3), "Times-Bold"),
                    (
                        "BACKGROUND",
                        (0, 3),
                        (-1, 3),
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    ("TEXTCOLOR", (0, 3), (-1, 3), HexColor("#ffffff")),
                    # Exercise table headers
                    ("FONTNAME", (0, 4), (-1, 4), "Times-Bold"),
                    (
                        "BACKGROUND",
                        (0, 4),
                        (-1, 4),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    ("FONTSIZE", (0, 4), (-1, 4), 8),
                    # Exercise content
                    ("FONTSIZE", (0, 5), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )

        return exercise_table

    def _build_phase_tracking(self, tracking_params: Dict[str, Any]) -> Table:
        """Build tracking parameters for each phase"""
        tracking_data = [
            ["PARAMÈTRES DE SUIVI", "", ""],
            ["Paramètre", "Valeur initiale", "Objectif"],
            [
                "Amplitude articulaire",
                tracking_params.get("rom_initial", "N/A"),
                tracking_params.get("rom_target", "ROM complet"),
            ],
            [
                "Force musculaire",
                tracking_params.get("strength_initial", "N/A"),
                tracking_params.get("strength_target", "5/5"),
            ],
            [
                "Échelle douleur (EVA)",
                tracking_params.get("pain_initial", "N/A"),
                tracking_params.get("pain_target", "< 3/10"),
            ],
            [
                "Fonction (questionnaire)",
                tracking_params.get("function_initial", "N/A"),
                tracking_params.get("function_target", "> 80%"),
            ],
        ]

        tracking_table = Table(tracking_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        tracking_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Times-Bold"),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        HexColor(self.merged_config["colors"]["surface"]),
                    ),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#48bb78")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return tracking_table

    def _build_monitoring_section(self) -> Table:
        """Build comprehensive monitoring and evaluation section"""
        monitoring_data = [
            ["SURVEILLANCE ET ÉVALUATION", "", ""],
            ["Paramètre", "Fréquence d'évaluation", "Seuils d'alerte"],
            ["Douleur (EVA)", "Chaque séance", "> 7/10: arrêt immédiat"],
            ["Amplitude articulaire", "Hebdomadaire", "Diminution > 5°: réévaluation"],
            ["Force musculaire", "Bi-hebdomadaire", "Diminution: adaptation programme"],
            [
                "Fonction globale",
                "Toutes les 2 semaines",
                "Stagnation: révision objectifs",
            ],
            ["Observance traitement", "Continue", "< 80%: renforcement motivation"],
            [
                "Effets indésirables",
                "Chaque séance",
                "Tout effet: documentation obligatoire",
            ],
        ]

        monitoring_table = Table(
            monitoring_data, colWidths=[2 * inch, 2 * inch, 2 * inch]
        )
        monitoring_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["warning"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Times-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#fffbeb")),
                    # Alert thresholds column
                    (
                        "TEXTCOLOR",
                        (2, 2),
                        (2, -1),
                        HexColor(self.merged_config["colors"]["error"]),
                    ),
                    ("FONTNAME", (2, 2), (2, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 2), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#d69e2e")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return monitoring_table

    def _build_medical_notes(self) -> Table:
        """Build medical notes and adaptations section"""
        notes = self.data.get("medical_notes", {})

        notes_data = [
            ["OBSERVATIONS MÉDICALES ET ADAPTATIONS", ""],
            [
                "Observations générales:",
                notes.get("general_observations", "Patient motivé et coopératif"),
            ],
            [
                "Adaptations nécessaires:",
                notes.get("necessary_adaptations", "Aucune à ce stade"),
            ],
            [
                "Réponse au traitement:",
                notes.get("treatment_response", "Évolution favorable"),
            ],
            [
                "Recommandations:",
                notes.get("recommendations", "Poursuivre programme actuel"),
            ],
            [
                "Prochaine réévaluation:",
                notes.get("next_evaluation", "Dans 2 semaines"),
            ],
            [
                "Communication avec médecin:",
                notes.get("physician_communication", "Rapport envoyé"),
            ],
            [
                "Notes pour continuité soins:",
                notes.get("continuity_notes", "Maintenir motivation patient"),
            ],
        ]

        notes_table = Table(notes_data, colWidths=[2.5 * inch, 3.5 * inch])
        notes_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#2b6cb0")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f7fafc")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return notes_table

    def _build_compliance_section(self) -> Table:
        """Build professional compliance and signature section"""
        compliance_data = [
            ["CONFORMITÉ PROFESSIONNELLE ET SIGNATURES", ""],
            ["Praticien responsable:", self.data.get("practitioner_name", "")],
            ["Signature:", "____________________"],
            ["Date:", self.data.get("prescription_date", "")],
            ["N° licence professionnelle:", self.data.get("license_number", "")],
            ["Validation supervision (si applicable):", "____________________"],
            ["Conforme aux recommandations HAS:", "☑ Oui ☐ Non"],
            ["Documentation archivée:", "☑ Dossier patient ☑ Base données"],
        ]

        compliance_table = Table(compliance_data, colWidths=[3 * inch, 3 * inch])
        compliance_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("SPAN", (0, 0), (-1, 0)),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2d3748")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#4a5568")),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#edf2f7")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return compliance_table

    def _generate_default_medical_blocks(self) -> List[Dict[str, Any]]:
        """Generate default medical exercise prescription"""
        return [
            {
                "phase_name": "Phase Préparatoire - Analgésie",
                "phase_info": {
                    "description": "Réduction de la douleur et inflammation",
                    "duration": "1-2 semaines",
                    "objective": "EVA < 5/10, mobilité passive libre",
                },
                "exercises": [
                    {
                        "name": "Mobilisation passive",
                        "prescription": "10 min, 2x/jour",
                        "parameters": "ROM disponible, sans douleur",
                        "precautions": "Respecter seuil douloureux",
                        "progression": "Amplitude selon tolérance",
                    },
                    {
                        "name": "Cryothérapie",
                        "prescription": "15 min post-exercice",
                        "parameters": "Froid sec, protection cutanée",
                        "precautions": "Vérifier sensibilité",
                        "progression": "Maintenir protocole",
                    },
                    {
                        "name": "Contractions isométriques",
                        "prescription": "5s x 10, 3 séries",
                        "parameters": "50% force maximale",
                        "precautions": "Arrêt si douleur",
                        "progression": "Augmentation durée puis force",
                    },
                ],
                "tracking_parameters": {
                    "rom_initial": "50% normale",
                    "rom_target": "80% normale",
                    "pain_initial": "7/10",
                    "pain_target": "3/10",
                    "strength_initial": "3/5",
                    "strength_target": "4/5",
                },
            },
            {
                "phase_name": "Phase Active - Renforcement",
                "phase_info": {
                    "description": "Récupération force et fonction",
                    "duration": "3-4 semaines",
                    "objective": "Force 4/5, fonction > 70%",
                },
                "exercises": [
                    {
                        "name": "Renforcement concentrique",
                        "prescription": "12-15 reps, 3 séries",
                        "parameters": "60-70% 1RM",
                        "precautions": "Progression graduelle",
                        "progression": "Charge +10% par semaine",
                    },
                    {
                        "name": "Exercices fonctionnels",
                        "prescription": "15 min, 3x/semaine",
                        "parameters": "Gestes de la vie quotidienne",
                        "precautions": "Adapter à l'activité patient",
                        "progression": "Complexité croissante",
                    },
                    {
                        "name": "Proprioception",
                        "prescription": "10 min, quotidien",
                        "parameters": "Surfaces instables",
                        "precautions": "Sécuriser environnement",
                        "progression": "Yeux fermés, perturbations",
                    },
                ],
                "tracking_parameters": {
                    "rom_initial": "80% normale",
                    "rom_target": "ROM complète",
                    "pain_initial": "3/10",
                    "pain_target": "1/10",
                    "strength_initial": "4/5",
                    "strength_target": "5/5",
                },
            },
        ]

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Medical template data requirements"""
        return {
            "type": "object",
            "properties": {
                "facility_name": {"type": "string"},
                "practitioner_name": {"type": "string"},
                "practitioner_credentials": {"type": "string"},
                "license_number": {"type": "string"},
                "prescription_date": {"type": "string"},
                "patient_info": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "primary_diagnosis": {"type": "string"},
                        "secondary_diagnosis": {"type": "string"},
                        "treatment_start": {"type": "string"},
                        "session_count": {"type": "integer"},
                        "prescribing_physician": {"type": "string"},
                        "therapeutic_goal": {"type": "string"},
                    },
                },
                "medical_assessment": {
                    "type": "object",
                    "properties": {
                        "general_condition": {"type": "string"},
                        "functional_limitations": {"type": "string"},
                        "absolute_contraindications": {"type": "string"},
                        "relative_contraindications": {"type": "string"},
                        "special_precautions": {"type": "string"},
                        "medications": {"type": "string"},
                        "last_evaluation": {"type": "string"},
                    },
                },
                "treatment_objectives": {
                    "type": "object",
                    "properties": {
                        "primary_objective": {"type": "string"},
                        "secondary_objectives": {"type": "string"},
                        "progression_criteria": {"type": "string"},
                        "estimated_duration": {"type": "string"},
                        "session_frequency": {"type": "string"},
                        "reevaluation_date": {"type": "string"},
                        "stop_criteria": {"type": "string"},
                    },
                },
                "exercise_prescription": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "phase_name": {"type": "string"},
                            "phase_info": {"type": "object"},
                            "exercises": {"type": "array"},
                            "tracking_parameters": {"type": "object"},
                        },
                    },
                },
                "medical_notes": {
                    "type": "object",
                    "properties": {
                        "general_observations": {"type": "string"},
                        "necessary_adaptations": {"type": "string"},
                        "treatment_response": {"type": "string"},
                        "recommendations": {"type": "string"},
                        "next_evaluation": {"type": "string"},
                        "physician_communication": {"type": "string"},
                        "continuity_notes": {"type": "string"},
                    },
                },
            },
            "required": [
                "facility_name",
                "practitioner_name",
                "practitioner_credentials",
            ],
        }
