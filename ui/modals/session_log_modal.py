from __future__ import annotations

from typing import Any, Dict, List

import customtkinter as ctk

from controllers.tracking_controller import TrackingController
from ui.modals.base_modal import BaseFormModal


class _ExercisesResultsField(ctk.CTkScrollableFrame):
    """Custom field listing exercises with inputs for results."""

    def __init__(self, master, exercises: List[Dict[str, Any]]):
        super().__init__(master, fg_color="transparent")
        self.entries: List[Dict[str, Any]] = []
        for ex in exercises:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=ex["name"], width=150, anchor="w").pack(
                side="left", padx=(0, 10)
            )
            poids = ctk.CTkEntry(row, width=60, placeholder_text="Poids")
            poids.pack(side="left", padx=5)
            reps = ctk.CTkEntry(row, width=60, placeholder_text="Répétitions")
            reps.pack(side="left", padx=5)
            rpe = ctk.CTkEntry(row, width=40, placeholder_text="RPE")
            rpe.pack(side="left", padx=5)
            series = ctk.CTkEntry(row, width=40, placeholder_text="Séries")
            series.pack(side="left", padx=5)

            res = ex.get("result", {})
            if res.get("poids") is not None:
                poids.insert(0, str(res["poids"]))
            if res.get("repetitions") is not None:
                reps.insert(0, str(res["repetitions"]))
            if res.get("rpe") is not None:
                rpe.insert(0, str(res["rpe"]))
            if res.get("series_effectuees") is not None:
                series.insert(0, str(res["series_effectuees"]))

            self.entries.append(
                {
                    "exercise_id": ex["id"],
                    "poids": poids,
                    "repetitions": reps,
                    "rpe": rpe,
                    "series": series,
                }
            )

    # Methods expected by BaseFormModal
    def get_value(self) -> List[Dict[str, Any]]:  # type: ignore[override]
        out: List[Dict[str, Any]] = []
        for item in self.entries:

            def _parse(entry, typ):
                value = entry.get().strip()
                if not value:
                    return None
                try:
                    return typ(value)
                except ValueError:
                    return None

            out.append(
                {
                    "exercise_id": item["exercise_id"],
                    "poids": _parse(item["poids"], float),
                    "repetitions": _parse(item["repetitions"], int),
                    "rpe": _parse(item["rpe"], int),
                    "series_effectuees": _parse(item["series"], int),
                }
            )
        return out

    def set_value(self, value: Any) -> None:  # type: ignore[override]
        pass

    def show_error(self, message: str) -> None:  # type: ignore[override]
        pass

    def hide_error(self) -> None:  # type: ignore[override]
        pass


class SessionLogModal(BaseFormModal):
    def __init__(
        self, parent, session_id: str, tracking_controller: TrackingController
    ) -> None:
        self.session_id = session_id
        self.controller = tracking_controller
        data = self.controller.get_session_for_logging(session_id)
        session = data.get("session")
        exercises = data.get("exercises", [])
        title = f"Résultats – {session.label}" if session else "Résultats"
        super().__init__(
            parent,
            title=title,
            form_fields={
                "results": lambda master: _ExercisesResultsField(master, exercises)
            },
            save_callback=self._on_save,
        )
        self.geometry("600x400")

    def _on_save(self, form_data: Dict[str, Any]) -> None:
        results = form_data.get("results", [])
        self.controller.save_session_results(self.session_id, results)
