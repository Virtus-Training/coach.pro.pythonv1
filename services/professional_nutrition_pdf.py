"""
Professional Nutrition PDF Generator
====================================

Premium-quality nutrition PDF generation system with:
- Multi-page professional layouts (4-6 pages)
- Advanced data visualizations and charts
- Branded design system
- Scientific presentation quality
- Coach-level professional standards
"""

from io import BytesIO
from pathlib import Path
from typing import Optional, Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

from services.advanced_nutrition_calculator import NutritionResults, ActivityLevel, NutritionGoal


class ProfessionalBrandingSystem:
    """Professional branding and design system for PDFs"""

    # Color Palette - Premium Coach Branding
    PRIMARY = "#1F2937"          # Dark slate
    SECONDARY = "#22D3EE"        # Cyan accent
    ACCENT = "#F59E0B"           # Amber
    SUCCESS = "#10B981"          # Emerald
    WARNING = "#F59E0B"          # Amber
    ERROR = "#EF4444"            # Red
    SURFACE = "#F8FAFC"          # Light gray
    SURFACE_DARK = "#374151"     # Medium gray
    TEXT_PRIMARY = "#111827"     # Almost black
    TEXT_SECONDARY = "#6B7280"   # Gray
    TEXT_MUTED = "#9CA3AF"       # Light gray
    WHITE = "#FFFFFF"

    # Macro colors for consistency
    PROTEIN_COLOR = "#3B82F6"    # Blue
    CARBS_COLOR = "#F59E0B"      # Amber
    FATS_COLOR = "#EF4444"       # Red

    # Typography System
    FONTS = {
        'title': ('Helvetica-Bold', 24),
        'subtitle': ('Helvetica-Bold', 18),
        'heading': ('Helvetica-Bold', 14),
        'body': ('Helvetica', 11),
        'small': ('Helvetica', 9),
        'caption': ('Helvetica-Oblique', 8)
    }

    # Layout Constants
    PAGE_MARGIN = 2.0 * cm
    CONTENT_WIDTH = A4[0] - (2 * PAGE_MARGIN)
    CONTENT_HEIGHT = A4[1] - (2 * PAGE_MARGIN)
    HEADER_HEIGHT = 3.5 * cm
    FOOTER_HEIGHT = 1.5 * cm

    @staticmethod
    def get_color(color_name: str) -> colors.Color:
        """Get ReportLab color from brand palette"""
        color_map = {
            'primary': ProfessionalBrandingSystem.PRIMARY,
            'secondary': ProfessionalBrandingSystem.SECONDARY,
            'accent': ProfessionalBrandingSystem.ACCENT,
            'success': ProfessionalBrandingSystem.SUCCESS,
            'warning': ProfessionalBrandingSystem.WARNING,
            'error': ProfessionalBrandingSystem.ERROR,
            'surface': ProfessionalBrandingSystem.SURFACE,
            'surface_dark': ProfessionalBrandingSystem.SURFACE_DARK,
            'text_primary': ProfessionalBrandingSystem.TEXT_PRIMARY,
            'text_secondary': ProfessionalBrandingSystem.TEXT_SECONDARY,
            'text_muted': ProfessionalBrandingSystem.TEXT_MUTED,
            'white': ProfessionalBrandingSystem.WHITE,
            'protein': ProfessionalBrandingSystem.PROTEIN_COLOR,
            'carbs': ProfessionalBrandingSystem.CARBS_COLOR,
            'fats': ProfessionalBrandingSystem.FATS_COLOR,
        }
        return colors.HexColor(color_map.get(color_name, '#000000'))


