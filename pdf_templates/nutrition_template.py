from __future__ import annotations

from pathlib import Path
from typing import Any, List

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from dtos.nutrition_dtos import NutritionPageDTO, RepasDTO
TABLE_HEADER_BG = "#374151"
TABLE_ROW_ODD_BG = "#1F2937"
TABLE_ROW_EVEN_BG = "#111827"
NEUTRAL_700 = "#374151"
TEXT = "#E5E7EB"


class NutritionPDFTemplate:
    def __init__(self, dto: NutritionPageDTO) -> None:
        self.dto = dto

    def build(self, file_path: str) -> None:
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements: List[Any] = []
        elements.extend(self._header())
        elements.extend(self._totals_table())
        for repas in self.dto.plan.repas:
            elements.extend(self._meal_table(repas))
        doc.build(elements)

    def _header(self) -> List[Any]:
        styles = getSampleStyleSheet()
        right = ParagraphStyle("right", parent=styles["Normal"], alignment=TA_RIGHT)
        lines = ["<b>Plan Alimentaire</b>"]
        client = self.dto.client
        if client:
            lines.append(f"{client.prenom} {client.nom}")
        para = Paragraph("<br/>".join(lines), right)
        logo_path = Path(__file__).resolve().parent.parent / "assets" / "Logo.png"
        logo = Image(str(logo_path), width=70, preserveAspectRatio=True)
        table = Table([[logo, para]], colWidths=[70, 470])
        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        return [table, Spacer(1, 20)]

    def _totals_table(self) -> List[Any]:
        fiche = self.dto.fiche
        plan = self.dto.plan
        data = [
            ["", "Kcal", "Protéines (g)", "Glucides (g)", "Lipides (g)"],
            [
                "Objectifs",
                f"{getattr(fiche, 'objectif_kcal', 0)}",
                f"{getattr(fiche, 'proteines_g', 0)}",
                f"{getattr(fiche, 'glucides_g', 0)}",
                f"{getattr(fiche, 'lipides_g', 0)}",
            ],
            [
                "Total du plan",
                f"{plan.totals_kcal:.0f}",
                f"{plan.totals_proteines:.1f}",
                f"{plan.totals_glucides:.1f}",
                f"{plan.totals_lipides:.1f}",
            ],
        ]
        table = Table(data, colWidths=[120, 90, 110, 110, 90])
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(TABLE_HEADER_BG)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(TEXT)),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(NEUTRAL_700)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ]
        for i in range(1, len(data)):
            bg = TABLE_ROW_ODD_BG if i % 2 else TABLE_ROW_EVEN_BG
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(bg)))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.HexColor(TEXT)))
        table.setStyle(TableStyle(style))
        return [table, Spacer(1, 20)]

    def _meal_table(self, repas: RepasDTO) -> List[Any]:
        styles = getSampleStyleSheet()
        elems: List[Any] = []
        elems.append(Paragraph(f"<b>{repas.nom}</b>", styles["Heading4"]))
        elems.append(Spacer(1, 6))
        data = [["Aliment", "Quantité", "Kcal", "P", "G", "L"]]
        for item in repas.items:
            qty = f"{item.quantite:.0f}{item.unite}"
            data.append(
                [
                    item.nom,
                    qty,
                    f"{item.kcal:.0f}",
                    f"{item.proteines:.1f}",
                    f"{item.glucides:.1f}",
                    f"{item.lipides:.1f}",
                ]
            )
        data.append(
            [
                "Sous-total",
                "",
                f"{repas.totals_kcal:.0f}",
                f"{repas.totals_proteines:.1f}",
                f"{repas.totals_glucides:.1f}",
                f"{repas.totals_lipides:.1f}",
            ]
        )
        table = Table(data, colWidths=[250, 80, 60, 60, 60, 60])
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(TABLE_HEADER_BG)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(TEXT)),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(NEUTRAL_700)),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
        for i in range(1, len(data) - 1):
            bg = TABLE_ROW_ODD_BG if i % 2 else TABLE_ROW_EVEN_BG
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(bg)))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.HexColor(TEXT)))
        last = len(data) - 1
        style.extend(
            [
                ("BACKGROUND", (0, last), (-1, last), colors.HexColor(TABLE_HEADER_BG)),
                ("TEXTCOLOR", (0, last), (-1, last), colors.HexColor(TEXT)),
                ("FONTNAME", (0, last), (-1, last), "Helvetica-Bold"),
            ]
        )
        table.setStyle(TableStyle(style))
        elems.append(table)
        elems.append(Spacer(1, 12))
        return elems


__all__ = ["NutritionPDFTemplate"]
