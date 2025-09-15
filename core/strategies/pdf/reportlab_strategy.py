"""
ReportLab PDF Generation Strategy

High-performance PDF generation using ReportLab library.
Optimized for complex layouts and professional documents.
"""

import io
import time
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart

from ..base import BaseStrategy, StrategyConfig, StrategyPriority
from .base import (
    PDFStrategyContext, PDFStrategyResult, PDFGenerationContext,
    PDFGenerationResult, PDFQualityMetrics, PDFQuality, PDFFormat, PDFComplexity
)


class ReportLabPDFStrategy(BaseStrategy[PDFGenerationContext]):
    """
    Enterprise-grade PDF generation using ReportLab.

    Features:
    - Professional document layouts
    - Complex charts and graphics
    - High-quality typography
    - Optimized performance for large documents
    - Advanced styling capabilities
    """

    def __init__(self):
        config = StrategyConfig(
            name="reportlab_pdf",
            version="1.0.0",
            priority=StrategyPriority.HIGH,
            timeout_seconds=60.0,
            cache_enabled=True,
            cache_ttl_seconds=1800  # 30 minutes
        )
        super().__init__(config)

        # Strategy metadata
        self._strategy_category = "pdf_generation"
        self._strategy_tags = {"professional", "complex_layouts", "high_performance"}

        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for professional documents"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50'),
            alignment=1  # Center
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#34495e'),
            alignment=1
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#2980b9'),
            borderWidth=0,
            borderPadding=0,
            leftIndent=0
        ))

        # Body text with better spacing
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14,
            textColor=colors.HexColor('#2c3e50')
        ))

        # Highlight box style
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#27ae60'),
            backColor=colors.HexColor('#ecf0f1'),
            borderWidth=1,
            borderColor=colors.HexColor('#bdc3c7'),
            borderPadding=8,
            spaceAfter=12
        ))

    async def execute_async(self, context: PDFStrategyContext) -> PDFStrategyResult:
        """Execute PDF generation with ReportLab"""
        start_time = time.time()

        try:
            pdf_context = context.data

            # Create PDF buffer
            buffer = io.BytesIO()

            # Setup document with proper page size
            page_size = self._get_page_size(pdf_context.format)
            doc = SimpleDocTemplate(
                buffer,
                pagesize=page_size,
                rightMargin=25*mm,
                leftMargin=25*mm,
                topMargin=25*mm,
                bottomMargin=25*mm,
                title=pdf_context.template.name
            )

            # Build document content
            story = []
            self._build_document_content(story, pdf_context)

            # Generate PDF
            doc.build(story)

            # Get PDF data
            pdf_data = buffer.getvalue()
            buffer.close()

            # Calculate metrics
            generation_time = (time.time() - start_time) * 1000
            quality_metrics = PDFQualityMetrics(
                file_size_kb=len(pdf_data) / 1024,
                generation_time_ms=generation_time,
                page_count=doc.page,
                image_quality_score=85.0,  # ReportLab typically produces high-quality images
                text_readability_score=90.0,  # Excellent typography
                layout_consistency_score=95.0  # Very consistent layouts
            )
            quality_metrics.calculate_overall_score()

            # Create result
            result = PDFGenerationResult(
                pdf_data=pdf_data,
                quality_metrics=quality_metrics,
                generation_engine="ReportLab",
                template_used=pdf_context.template.name,
                success=True
            )

            return PDFStrategyResult(
                data=result,
                success=True,
                execution_time_ms=generation_time,
                strategy_name=self.name,
                strategy_version=self.version
            )

        except Exception as e:
            generation_time = (time.time() - start_time) * 1000
            return PDFStrategyResult(
                data=None,
                success=False,
                execution_time_ms=generation_time,
                strategy_name=self.name,
                error_message=f"ReportLab PDF generation failed: {str(e)}"
            )

    def _get_page_size(self, format_type: PDFFormat):
        """Get page size for document"""
        size_map = {
            PDFFormat.A4_PORTRAIT: A4,
            PDFFormat.A4_LANDSCAPE: landscape(A4),
            PDFFormat.LETTER_PORTRAIT: letter,
            PDFFormat.LETTER_LANDSCAPE: landscape(letter),
        }
        return size_map.get(format_type, A4)

    def _build_document_content(self, story: List, context: PDFGenerationContext):
        """Build the main document content"""
        template = context.template
        data = context.data

        # Document header
        if template.template_type == "workout":
            self._build_workout_document(story, data, context)
        elif template.template_type == "nutrition":
            self._build_nutrition_document(story, data, context)
        elif template.template_type == "progress_report":
            self._build_progress_document(story, data, context)
        else:
            self._build_generic_document(story, data, context)

    def _build_workout_document(self, story: List, data: Dict[str, Any], context: PDFGenerationContext):
        """Build workout session document"""
        # Title
        title = data.get('title', 'Séance d\'Entraînement')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))

        # Session info
        session_info = data.get('session_info', {})
        if session_info:
            info_data = [
                ['Date:', session_info.get('date', 'N/A')],
                ['Durée:', f"{session_info.get('duration', 'N/A')} minutes"],
                ['Type:', session_info.get('type', 'N/A')],
                ['Coach:', session_info.get('coach', 'N/A')]
            ]

            info_table = Table(info_data, colWidths=[2*inch, 3*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1'))
            ]))

            story.append(info_table)
            story.append(Spacer(1, 20))

        # Exercises
        exercises = data.get('exercises', [])
        if exercises:
            story.append(Paragraph("Exercices", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))

            for i, exercise in enumerate(exercises, 1):
                # Exercise header
                exercise_title = f"{i}. {exercise.get('name', 'Exercice sans nom')}"
                story.append(Paragraph(exercise_title, self.styles['Heading4']))

                # Exercise details
                sets = exercise.get('sets', [])
                if sets:
                    # Create sets table
                    headers = ['Série', 'Répétitions', 'Poids (kg)', 'Repos (s)']
                    sets_data = [headers]

                    for j, set_data in enumerate(sets, 1):
                        sets_data.append([
                            str(j),
                            str(set_data.get('reps', '-')),
                            str(set_data.get('weight', '-')),
                            str(set_data.get('rest', '-'))
                        ])

                    sets_table = Table(sets_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                    sets_table.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER')
                    ]))

                    story.append(sets_table)

                # Exercise notes
                notes = exercise.get('notes', '')
                if notes:
                    story.append(Spacer(1, 6))
                    story.append(Paragraph(f"<b>Notes:</b> {notes}", self.styles['CustomBody']))

                story.append(Spacer(1, 15))

        # Notes section
        notes = data.get('notes', '')
        if notes:
            story.append(Paragraph("Notes du Coach", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            story.append(Paragraph(notes, self.styles['HighlightBox']))

    def _build_nutrition_document(self, story: List, data: Dict[str, Any], context: PDFGenerationContext):
        """Build nutrition plan document"""
        # Title
        title = data.get('title', 'Plan Nutritionnel')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))

        # Client info
        client_info = data.get('client_info', {})
        if client_info:
            story.append(Paragraph("Informations Client", self.styles['SectionHeader']))

            client_data = [
                ['Nom:', f"{client_info.get('first_name', '')} {client_info.get('last_name', '')}"],
                ['Objectif:', client_info.get('goal', 'N/A')],
                ['Calories cibles:', f"{client_info.get('target_calories', 'N/A')} kcal/jour"],
                ['Protéines:', f"{client_info.get('target_protein', 'N/A')} g/jour"],
                ['Glucides:', f"{client_info.get('target_carbs', 'N/A')} g/jour"],
                ['Lipides:', f"{client_info.get('target_fats', 'N/A')} g/jour"]
            ]

            client_table = Table(client_data, colWidths=[2*inch, 3*inch])
            client_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1'))
            ]))

            story.append(client_table)
            story.append(Spacer(1, 20))

        # Meal plan
        meals = data.get('meals', [])
        if meals:
            story.append(Paragraph("Plan Alimentaire", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))

            for meal in meals:
                # Meal header
                meal_name = meal.get('name', 'Repas')
                meal_time = meal.get('time', '')
                header_text = f"{meal_name}"
                if meal_time:
                    header_text += f" - {meal_time}"

                story.append(Paragraph(header_text, self.styles['Heading4']))

                # Foods table
                foods = meal.get('foods', [])
                if foods:
                    headers = ['Aliment', 'Quantité', 'Calories', 'Protéines (g)', 'Glucides (g)', 'Lipides (g)']
                    food_data = [headers]

                    total_calories = 0
                    total_protein = 0
                    total_carbs = 0
                    total_fats = 0

                    for food in foods:
                        calories = food.get('calories', 0)
                        protein = food.get('protein', 0)
                        carbs = food.get('carbs', 0)
                        fats = food.get('fats', 0)

                        food_data.append([
                            food.get('name', ''),
                            food.get('quantity', ''),
                            str(calories),
                            str(protein),
                            str(carbs),
                            str(fats)
                        ])

                        total_calories += calories
                        total_protein += protein
                        total_carbs += carbs
                        total_fats += fats

                    # Add totals row
                    food_data.append([
                        'TOTAL', '', str(total_calories), str(total_protein), str(total_carbs), str(total_fats)
                    ])

                    food_table = Table(food_data, colWidths=[2*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
                    food_table.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                    ]))

                    story.append(food_table)

                story.append(Spacer(1, 15))

    def _build_progress_document(self, story: List, data: Dict[str, Any], context: PDFGenerationContext):
        """Build progress report document"""
        # Title
        title = data.get('title', 'Rapport de Progression')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))

        # Add charts if available and enabled
        if context.include_charts and data.get('charts'):
            self._add_progress_charts(story, data.get('charts', {}))

        # Progress metrics
        metrics = data.get('metrics', {})
        if metrics:
            story.append(Paragraph("Métriques de Progression", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))

            metrics_data = []
            for key, value in metrics.items():
                metrics_data.append([key.replace('_', ' ').title(), str(value)])

            if metrics_data:
                metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
                metrics_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT')
                ]))

                story.append(metrics_table)
                story.append(Spacer(1, 20))

    def _build_generic_document(self, story: List, data: Dict[str, Any], context: PDFGenerationContext):
        """Build generic document"""
        # Title
        title = data.get('title', 'Document')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))

        # Content sections
        sections = data.get('sections', [])
        for section in sections:
            section_title = section.get('title', '')
            if section_title:
                story.append(Paragraph(section_title, self.styles['SectionHeader']))
                story.append(Spacer(1, 10))

            section_content = section.get('content', '')
            if section_content:
                story.append(Paragraph(section_content, self.styles['CustomBody']))
                story.append(Spacer(1, 15))

    def _add_progress_charts(self, story: List, charts_data: Dict[str, Any]):
        """Add progress charts to document"""
        try:
            # Weight progress chart
            weight_data = charts_data.get('weight_progress')
            if weight_data:
                drawing = Drawing(400, 200)
                chart = HorizontalLineChart()
                chart.x = 50
                chart.y = 50
                chart.height = 125
                chart.width = 300
                chart.data = [weight_data.get('values', [])]
                chart.categoryAxis.categoryNames = weight_data.get('labels', [])
                chart.valueAxis.valueMin = min(weight_data.get('values', [0])) - 5
                chart.valueAxis.valueMax = max(weight_data.get('values', [100])) + 5

                drawing.add(chart)
                story.append(drawing)
                story.append(Spacer(1, 20))

        except Exception as e:
            # If chart generation fails, add a note
            story.append(Paragraph(f"Graphique non disponible: {str(e)}", self.styles['CustomBody']))
            story.append(Spacer(1, 20))

    def validate_context(self, context: PDFStrategyContext) -> List[str]:
        """Validate PDF generation context"""
        errors = []
        pdf_context = context.data

        if not pdf_context.template:
            errors.append("Template is required")

        if not pdf_context.data:
            errors.append("Data is required for PDF generation")

        # Check if ReportLab can handle the complexity
        if pdf_context.complexity == PDFComplexity.ADVANCED:
            if not pdf_context.include_charts and not pdf_context.include_images:
                # Advanced complexity without charts/images might not be suitable for ReportLab
                pass

        return errors

    def get_supported_context_types(self) -> List[type]:
        """Get supported context types"""
        return [PDFGenerationContext]

    @property
    def preferred_contexts(self) -> List[type]:
        """Contexts where this strategy performs best"""
        return [PDFGenerationContext]