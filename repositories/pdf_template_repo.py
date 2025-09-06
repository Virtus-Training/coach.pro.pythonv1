from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from db.database_manager import db_manager


@dataclass
class PdfTemplate:
    id: int
    name: str
    type: str  # 'session' or 'nutrition'
    style: Dict[str, Any]
    is_default: bool
    updated_at: str


class PdfTemplateRepository:
    def list_by_type(self, t: str) -> List[PdfTemplate]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT id,name,type,style_json,is_default,updated_at FROM pdf_templates WHERE type = ? ORDER BY name",
                (t,),
            ).fetchall()
        out: List[PdfTemplate] = []
        for r in rows:
            try:
                style = json.loads(r["style_json"]) if r["style_json"] else {}
            except Exception:
                style = {}
            out.append(
                PdfTemplate(
                    id=r["id"],
                    name=r["name"],
                    type=r["type"],
                    style=style,
                    is_default=bool(r["is_default"]),
                    updated_at=r["updated_at"],
                )
            )
        return out

    def get_default(self, t: str) -> Optional[PdfTemplate]:
        with db_manager.get_connection() as conn:
            r = conn.execute(
                "SELECT id,name,type,style_json,is_default,updated_at FROM pdf_templates WHERE type = ? AND is_default = 1 LIMIT 1",
                (t,),
            ).fetchone()
        if not r:
            return None
        try:
            style = json.loads(r["style_json"]) if r["style_json"] else {}
        except Exception:
            style = {}
        return PdfTemplate(
            id=r["id"],
            name=r["name"],
            type=r["type"],
            style=style,
            is_default=bool(r["is_default"]),
            updated_at=r["updated_at"],
        )

    def get_by_id(self, template_id: int) -> Optional[PdfTemplate]:
        with db_manager.get_connection() as conn:
            r = conn.execute(
                "SELECT id,name,type,style_json,is_default,updated_at FROM pdf_templates WHERE id = ?",
                (template_id,),
            ).fetchone()
        if not r:
            return None
        try:
            style = json.loads(r["style_json"]) if r["style_json"] else {}
        except Exception:
            style = {}
        return PdfTemplate(
            id=r["id"],
            name=r["name"],
            type=r["type"],
            style=style,
            is_default=bool(r["is_default"]),
            updated_at=r["updated_at"],
        )

    def create(self, name: str, t: str, style: Dict[str, Any], is_default: bool = False) -> int:
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO pdf_templates(name, type, style_json, is_default) VALUES (?,?,?,?)",
                (name, t, json.dumps(style, ensure_ascii=False), 1 if is_default else 0),
            )
            if is_default:
                conn.execute(
                    "UPDATE pdf_templates SET is_default = 0 WHERE type = ? AND id != ?",
                    (t, cur.lastrowid),
                )
            conn.commit()
            return int(cur.lastrowid)

    def update(self, template_id: int, style: Dict[str, Any], is_default: Optional[bool] = None) -> None:
        with db_manager.get_connection() as conn:
            conn.execute(
                "UPDATE pdf_templates SET style_json = json(?), updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(style, ensure_ascii=False), template_id),
            )
            if is_default is not None:
                conn.execute("UPDATE pdf_templates SET is_default = ? WHERE id = ?", (1 if is_default else 0, template_id))
            conn.commit()

    def set_default(self, template_id: int, t: str) -> None:
        with db_manager.get_connection() as conn:
            conn.execute("UPDATE pdf_templates SET is_default = 0 WHERE type = ?", (t,))
            conn.execute("UPDATE pdf_templates SET is_default = 1 WHERE id = ?", (template_id,))
            conn.commit()

    def delete(self, template_id: int) -> None:
        with db_manager.get_connection() as conn:
            conn.execute("DELETE FROM pdf_templates WHERE id = ?", (template_id,))
            conn.commit()

