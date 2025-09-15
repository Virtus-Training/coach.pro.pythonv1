"""Controller handling session preview generation and persistence."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from models.session import Session
from services.client_service import ClientService
from services.exercise_service import ExerciseService
from services.pdf_generator import (
    generate_session_pdf,
    generate_session_pdf_with_style,
)
from services.pdf_template_service import PdfTemplateService
from services.session_generator import generate_collectif, generate_individuel
from services.session_service import SessionService
from services.smart_workout_generator import SmartWorkoutGenerator
from services.workout_config_service import WorkoutConfigService


class SessionController:
    def __init__(
        self,
        session_service: SessionService,
        client_service: ClientService,
        exercise_service: ExerciseService,
    ) -> None:
        self.session_service = session_service
        self.client_service = client_service
        self.exercise_service = exercise_service

        # Initialiser les services smart
        self.config_service = WorkoutConfigService()
        self.smart_generator = SmartWorkoutGenerator(exercise_service, self.config_service)

    def build_session_preview_dto(
        self, blocks: list[Any], exercises_by_id: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Map session blocks to a DTO consumable by the view."""
        blocks_out: list[Dict[str, Any]] = []
        for blk in blocks:
            # Build block title with format, duration, and rounds
            title_parts = [blk.type]
            duration_txt = ""

            # Ajouter le nombre de tours (sauf pour AMRAP)
            if hasattr(blk, 'rounds') and blk.rounds and blk.rounds > 0 and blk.type.upper() != "AMRAP":
                title_parts.append(f"{blk.rounds} tours")

            # Ajouter la durée en minutes
            if getattr(blk, "duration_sec", None):
                mins = blk.duration_sec // 60
                title_parts.append(f"{mins} min")
                duration_txt = f"{mins} min"

            title = " · ".join(title_parts)

            block_dto = {
                "title": title,
                "format": blk.type,
                "duration": duration_txt,
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
            "duration": int(params.get("duration", 0)),
            "equipment": params.get("equipment", []),
            "variability": int(params.get("variability", 0)),
            "volume": int(params.get("volume", 0)),
            "enabled_formats": params.get("formats", []),
            "continuum": int(params.get("continuum", 0)),
            "focus": params.get("focus"),
            "objective": params.get("objective"),
            "auto_include": params.get("auto_include", []),
            "course_type": params.get("course_type", "Cross-Training"),
            "intensity": params.get("intensity", "Moyenne"),
            "custom_blocks": params.get("custom_blocks"),  # Ajouter les blocs personnalisés
        }
        # Utiliser le générateur intelligent avec fallback vers l'ancien
        try:
            session = self.smart_generator.generate_collectif_smart(svc_params)
        except Exception as e:
            # Fallback vers l'ancien générateur en cas d'erreur
            print(f"Smart generator failed, fallback to basic: {e}")
            session = generate_collectif(svc_params)
        ids = [it.exercise_id for b in session.blocks for it in b.items]
        meta = self.exercise_service.get_meta_by_ids(ids)
        dto = self.build_session_preview_dto(session.blocks, meta)
        dto["meta"] = {
            "title": session.label,
            "duration": f"{session.duration_sec // 60} min",
            "course_type": svc_params.get("course_type"),
            "intensity": svc_params.get("intensity"),
            "smart_generated": hasattr(session, '_smart_generated'),
        }
        return session, dto

    def generate_individual_session(
        self, client_id: int, objectif: str, duree_minutes: int
    ) -> Tuple[Any, Dict[str, Any]]:
        session = generate_individuel(client_id, objectif, duree_minutes)
        ids = [it.exercise_id for b in session.blocks for it in b.items]
        meta = self.exercise_service.get_meta_by_ids(ids)
        dto = self.build_session_preview_dto(session.blocks, meta)
        dto["meta"] = {
            "title": session.label,
            "goal": objectif,
            "duration": f"{session.duration_sec // 60} min",
        }
        return session, dto

    def build_preview_from_session(self, session: Session) -> Dict[str, Any]:
        ids = [it.exercise_id for b in session.blocks for it in b.items]
        meta = self.exercise_service.get_meta_by_ids(ids)
        dto = self.build_session_preview_dto(session.blocks, meta)
        dto["meta"] = {
            "title": session.label,
            "duration": f"{session.duration_sec // 60} min",
            "smart_generated": hasattr(session, '_smart_generated'),
        }
        return dto

    def save_session(self, session_dto: Dict[str, Any], client_id: int | None) -> None:
        """Persist a generated session from its DTO representation."""
        self.session_service.save_session_from_dto(session_dto, client_id)

    def get_workout_config_service(self) -> WorkoutConfigService:
        """Expose le service de configuration pour l'UI des paramètres."""
        return self.config_service

    def export_session_to_pdf(
        self, session_dto: Dict[str, Any], client_id: int | None, file_path: str
    ) -> None:
        client_name: str | None = None
        if client_id is not None:
            client = self.client_service.get_client_by_id(client_id)
            if client:
                client_name = f"{client.prenom} {client.nom}"
        try:
            style = PdfTemplateService().get_session_style()
            generate_session_pdf_with_style(session_dto, client_name, file_path, style)
        except Exception:
            generate_session_pdf(session_dto, client_name, file_path)


__all__ = ["SessionController"]
