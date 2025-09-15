"""
FPDF Lightweight PDF Generation Strategy

Minimal, fast PDF generation using FPDF library.
Optimized for simple documents and emergency fallback.
"""

import time
from typing import Any, Dict, List, Optional

try:
    from fpdf import FPDF

    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

from ..base import BaseStrategy, StrategyConfig, StrategyPriority
from .base import (
    PDFComplexity,
    PDFGenerationContext,
    PDFGenerationResult,
    PDFQualityMetrics,
    PDFStrategyContext,
    PDFStrategyResult,
)


class CustomFPDF(FPDF):
    """Custom FPDF class with enhanced features"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        """Page header"""
        if hasattr(self, "doc_title"):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, self.doc_title, 0, 1, "C")
            self.ln(10)

    def footer(self):
        """Page footer"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title: str):
        """Add chapter title"""
        self.set_font("Arial", "B", 14)
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, "L", True)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def section_title(self, title: str):
        """Add section title"""
        self.set_font("Arial", "B", 12)
        self.set_text_color(41, 128, 185)
        self.cell(0, 8, title, 0, 1, "L")
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def body_text(self, text: str):
        """Add body text"""
        self.set_font("Arial", "", 10)
        # Handle text wrapping
        lines = text.split("\n")
        for line in lines:
            self.cell(
                0, 6, line.encode("latin-1", "replace").decode("latin-1"), 0, 1, "L"
            )

    def add_table(
        self,
        headers: List[str],
        data: List[List[str]],
        col_widths: Optional[List[int]] = None,
    ):
        """Add a table"""
        if not col_widths:
            col_widths = [190 // len(headers)] * len(headers)

        # Table header
        self.set_font("Arial", "B", 9)
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255, 255, 255)

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, "C", True)
        self.ln()

        # Table data
        self.set_font("Arial", "", 9)
        self.set_text_color(0, 0, 0)
        fill = False

        for row in data:
            if fill:
                self.set_fill_color(240, 240, 240)
            else:
                self.set_fill_color(255, 255, 255)

            for i, cell in enumerate(row):
                if i < len(col_widths):
                    # Ensure text fits in cell
                    cell_text = str(cell)[:20]  # Truncate if too long
                    self.cell(col_widths[i], 6, cell_text, 1, 0, "C", True)
            self.ln()
            fill = not fill

    def add_highlight_box(self, text: str):
        """Add highlighted text box"""
        self.set_fill_color(236, 240, 241)
        self.set_draw_color(189, 195, 199)
        self.rect(self.get_x(), self.get_y(), 190, 15, "DF")

        self.set_font("Arial", "", 10)
        self.set_text_color(39, 174, 96)
        self.cell(
            190, 15, text.encode("latin-1", "replace").decode("latin-1"), 0, 1, "L"
        )
        self.set_text_color(0, 0, 0)
        self.ln(5)


