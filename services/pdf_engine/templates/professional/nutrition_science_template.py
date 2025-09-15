"""
Nutrition Science Template - Data-driven precision nutrition
Advanced analytics and scientific approach to nutrition planning
Target: Nutritionnistes, bodybuilders, athlètes performance
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4

from ..base_template import BaseTemplate
from ...components.professional_components import (
    MacronutrientWheelComponent,
    DataVisualizationComponent,
    NutritionFactsComponent,
    PremiumHeaderComponent
)


class NutritionScienceTemplate(BaseTemplate):
    """
    Nutrition Science Template - Data-driven with advanced analytics
    Precision nutrition with scientific backing and detailed breakdowns
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "theme": "data_precision",
            "layout": "dashboard_analytics",
            "scientific_approach": True,
            "precision_level": "high",
            "chart_complexity": "advanced",
            "colors": {
                "primary": "#1a202c",
                "secondary": "#4a5568",
                "accent": "#0bc5ea",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text_primary": "#1a202c",
                "text_secondary": "#4a5568",
                "success": "#38a169",
                "warning": "#d69e2e",
                "data_primary": "#3182ce",
                "data_secondary": "#805ad5",
                "chart_accent": "#ed64a6"
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 22},
                "subtitle": {"name": "Helvetica-Bold", "size": 16},
                "heading": {"name": "Helvetica-Bold", "size": 13},
                "body": {"name": "Helvetica", "size": 10},
                "caption": {"name": "Helvetica", "size": 8},
                "data": {"name": "Courier", "size": 9},
                "scientific": {"name": "Times-Roman", "size": 9}
            },
            "layout": {
                "margins": {"top": 50, "bottom": 50, "left": 40, "right": 40},
                "header_height": 100,
                "footer_height": 40,
                "block_spacing": 20,
                "data_density": "high"
            },
            "analytics": {
                "show_macros_breakdown": True,
                "show_micros_analysis": True,
                "show_trends": True,
                "show_ratios": True,
                "show_timing": True,
                "show_biomarkers": True
            }
        }

    def _build_content(self) -> List[Any]:
        """Build scientific nutrition content with advanced analytics"""
        elements = []

        # Scientific header with client metrics
        elements.append(self._build_scientific_header())
        elements.append(Spacer(1, 15))

        # Nutritional analytics dashboard
        elements.append(self._build_analytics_dashboard())
        elements.append(Spacer(1, 20))

        # Macronutrient scientific breakdown
        elements.append(self._build_macro_science_analysis())
        elements.append(Spacer(1, 15))

        # Micronutrient analysis
        elements.append(self._build_micronutrient_analysis())
        elements.append(Spacer(1, 20))

        # Metabolic calculations and requirements
        elements.append(self._build_metabolic_calculations())
        elements.append(Spacer(1, 15))

        # Meal timing and distribution analysis
        elements.append(self._build_meal_timing_analysis())
        elements.append(Spacer(1, 15))

        # Scientific recommendations with evidence
        elements.append(self._build_scientific_recommendations())

        # Performance biomarkers correlation
        if self.data.get("biomarkers"):
            elements.append(self._build_biomarkers_correlation())

        return elements

    def _build_scientific_header(self) -> Table:
        """Build scientific header with client biometrics and calculations"""
        client_name = self.data.get("client_name", "Client")
        analysis_date = self.data.get("analysis_date", "Date non spécifiée")
        biometrics = self.data.get("biometrics", {})

        header_data = [
            ["ANALYSE NUTRITIONNELLE SCIENTIFIQUE", f"Date: {analysis_date}"],
            [f"Client: {client_name}", "Approche Evidence-Based"],
            [
                f"Âge: {biometrics.get('age', 'N/A')} | "
                f"Poids: {biometrics.get('weight', 'N/A')}kg | "
                f"Taille: {biometrics.get('height', 'N/A')}cm",
                f"BF%: {biometrics.get('body_fat', 'N/A')}% | "
                f"FFM: {biometrics.get('lean_mass', 'N/A')}kg"
            ]
        ]

        header_table = Table(header_data, colWidths=[3.5*inch, 2.5*inch])
        header_table.setStyle(TableStyle([
            # Main header
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('TEXTCOLOR', (0, 0), (0, 0), HexColor(self.merged_config["colors"]["primary"])),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["surface"])),

            # Client info
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 12),

            # Biometrics
            ('FONTNAME', (0, 2), (-1, 2), 'Courier'),
            ('FONTSIZE', (0, 2), (-1, 2), 10),
            ('TEXTCOLOR', (0, 2), (-1, 2), HexColor(self.merged_config["colors"]["text_secondary"])),

            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, HexColor(self.merged_config["colors"]["primary"])),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))

        return header_table

    def _build_analytics_dashboard(self) -> Table:
        """Build comprehensive nutritional analytics dashboard"""
        nutrition_data = self.data.get("nutrition_analytics", {})

        # Key metrics calculation
        tdee = nutrition_data.get("tdee", 2200)
        target_calories = nutrition_data.get("target_calories", tdee)
        protein_g = nutrition_data.get("protein_g", 150)
        carbs_g = nutrition_data.get("carbs_g", 200)
        fat_g = nutrition_data.get("fat_g", 80)

        # Calculate percentages
        total_calories = (protein_g * 4) + (carbs_g * 4) + (fat_g * 9)
        protein_pct = round((protein_g * 4 / total_calories) * 100, 1) if total_calories > 0 else 0
        carbs_pct = round((carbs_g * 4 / total_calories) * 100, 1) if total_calories > 0 else 0
        fat_pct = round((fat_g * 9 / total_calories) * 100, 1) if total_calories > 0 else 0

        # Macronutrient wheel
        macro_wheel = MacronutrientWheelComponent(protein_g, carbs_g, fat_g, width=120, height=120)

        # Analytics table
        analytics_data = [
            ["TABLEAU DE BORD ANALYTIQUE", "", ""],
            ["Métrique", "Valeur", "Référence Scientifique"],
            ["TDEE Calculé", f"{tdee} kcal", "Mifflin-St Jeor + NAF"],
            ["Calories Cibles", f"{target_calories} kcal", f"TDEE {'+' if target_calories > tdee else ''}{target_calories - tdee:+d}"],
            ["Protéines", f"{protein_g}g ({protein_pct}%)", f"{round(protein_g / nutrition_data.get('weight', 70), 1)}g/kg"],
            ["Glucides", f"{carbs_g}g ({carbs_pct}%)", "45-65% calories totales"],
            ["Lipides", f"{fat_g}g ({fat_pct}%)", "20-35% calories totales"],
            ["Ratio P:C:L", f"{protein_pct}:{carbs_pct}:{fat_pct}", "Optimisation performance"],
            ["Fibres Cibles", f"{nutrition_data.get('fiber_target', 25)}g", "14g/1000 kcal"],
            ["Hydratation", f"{nutrition_data.get('water_target', 35)}ml/kg", "EFSA 2010"]
        ]

        # Create combined layout
        dashboard_layout = [
            [analytics_data, macro_wheel]
        ]

        dashboard = Table(dashboard_layout, colWidths=[4*inch, 2*inch])
        dashboard.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        ]))

        # Style the analytics table
        analytics_table = Table(analytics_data, colWidths=[2*inch, 1.5*inch, 2*inch])
        analytics_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["data_primary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor(self.merged_config["colors"]["surface"])),

            # Data rows
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 2), (1, -1), 'Courier'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["data_primary"])),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
        ]))

        return analytics_table

    def _build_macro_science_analysis(self) -> Table:
        """Build detailed macronutrient scientific analysis"""
        macro_analysis = self.data.get("macronutrient_analysis", {})

        analysis_data = [
            ["ANALYSE SCIENTIFIQUE DES MACRONUTRIMENTS", "", "", ""],
            ["Nutriment", "Distribution", "Timing Optimal", "Justification Scientifique"],
            [
                "Protéines",
                f"{macro_analysis.get('protein_distribution', '25-30-30-15')}%",
                "Post-exercice + répartition",
                "Synthèse protéique max (Moore et al., 2014)"
            ],
            [
                "Glucides",
                f"{macro_analysis.get('carb_distribution', '40-30-20-10')}%",
                "Pré/post entraînement",
                "Resynthèse glycogène (Ivy & Robert, 2018)"
            ],
            [
                "Lipides",
                f"{macro_analysis.get('fat_distribution', '30-25-25-20')}%",
                "Repas éloignés exercice",
                "Absorption et hormones (Helms et al., 2014)"
            ],
            [
                "Fibres",
                f"{macro_analysis.get('fiber_per_meal', '6-8-5-6')}g",
                "Repas principaux",
                "Santé intestinale et satiété (Slavin, 2013)"
            ]
        ]

        analysis_table = Table(analysis_data, colWidths=[1.2*inch, 1.5*inch, 1.8*inch, 2*inch])
        analysis_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["data_secondary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor(self.merged_config["colors"]["surface"])),
            ('FONTSIZE', (0, 1), (-1, 1), 9),

            # Content
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["data_secondary"])),

            # Highlight scientific references
            ('TEXTCOLOR', (3, 2), (3, -1), HexColor(self.merged_config["colors"]["accent"])),
            ('FONTNAME', (3, 2), (3, -1), 'Times-Italic'),

            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
        ]))

        return analysis_table

    def _build_micronutrient_analysis(self) -> Table:
        """Build comprehensive micronutrient analysis"""
        micro_data = self.data.get("micronutrient_analysis", {})

        # Priority micronutrients for athletes/performance
        micronutrients_data = [
            ["ANALYSE MICRONUTRIMENTS - FOCUS PERFORMANCE", "", "", ""],
            ["Micronutriment", "Apport Actuel", "AJR/Optimal", "Statut"],
            ["Vitamine D", f"{micro_data.get('vit_d', 15)}μg", "20-50μg", self._get_status(micro_data.get('vit_d', 15), 20, 50)],
            ["B12", f"{micro_data.get('b12', 2.4)}μg", "2.4-100μg", self._get_status(micro_data.get('b12', 2.4), 2.4, 100)],
            ["Fer", f"{micro_data.get('iron', 14)}mg", "8-18mg", self._get_status(micro_data.get('iron', 14), 8, 18)],
            ["Magnésium", f"{micro_data.get('magnesium', 320)}mg", "400-420mg", self._get_status(micro_data.get('magnesium', 320), 400, 420)],
            ["Zinc", f"{micro_data.get('zinc', 9)}mg", "8-11mg", self._get_status(micro_data.get('zinc', 9), 8, 11)],
            ["Oméga-3", f"{micro_data.get('omega3', 1.2)}g", "2-3g", self._get_status(micro_data.get('omega3', 1.2), 2, 3)],
            ["Créatine", f"{micro_data.get('creatine', 0)}g", "3-5g", self._get_status(micro_data.get('creatine', 0), 3, 5)],
            ["Caféine", f"{micro_data.get('caffeine', 100)}mg", "3-6mg/kg", "Timing optimal"]
        ]

        micro_table = Table(micronutrients_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 2*inch])
        micro_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["chart_accent"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor("#fdf2f8")),
            ('FONTSIZE', (0, 1), (-1, 1), 9),

            # Content
            ('FONTSIZE', (0, 2), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["chart_accent"])),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
        ]))

        return micro_table

    def _build_metabolic_calculations(self) -> Table:
        """Build detailed metabolic calculations and requirements"""
        metabolism = self.data.get("metabolic_calculations", {})

        calc_data = [
            ["CALCULS MÉTABOLIQUES AVANCÉS", "", ""],
            ["Paramètre", "Valeur Calculée", "Méthode/Formule"],
            ["BMR (Métabolisme Basal)", f"{metabolism.get('bmr', 1650)} kcal", "Mifflin-St Jeor"],
            ["NEAT (Thermogenèse)", f"{metabolism.get('neat', 350)} kcal", "15-30% TDEE"],
            ["TEF (Effet Thermique)", f"{metabolism.get('tef', 220)} kcal", "10% apport calorique"],
            ["EAT (Exercice)", f"{metabolism.get('eat', 300)} kcal", "Cardio + Résistance"],
            ["TDEE Total", f"{metabolism.get('tdee', 2520)} kcal", "BMR + NEAT + TEF + EAT"],
            ["Déficit/Surplus Cible", f"{metabolism.get('target_deficit', -500)} kcal", "0.5-1kg/semaine"],
            ["Protein Leverage", f"{metabolism.get('protein_leverage', 2.2)}g/kg", "Performance + Satiété"],
            ["Leucine Threshold", f"{metabolism.get('leucine_threshold', 2.5)}g", "mTOR activation"]
        ]

        calc_table = Table(calc_data, colWidths=[2.2*inch, 1.8*inch, 2*inch])
        calc_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["success"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor("#f0fff4")),

            # Calculations
            ('FONTNAME', (1, 2), (1, -1), 'Courier'),
            ('FONTNAME', (2, 2), (2, -1), 'Times-Italic'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["success"])),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
        ]))

        return calc_table

    def _build_meal_timing_analysis(self) -> Table:
        """Build meal timing and nutrient distribution analysis"""
        timing_data = self.data.get("meal_timing", {})

        timing_analysis = [
            ["CHRONONUTRITION ET RÉPARTITION OPTIMALE", "", "", ""],
            ["Repas/Timing", "Macros (P:C:L)", "Timing Exercice", "Justification"],
            ["Petit-déjeuner", timing_data.get('breakfast_macros', '25:45:30'), "2-3h avant", "Glycémie stable (O'Neil et al.)"],
            ["Collation Pré-WO", timing_data.get('preworkout_macros', '10:80:10'), "30-60min avant", "Performance glycolytique"],
            ["Post-Workout", timing_data.get('postworkout_macros', '40:50:10'), "0-30min après", "Fenêtre anabolique"],
            ["Déjeuner", timing_data.get('lunch_macros', '30:40:30'), "2-3h post-WO", "Récupération complète"],
            ["Collation PM", timing_data.get('snack_macros', '20:20:60'), "Entre repas", "Hormones et satiété"],
            ["Dîner", timing_data.get('dinner_macros', '35:25:40'), "3h avant coucher", "Récupération nocturne"],
            ["Casein (optionnel)", timing_data.get('casein_macros', '90:5:5'), "Avant coucher", "Anti-catabolisme nocturne"]
        ]

        timing_table = Table(timing_analysis, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 2*inch])
        timing_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["warning"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor("#fffbeb")),
            ('FONTSIZE', (0, 1), (-1, 1), 8),

            # Content
            ('FONTSIZE', (0, 2), (-1, -1), 8),
            ('FONTNAME', (1, 2), (1, -1), 'Courier'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["warning"])),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
        ]))

        return timing_table

    def _build_scientific_recommendations(self) -> Table:
        """Build evidence-based scientific recommendations"""
        recommendations = self.data.get("scientific_recommendations", {})

        rec_data = [
            ["RECOMMANDATIONS SCIENTIFIQUES PERSONNALISÉES", ""],
            ["Priorité", "Recommandation Evidence-Based"],
            ["Hydratation", recommendations.get("hydration", "35ml/kg + 500-750ml/h exercice (Position ACSM)")],
            ["Timing Protéine", recommendations.get("protein_timing", "20-25g leucine riche dans 2h post-exercice")],
            ["Supplémentation", recommendations.get("supplements", "Créatine 3g/j + Vitamine D3 2000UI si déficit")],
            ["Récupération", recommendations.get("recovery", "Glucides 1-1.2g/kg dans 4h post-exercice")],
            ["Performance", recommendations.get("performance", "Caféine 3-6mg/kg 30-60min pré-exercice")],
            ["Composition Corporelle", recommendations.get("body_comp", "Déficit modéré 300-500kcal + entraînement résistance")],
            ["Surveillance", recommendations.get("monitoring", "Pesée hebdomadaire + photos + biomarqueurs trimestriels")]
        ]

        rec_table = Table(rec_data, colWidths=[1.5*inch, 4.5*inch])
        rec_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.merged_config["colors"]["primary"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor(self.merged_config["colors"]["surface"])),

            # Priority labels
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 2), (0, -1), HexColor(self.merged_config["colors"]["accent"])),

            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor(self.merged_config["colors"]["primary"])),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
        ]))

        return rec_table

    def _build_biomarkers_correlation(self) -> Table:
        """Build biomarkers correlation analysis"""
        biomarkers = self.data.get("biomarkers", {})

        biomarkers_data = [
            ["CORRÉLATION BIOMARQUEURS NUTRITIONNELS", "", "", ""],
            ["Biomarqueur", "Valeur Actuelle", "Référence Optimale", "Impact Nutritionnel"],
            ["HbA1c", f"{biomarkers.get('hba1c', 5.2)}%", "<5.5%", "Gestion glucides et timing"],
            ["Lipides (HDL/LDL)", f"{biomarkers.get('hdl', 60)}/{biomarkers.get('ldl', 100)}", ">60/<100", "Qualité lipides (oméga-3)"],
            ["CRP", f"{biomarkers.get('crp', 1.2)}mg/L", "<1.0mg/L", "Anti-inflammatoire (polyphénols)"],
            ["Ferritine", f"{biomarkers.get('ferritin', 80)}μg/L", "30-150μg/L", "Absorption fer + vitamine C"],
            ["25(OH)D", f"{biomarkers.get('vitamin_d', 25)}ng/mL", ">30ng/mL", "Supplémentation D3"],
            ["B12", f"{biomarkers.get('b12_serum', 350)}pg/mL", ">300pg/mL", "Sources B12 ou supplément"],
            ["Homocystéine", f"{biomarkers.get('homocysteine', 8)}μmol/L", "<10μmol/L", "Folates + B6/B12"]
        ]

        biomarkers_table = Table(biomarkers_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 2*inch])
        biomarkers_table.setStyle(TableStyle([
            # Header
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#6b46c1")),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),

            # Subheader
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), HexColor("#f3f4f6")),
            ('FONTSIZE', (0, 1), (-1, 1), 8),

            # Values
            ('FONTNAME', (1, 2), (1, -1), 'Courier'),
            ('FONTNAME', (2, 2), (2, -1), 'Courier'),
            ('FONTSIZE', (0, 2), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#6b46c1")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
        ]))

        return biomarkers_table

    def _get_status(self, current: float, min_optimal: float, max_optimal: float) -> str:
        """Get nutrient status based on optimal ranges"""
        if current < min_optimal:
            return "⚠️ INSUFFISANT"
        elif current > max_optimal:
            return "⚠️ EXCÈS"
        else:
            return "✅ OPTIMAL"

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for Nutrition Science template data requirements"""
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string"},
                "analysis_date": {"type": "string"},
                "biometrics": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "integer"},
                        "weight": {"type": "number"},
                        "height": {"type": "integer"},
                        "body_fat": {"type": "number"},
                        "lean_mass": {"type": "number"}
                    }
                },
                "nutrition_analytics": {
                    "type": "object",
                    "properties": {
                        "tdee": {"type": "integer"},
                        "target_calories": {"type": "integer"},
                        "protein_g": {"type": "integer"},
                        "carbs_g": {"type": "integer"},
                        "fat_g": {"type": "integer"},
                        "fiber_target": {"type": "integer"},
                        "water_target": {"type": "integer"}
                    }
                },
                "macronutrient_analysis": {
                    "type": "object",
                    "properties": {
                        "protein_distribution": {"type": "string"},
                        "carb_distribution": {"type": "string"},
                        "fat_distribution": {"type": "string"},
                        "fiber_per_meal": {"type": "string"}
                    }
                },
                "micronutrient_analysis": {
                    "type": "object",
                    "properties": {
                        "vit_d": {"type": "number"},
                        "b12": {"type": "number"},
                        "iron": {"type": "number"},
                        "magnesium": {"type": "number"},
                        "zinc": {"type": "number"},
                        "omega3": {"type": "number"},
                        "creatine": {"type": "number"},
                        "caffeine": {"type": "number"}
                    }
                },
                "metabolic_calculations": {
                    "type": "object",
                    "properties": {
                        "bmr": {"type": "integer"},
                        "neat": {"type": "integer"},
                        "tef": {"type": "integer"},
                        "eat": {"type": "integer"},
                        "tdee": {"type": "integer"},
                        "target_deficit": {"type": "integer"},
                        "protein_leverage": {"type": "number"},
                        "leucine_threshold": {"type": "number"}
                    }
                },
                "meal_timing": {
                    "type": "object",
                    "properties": {
                        "breakfast_macros": {"type": "string"},
                        "preworkout_macros": {"type": "string"},
                        "postworkout_macros": {"type": "string"},
                        "lunch_macros": {"type": "string"},
                        "snack_macros": {"type": "string"},
                        "dinner_macros": {"type": "string"},
                        "casein_macros": {"type": "string"}
                    }
                },
                "scientific_recommendations": {
                    "type": "object",
                    "properties": {
                        "hydration": {"type": "string"},
                        "protein_timing": {"type": "string"},
                        "supplements": {"type": "string"},
                        "recovery": {"type": "string"},
                        "performance": {"type": "string"},
                        "body_comp": {"type": "string"},
                        "monitoring": {"type": "string"}
                    }
                },
                "biomarkers": {
                    "type": "object",
                    "properties": {
                        "hba1c": {"type": "number"},
                        "hdl": {"type": "integer"},
                        "ldl": {"type": "integer"},
                        "crp": {"type": "number"},
                        "ferritin": {"type": "integer"},
                        "vitamin_d": {"type": "integer"},
                        "b12_serum": {"type": "integer"},
                        "homocysteine": {"type": "integer"}
                    }
                }
            },
            "required": ["client_name"]
        }