class ChartGenerator:
    """Advanced chart generation for nutrition PDFs"""

    @staticmethod
    def create_macro_pie_chart(
        protein_kcal: int,
        carbs_kcal: int,
        fats_kcal: int,
        size: tuple = (4, 4),
        dpi: int = 300
    ) -> BytesIO:
        """Create professional macronutrient pie chart"""
        fig = Figure(figsize=size, dpi=dpi, facecolor='white')
        ax = fig.add_subplot(111)

        # Data preparation
        sizes = [protein_kcal, carbs_kcal, fats_kcal]
        labels = ['Protéines', 'Glucides', 'Lipides']
        colors_pie = [
            ProfessionalBrandingSystem.PROTEIN_COLOR,
            ProfessionalBrandingSystem.CARBS_COLOR,
            ProfessionalBrandingSystem.FATS_COLOR
        ]

        # Calculate percentages
        total = sum(sizes)
        percentages = [size/total * 100 if total > 0 else 0 for size in sizes]

        # Create pie chart with professional styling
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors_pie,
            autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
            startangle=90,
            wedgeprops={
                'linewidth': 2,
                'edgecolor': 'white',
                'alpha': 0.9
            },
            textprops={
                'fontsize': 10,
                'fontweight': 'bold',
                'color': '#1F2937'
            },
            pctdistance=0.8
        )

        # Enhance autotext styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        # Add center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.50, fc='white', linewidth=2, edgecolor='#E5E7EB')
        ax.add_artist(centre_circle)

        # Center text with total calories
        ax.text(0, 0, f'{total}\nkcal', ha='center', va='center',
                fontsize=14, fontweight='bold', color='#1F2937')

        ax.axis('equal')
        ax.set_title('Répartition Macronutriments', fontsize=12, fontweight='bold',
                     color='#1F2937', pad=20)

        # Save to BytesIO
        buf = BytesIO()
        fig.savefig(buf, format='PNG', dpi=dpi, bbox_inches='tight',
                    transparent=True, pad_inches=0.1)
        buf.seek(0)
        return buf

    @staticmethod
    def create_metabolism_breakdown(
        bmr: float,
        tdee: float,
        target_calories: float,
        size: tuple = (6, 4),
        dpi: int = 300
    ) -> BytesIO:
        """Create metabolism breakdown bar chart"""
        fig = Figure(figsize=size, dpi=dpi, facecolor='white')
        ax = fig.add_subplot(111)

        # Data
        activity_calories = tdee - bmr
        adjustment = target_calories - tdee

        categories = ['BMR\n(Base)', 'Activité\n(Quotidienne)', 'Objectif\n(Total)']
        values = [bmr, activity_calories, target_calories]
        colors_bars = [
            ProfessionalBrandingSystem.SURFACE_DARK,
            ProfessionalBrandingSystem.SECONDARY,
            ProfessionalBrandingSystem.ACCENT if adjustment >= 0 else ProfessionalBrandingSystem.ERROR
        ]

        # Create horizontal bar chart
        bars = ax.barh(categories, values, color=colors_bars, alpha=0.8, height=0.6)

        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            width = bar.get_width()
            ax.text(width + 50, bar.get_y() + bar.get_height()/2,
                    f'{int(value)} kcal', ha='left', va='center',
                    fontweight='bold', fontsize=10, color='#1F2937')

        # Styling
        ax.set_xlabel('Calories (kcal/jour)', fontweight='bold', fontsize=11, color='#1F2937')
        ax.set_title('Analyse Métabolique Détaillée', fontsize=14, fontweight='bold',
                     color='#1F2937', pad=20)

        # Remove spines and ticks for cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(left=False, bottom=True)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Adjust layout
        ax.set_xlim(0, max(values) * 1.2)

        buf = BytesIO()
        fig.savefig(buf, format='PNG', dpi=dpi, bbox_inches='tight',
                    transparent=True, pad_inches=0.1)
        buf.seek(0)
        return buf

    @staticmethod
    def create_timeline_chart(
        current_weight: float,
        target_change: float,
        timeline_months: int = 6,
        size: tuple = (6, 3),
        dpi: int = 300
    ) -> BytesIO:
        """Create weight timeline projection chart"""
        fig = Figure(figsize=size, dpi=dpi, facecolor='white')
        ax = fig.add_subplot(111)

        # Generate timeline data
        months = list(range(timeline_months + 1))
        projected_weights = [current_weight + (target_change * month) for month in months]

        # Color based on goal
        line_color = (ProfessionalBrandingSystem.SUCCESS if target_change > 0
                     else ProfessionalBrandingSystem.ERROR if target_change < 0
                     else ProfessionalBrandingSystem.TEXT_SECONDARY)

        # Plot line with markers
        ax.plot(months, projected_weights, color=line_color, linewidth=3,
                marker='o', markersize=6, markerfacecolor='white',
                markeredgewidth=2, markeredgecolor=line_color)

        # Fill area under curve
        ax.fill_between(months, projected_weights,
                        alpha=0.1, color=line_color)

        # Styling
        ax.set_xlabel('Mois', fontweight='bold', fontsize=11, color='#1F2937')
        ax.set_ylabel('Poids (kg)', fontweight='bold', fontsize=11, color='#1F2937')
        ax.set_title('Projection Évolution Poids', fontsize=14, fontweight='bold',
                     color='#1F2937', pad=20)

        # Grid and spines
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add target annotations
        if timeline_months > 3:
            mid_point = timeline_months // 2
            ax.annotate(f'{projected_weights[mid_point]:.1f} kg',
                       (mid_point, projected_weights[mid_point]),
                       textcoords="offset points", xytext=(0, 15),
                       ha='center', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white',
                                edgecolor=line_color, alpha=0.8))

        buf = BytesIO()
        fig.savefig(buf, format='PNG', dpi=dpi, bbox_inches='tight',
                    transparent=True, pad_inches=0.1)
        buf.seek(0)
        return buf


