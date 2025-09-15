"""
WeasyPrint PDF Generation Strategy

HTML/CSS-based PDF generation using WeasyPrint library.
Optimized for web-like layouts and modern CSS styling.
"""

import io
import time
from typing import List, Dict, Any, Optional

try:
    import weasyprint
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

from ..base import BaseStrategy, StrategyConfig, StrategyPriority
from .base import (
    PDFStrategyContext, PDFStrategyResult, PDFGenerationContext,
    PDFGenerationResult, PDFQualityMetrics, PDFQuality, PDFFormat, PDFComplexity
)


class WeasyPrintPDFStrategy(BaseStrategy[PDFGenerationContext]):
    """
    Modern HTML/CSS-based PDF generation using WeasyPrint.

    Features:
    - CSS3 and modern web standards support
    - Responsive design capabilities
    - Advanced typography and layouts
    - Web-to-PDF conversion
    - Vector graphics support
    """

    def __init__(self):
        config = StrategyConfig(
            name="weasyprint_pdf",
            version="1.0.0",
            priority=StrategyPriority.NORMAL,
            timeout_seconds=45.0,
            cache_enabled=True,
            cache_ttl_seconds=1800
        )
        super().__init__(config)

        # Strategy metadata
        self._strategy_category = "pdf_generation"
        self._strategy_tags = {"html_css", "modern_layouts", "responsive"}

        # Check availability
        self.available = WEASYPRINT_AVAILABLE

    async def execute_async(self, context: PDFStrategyContext) -> PDFStrategyResult:
        """Execute PDF generation with WeasyPrint"""
        if not self.available:
            return PDFStrategyResult(
                data=None,
                success=False,
                error_message="WeasyPrint library not available"
            )

        start_time = time.time()

        try:
            pdf_context = context.data

            # Generate HTML content
            html_content = self._generate_html_content(pdf_context)
            css_content = self._generate_css_styles(pdf_context)

            # Create WeasyPrint document
            html_doc = HTML(string=html_content)
            css_styles = CSS(string=css_content) if css_content else None

            # Generate PDF
            pdf_bytes = html_doc.write_pdf(stylesheets=[css_styles] if css_styles else None)

            # Calculate metrics
            generation_time = (time.time() - start_time) * 1000
            quality_metrics = PDFQualityMetrics(
                file_size_kb=len(pdf_bytes) / 1024,
                generation_time_ms=generation_time,
                page_count=self._estimate_page_count(pdf_bytes),
                image_quality_score=80.0,  # Good image quality
                text_readability_score=95.0,  # Excellent typography with CSS
                layout_consistency_score=90.0  # Very good layout consistency
            )
            quality_metrics.calculate_overall_score()

            # Create result
            result = PDFGenerationResult(
                pdf_data=pdf_bytes,
                quality_metrics=quality_metrics,
                generation_engine="WeasyPrint",
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
                error_message=f"WeasyPrint PDF generation failed: {str(e)}"
            )

    def _generate_html_content(self, context: PDFGenerationContext) -> str:
        """Generate HTML content for PDF"""
        template = context.template
        data = context.data

        if template.template_type == "workout":
            return self._generate_workout_html(data, context)
        elif template.template_type == "nutrition":
            return self._generate_nutrition_html(data, context)
        elif template.template_type == "progress_report":
            return self._generate_progress_html(data, context)
        else:
            return self._generate_generic_html(data, context)

    def _generate_workout_html(self, data: Dict[str, Any], context: PDFGenerationContext) -> str:
        """Generate HTML for workout session"""
        title = data.get('title', 'Séance d\'Entraînement')
        session_info = data.get('session_info', {})
        exercises = data.get('exercises', [])
        notes = data.get('notes', '')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <div class="document">
                <header class="header">
                    <h1 class="title">{title}</h1>
                    <div class="session-info">
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">Date:</span>
                                <span class="value">{session_info.get('date', 'N/A')}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Durée:</span>
                                <span class="value">{session_info.get('duration', 'N/A')} minutes</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Type:</span>
                                <span class="value">{session_info.get('type', 'N/A')}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Coach:</span>
                                <span class="value">{session_info.get('coach', 'N/A')}</span>
                            </div>
                        </div>
                    </div>
                </header>

                <main class="content">
                    <section class="exercises">
                        <h2 class="section-title">Exercices</h2>
        """

        # Add exercises
        for i, exercise in enumerate(exercises, 1):
            exercise_name = exercise.get('name', 'Exercice sans nom')
            sets = exercise.get('sets', [])
            exercise_notes = exercise.get('notes', '')

            html += f"""
                        <div class="exercise">
                            <h3 class="exercise-title">{i}. {exercise_name}</h3>
            """

            if sets:
                html += """
                            <table class="sets-table">
                                <thead>
                                    <tr>
                                        <th>Série</th>
                                        <th>Répétitions</th>
                                        <th>Poids (kg)</th>
                                        <th>Repos (s)</th>
                                    </tr>
                                </thead>
                                <tbody>
                """

                for j, set_data in enumerate(sets, 1):
                    html += f"""
                                    <tr>
                                        <td>{j}</td>
                                        <td>{set_data.get('reps', '-')}</td>
                                        <td>{set_data.get('weight', '-')}</td>
                                        <td>{set_data.get('rest', '-')}</td>
                                    </tr>
                    """

                html += """
                                </tbody>
                            </table>
                """

            if exercise_notes:
                html += f"""
                            <div class="exercise-notes">
                                <strong>Notes:</strong> {exercise_notes}
                            </div>
                """

            html += """
                        </div>
            """

        # Add coach notes
        if notes:
            html += f"""
                    </section>
                    <section class="notes">
                        <h2 class="section-title">Notes du Coach</h2>
                        <div class="notes-content">
                            {notes}
                        </div>
                    </section>
            """

        html += """
                </main>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_nutrition_html(self, data: Dict[str, Any], context: PDFGenerationContext) -> str:
        """Generate HTML for nutrition plan"""
        title = data.get('title', 'Plan Nutritionnel')
        client_info = data.get('client_info', {})
        meals = data.get('meals', [])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <div class="document">
                <header class="header">
                    <h1 class="title">{title}</h1>
                </header>

                <main class="content">
        """

        # Client information
        if client_info:
            full_name = f"{client_info.get('first_name', '')} {client_info.get('last_name', '')}"
            html += f"""
                    <section class="client-info">
                        <h2 class="section-title">Informations Client</h2>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">Nom:</span>
                                <span class="value">{full_name}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Objectif:</span>
                                <span class="value">{client_info.get('goal', 'N/A')}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Calories cibles:</span>
                                <span class="value">{client_info.get('target_calories', 'N/A')} kcal/jour</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Protéines:</span>
                                <span class="value">{client_info.get('target_protein', 'N/A')} g/jour</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Glucides:</span>
                                <span class="value">{client_info.get('target_carbs', 'N/A')} g/jour</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Lipides:</span>
                                <span class="value">{client_info.get('target_fats', 'N/A')} g/jour</span>
                            </div>
                        </div>
                    </section>
            """

        # Meals
        if meals:
            html += """
                    <section class="meals">
                        <h2 class="section-title">Plan Alimentaire</h2>
            """

            for meal in meals:
                meal_name = meal.get('name', 'Repas')
                meal_time = meal.get('time', '')
                foods = meal.get('foods', [])

                html += f"""
                        <div class="meal">
                            <h3 class="meal-title">{meal_name}
                """

                if meal_time:
                    html += f" - {meal_time}"

                html += """</h3>"""

                if foods:
                    html += """
                            <table class="foods-table">
                                <thead>
                                    <tr>
                                        <th>Aliment</th>
                                        <th>Quantité</th>
                                        <th>Calories</th>
                                        <th>Protéines (g)</th>
                                        <th>Glucides (g)</th>
                                        <th>Lipides (g)</th>
                                    </tr>
                                </thead>
                                <tbody>
                    """

                    total_calories = 0
                    total_protein = 0
                    total_carbs = 0
                    total_fats = 0

                    for food in foods:
                        calories = food.get('calories', 0)
                        protein = food.get('protein', 0)
                        carbs = food.get('carbs', 0)
                        fats = food.get('fats', 0)

                        html += f"""
                                    <tr>
                                        <td>{food.get('name', '')}</td>
                                        <td>{food.get('quantity', '')}</td>
                                        <td>{calories}</td>
                                        <td>{protein}</td>
                                        <td>{carbs}</td>
                                        <td>{fats}</td>
                                    </tr>
                        """

                        total_calories += calories
                        total_protein += protein
                        total_carbs += carbs
                        total_fats += fats

                    # Totals row
                    html += f"""
                                    <tr class="totals-row">
                                        <td><strong>TOTAL</strong></td>
                                        <td></td>
                                        <td><strong>{total_calories}</strong></td>
                                        <td><strong>{total_protein}</strong></td>
                                        <td><strong>{total_carbs}</strong></td>
                                        <td><strong>{total_fats}</strong></td>
                                    </tr>
                                </tbody>
                            </table>
                    """

                html += """
                        </div>
                """

            html += """
                    </section>
            """

        html += """
                </main>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_progress_html(self, data: Dict[str, Any], context: PDFGenerationContext) -> str:
        """Generate HTML for progress report"""
        title = data.get('title', 'Rapport de Progression')
        metrics = data.get('metrics', {})

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <div class="document">
                <header class="header">
                    <h1 class="title">{title}</h1>
                </header>

                <main class="content">
                    <section class="metrics">
                        <h2 class="section-title">Métriques de Progression</h2>
                        <div class="metrics-grid">
        """

        for key, value in metrics.items():
            formatted_key = key.replace('_', ' ').title()
            html += f"""
                            <div class="metric-item">
                                <span class="metric-label">{formatted_key}:</span>
                                <span class="metric-value">{value}</span>
                            </div>
            """

        html += """
                        </div>
                    </section>
                </main>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_generic_html(self, data: Dict[str, Any], context: PDFGenerationContext) -> str:
        """Generate HTML for generic document"""
        title = data.get('title', 'Document')
        sections = data.get('sections', [])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <div class="document">
                <header class="header">
                    <h1 class="title">{title}</h1>
                </header>

                <main class="content">
        """

        for section in sections:
            section_title = section.get('title', '')
            section_content = section.get('content', '')

            if section_title:
                html += f"""
                    <section class="section">
                        <h2 class="section-title">{section_title}</h2>
                        <div class="section-content">
                            {section_content}
                        </div>
                    </section>
                """

        html += """
                </main>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_css_styles(self, context: PDFGenerationContext) -> str:
        """Generate CSS styles for PDF"""
        return """
        @page {
            size: A4;
            margin: 2cm;
        }

        body {
            font-family: -webkit-system-font, "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        .document {
            max-width: 100%;
        }

        .header {
            border-bottom: 2px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }

        .title {
            font-size: 24pt;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
            margin: 0 0 20px 0;
        }

        .section-title {
            font-size: 16pt;
            font-weight: 600;
            color: #2980b9;
            margin: 20px 0 15px 0;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
        }

        .label {
            font-weight: 600;
            color: #34495e;
        }

        .value {
            color: #2c3e50;
        }

        .exercise {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }

        .exercise-title {
            font-size: 14pt;
            font-weight: 600;
            color: #34495e;
            margin: 0 0 10px 0;
        }

        .sets-table, .foods-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 9pt;
        }

        .sets-table th, .foods-table th {
            background: #3498db;
            color: white;
            padding: 8px;
            text-align: center;
            font-weight: 600;
        }

        .sets-table td, .foods-table td {
            padding: 6px 8px;
            text-align: center;
            border: 1px solid #bdc3c7;
        }

        .sets-table tr:nth-child(even), .foods-table tr:nth-child(even) {
            background: #f8f9fa;
        }

        .totals-row {
            background: #ecf0f1 !important;
            font-weight: 600;
        }

        .exercise-notes {
            background: #e8f6f3;
            padding: 10px;
            border-radius: 3px;
            margin-top: 10px;
            font-size: 10pt;
        }

        .meal {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }

        .meal-title {
            font-size: 14pt;
            font-weight: 600;
            color: #27ae60;
            margin: 0 0 10px 0;
        }

        .notes {
            margin-top: 30px;
        }

        .notes-content {
            background: #e8f6f3;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #27ae60;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .metric-item {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 3px;
        }

        .metric-label {
            font-weight: 600;
            color: #34495e;
        }

        .metric-value {
            font-weight: 700;
            color: #2980b9;
        }
        """

    def _estimate_page_count(self, pdf_bytes: bytes) -> int:
        """Estimate page count from PDF bytes"""
        try:
            # Simple estimation based on file size
            # This is a rough approximation
            size_kb = len(pdf_bytes) / 1024
            if size_kb < 50:
                return 1
            elif size_kb < 150:
                return 2
            elif size_kb < 300:
                return 3
            else:
                return max(1, int(size_kb / 100))
        except:
            return 1

    def validate_context(self, context: PDFStrategyContext) -> List[str]:
        """Validate PDF generation context"""
        errors = []

        if not self.available:
            errors.append("WeasyPrint library is not available")

        pdf_context = context.data

        if not pdf_context.template:
            errors.append("Template is required")

        if not pdf_context.data:
            errors.append("Data is required for PDF generation")

        return errors

    def get_supported_context_types(self) -> List[type]:
        """Get supported context types"""
        return [PDFGenerationContext]

    @property
    def preferred_contexts(self) -> List[type]:
        """Contexts where this strategy performs best"""
        return [PDFGenerationContext]