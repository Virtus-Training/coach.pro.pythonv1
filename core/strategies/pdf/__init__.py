"""
PDF Generation Strategy Engine

Multi-provider PDF generation with automatic fallback,
quality assessment, and performance optimization.
"""

from .base import PDFGenerationContext, PDFGenerationResult
from .fpdf_strategy import FPDFStrategy
from .manager import PDFStrategyManager
from .reportlab_strategy import ReportLabPDFStrategy
from .weasyprint_strategy import WeasyPrintPDFStrategy

__all__ = [
    "PDFGenerationContext",
    "PDFGenerationResult",
    "ReportLabPDFStrategy",
    "WeasyPrintPDFStrategy",
    "FPDFStrategy",
    "PDFStrategyManager",
]
