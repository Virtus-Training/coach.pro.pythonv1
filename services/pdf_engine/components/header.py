"""
Header Component - Reusable header for all PDF templates
Professional branding and layout
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


class HeaderComponent:
    """
    Professional header component with logo, title, and metadata
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.default_logo_path = Path(__file__).parent.parent.parent.parent / "assets" / "Logo.png"

    def build(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> List[Any]:
        """Build header elements"""
        elements = []

        if not self.config.get("enabled", True):
            return elements

        # Header background bar
        if self.config.get("show_background", True):
            elements.extend(self._build_background_bar(template_config))

        # Logo and title row
        header_table = self._build_header_table(data, template_config)
        if header_table:
            elements.append(header_table)

        # Separator line
        if self.config.get("show_separator", True):
            elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_background_bar(self, template_config: Dict[str, Any]) -> List[Any]:
        """Build colored background bar"""
        colors_config = template_config.get("colors", {})

        # Handle case where colors_config is a string (theme name)
        if isinstance(colors_config, str):
            primary_color = "#2563EB"  # Default color
        else:
            primary_color = colors_config.get("primary", "#2563EB")

        # Create colored rectangle using Table
        bar_data = [[""]]
        bar_table = Table(bar_data, colWidths=[18 * cm], rowHeights=[0.8 * cm])
        bar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(primary_color)),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ]))

        return [bar_table, Spacer(1, -0.5 * cm)]

    def _build_header_table(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Build main header table with logo and title"""
        # Get configuration
        colors_config = template_config.get("colors", {})
        fonts_config = template_config.get("fonts", {})

        # Handle case where configs are strings (theme names)
        if isinstance(colors_config, str):
            colors_config = {"text_primary": "#000000", "text_secondary": "#666666"}
        if isinstance(fonts_config, str):
            fonts_config = {}

        # Prepare data for header table
        header_data = []
        col_widths = []

        # Logo column (if enabled)
        logo_element = None
        if self.config.get("show_logo", True):
            logo_element = self._get_logo_element(template_config)
            if logo_element:
                col_widths.append(3 * cm)

        # Title and info column
        title_element = self._get_title_element(data, template_config)
        info_element = self._get_info_element(data, template_config)

        # Metadata column (if enabled)
        metadata_element = None
        if self.config.get("show_metadata", True):
            metadata_element = self._get_metadata_element(data, template_config)
            if metadata_element:
                col_widths.append(4 * cm)

        # Calculate main content width
        used_width = sum(col_widths)
        main_width = 18 * cm - used_width
        if main_width > 0:
            col_widths.insert(-1 if metadata_element else len(col_widths), main_width)

        # Build table data
        row_data = []
        if logo_element:
            row_data.append(logo_element)

        # Main content cell
        main_content = [title_element]
        if info_element:
            main_content.extend([Spacer(1, 0.2 * cm), info_element])

        row_data.append(main_content)

        if metadata_element:
            row_data.append(metadata_element)

        header_data = [row_data]

        # Create and style table
        if header_data and col_widths:
            table = Table(header_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            return table

        return None

    def _get_logo_element(self, template_config: Dict[str, Any]) -> Any:
        """Get logo element if available"""
        logo_config = template_config.get("brand", {})
        logo_path = logo_config.get("logo_path")

        if not logo_path:
            logo_path = str(self.default_logo_path)

        try:
            if Path(logo_path).exists():
                logo_width = logo_config.get("logo_width", 2.5) * cm
                logo_height = logo_config.get("logo_height", 2.5) * cm
                return Image(logo_path, width=logo_width, height=logo_height)
        except Exception:
            pass

        return None

    def _get_title_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get title element"""
        title = data.get("title", "Document")
        subtitle = data.get("subtitle", "")

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(colors_config, str):
            colors_config = {"text_primary": "#000000", "text_secondary": "#666666"}
        if isinstance(fonts_config, str):
            fonts_config = {}

        title_style = f"""
        <font name="{fonts_config.get('title', {}).get('name', 'Helvetica-Bold')}"
              size="{fonts_config.get('title', {}).get('size', 20)}"
              color="{colors_config.get('text_primary', '#000000')}">
        <b>{title}</b></font>
        """

        if subtitle:
            subtitle_style = f"""
            <font name="{fonts_config.get('subtitle', {}).get('name', 'Helvetica')}"
                  size="{fonts_config.get('subtitle', {}).get('size', 12)}"
                  color="{colors_config.get('text_secondary', '#666666')}">
            {subtitle}</font>
            """
            title_style += f"<br/>{subtitle_style}"

        return Paragraph(title_style, self._get_paragraph_style('left'))

    def _get_info_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get info element (client name, date, etc.)"""
        info_parts = []

        # Client name
        client_name = data.get("client_name")
        if client_name:
            info_parts.append(f"Client: {client_name}")

        # Date
        created_date = data.get("created_at") or data.get("date")
        if created_date:
            if isinstance(created_date, str):
                # Format date string
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                    formatted_date = dt.strftime("%d/%m/%Y")
                except:
                    formatted_date = created_date
            else:
                formatted_date = str(created_date)
            info_parts.append(f"Date: {formatted_date}")

        if not info_parts:
            return None

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(colors_config, str):
            colors_config = {"text_primary": "#000000", "text_secondary": "#666666"}
        if isinstance(fonts_config, str):
            fonts_config = {}

        info_text = " • ".join(info_parts)
        info_style = f"""
        <font name="{fonts_config.get('body', {}).get('name', 'Helvetica')}"
              size="{fonts_config.get('body', {}).get('size', 10)}"
              color="{colors_config.get('text_secondary', '#666666')}">
        {info_text}</font>
        """

        return Paragraph(info_style, self._get_paragraph_style('left'))

    def _get_metadata_element(self, data: Dict[str, Any], template_config: Dict[str, Any]) -> Any:
        """Get metadata element (duration, type, etc.)"""
        metadata_parts = []

        # Duration
        duration = data.get("duration") or data.get("duree_minutes")
        if duration:
            if isinstance(duration, (int, float)):
                metadata_parts.append(f"T {int(duration)} min")  # Removed emoji
            else:
                metadata_parts.append(f"T {duration}")  # Removed emoji

        # Type/Mode
        doc_type = data.get("type") or data.get("mode")
        if doc_type:
            metadata_parts.append(f"Type: {doc_type}")  # Removed emoji

        # Status
        status = data.get("status")
        if status:
            status_icons = {"draft": "D", "final": "F", "archived": "A"}  # Removed emojis
            status_icon = status_icons.get(status.lower(), "S")
            metadata_parts.append(f"{status_icon} {status}")

        if not metadata_parts:
            return None

        fonts_config = template_config.get("fonts", {})
        colors_config = template_config.get("colors", {})

        # Handle case where configs are strings (theme names)
        if isinstance(colors_config, str):
            colors_config = {"text_primary": "#000000", "text_secondary": "#666666"}
        if isinstance(fonts_config, str):
            fonts_config = {}

        metadata_text = "<br/>".join(metadata_parts)
        metadata_style = f"""
        <font name="{fonts_config.get('caption', {}).get('name', 'Helvetica')}"
              size="{fonts_config.get('caption', {}).get('size', 9)}"
              color="{colors_config.get('text_secondary', '#666666')}">
        {metadata_text}</font>
        """

        return Paragraph(metadata_style, self._get_paragraph_style('right'))

    def _get_paragraph_style(self, alignment: str):
        """Get paragraph style for text alignment"""
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

        align_map = {
            'left': TA_LEFT,
            'center': TA_CENTER,
            'right': TA_RIGHT,
        }

        return ParagraphStyle(
            'HeaderStyle',
            alignment=align_map.get(alignment, TA_LEFT),
            spaceAfter=0,
        )