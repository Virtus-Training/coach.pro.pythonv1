from __future__ import annotations

import json
from typing import Any, Dict, Optional

from repositories.pdf_template_repo import PdfTemplateRepository


DEFAULT_SESSION_STYLE: Dict[str, Any] = {
    "logo_width": 70,
    "colors": {
        "table_header_bg": "#374151",
        "table_row_odd_bg": "#1F2937",
        "table_row_even_bg": "#111827",
        "table_grid": "#374151",
        "table_text": "#E5E7EB",
    },
    "column_widths": {
        "TABATA": [310, 180],
        "AMRAP": [250, 180],
        "EMOM": [250, 180],
        "FORTIME": [250, 180],
        "DEFAULT": [250, 60, 120, 60],
    },
}


class PdfTemplateService:
    def __init__(self, repo: Optional[PdfTemplateRepository] = None) -> None:
        self.repo = repo or PdfTemplateRepository()

    def ensure_default_exists(self) -> None:
        # Ensure at least one default session template exists
        tpl = self.repo.get_default("session")
        if not tpl:
            self.repo.create("Par défaut (Séance)", "session", DEFAULT_SESSION_STYLE, is_default=True)

    def list_session_templates(self) -> list[dict]:
        return [
            {
                "id": t.id,
                "name": t.name,
                "is_default": t.is_default,
                "updated_at": t.updated_at,
            }
            for t in self.repo.list_by_type("session")
        ]

    def get_session_style(self, template_id: Optional[int] = None) -> Dict[str, Any]:
        if template_id is not None:
            tpl = self.repo.get_by_id(template_id)
            if tpl:
                return tpl.style or DEFAULT_SESSION_STYLE
        tpl = self.repo.get_default("session")
        return (tpl.style if tpl else None) or DEFAULT_SESSION_STYLE

    def save_session_template(self, name: str, style: Dict[str, Any], template_id: Optional[int] = None, set_default: bool = False) -> int:
        if template_id:
            self.repo.update(template_id, style, is_default=set_default)
            if set_default:
                self.repo.set_default(template_id, "session")
            return template_id
        tpl_id = self.repo.create(name, "session", style, is_default=set_default)
        if set_default:
            self.repo.set_default(tpl_id, "session")
        return tpl_id

    def delete_template(self, template_id: int) -> None:
        self.repo.delete(template_id)

