"""
Base Template Class - Foundation for all PDF templates
Implements common functionality and template pattern
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from ..components.footer import FooterComponent
from ..components.header import HeaderComponent
from ..managers.style_manager import StyleManager


class BaseTemplate(ABC):
    """
    Abstract base class for all PDF templates
    Implements Template Method pattern for consistent PDF generation
    """

    def __init__(self, data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        self.data = data
        self.config = config or {}
        self.style_manager = StyleManager()
        self.page_count = 0
        self.preview_mode = False
        self.max_preview_pages = 3

        # Default configuration
        self.default_config = self._get_default_config()
        self.merged_config = {**self.default_config, **self.config}

        # Components
        self.header = HeaderComponent(self.merged_config.get("header", {}))
        self.footer = FooterComponent(self.merged_config.get("footer", {}))

        # Styles
        self._setup_styles()

    def build(self, output: Union[str, BytesIO]) -> None:
        """
        Main template method - builds the complete PDF
        """
        start_time = time.perf_counter()

        if isinstance(output, str):
            doc = SimpleDocTemplate(
                output, pagesize=self._get_page_size(), **self._get_doc_margins()
            )
        else:
            doc = SimpleDocTemplate(
                output, pagesize=self._get_page_size(), **self._get_doc_margins()
            )

        # Build document elements
        elements = []
        elements.extend(self._build_header())
        elements.extend(self._build_content())
        elements.extend(self._build_footer())

        # Build PDF
        doc.build(
            elements, onFirstPage=self._on_first_page, onLaterPages=self._on_later_pages
        )

        # Update page count
        self.page_count = doc.page

        build_time = time.perf_counter() - start_time
        if build_time > 3.0:  # Performance warning
            print(f"⚠️ PDF generation took {build_time:.2f}s (target: <3s)")

    @abstractmethod
    def _build_content(self) -> List[Any]:
        """Build main content - must be implemented by subclasses"""
        pass

    @abstractmethod
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for this template type"""
        pass

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for required data structure"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
            },
            "required": ["title"],
        }

    def set_preview_mode(self, enabled: bool, max_pages: int = 3) -> None:
        """Enable preview mode for faster rendering"""
        self.preview_mode = enabled
        self.max_preview_pages = max_pages

    def apply_style_overrides(self, overrides: Dict[str, Any]) -> None:
        """Apply style overrides to template configuration"""
        self.merged_config = {**self.merged_config, **overrides}
        self._setup_styles()

    def _build_header(self) -> List[Any]:
        """Build header elements"""
        if self.merged_config.get("show_header", True):
            return self.header.build(self.data, self.merged_config)
        return []

    def _build_footer(self) -> List[Any]:
        """Build footer elements"""
        if self.merged_config.get("show_footer", True):
            return self.footer.build(self.data, self.merged_config)
        return []

    def _setup_styles(self) -> None:
        """Setup paragraph and table styles"""
        base_styles = getSampleStyleSheet()

        # Extract style configuration
        self.merged_config.get("styles", {})
        colors = self.merged_config.get("colors", {})
        fonts = self.merged_config.get("fonts", {})

        # Handle case where colors is a theme name instead of a dict
        if isinstance(colors, str):
            # If colors is a theme name, use default colors for now
            colors = {
                "primary": "#2563EB",
                "secondary": "#7C3AED",
                "text_primary": "#1F2937",
                "text_secondary": "#6B7280",
            }

        # Create custom styles
        self.styles = {
            "title": ParagraphStyle(
                "Title",
                parent=base_styles["Title"],
                fontName=fonts.get("title", {}).get("name", "Helvetica-Bold"),
                fontSize=fonts.get("title", {}).get("size", 20),
                textColor=self._hex_to_color(colors.get("text_primary", "#000000")),
                spaceAfter=20,
            ),
            "heading": ParagraphStyle(
                "Heading",
                parent=base_styles["Heading1"],
                fontName=fonts.get("heading", {}).get("name", "Helvetica-Bold"),
                fontSize=fonts.get("heading", {}).get("size", 14),
                textColor=self._hex_to_color(colors.get("text_primary", "#000000")),
                spaceBefore=12,
                spaceAfter=8,
            ),
            "body": ParagraphStyle(
                "Body",
                parent=base_styles["Normal"],
                fontName=fonts.get("body", {}).get("name", "Helvetica"),
                fontSize=fonts.get("body", {}).get("size", 10),
                textColor=self._hex_to_color(colors.get("text_primary", "#000000")),
                spaceAfter=6,
            ),
            "caption": ParagraphStyle(
                "Caption",
                parent=base_styles["Normal"],
                fontName=fonts.get("caption", {}).get("name", "Helvetica"),
                fontSize=fonts.get("caption", {}).get("size", 8),
                textColor=self._hex_to_color(colors.get("text_secondary", "#666666")),
                spaceAfter=4,
            ),
        }

    def _get_page_size(self) -> tuple:
        """Get page size from configuration"""
        size = self.merged_config.get("page_size", "A4")
        return A4 if size == "A4" else LETTER

    def _get_doc_margins(self) -> Dict[str, float]:
        """Get document margins from configuration"""
        margins = self.merged_config.get("layout", {}).get("margins", {})
        return {
            "topMargin": margins.get("top", 60),
            "bottomMargin": margins.get("bottom", 60),
            "leftMargin": margins.get("left", 50),
            "rightMargin": margins.get("right", 50),
        }

    def _on_first_page(self, canvas, doc) -> None:
        """Callback for first page rendering"""
        # Add watermark if configured
        if self.merged_config.get("watermark", {}).get("enabled", False):
            self._add_watermark(canvas, doc)

    def _on_later_pages(self, canvas, doc) -> None:
        """Callback for subsequent pages"""
        # Add page numbers
        if self.merged_config.get("show_page_numbers", True):
            self._add_page_number(canvas, doc)

    def _add_watermark(self, canvas, doc) -> None:
        """Add watermark to page"""
        watermark_config = self.merged_config.get("watermark", {})
        text = watermark_config.get("text", "DRAFT")

        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 50)
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.rotate(45)
        canvas.drawCentredText(300, -100, text)
        canvas.restoreState()

    def _add_page_number(self, canvas, doc) -> None:
        """Add page number to footer"""
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"

        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColorRGB(0.5, 0.5, 0.5)
        canvas.drawRightString(doc.pagesize[0] - 50, 30, text)
        canvas.restoreState()

    def _hex_to_color(self, hex_color: str) -> Color:
        """Convert hex color string to ReportLab Color"""
        if hex_color.startswith("#"):
            return HexColor(hex_color)
        return HexColor(f"#{hex_color}")

    def _should_break_page(self) -> bool:
        """Check if we should break to next page in preview mode"""
        return self.preview_mode and self.page_count >= self.max_preview_pages
