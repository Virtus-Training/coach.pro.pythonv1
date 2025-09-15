from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from services.pdf_generator import generate_session_pdf_with_style
from services.pdf_template_service import PdfTemplateService


class PdfTemplateController:
    def __init__(self, service: Optional[PdfTemplateService] = None) -> None:
        self.service = service or PdfTemplateService()
        # Ensure at least a default exists
        try:
            self.service.ensure_default_exists()
        except Exception:
            pass

    def list_session_templates(self) -> List[Dict[str, Any]]:
        return self.service.list_session_templates()

    # Generic families --------------------------------------------------------
    def list_templates(self, t: str) -> List[Dict[str, Any]]:
        try:
            return self.service.list_templates(t)
        except Exception:
            return []

    def get_session_style(self, template_id: Optional[int] = None) -> Dict[str, Any]:
        return self.service.get_session_style(template_id)

    def get_style(self, t: str, template_id: Optional[int] = None) -> Dict[str, Any]:
        return self.service.get_style(t, template_id)

    def save_session_template(
        self,
        name: str,
        style_json: str,
        template_id: Optional[int] = None,
        set_default: bool = False,
    ) -> int:
        style = json.loads(style_json)
        return self.service.save_session_template(name, style, template_id, set_default)

    def save_template(
        self,
        t: str,
        name: str,
        style_json: str,
        template_id: Optional[int] = None,
        set_default: bool = False,
    ) -> int:
        style = json.loads(style_json)
        return self.service.save_template(t, name, style, template_id, set_default)

    def delete_template(self, template_id: int) -> None:
        self.service.delete_template(template_id)

    def export_preview(
        self, session_dto: dict, file_path: str, template_id: Optional[int] = None
    ) -> None:
        style = self.get_session_style(template_id)
        generate_session_pdf_with_style(session_dto, None, file_path, style)


__all__ = ["PdfTemplateController"]
