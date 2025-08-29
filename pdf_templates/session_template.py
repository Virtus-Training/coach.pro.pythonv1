from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

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

TABLE_HEADER_BG = "#374151"
TABLE_ROW_ODD_BG = "#1F2937"
TABLE_ROW_EVEN_BG = "#111827"
NEUTRAL_700 = "#374151"
TEXT = "#E5E7EB"


class SessionPDFTemplate:
    def __init__(
        self, session_dto: Dict[str, Any], client_name: str | None = None
    ) -> None:
        self.session = session_dto
        self.client_name = client_name

    def build(self, file_path: str) -> None:
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements: List[Any] = []
        elements.extend(self._header())
        for block in self.session.get("blocks", []):
            elements.extend(self._block_table(block))
        doc.build(elements)

    def _header(self) -> List[Any]:
        styles = getSampleStyleSheet()
        right = ParagraphStyle("right", parent=styles["Normal"], alignment=TA_RIGHT)
        title = self.session.get("meta", {}).get("title", "Séance")
        lines = [f"<b>{title}</b>"]
        if self.client_name:
            lines.append(f"Client : {self.client_name}")
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

    def _block_table(self, block: Dict[str, Any]) -> List[Any]:
        styles = getSampleStyleSheet()
        elems: List[Any] = []
        title = block.get("title") or block.get("format", "")
        if title:
            elems.append(Paragraph(f"<b>{title}</b>", styles["Heading4"]))
            elems.append(Spacer(1, 6))
        fmt = (block.get("format", "") or "").upper().replace(" ", "")
        data: list[list[str]]
        col_widths: list[int]
        if fmt == "TABATA":
            data = [["Exercice", "Notes"]]
            for ex in block.get("exercises", []):
                note = ex.get("notes") or ex.get("reps", "")
                data.append([ex.get("nom", ""), note])
            col_widths = [310, 180]
        elif fmt == "AMRAP":
            data = [["Exercice", "Séries/Reps"]]
            for ex in block.get("exercises", []):
                series, reps = self._split_series_reps(ex.get("reps"))
                combo = f"{series}x{reps}" if series and reps else series or reps
                data.append([ex.get("nom", ""), combo])
            col_widths = [250, 180]
        elif fmt in {"EMOM", "FORTIME"}:
            data = [["Exercice", "Répétitions"]]
            for ex in block.get("exercises", []):
                _, reps = self._split_series_reps(ex.get("reps"))
                data.append([ex.get("nom", ""), reps])
            col_widths = [250, 180]
        else:
            data = [["Exercice", "Séries", "Répétitions", "Repos"]]
            for ex in block.get("exercises", []):
                series, reps = self._split_series_reps(ex.get("reps"))
                rest = ex.get("repos_s")
                rest_str = f"{rest}s" if rest else ""
                data.append([ex.get("nom", ""), series, reps, rest_str])
            col_widths = [250, 60, 120, 60]

        table = Table(data, colWidths=col_widths)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(TABLE_HEADER_BG)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(TEXT)),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(NEUTRAL_700)),
        ]
        for i in range(1, len(data)):
            bg = TABLE_ROW_ODD_BG if i % 2 else TABLE_ROW_EVEN_BG
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(bg)))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.HexColor(TEXT)))
        table.setStyle(TableStyle(style))
        elems.append(table)
        elems.append(Spacer(1, 12))
        return elems

    @staticmethod
    def _split_series_reps(text: str | None) -> Tuple[str, str]:
        if not text:
            return "", ""
        parts = text.split("x", 1)
        if len(parts) == 2:
            series = parts[0].strip()
            reps = parts[1].strip()
        else:
            series = "1"
            reps = parts[0].strip()
        reps = reps.replace("reps", "").strip()
        return series, reps
