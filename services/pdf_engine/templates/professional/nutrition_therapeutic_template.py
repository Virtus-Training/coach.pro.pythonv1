"""
Nutrition Therapeutic Template - Medical compliance and therapeutic nutrition
Clinical-grade nutrition planning for medical conditions and dietary restrictions
Target: Diététiciens, pathologies, régimes stricts
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import Spacer, Table, TableStyle

from ..base_template import BaseTemplate


class NutritionTherapeuticTemplate(BaseTemplate):
    """
    Nutrition Therapeutic Template - Medical compliance with detailed tracking
    Clinical format for therapeutic nutrition interventions
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "medical_compliance",
            "layout": "clinical_format",
            "compliance": True,
            "allergen_tracking": True,
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
                "therapeutic": "#6b46c1",
            },
            "fonts": {
                "title": {"name": "Times-Bold", "size": 18},
                "subtitle": {"name": "Times-Bold", "size": 14},
                "heading": {"name": "Times-Bold", "size": 12},
                "body": {"name": "Times-Roman", "size": 10},
                "caption": {"name": "Times-Italic", "size": 8},
                "medical": {"name": "Times-Roman", "size": 9},
            },
            "layout": {
                "margins": {"top": 60, "bottom": 60, "left": 50, "right": 50},
                "header_height": 80,
                "footer_height": 50,
                "block_spacing": 15,
                "medical_format": True,
            },
            "therapeutic": {
                "show_allergens": True,
                "show_contraindications": True,
                "show_monitoring": True,
                "show_substitutions": True,
                "show_compliance": True,
            },
        }

    def _build_content(self) -> List[Any]:
        """Build therapeutic nutrition content with medical compliance"""
        elements = []

        # Medical header with practitioner information
        elements.append(self._build_medical_header())
        elements.append(Spacer(1, 15))

        # Patient information and medical context
        elements.append(self._build_patient_medical_info())
        elements.append(Spacer(1, 15))

        # Therapeutic nutrition assessment
        elements.append(self._build_therapeutic_assessment())
        elements.append(Spacer(1, 15))

        # Dietary restrictions and allergens
        elements.append(self._build_restrictions_allergens())
        elements.append(Spacer(1, 15))

        # Therapeutic nutrition plan
        elements.append(self._build_therapeutic_nutrition_plan())
        elements.append(Spacer(1, 15))

        # Monitoring and compliance
        elements.append(self._build_monitoring_compliance())
        elements.append(Spacer(1, 15))

        # Substitutions and adaptations
        elements.append(self._build_substitutions_guide())
        elements.append(Spacer(1, 15))

        # Medical follow-up and documentation
        elements.append(self._build_medical_followup())

        return elements

    def _build_medical_header(self) -> Table:
        """Build medical header with practitioner credentials"""
        facility = self.data.get("facility_name", "Cabinet de Diététique Thérapeutique")
        practitioner = self.data.get("practitioner_name", "Diététicien(ne) D.E.")
        credentials = self.data.get(
            "practitioner_credentials", "Spécialiste Nutrition Thérapeutique"
        )
        date = self.data.get("plan_date", "Date non spécifiée")

        header_data = [
            [f"{facility}", f"Date: {date}"],
            [f"{practitioner}", "PLAN NUTRITIONNEL THÉRAPEUTIQUE"],
            [f"{credentials}", "Approche Evidence-Based"],
            [
                f"N° ADELI: {self.data.get('adeli_number', 'N/A')}",
                f"Ordonnance: {self.data.get('prescription_ref', 'N/A')}",
            ],
        ]

        header_table = Table(header_data, colWidths=[3 * inch, 3 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    # Facility and date
                    ("FONTNAME", (0, 0), (0, 0), "Times-Bold"),
                    ("FONTNAME", (1, 0), (1, 0), "Times-Roman"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    # Practitioner and title
                    ("FONTNAME", (0, 1), (0, 1), "Times-Roman"),
                    ("FONTNAME", (1, 1), (1, 1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (0, 1), 10),
                    ("FONTSIZE", (1, 1), (1, 1), 13),
                    (
                        "TEXTCOLOR",
                        (1, 1),
                        (1, 1),
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    # Credentials and evidence
                    ("FONTSIZE", (0, 2), (-1, 2), 9),
                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (-1, 2),
                        HexColor(self.merged_config["colors"]["text_secondary"]),
                    ),
                    # Professional numbers
                    ("FONTSIZE", (0, 3), (-1, 3), 8),
                    ("FONTNAME", (0, 3), (-1, 3), "Times-Italic"),
                    (
                        "TEXTCOLOR",
                        (0, 3),
                        (-1, 3),
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
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return header_table

    def _build_patient_medical_info(self) -> Table:
        """Build comprehensive patient medical information"""
        patient = self.data.get("patient_info", {})

        patient_data = [
            ["INFORMATIONS PATIENT ET CONTEXTE MÉDICAL", "", ""],
            [
                "Nom/Prénom:",
                patient.get("name", "Non spécifié"),
                "Âge: " + str(patient.get("age", "N/A")),
            ],
            [
                "Poids actuel:",
                f"{patient.get('current_weight', 'N/A')} kg",
                "Taille: " + f"{patient.get('height', 'N/A')} cm",
            ],
            [
                "IMC:",
                f"{patient.get('bmi', 'N/A')} kg/m²",
                "Poids cible: " + f"{patient.get('target_weight', 'N/A')} kg",
            ],
            [
                "Diagnostic principal:",
                patient.get("primary_diagnosis", "Non spécifié"),
                "",
            ],
            ["Comorbidités:", patient.get("comorbidities", "Aucune"), ""],
            [
                "Médecin prescripteur:",
                patient.get("prescribing_physician", "Non spécifié"),
                "",
            ],
            [
                "Traitement médicamenteux:",
                patient.get("current_medications", "Aucun"),
                "",
            ],
            [
                "Antécédents nutritionnels:",
                patient.get("nutrition_history", "Non documentés"),
                "",
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
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor(self.merged_config["colors"]["therapeutic"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["therapeutic"]),
                    ),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#faf5ff")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        return patient_table

    def _build_therapeutic_assessment(self) -> Table:
        """Build therapeutic nutrition assessment"""
        assessment = self.data.get("therapeutic_assessment", {})

        assessment_data = [
            ["ÉVALUATION NUTRITIONNELLE THÉRAPEUTIQUE", ""],
            [
                "Besoins énergétiques:",
                f"{assessment.get('energy_needs', 'Non calculé')} kcal/j",
            ],
            [
                "Besoins protéiques:",
                f"{assessment.get('protein_needs', 'Non calculé')} g/kg/j",
            ],
            ["Restrictions hydriques:", assessment.get("fluid_restrictions", "Aucune")],
            [
                "Textures alimentaires:",
                assessment.get("texture_modifications", "Normales"),
            ],
            [
                "Voie d'alimentation:",
                assessment.get("feeding_route", "Orale exclusive"),
            ],
            [
                "Dénutrition (MNA/NRS):",
                assessment.get("malnutrition_score", "Score non évalué"),
            ],
            [
                "Troubles déglutition:",
                assessment.get("swallowing_issues", "Non détectés"),
            ],
            [
                "Intolérances digestives:",
                assessment.get("digestive_issues", "Aucune rapportée"),
            ],
            [
                "Objectifs thérapeutiques:",
                assessment.get("therapeutic_goals", "À définir"),
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
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Content
                    ("FONTNAME", (0, 1), (0, -1), "Times-Bold"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["accent"]),
                    ),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f0fff4")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return assessment_table

    def _build_restrictions_allergens(self) -> Table:
        """Build dietary restrictions and allergen management"""
        restrictions = self.data.get("dietary_restrictions", {})

        restrictions_data = [
            ["⚠️ RESTRICTIONS ALIMENTAIRES ET ALLERGÈNES", "", ""],
            ["Type de Restriction", "Détails", "Niveau Criticité"],
            [
                "🚫 Allergies alimentaires",
                restrictions.get("food_allergies", "Aucune connue"),
                restrictions.get("allergy_severity", "N/A"),
            ],
            [
                "⚡ Intolérances",
                restrictions.get("food_intolerances", "Aucune rapportée"),
                restrictions.get("intolerance_level", "N/A"),
            ],
            [
                "🥗 Régime spécifique",
                restrictions.get("special_diet", "Aucun"),
                restrictions.get("diet_strictness", "N/A"),
            ],
            [
                "💊 Interactions médicamenteuses",
                restrictions.get("drug_interactions", "Aucune connue"),
                restrictions.get("interaction_risk", "N/A"),
            ],
            [
                "🍽️ Restrictions religieuses/culturelles",
                restrictions.get("cultural_restrictions", "Aucune"),
                "Information",
            ],
            [
                "⚖️ Restrictions quantitatives",
                restrictions.get("portion_restrictions", "Aucune"),
                restrictions.get("portion_importance", "N/A"),
            ],
        ]

        restrictions_table = Table(
            restrictions_data, colWidths=[2.2 * inch, 2.8 * inch, 1 * inch]
        )
        restrictions_table.setStyle(
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
                    ("FONTSIZE", (0, 1), (-1, 1), 9),
                    # Critical rows highlighting
                    (
                        "TEXTCOLOR",
                        (2, 2),
                        (2, 2),
                        HexColor(self.merged_config["colors"]["error"]),
                    ),  # Allergies
                    (
                        "TEXTCOLOR",
                        (2, 5),
                        (2, 5),
                        HexColor(self.merged_config["colors"]["error"]),
                    ),  # Drug interactions
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["warning"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return restrictions_table

    def _build_therapeutic_nutrition_plan(self) -> Table:
        """Build detailed therapeutic nutrition plan"""
        nutrition_plan = self.data.get("nutrition_plan", {})

        plan_data = [
            ["PLAN NUTRITIONNEL THÉRAPEUTIQUE DÉTAILLÉ", "", "", ""],
            ["Repas", "Composition", "Quantités", "Observations Thérapeutiques"],
            [
                "Petit-déjeuner",
                nutrition_plan.get(
                    "breakfast_composition", "À définir selon pathologie"
                ),
                nutrition_plan.get("breakfast_portions", "Selon besoins"),
                nutrition_plan.get("breakfast_notes", "Respecter les interactions"),
            ],
            [
                "Collation matinale",
                nutrition_plan.get("morning_snack", "Si prescrite"),
                nutrition_plan.get("morning_snack_portions", ""),
                nutrition_plan.get("morning_snack_notes", "Optionnelle selon bilan"),
            ],
            [
                "Déjeuner",
                nutrition_plan.get("lunch_composition", "Repas principal équilibré"),
                nutrition_plan.get("lunch_portions", "Selon prescription"),
                nutrition_plan.get("lunch_notes", "Surveillance post-prandiale"),
            ],
            [
                "Collation",
                nutrition_plan.get("afternoon_snack", "Si besoins énergétiques"),
                nutrition_plan.get("afternoon_portions", ""),
                nutrition_plan.get("afternoon_notes", "Adaptation selon tolérance"),
            ],
            [
                "Dîner",
                nutrition_plan.get("dinner_composition", "Léger et digestible"),
                nutrition_plan.get("dinner_portions", "Réduit si nécessaire"),
                nutrition_plan.get("dinner_notes", "3h avant coucher minimum"),
            ],
            [
                "Supplémentation",
                nutrition_plan.get("supplementation", "Selon prescription médicale"),
                nutrition_plan.get("supplement_doses", "Posologie stricte"),
                nutrition_plan.get(
                    "supplement_notes", "Surveillance effets secondaires"
                ),
            ],
        ]

        plan_table = Table(
            plan_data, colWidths=[1.2 * inch, 2 * inch, 1.3 * inch, 1.5 * inch]
        )
        plan_table.setStyle(
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
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Times-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#eff6ff")),
                    ("FONTSIZE", (0, 1), (-1, 1), 8),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["medical"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )

        return plan_table

    def _build_monitoring_compliance(self) -> Table:
        """Build monitoring and compliance tracking section"""
        monitoring = self.data.get("monitoring_plan", {})

        monitoring_data = [
            ["SURVEILLANCE ET COMPLIANCE THÉRAPEUTIQUE", "", ""],
            ["Paramètre de Suivi", "Fréquence", "Seuils d'Alerte"],
            [
                "📊 Poids corporel",
                monitoring.get("weight_frequency", "Hebdomadaire"),
                f"±{monitoring.get('weight_threshold', '2')}kg/mois",
            ],
            [
                "🩸 Paramètres biologiques",
                monitoring.get("bio_frequency", "Selon prescription"),
                "Selon normes laboratoire",
            ],
            [
                "🍽️ Apports alimentaires",
                monitoring.get("intake_frequency", "Quotidien"),
                "< 75% des recommandations",
            ],
            [
                "💧 Bilan hydrique",
                monitoring.get("fluid_frequency", "Si applicable"),
                monitoring.get("fluid_limits", "Selon pathologie"),
            ],
            [
                "😌 Tolérance digestive",
                monitoring.get("tolerance_frequency", "Quotidien"),
                "Symptômes persistants >48h",
            ],
            [
                "💊 Observance suppléments",
                monitoring.get("supplement_frequency", "Si prescrits"),
                "< 80% des prises",
            ],
            [
                "📝 Tenue carnet alimentaire",
                monitoring.get("diary_frequency", "Première semaine"),
                "Manque >2 jours consécutifs",
            ],
            [
                "👨‍⚕️ Consultation de suivi",
                monitoring.get("followup_frequency", "Selon protocole"),
                "Dégradation état général",
            ],
        ]

        monitoring_table = Table(
            monitoring_data, colWidths=[2.2 * inch, 1.8 * inch, 2 * inch]
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
                        HexColor(self.merged_config["colors"]["caution"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Times-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#fef7ed")),
                    ("FONTSIZE", (0, 1), (-1, 1), 8),
                    # Alert thresholds
                    (
                        "TEXTCOLOR",
                        (2, 2),
                        (2, -1),
                        HexColor(self.merged_config["colors"]["error"]),
                    ),
                    ("FONTNAME", (2, 2), (2, -1), "Times-Bold"),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["caution"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return monitoring_table

    def _build_substitutions_guide(self) -> Table:
        """Build food substitutions and adaptations guide"""
        substitutions = self.data.get("substitutions_guide", {})

        substitutions_data = [
            ["GUIDE DES SUBSTITUTIONS THÉRAPEUTIQUES", "", ""],
            [
                "Aliment à Éviter",
                "Substitution Recommandée",
                "Justification Thérapeutique",
            ],
            [
                substitutions.get("avoid_1", "Selon restrictions"),
                substitutions.get("substitute_1", "Alternative sûre"),
                substitutions.get("reason_1", "Éviter interactions/allergie"),
            ],
            [
                substitutions.get("avoid_2", "Selon restrictions"),
                substitutions.get("substitute_2", "Alternative sûre"),
                substitutions.get("reason_2", "Contrôle pathologie"),
            ],
            [
                substitutions.get("avoid_3", "Selon restrictions"),
                substitutions.get("substitute_3", "Alternative sûre"),
                substitutions.get("reason_3", "Optimisation thérapeutique"),
            ],
            [
                "🧂 Sodium (si restriction)",
                "Herbes, épices, citron",
                "Contrôle tension/rétention hydrique",
            ],
            [
                "🍬 Sucres simples (si diabète)",
                "Édulcorants autorisés",
                "Gestion glycémique",
            ],
            [
                "🥛 Lactose (si intolérance)",
                "Alternatives végétales enrichies",
                "Prévention troubles digestifs",
            ],
        ]

        substitutions_table = Table(
            substitutions_data, colWidths=[2 * inch, 2 * inch, 2 * inch]
        )
        substitutions_table.setStyle(
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
                    # Subheader
                    ("FONTNAME", (0, 1), (-1, 1), "Times-Bold"),
                    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#f0fff4")),
                    ("FONTSIZE", (0, 1), (-1, 1), 8),
                    # Content
                    ("FONTSIZE", (0, 2), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["success"]),
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return substitutions_table

    def _build_medical_followup(self) -> Table:
        """Build medical follow-up and documentation section"""
        followup = self.data.get("medical_followup", {})

        followup_data = [
            ["SUIVI MÉDICAL ET DOCUMENTATION", ""],
            [
                "Prochaine consultation:",
                followup.get("next_consultation", "À programmer selon évolution"),
            ],
            [
                "Paramètres à surveiller:",
                followup.get("monitoring_parameters", "Selon protocole pathologie"),
            ],
            [
                "Critères de réussite:",
                followup.get("success_criteria", "À définir avec équipe médicale"),
            ],
            [
                "Critères d'alerte:",
                followup.get("alert_criteria", "Dégradation état nutritionnel"),
            ],
            [
                "Communication équipe:",
                followup.get("team_communication", "Transmission régulière au médecin"),
            ],
            [
                "Documentation requise:",
                followup.get("documentation", "Carnet alimentaire + bilan mensuel"),
            ],
            [
                "Éducation thérapeutique:",
                followup.get("education_plan", "Selon besoin patient/famille"),
            ],
            [
                "Contact urgence:",
                followup.get("emergency_contact", "Médecin prescripteur ou service"),
            ],
            [
                "Révision plan:",
                followup.get("plan_revision", "Selon évolution clinique"),
            ],
        ]

        followup_table = Table(followup_data, colWidths=[2.5 * inch, 3.5 * inch])
        followup_table.setStyle(
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
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#eff6ff")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        return followup_table

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Nutrition Therapeutic template data requirements"""
        return {
            "type": "object",
            "properties": {
                "facility_name": {"type": "string"},
                "practitioner_name": {"type": "string"},
                "practitioner_credentials": {"type": "string"},
                "adeli_number": {"type": "string"},
                "prescription_ref": {"type": "string"},
                "plan_date": {"type": "string"},
                "patient_info": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "current_weight": {"type": "number"},
                        "height": {"type": "integer"},
                        "bmi": {"type": "number"},
                        "target_weight": {"type": "number"},
                        "primary_diagnosis": {"type": "string"},
                        "comorbidities": {"type": "string"},
                        "prescribing_physician": {"type": "string"},
                        "current_medications": {"type": "string"},
                        "nutrition_history": {"type": "string"},
                    },
                },
                "therapeutic_assessment": {
                    "type": "object",
                    "properties": {
                        "energy_needs": {"type": "string"},
                        "protein_needs": {"type": "string"},
                        "fluid_restrictions": {"type": "string"},
                        "texture_modifications": {"type": "string"},
                        "feeding_route": {"type": "string"},
                        "malnutrition_score": {"type": "string"},
                        "swallowing_issues": {"type": "string"},
                        "digestive_issues": {"type": "string"},
                        "therapeutic_goals": {"type": "string"},
                    },
                },
                "dietary_restrictions": {
                    "type": "object",
                    "properties": {
                        "food_allergies": {"type": "string"},
                        "allergy_severity": {"type": "string"},
                        "food_intolerances": {"type": "string"},
                        "intolerance_level": {"type": "string"},
                        "special_diet": {"type": "string"},
                        "diet_strictness": {"type": "string"},
                        "drug_interactions": {"type": "string"},
                        "interaction_risk": {"type": "string"},
                        "cultural_restrictions": {"type": "string"},
                        "portion_restrictions": {"type": "string"},
                        "portion_importance": {"type": "string"},
                    },
                },
                "nutrition_plan": {
                    "type": "object",
                    "properties": {
                        "breakfast_composition": {"type": "string"},
                        "breakfast_portions": {"type": "string"},
                        "breakfast_notes": {"type": "string"},
                        "morning_snack": {"type": "string"},
                        "morning_snack_portions": {"type": "string"},
                        "morning_snack_notes": {"type": "string"},
                        "lunch_composition": {"type": "string"},
                        "lunch_portions": {"type": "string"},
                        "lunch_notes": {"type": "string"},
                        "afternoon_snack": {"type": "string"},
                        "afternoon_portions": {"type": "string"},
                        "afternoon_notes": {"type": "string"},
                        "dinner_composition": {"type": "string"},
                        "dinner_portions": {"type": "string"},
                        "dinner_notes": {"type": "string"},
                        "supplementation": {"type": "string"},
                        "supplement_doses": {"type": "string"},
                        "supplement_notes": {"type": "string"},
                    },
                },
                "monitoring_plan": {
                    "type": "object",
                    "properties": {
                        "weight_frequency": {"type": "string"},
                        "weight_threshold": {"type": "string"},
                        "bio_frequency": {"type": "string"},
                        "intake_frequency": {"type": "string"},
                        "fluid_frequency": {"type": "string"},
                        "fluid_limits": {"type": "string"},
                        "tolerance_frequency": {"type": "string"},
                        "supplement_frequency": {"type": "string"},
                        "diary_frequency": {"type": "string"},
                        "followup_frequency": {"type": "string"},
                    },
                },
                "substitutions_guide": {
                    "type": "object",
                    "properties": {
                        "avoid_1": {"type": "string"},
                        "substitute_1": {"type": "string"},
                        "reason_1": {"type": "string"},
                        "avoid_2": {"type": "string"},
                        "substitute_2": {"type": "string"},
                        "reason_2": {"type": "string"},
                        "avoid_3": {"type": "string"},
                        "substitute_3": {"type": "string"},
                        "reason_3": {"type": "string"},
                    },
                },
                "medical_followup": {
                    "type": "object",
                    "properties": {
                        "next_consultation": {"type": "string"},
                        "monitoring_parameters": {"type": "string"},
                        "success_criteria": {"type": "string"},
                        "alert_criteria": {"type": "string"},
                        "team_communication": {"type": "string"},
                        "documentation": {"type": "string"},
                        "education_plan": {"type": "string"},
                        "emergency_contact": {"type": "string"},
                        "plan_revision": {"type": "string"},
                    },
                },
            },
            "required": ["facility_name", "practitioner_name", "patient_info"],
        }
