"""
Base classes for PDF generation strategies
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
import base64

from ..base import StrategyContext, StrategyResult


class PDFQuality(Enum):
    """PDF quality levels"""
    DRAFT = "draft"          # Fast generation, basic formatting
    STANDARD = "standard"    # Good balance of quality and speed
    HIGH = "high"           # High quality, slower generation
    PRINT_READY = "print"   # Print-ready quality, slowest


class PDFFormat(Enum):
    """PDF output formats"""
    A4_PORTRAIT = "a4_portrait"
    A4_LANDSCAPE = "a4_landscape"
    LETTER_PORTRAIT = "letter_portrait"
    LETTER_LANDSCAPE = "letter_landscape"
    CUSTOM = "custom"


class PDFComplexity(Enum):
    """PDF content complexity levels"""
    SIMPLE = "simple"        # Text only, minimal formatting
    MEDIUM = "medium"        # Text + basic graphics/tables
    COMPLEX = "complex"      # Rich formatting, charts, images
    ADVANCED = "advanced"    # Complex layouts, advanced graphics


@dataclass
class PDFTemplate:
    """PDF template configuration"""
    name: str
    template_type: str  # workout, nutrition, report, etc.
    layout: str
    styles: Dict[str, Any] = field(default_factory=dict)
    sections: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    assets: Dict[str, str] = field(default_factory=dict)  # logos, images, etc.


@dataclass
class PDFGenerationContext:
    """Context for PDF generation"""
    template: PDFTemplate
    data: Dict[str, Any]
    quality: PDFQuality = PDFQuality.STANDARD
    format: PDFFormat = PDFFormat.A4_PORTRAIT
    complexity: PDFComplexity = PDFComplexity.MEDIUM
    output_filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Performance preferences
    max_generation_time_seconds: float = 30.0
    prefer_speed_over_quality: bool = False
    enable_compression: bool = True

    # Content options
    include_charts: bool = True
    include_images: bool = True
    include_watermark: bool = False
    page_numbering: bool = True

    # Accessibility
    enable_accessibility: bool = False
    alt_text_required: bool = False


@dataclass
class PDFQualityMetrics:
    """Quality assessment metrics for generated PDF"""
    file_size_kb: float
    generation_time_ms: float
    page_count: int
    image_quality_score: float = 0.0  # 0-100
    text_readability_score: float = 0.0  # 0-100
    layout_consistency_score: float = 0.0  # 0-100
    overall_quality_score: float = 0.0  # 0-100

    def calculate_overall_score(self):
        """Calculate overall quality score"""
        scores = [
            self.image_quality_score,
            self.text_readability_score,
            self.layout_consistency_score
        ]

        valid_scores = [s for s in scores if s > 0]
        if valid_scores:
            self.overall_quality_score = sum(valid_scores) / len(valid_scores)
        else:
            self.overall_quality_score = 0.0


@dataclass
class PDFGenerationResult:
    """Result of PDF generation"""
    pdf_data: bytes
    quality_metrics: PDFQualityMetrics
    generation_engine: str
    template_used: str
    success: bool = True
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def pdf_base64(self) -> str:
        """Get PDF data as base64 string"""
        return base64.b64encode(self.pdf_data).decode('utf-8')

    @property
    def file_size_mb(self) -> float:
        """Get file size in MB"""
        return len(self.pdf_data) / (1024 * 1024)

    def save_to_file(self, filepath: str) -> bool:
        """Save PDF to file"""
        try:
            with open(filepath, 'wb') as f:
                f.write(self.pdf_data)
            return True
        except Exception as e:
            self.error_message = f"Failed to save PDF: {e}"
            return False


# Type aliases for strategy framework integration
PDFStrategyContext = StrategyContext[PDFGenerationContext]
PDFStrategyResult = StrategyResult[PDFGenerationResult]