class FPDFStrategy(BaseStrategy[PDFGenerationContext]):
    """
    Lightweight PDF generation using FPDF.

    Features:
    - Fast generation for simple documents
    - Minimal dependencies
    - Emergency fallback capability
    - Small file sizes
    - Basic formatting only
    """

    def __init__(self):
        config = StrategyConfig(
            name="fpdf_pdf",
            version="1.0.0",
            priority=StrategyPriority.FALLBACK,
            timeout_seconds=20.0,
            cache_enabled=True,
            cache_ttl_seconds=3600,  # 1 hour
        )
        super().__init__(config)

        # Strategy metadata
        self._strategy_category = "pdf_generation"
        self._strategy_tags = {"lightweight", "fallback", "simple"}

        # Check availability
        self.available = FPDF_AVAILABLE

    async def execute_async(self, context: PDFStrategyContext) -> PDFStrategyResult:
        """Execute PDF generation with FPDF"""
        if not self.available:
            return PDFStrategyResult(
                data=None, success=False, error_message="FPDF library not available"
            )

        start_time = time.time()

        try:
            pdf_context = context.data

            # Create FPDF document
            pdf = CustomFPDF()
            pdf.doc_title = pdf_context.template.name

            # Build document content
            self._build_document_content(pdf, pdf_context)

            # Get PDF data
            pdf_data = pdf.output(dest="S").encode("latin-1")

            # Calculate metrics
            generation_time = (time.time() - start_time) * 1000
            quality_metrics = PDFQualityMetrics(
                file_size_kb=len(pdf_data) / 1024,
                generation_time_ms=generation_time,
                page_count=pdf.page_no(),
                image_quality_score=50.0,  # Limited image support
                text_readability_score=70.0,  # Basic typography
                layout_consistency_score=75.0,  # Simple but consistent
            )
            quality_metrics.calculate_overall_score()

            # Create result
            result = PDFGenerationResult(
                pdf_data=pdf_data,
                quality_metrics=quality_metrics,
                generation_engine="FPDF",
                template_used=pdf_context.template.name,
                success=True,
            )

            return PDFStrategyResult(
                data=result,
                success=True,
                execution_time_ms=generation_time,
                strategy_name=self.name,
                strategy_version=self.version,
            )

        except Exception as e:
            generation_time = (time.time() - start_time) * 1000
            return PDFStrategyResult(
                data=None,
                success=False,
                execution_time_ms=generation_time,
                strategy_name=self.name,
                error_message=f"FPDF PDF generation failed: {str(e)}",
            )

    def _build_document_content(self, pdf: CustomFPDF, context: PDFGenerationContext):
        """Build document content"""
        template = context.template
        data = context.data

        # Add first page
        pdf.add_page()

        if template.template_type == "workout":
            self._build_workout_document(pdf, data, context)
        elif template.template_type == "nutrition":
            self._build_nutrition_document(pdf, data, context)
        elif template.template_type == "progress_report":
            self._build_progress_document(pdf, data, context)
        else:
            self._build_generic_document(pdf, data, context)

    def _build_workout_document(
        self, pdf: CustomFPDF, data: Dict[str, Any], context: PDFGenerationContext
    ):
        """Build workout session document"""
        # Title
        title = data.get("title", "Séance d'Entraînement")
        pdf.chapter_title(title)

        # Session info
        session_info = data.get("session_info", {})
        if session_info:
            pdf.section_title("Informations de la séance")

            info_text = f"""Date: {session_info.get("date", "N/A")}
Durée: {session_info.get("duration", "N/A")} minutes
Type: {session_info.get("type", "N/A")}
Coach: {session_info.get("coach", "N/A")}"""

            pdf.body_text(info_text)
            pdf.ln(10)

        # Exercises
        exercises = data.get("exercises", [])
        if exercises:
            pdf.section_title("Exercices")

            for i, exercise in enumerate(exercises, 1):
                exercise_name = exercise.get("name", "Exercice sans nom")
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, f"{i}. {exercise_name}", 0, 1, "L")

                sets = exercise.get("sets", [])
                if sets:
                    # Create sets table
                    headers = ["Série", "Reps", "Poids", "Repos"]
                    table_data = []

                    for j, set_data in enumerate(sets, 1):
                        table_data.append(
                            [
                                str(j),
                                str(set_data.get("reps", "-")),
                                str(set_data.get("weight", "-")),
                                str(set_data.get("rest", "-")),
                            ]
                        )

                    pdf.add_table(headers, table_data, [30, 40, 40, 40])

                # Exercise notes
                notes = exercise.get("notes", "")
                if notes:
                    pdf.ln(3)
                    pdf.set_font("Arial", "I", 9)
                    pdf.cell(
                        0, 6, f"Notes: {notes[:100]}", 0, 1, "L"
                    )  # Truncate long notes

                pdf.ln(8)

        # Coach notes
        notes = data.get("notes", "")
        if notes:
            pdf.section_title("Notes du Coach")
            pdf.add_highlight_box(notes[:200])  # Truncate if too long

    def _build_nutrition_document(
        self, pdf: CustomFPDF, data: Dict[str, Any], context: PDFGenerationContext
    ):
        """Build nutrition plan document"""
        # Title
        title = data.get("title", "Plan Nutritionnel")
        pdf.chapter_title(title)

        # Client info
        client_info = data.get("client_info", {})
        if client_info:
            pdf.section_title("Informations Client")

            info_text = f"""Nom: {client_info.get("first_name", "")} {client_info.get("last_name", "")}
Objectif: {client_info.get("goal", "N/A")}
Calories: {client_info.get("target_calories", "N/A")} kcal/jour
Protéines: {client_info.get("target_protein", "N/A")} g/jour
Glucides: {client_info.get("target_carbs", "N/A")} g/jour
Lipides: {client_info.get("target_fats", "N/A")} g/jour"""

            pdf.body_text(info_text)
            pdf.ln(10)

        # Meals
        meals = data.get("meals", [])
        if meals:
            pdf.section_title("Plan Alimentaire")

            for meal in meals:
                meal_name = meal.get("name", "Repas")
                meal_time = meal.get("time", "")

                header_text = meal_name
                if meal_time:
                    header_text += f" - {meal_time}"

                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, header_text, 0, 1, "L")

                foods = meal.get("foods", [])
                if foods:
                    # Simplified food table
                    headers = ["Aliment", "Quantité", "Cal", "Prot"]
                    food_data = []

                    total_calories = 0
                    total_protein = 0

                    for food in foods[:5]:  # Limit to 5 foods per meal
                        calories = food.get("calories", 0)
                        protein = food.get("protein", 0)

                        food_data.append(
                            [
                                food.get("name", "")[:15],  # Truncate name
                                food.get("quantity", "")[:10],
                                str(calories),
                                str(protein),
                            ]
                        )

                        total_calories += calories
                        total_protein += protein

                    # Add totals
                    food_data.append(
                        ["TOTAL", "", str(total_calories), str(total_protein)]
                    )

                    pdf.add_table(headers, food_data, [80, 40, 30, 30])

                pdf.ln(8)

    def _build_progress_document(
        self, pdf: CustomFPDF, data: Dict[str, Any], context: PDFGenerationContext
    ):
        """Build progress report document"""
        # Title
        title = data.get("title", "Rapport de Progression")
        pdf.chapter_title(title)

        # Metrics
        metrics = data.get("metrics", {})
        if metrics:
            pdf.section_title("Métriques de Progression")

            # Display metrics in a simple format
            for key, value in list(metrics.items())[:10]:  # Limit to 10 metrics
                formatted_key = key.replace("_", " ").title()
                pdf.body_text(f"{formatted_key}: {value}")

            pdf.ln(10)

    def _build_generic_document(
        self, pdf: CustomFPDF, data: Dict[str, Any], context: PDFGenerationContext
    ):
        """Build generic document"""
        # Title
        title = data.get("title", "Document")
        pdf.chapter_title(title)

        # Sections
        sections = data.get("sections", [])
        for section in sections[:5]:  # Limit to 5 sections
            section_title = section.get("title", "")
            section_content = section.get("content", "")

            if section_title:
                pdf.section_title(section_title)

            if section_content:
                # Truncate content to fit in simple PDF
                truncated_content = section_content[:500]
                if len(section_content) > 500:
                    truncated_content += "..."

                pdf.body_text(truncated_content)
                pdf.ln(8)

    def validate_context(self, context: PDFStrategyContext) -> List[str]:
        """Validate PDF generation context"""
        errors = []

        if not self.available:
            errors.append("FPDF library is not available")

        pdf_context = context.data

        if not pdf_context.template:
            errors.append("Template is required")

        if not pdf_context.data:
            errors.append("Data is required for PDF generation")

        # FPDF works best with simple content
        if pdf_context.complexity == PDFComplexity.ADVANCED:
            errors.append(
                "FPDF strategy is not suitable for advanced complexity documents"
            )

        return errors

    def get_supported_context_types(self) -> List[type]:
        """Get supported context types"""
        return [PDFGenerationContext]

    @property
    def preferred_contexts(self) -> List[type]:
        """Contexts where this strategy performs best"""
        # FPDF is best for simple, emergency fallback scenarios
        return []