class ProfessionalNutritionPDF:
    """
    Professional nutrition PDF generator with premium layouts.

    Generates comprehensive nutrition reports with:
    - Multi-page structured layout
    - Professional branding and typography
    - Advanced data visualizations
    - Evidence-based recommendations
    - Coach-quality presentation
    """

    def __init__(self, results: NutritionResults, coach_info: Optional[Dict] = None):
        self.results = results
        self.coach_info = coach_info or {}
        self.branding = ProfessionalBrandingSystem()

    def generate(self, output_path: str):
        """Generate complete professional nutrition PDF"""
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # Generate all pages
        self._page_1_header_profile(c, width, height)
        c.showPage()

        self._page_2_metabolic_analysis(c, width, height)
        c.showPage()

        self._page_3_macronutrient_distribution(c, width, height)
        c.showPage()

        self._page_4_personalized_recommendations(c, width, height)
        c.showPage()

        self._page_5_timeline_planning(c, width, height)
        c.showPage()

        c.save()

    def _draw_header(self, c: canvas.Canvas, width: float, height: float, page_num: int, total_pages: int = 5):
        """Draw professional header for all pages"""
        # Header background
        c.setFillColor(self.branding.get_color('primary'))
        c.rect(0, height - self.branding.HEADER_HEIGHT, width, self.branding.HEADER_HEIGHT, stroke=0, fill=1)

        # Header accent line
        c.setFillColor(self.branding.get_color('secondary'))
        c.rect(0, height - self.branding.HEADER_HEIGHT, width, 0.3 * cm, stroke=0, fill=1)

        # Title
        c.setFillColor(self.branding.get_color('white'))
        c.setFont(*self.branding.FONTS['title'])
        full_name = f"{self.results.personal_data.prenom} {self.results.personal_data.nom}"
        c.drawString(self.branding.PAGE_MARGIN, height - 2.2 * cm,
                     f"BILAN NUTRITIONNEL PERSONNALISÉ")

        # Subtitle
        c.setFont(*self.branding.FONTS['body'])
        c.drawString(self.branding.PAGE_MARGIN, height - 2.8 * cm, full_name)

        # Page number
        c.setFont(*self.branding.FONTS['small'])
        c.drawRightString(width - self.branding.PAGE_MARGIN, height - 2.8 * cm,
                         f"Page {page_num} / {total_pages}")

        # Coach logo/info (if available)
        coach_name = self.coach_info.get('name', 'Coach Professionnel')
        c.setFont(*self.branding.FONTS['caption'])
        c.drawRightString(width - self.branding.PAGE_MARGIN, height - 3.2 * cm, coach_name)

    def _draw_footer(self, c: canvas.Canvas, width: float, height: float):
        """Draw professional footer"""
        c.setFillColor(self.branding.get_color('text_muted'))
        c.setFont(*self.branding.FONTS['caption'])

        # Date
        current_date = datetime.now().strftime("%d/%m/%Y")
        c.drawString(self.branding.PAGE_MARGIN, 1.2 * cm,
                     f"Généré le {current_date}")

        # Disclaimer
        c.drawRightString(width - self.branding.PAGE_MARGIN, 1.2 * cm,
                         "Document personnalisé - Consultation nutritionnelle professionnelle")

    def _page_1_header_profile(self, c: canvas.Canvas, width: float, height: float):
        """Page 1: Header & Client Profile"""
        self._draw_header(c, width, height, 1)
        self._draw_footer(c, width, height)

        # Starting position after header
        y_pos = height - self.branding.HEADER_HEIGHT - 1 * cm

        # Client Profile Section
        c.setFillColor(self.branding.get_color('primary'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "👤 Profil Client")
        y_pos -= 1.2 * cm

        # Profile data in elegant cards
        profile_data = [
            ("Âge", f"{self.results.personal_data.age} ans"),
            ("Sexe", self.results.personal_data.sexe),
            ("Taille", f"{self.results.personal_data.taille_cm} cm"),
            ("Poids", f"{self.results.personal_data.poids_kg} kg"),
            ("Niveau d'activité", self.results.personal_data.niveau_activite.label),
            ("Objectif", self.results.personal_data.objectif.label),
        ]

        # Calculate BMI
        height_m = self.results.personal_data.taille_cm / 100
        bmi = self.results.personal_data.poids_kg / (height_m ** 2)
        profile_data.append(("IMC", f"{bmi:.1f}"))

        # Draw profile cards (2 columns)
        card_width = (self.branding.CONTENT_WIDTH - 1 * cm) / 2
        card_height = 1.8 * cm
        cards_per_row = 2

        for i, (label, value) in enumerate(profile_data):
            row = i // cards_per_row
            col = i % cards_per_row

            x_pos = self.branding.PAGE_MARGIN + col * (card_width + 1 * cm)
            card_y = y_pos - (row * (card_height + 0.5 * cm))

            # Card background
            c.setFillColor(self.branding.get_color('surface'))
            c.roundRect(x_pos, card_y - card_height, card_width, card_height,
                       0.3 * cm, stroke=0, fill=1)

            # Card content
            c.setFillColor(self.branding.get_color('text_secondary'))
            c.setFont(*self.branding.FONTS['small'])
            c.drawString(x_pos + 0.5 * cm, card_y - 0.8 * cm, label)

            c.setFillColor(self.branding.get_color('text_primary'))
            c.setFont(*self.branding.FONTS['heading'])
            c.drawString(x_pos + 0.5 * cm, card_y - 1.4 * cm, value)

        # Objective highlight
        y_pos -= 7 * cm
        c.setFillColor(self.branding.get_color('accent'))
        c.roundRect(self.branding.PAGE_MARGIN, y_pos - 3 * cm,
                   self.branding.CONTENT_WIDTH, 3 * cm, 0.5 * cm, stroke=0, fill=1)

        c.setFillColor(self.branding.get_color('white'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawCentredText(width / 2, y_pos - 1.2 * cm,
                         f"🎯 OBJECTIF: {self.results.personal_data.objectif.label.upper()}")

        c.setFont(*self.branding.FONTS['body'])
        c.drawCentredText(width / 2, y_pos - 1.8 * cm,
                         self.results.personal_data.objectif.description)

        # Caloric target highlight
        c.setFont(*self.branding.FONTS['heading'])
        c.drawCentredText(width / 2, y_pos - 2.4 * cm,
                         f"Calories objectif: {self.results.objectif_kcal} kcal/jour")

    def _page_2_metabolic_analysis(self, c: canvas.Canvas, width: float, height: float):
        """Page 2: Metabolic Analysis with Charts"""
        self._draw_header(c, width, height, 2)
        self._draw_footer(c, width, height)

        y_pos = height - self.branding.HEADER_HEIGHT - 1 * cm

        # Section title
        c.setFillColor(self.branding.get_color('primary'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "🔥 Analyse Métabolique")
        y_pos -= 1.5 * cm

        # Metabolic data table
        metabolic_data = [
            ["Métrique", "Valeur", "Description"],
            ["BMR (Métabolisme de base)", f"{self.results.bmr_kcal} kcal/jour",
             "Calories nécessaires au repos"],
            ["TDEE (Dépense totale)", f"{self.results.tdee_kcal} kcal/jour",
             "Calories avec activité physique"],
            ["Facteur d'activité", f"×{self.results.activite_factor}",
             self.results.personal_data.niveau_activite.description],
            ["Balance énergétique", f"{self.results.deficit_surplus:+d} kcal/jour",
             "Surplus/déficit pour l'objectif"],
            ["Méthode de calcul", self.results.bmr_method.value.replace('_', '-').title(),
             "Formule scientifique utilisée"]
        ]

        # Create table
        table = Table(metabolic_data)
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.branding.get_color('primary')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.branding.get_color('white')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),

            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), self.branding.get_color('white')),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.branding.get_color('text_primary')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),

            # Alternating row colors
            ('BACKGROUND', (0, 2), (-1, 2), self.branding.get_color('surface')),
            ('BACKGROUND', (0, 4), (-1, 4), self.branding.get_color('surface')),

            # Borders
            ('GRID', (0, 0), (-1, -1), 1, self.branding.get_color('text_muted')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]))

        # Draw table
        table.wrapOn(c, self.branding.CONTENT_WIDTH, 0)
        table_height = table._height
        table.drawOn(c, self.branding.PAGE_MARGIN, y_pos - table_height)
        y_pos -= table_height + 1.5 * cm

        # Metabolism breakdown chart
        try:
            chart_buffer = ChartGenerator.create_metabolism_breakdown(
                self.results.bmr_kcal,
                self.results.tdee_kcal,
                self.results.objectif_kcal
            )

            chart_image = ImageReader(chart_buffer)
            chart_width = 12 * cm
            chart_height = 8 * cm

            c.drawImage(chart_image,
                       (width - chart_width) / 2, y_pos - chart_height,
                       chart_width, chart_height, mask='auto')

        except Exception:
            # Fallback text if chart fails
            c.setFont(*self.branding.FONTS['body'])
            c.drawCentredText(width / 2, y_pos - 4 * cm,
                             "Graphique métabolique non disponible")

    def _page_3_macronutrient_distribution(self, c: canvas.Canvas, width: float, height: float):
        """Page 3: Macronutrient Distribution with Visualizations"""
        self._draw_header(c, width, height, 3)
        self._draw_footer(c, width, height)

        y_pos = height - self.branding.HEADER_HEIGHT - 1 * cm

        # Section title
        c.setFillColor(self.branding.get_color('primary'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "🥗 Répartition Macronutriments")
        y_pos -= 2 * cm

        # Macros comparison table
        macros_data = [
            ["Macronutriment", "Grammes", "Calories", "Pourcentage", "Objectif par repas"],
            [
                "🥩 Protéines",
                f"{self.results.proteines_g}g",
                f"{self.results.proteines_kcal} kcal",
                f"{self.results.proteines_pct}%",
                f"{self.results.proteines_g // 4}g par repas"
            ],
            [
                "🍞 Glucides",
                f"{self.results.glucides_g}g",
                f"{self.results.glucides_kcal} kcal",
                f"{self.results.glucides_pct}%",
                f"{self.results.glucides_g // 4}g par repas"
            ],
            [
                "🥑 Lipides",
                f"{self.results.lipides_g}g",
                f"{self.results.lipides_kcal} kcal",
                f"{self.results.lipides_pct}%",
                f"{self.results.lipides_g // 4}g par repas"
            ],
            [
                "🔥 TOTAL",
                f"{self.results.proteines_g + self.results.glucides_g + self.results.lipides_g}g",
                f"{self.results.objectif_kcal} kcal",
                "100%",
                "Répartir équitablement"
            ]
        ]

        # Enhanced table styling
        macro_table = Table(macros_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4*cm])
        macro_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), self.branding.get_color('primary')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.branding.get_color('white')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),

            # Protein row
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor(self.branding.PROTEIN_COLOR + '20')),
            ('TEXTCOLOR', (0, 1), (0, 1), self.branding.get_color('protein')),

            # Carbs row
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor(self.branding.CARBS_COLOR + '20')),
            ('TEXTCOLOR', (0, 2), (0, 2), self.branding.get_color('carbs')),

            # Fats row
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor(self.branding.FATS_COLOR + '20')),
            ('TEXTCOLOR', (0, 3), (0, 3), self.branding.get_color('fats')),

            # Total row
            ('BACKGROUND', (0, 4), (-1, 4), self.branding.get_color('accent')),
            ('TEXTCOLOR', (0, 4), (-1, 4), self.branding.get_color('white')),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),

            # General styling
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, self.branding.get_color('text_muted')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ]))

        # Draw table
        macro_table.wrapOn(c, self.branding.CONTENT_WIDTH, 0)
        macro_table_height = macro_table._height
        macro_table.drawOn(c, self.branding.PAGE_MARGIN, y_pos - macro_table_height)
        y_pos -= macro_table_height + 2 * cm

        # Macronutrient pie chart
        try:
            pie_chart_buffer = ChartGenerator.create_macro_pie_chart(
                self.results.proteines_kcal,
                self.results.glucides_kcal,
                self.results.lipides_kcal
            )

            pie_chart_image = ImageReader(pie_chart_buffer)
            chart_size = 8 * cm

            c.drawImage(pie_chart_image,
                       (width - chart_size) / 2, y_pos - chart_size,
                       chart_size, chart_size, mask='auto')

        except Exception:
            # Fallback
            c.setFont(*self.branding.FONTS['body'])
            c.drawCentredText(width / 2, y_pos - 4 * cm,
                             "Graphique macronutriments non disponible")

    def _page_4_personalized_recommendations(self, c: canvas.Canvas, width: float, height: float):
        """Page 4: Personalized Recommendations & Advice"""
        self._draw_header(c, width, height, 4)
        self._draw_footer(c, width, height)

        y_pos = height - self.branding.HEADER_HEIGHT - 1 * cm

        # Section title
        c.setFillColor(self.branding.get_color('primary'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "💡 Conseils Personnalisés")
        y_pos -= 1.5 * cm

        # Get personalized recommendations
        from services.advanced_nutrition_calculator import AdvancedNutritionCalculator
        recommendations = AdvancedNutritionCalculator.get_personalized_recommendations(self.results)

        # Split recommendations into categories
        general_recs = recommendations[:6]
        specific_recs = recommendations[6:]

        # General recommendations
        c.setFillColor(self.branding.get_color('text_primary'))
        c.setFont(*self.branding.FONTS['heading'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "📋 Recommandations Générales")
        y_pos -= 1 * cm

        for i, rec in enumerate(general_recs):
            if y_pos < 8 * cm:  # Leave space for footer
                break

            # Recommendation card
            card_height = 1.2 * cm
            c.setFillColor(self.branding.get_color('surface'))
            c.roundRect(self.branding.PAGE_MARGIN, y_pos - card_height,
                       self.branding.CONTENT_WIDTH, card_height, 0.2 * cm, stroke=0, fill=1)

            # Recommendation text
            c.setFillColor(self.branding.get_color('text_primary'))
            c.setFont(*self.branding.FONTS['body'])
            text_y = y_pos - 0.7 * cm
            c.drawString(self.branding.PAGE_MARGIN + 0.5 * cm, text_y, f"• {rec}")

            y_pos -= card_height + 0.3 * cm

        # Specific recommendations (if space allows)
        if y_pos > 12 * cm and specific_recs:
            y_pos -= 1 * cm
            c.setFillColor(self.branding.get_color('text_primary'))
            c.setFont(*self.branding.FONTS['heading'])
            c.drawString(self.branding.PAGE_MARGIN, y_pos, "🎯 Conseils Spécifiques à l'Objectif")
            y_pos -= 1 * cm

            for rec in specific_recs[:3]:  # Limit to 3 specific recommendations
                if y_pos < 8 * cm:
                    break

                card_height = 1.2 * cm
                c.setFillColor(self.branding.get_color('accent'))
                c.setStrokeColor(self.branding.get_color('accent'))
                c.setLineWidth(2)
                c.roundRect(self.branding.PAGE_MARGIN, y_pos - card_height,
                           self.branding.CONTENT_WIDTH, card_height, 0.2 * cm, stroke=1, fill=0)

                c.setFillColor(self.branding.get_color('text_primary'))
                c.setFont(*self.branding.FONTS['body'])
                text_y = y_pos - 0.7 * cm
                c.drawString(self.branding.PAGE_MARGIN + 0.5 * cm, text_y, f"• {rec}")

                y_pos -= card_height + 0.3 * cm

        # Hydration calculation
        y_pos -= 1 * cm
        poids = self.results.personal_data.poids_kg
        hydration_ml = int(poids * 35)

        # Hydration highlight box
        c.setFillColor(self.branding.get_color('secondary'))
        c.roundRect(self.branding.PAGE_MARGIN, y_pos - 3 * cm,
                   self.branding.CONTENT_WIDTH, 2.5 * cm, 0.5 * cm, stroke=0, fill=1)

        c.setFillColor(self.branding.get_color('white'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawCentredText(width / 2, y_pos - 1.2 * cm, "💧 HYDRATATION QUOTIDIENNE")

        c.setFont(*self.branding.FONTS['heading'])
        c.drawCentredText(width / 2, y_pos - 1.8 * cm, f"{hydration_ml} mL par jour")

        c.setFont(*self.branding.FONTS['body'])
        c.drawCentredText(width / 2, y_pos - 2.2 * cm, f"({hydration_ml // 250} verres de 250ml)")

    def _page_5_timeline_planning(self, c: canvas.Canvas, width: float, height: float):
        """Page 5: Timeline & Planning"""
        self._draw_header(c, width, height, 5)
        self._draw_footer(c, width, height)

        y_pos = height - self.branding.HEADER_HEIGHT - 1 * cm

        # Section title
        c.setFillColor(self.branding.get_color('primary'))
        c.setFont(*self.branding.FONTS['subtitle'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "📅 Planning & Suivi")
        y_pos -= 1.5 * cm

        # Timeline estimation
        from services.advanced_nutrition_calculator import AdvancedNutritionCalculator
        timeline = AdvancedNutritionCalculator.estimate_timeline(self.results)

        # Timeline info box
        c.setFillColor(self.branding.get_color('surface'))
        c.roundRect(self.branding.PAGE_MARGIN, y_pos - 4 * cm,
                   self.branding.CONTENT_WIDTH, 4 * cm, 0.5 * cm, stroke=0, fill=1)

        c.setFillColor(self.branding.get_color('text_primary'))
        c.setFont(*self.branding.FONTS['heading'])
        c.drawString(self.branding.PAGE_MARGIN + 1 * cm, y_pos - 1.2 * cm,
                    "⏱️ Estimation Temporelle")

        c.setFont(*self.branding.FONTS['body'])
        c.drawString(self.branding.PAGE_MARGIN + 1 * cm, y_pos - 1.8 * cm,
                    f"• Rythme prévu: {timeline.get('rate', 'Variable')}")
        c.drawString(self.branding.PAGE_MARGIN + 1 * cm, y_pos - 2.3 * cm,
                    f"• Durée recommandée: {timeline.get('timeline', 'À déterminer')}")

        if timeline.get('target_5kg') != 'N/A':
            c.drawString(self.branding.PAGE_MARGIN + 1 * cm, y_pos - 2.8 * cm,
                        f"• Objectif 5kg: {timeline.get('target_5kg')} environ")

        y_pos -= 5 * cm

        # Progress tracking chart (if weight change expected)
        if abs(self.results.deficit_surplus) > 50:
            try:
                monthly_change = (self.results.deficit_surplus * 30) / 7700  # 1kg fat = 7700 kcal
                timeline_chart = ChartGenerator.create_timeline_chart(
                    self.results.personal_data.poids_kg,
                    monthly_change,
                    6
                )

                timeline_image = ImageReader(timeline_chart)
                chart_width = 12 * cm
                chart_height = 6 * cm

                c.drawImage(timeline_image,
                           (width - chart_width) / 2, y_pos - chart_height,
                           chart_width, chart_height, mask='auto')

                y_pos -= chart_height + 1 * cm

            except Exception:
                pass

        # Follow-up recommendations
        followup_recs = [
            "📊 Suivi hebdomadaire: pesée et mesures corporelles",
            "📱 Application recommandée: MyFitnessPal ou Cronometer",
            "🔄 Réévaluation: tous les 4-6 semaines avec votre coach",
            "📝 Journal alimentaire: noter ressentis et énergie",
            "⚡ Ajustements: adapter selon les résultats observés"
        ]

        # Follow-up section
        c.setFillColor(self.branding.get_color('text_primary'))
        c.setFont(*self.branding.FONTS['heading'])
        c.drawString(self.branding.PAGE_MARGIN, y_pos, "📈 Méthodes de Suivi")
        y_pos -= 0.8 * cm

        for rec in followup_recs:
            if y_pos < 6 * cm:
                break
            c.setFont(*self.branding.FONTS['body'])
            c.drawString(self.branding.PAGE_MARGIN, y_pos, rec)
            y_pos -= 0.6 * cm

        # Contact information
        y_pos -= 1 * cm
        contact_info = self.coach_info.get('contact', 'Contactez votre coach pour tout ajustement')
        c.setFillColor(self.branding.get_color('accent'))
        c.roundRect(self.branding.PAGE_MARGIN, y_pos - 2 * cm,
                   self.branding.CONTENT_WIDTH, 1.5 * cm, 0.3 * cm, stroke=0, fill=1)

        c.setFillColor(self.branding.get_color('white'))
        c.setFont(*self.branding.FONTS['body'])
        c.drawCentredText(width / 2, y_pos - 1.2 * cm,
                         f"📞 Contact Coach: {contact_info}")


def generate_professional_nutrition_pdf(
    results: NutritionResults,
    output_path: str,
    coach_info: Optional[Dict] = None
) -> None:
    """
    Generate professional nutrition PDF with premium quality.

    Args:
        results: Complete nutrition calculation results
        output_path: Path where PDF will be saved
        coach_info: Optional coach information for branding

    Example:
        >>> results = AdvancedNutritionCalculator.calculate_complete_nutrition(...)
        >>> generate_professional_nutrition_pdf(results, "nutrition_sheet.pdf")
    """
    generator = ProfessionalNutritionPDF(results, coach_info)
    generator.generate(output_path)