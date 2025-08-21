"""Controller handling session preview generation and persistence."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from repositories.exercices_repo import ExerciseRepository
from services.session_generator import generate_collectif, generate_individuel
from services.session_service import SessionService


class SessionController:
    def __init__(self, session_service: SessionService) -> None:
        self.session_service = session_service

    def build_session_preview_dto(
        self, blocks: list[Any], exercises_by_id: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Map session blocks to a DTO consumable by the view."""
        blocks_out: list[Dict[str, Any]] = []
        for blk in blocks:
            title = (
                f"{blk.type} — {blk.duration_sec // 60}’" if blk.duration_sec else blk.type
            )
            block_dto = {
                "title": title,
                "format": blk.type,
                "duration": f"{blk.duration_sec // 60}’" if blk.duration_sec else "",
                "exercises": [],
            }
            for item in blk.items:
                meta = exercises_by_id.get(item.exercise_id, {})
                name = meta.get("name", f"Exercice #{item.exercise_id}")
                muscle = meta.get("primary_muscle", "")
                equip = " / ".join(meta.get("equipment", []))
                presc = item.prescription or {}
                reps = None
                if "reps" in presc:
                    reps = f"{presc['reps']} reps"
                elif "work_sec" in presc:
                    reps = f"{presc['work_sec']}s"
                exercise = {
                    "id": item.exercise_id,
                    "nom": name,
                    "reps": reps,
                    "repos_s": presc.get("rest_sec"),
                    "muscle": muscle,
                    "equip": equip,
                }
                block_dto["exercises"].append(exercise)
            blocks_out.append(block_dto)
        return {"blocks": blocks_out}

    def generate_session_preview(
        self, params: Dict[str, Any], mode: str = "collectif"
    ) -> Tuple[Any, Dict[str, Any]]:
        """Generate a collective session and its preview DTO."""
        if mode != "collectif":
            raise ValueError(f"Unknown mode: {mode}")
        svc_params = {
            "course_type": params.get("course_type"),
            "duration": int(params.get("duration", 0)),
            "intensity": params.get("intensity"),
            "equipment": params.get("equipment", []),
        }
        session = generate_collectif(svc_params)
        ids = [it.exercise_id for b in session.blocks for it in b.items]
        repo = ExerciseRepository()
        meta = repo.get_meta_by_ids(ids)
        dto = self.build_session_preview_dto(session.blocks, meta)
        dto["meta"] = {
            "title": session.label,
            "duration": f"{session.duration_sec // 60} min",
        }
        return session, dto

    def generate_individual_session(
        self, client_id: int, objectif: str, duree_minutes: int
    ) -> Tuple[Any, Dict[str, Any]]:
        session = generate_individuel(client_id, objectif, duree_minutes)
        ids = [it.exercise_id for b in session.blocks for it in b.items]
        repo = ExerciseRepository()
        meta = repo.get_meta_by_ids(ids)
        dto = self.build_session_preview_dto(session.blocks, meta)
        dto["meta"] = {
            "title": session.label,
            "goal": objectif,
            "duration": f"{session.duration_sec // 60} min",
        }
        return session, dto

    def save_session(self, session_dto: Dict[str, Any], client_id: int | None) -> None:
        """Persist a generated session from its DTO representation."""
        self.session_service.save_session_from_dto(session_dto, client_id)


__all__ = ["SessionController"]
