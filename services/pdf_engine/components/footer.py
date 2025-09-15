"""
Footer Component - Professional footer with branding and page numbers
"""

from __future__ import annotations

from typing import Any, Dict, List

from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class FooterComponent:
    """
    Professional footer component with branding, page numbers, and custom text
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def build(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> List[Any]:
        """Build footer elements"""
        elements = []

        if not self.config.get("enabled", True):
            return elements

        # Add spacer before footer
        elements.append(Spacer(1, 0.5 * cm))

        # Separator line
        if self.config.get("show_separator", True):
            elements.append(self._build_separator_line(template_config))

        # Footer content
        footer_table = self._build_footer_table(data, template_config)
        if footer_table:
            elements.append(footer_table)

        return elements

    def _build_separator_line(self, template_config: Dict[str, Any]) -> Any:
        """Build separator line above footer"""
        colors_config = template_config.get("colors", {})

        # Handle case where colors_config is a string (theme name)
        if isinstance(colors_config, str):
            colors_config = {"border": "#E5E7EB"}

        border_color = colors_config.get("border", "#E5E7EB")

        line_data = [[""]]
        line_table = Table(line_data, colWidths=[18 * cm], rowHeights=[0.05 * cm])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(border_color)),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ]))

        return line_table

    def _build_footer_table(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Build main footer table"""
        # Get configuration
        colors_config = template_config.get("colors", {})
        fonts_config = template_config.get("fonts", {})

        # Prepare footer elements
        left_element = self._get_left_element(data, template_config)
        center_element = self._get_center_element(data, template_config)
        right_element = self._get_right_element(data, template_config)

        # Build table data
        footer_data = [[left_element, center_element, right_element]]
        col_widths = [6 * cm, 6 * cm, 6 * cm]

        # Create and style table
        table = Table(footer_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))

        return table

    def _get_left_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get left footer element (brand info)"""
        if not self.config.get("show_branding", True):
            return Paragraph("", self._get_paragraph_style('left', template_config))

        brand_config = template_config.get("brand", {})
        brand_name = brand_config.get("name", "CoachPro")
        tagline = brand_config.get("tagline", "")

        brand_text = brand_name
        if tagline:
            brand_text += f"<br/><i>{tagline}</i>"

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(fonts_config, str):
            fonts_config = {"caption": {"name": "Helvetica", "size": 8}}
        if isinstance(colors_config, str):
            colors_config = {"text_secondary": "#666666"}

        brand_style = f"""
        <font name="{fonts_config.get('caption', {}).get('name', 'Helvetica')}"
              size="{fonts_config.get('caption', {}).get('size', 8)}"
              color="{colors_config.get('text_secondary', '#666666')}">
        <b>{brand_text}</b></font>
        """

        return Paragraph(brand_style, self._get_paragraph_style('left', template_config))

    def _get_center_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get center footer element (custom text)"""
        footer_text = self.config.get("text", "")
        if not footer_text:
            # Default text
            footer_text = "Généré avec CoachPro - Votre partenaire fitness"

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(fonts_config, str):
            fonts_config = {"caption": {"name": "Helvetica", "size": 8}}
        if isinstance(colors_config, str):
            colors_config = {"text_secondary": "#666666"}

        text_style = f"""
        <font name="{fonts_config.get('caption', {}).get('name', 'Helvetica')}"
              size="{fonts_config.get('caption', {}).get('size', 8)}"
              color="{colors_config.get('text_secondary', '#666666')}">
        {footer_text}</font>
        """

        return Paragraph(text_style, self._get_paragraph_style('center', template_config))

    def _get_right_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get right footer element (page numbers, date)"""
        if not self.config.get("show_page_numbers", True):
            return Paragraph("", self._get_paragraph_style('right', template_config))

        # Note: Page numbers are handled by ReportLab's canvas callbacks
        # This is a placeholder for other right-aligned content

        # Generation date
        from datetime import datetime
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y à %H:%M")

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(fonts_config, str):
            fonts_config = {"caption": {"name": "Helvetica", "size": 8}}
        if isinstance(colors_config, str):
            colors_config = {"text_secondary": "#666666"}

        date_style = f"""
        <font name="{fonts_config.get('caption', {}).get('name', 'Helvetica')}"
              size="{fonts_config.get('caption', {}).get('size', 8)}"
              color="{colors_config.get('text_secondary', '#666666')}">
        Généré le {date_text}</font>
        """

        return Paragraph(date_style, self._get_paragraph_style('right', template_config))

    def _get_paragraph_style(self, alignment: str, template_config: Dict[str, Any]):
        """Get paragraph style for text alignment"""
        from reportlab.lib.styles import ParagraphStyle

        align_map = {
            'left': TA_LEFT,
            'center': TA_CENTER,
            'right': TA_RIGHT,
        }

        return ParagraphStyle(
            'FooterStyle',
            alignment=align_map.get(alignment, TA_LEFT),
            spaceAfter=0,
            spaceBefore=0,
        )