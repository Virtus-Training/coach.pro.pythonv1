"""
Minimal PDF Test - Create a simple working template to isolate the issue
"""

import sys
import tempfile
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import mm

print("MINIMAL PDF TEST")
print("=" * 40)

try:
    from services.pdf_engine.templates.base_template import BaseTemplate
    from typing import Dict, Any, List

    class TestTemplate(BaseTemplate):
        def _build_content(self) -> List[Any]:
            """Simple test content"""
            content = []

            # Create a simple paragraph
            title_style = ParagraphStyle(
                'TestTitle',
                fontSize=16,
                textColor=colors.black,
                alignment=TA_LEFT
            )

            content.append(
                Paragraph(f"<b>Test PDF - {self.data.get('title', 'No title')}</b>", title_style)
            )
            content.append(Spacer(1, 10*mm))

            # Create a simple table with proper Paragraphs
            body_style = ParagraphStyle(
                'TestBody',
                fontSize=12,
                textColor=colors.black,
                alignment=TA_LEFT
            )

            table_data = [
                [
                    Paragraph("<b>Field</b>", body_style),
                    Paragraph("<b>Value</b>", body_style)
                ],
                [
                    Paragraph("Client", body_style),
                    Paragraph(self.data.get('client_name', 'N/A'), body_style)
                ],
                [
                    Paragraph("Date", body_style),
                    Paragraph(self.data.get('session_date', 'N/A'), body_style)
                ]
            ]

            table = Table(table_data, colWidths=[5*mm*20, 5*mm*20])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            content.append(table)

            return content

        def _get_default_config(self) -> Dict[str, Any]:
            return {
                "page_size": "A4",
                "margins": {
                    "top": 25*mm,
                    "bottom": 25*mm,
                    "left": 25*mm,
                    "right": 25*mm
                }
            }

    # Test the minimal template
    test_data = {
        "title": "Test Workout",
        "client_name": "John Doe",
        "session_date": "2024-01-15"
    }

    template = TestTemplate(test_data)
    print("SUCCESS: Test template created")

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        output_path = tmp.name

    template.build(output_path)
    print(f"SUCCESS: PDF generated at {output_path}")

    if Path(output_path).exists():
        size = Path(output_path).stat().st_size
        print(f"File size: {size} bytes")

    # Now test with PDFEngine
    print("\nTesting with PDFEngine...")
    from services.pdf_engine.core.template_factory import TemplateFactory
    from services.pdf_engine.core.pdf_engine import PDFEngine

    class TestFactory(TemplateFactory):
        def create_template(self, template_type, data, config=None):
            if template_type == "test":
                return TestTemplate(data, config)
            return super().create_template(template_type, data, config)

    engine = PDFEngine()
    engine.template_factory = TestFactory()

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        output_path2 = tmp.name

    result = engine.generate_sync("test", test_data, output_path2)
    print(f"SUCCESS: PDFEngine result: {result}")

except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()

print("\nMINIMAL TEST COMPLETED")
print("=" * 40)