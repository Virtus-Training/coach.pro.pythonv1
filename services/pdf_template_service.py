from __future__ import annotations

from typing import Any, Dict, List, Optional

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

# --- Extensions for multiple template families ------------------------------

# Basic defaults for other families (kept simple for now)
DEFAULT_NUTRITION_STYLE: Dict[str, Any] = {
    "logo_width": 70,
    "colors": {
        "header_bg": "#374151",
        "row_odd_bg": "#1F2937",
        "row_even_bg": "#111827",
        "grid": "#374151",
        "text": "#E5E7EB",
    },
}

DEFAULT_MEALPLAN_STYLE: Dict[str, Any] = DEFAULT_NUTRITION_STYLE
DEFAULT_PROGRAM_STYLE: Dict[str, Any] = DEFAULT_SESSION_STYLE


def _default_for(t: str) -> Dict[str, Any]:
    return {
        "session": DEFAULT_SESSION_STYLE,
        "nutrition": DEFAULT_NUTRITION_STYLE,
        "meal_plan": DEFAULT_MEALPLAN_STYLE,
        "program": DEFAULT_PROGRAM_STYLE,
    }.get(t, {})


class PdfTemplateService(PdfTemplateService):  # type: ignore[misc]
    def ensure_all_defaults_exist(self) -> None:
        if not self.repo.get_default("session"):
            self.repo.create("Par défaut (Séance)", "session", DEFAULT_SESSION_STYLE, is_default=True)
        if not self.repo.get_default("nutrition"):
            self.repo.create("Par défaut (Fiche nutrition)", "nutrition", DEFAULT_NUTRITION_STYLE, is_default=True)
        if not self.repo.get_default("meal_plan"):
            self.repo.create("Par défaut (Plan alimentaire)", "meal_plan", DEFAULT_MEALPLAN_STYLE, is_default=True)
        if not self.repo.get_default("program"):
            self.repo.create("Par défaut (Programme)", "program", DEFAULT_PROGRAM_STYLE, is_default=True)

    def list_templates(self, t: str) -> List[dict]:
        return [
            {
                "id": x.id,
                "name": x.name,
                "is_default": x.is_default,
                "updated_at": x.updated_at,
            }
            for x in self.repo.list_by_type(t)
        ]

    def get_style(self, t: str, template_id: Optional[int] = None) -> Dict[str, Any]:
        if template_id is not None:
            tpl = self.repo.get_by_id(template_id)
            if tpl:
                return tpl.style or _default_for(t)
        tpl = self.repo.get_default(t)
        return (tpl.style if tpl else None) or _default_for(t)

    def save_template(
        self,
        t: str,
        name: str,
        style: Dict[str, Any],
        template_id: Optional[int] = None,
        set_default: bool = False,
    ) -> int:
        if template_id:
            self.repo.update(template_id, style, is_default=set_default)
            if set_default:
                self.repo.set_default(template_id, t)
            return template_id
        tpl_id = self.repo.create(name, t, style, is_default=set_default)
        if set_default:
            self.repo.set_default(tpl_id, t)
        return tpl_id

