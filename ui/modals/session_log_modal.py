from typing import Callable, Dict, List

import customtkinter as ctk

from models.resultat_exercice import ResultatExercice
from models.seance import Seance
from repositories.exercices_repo import ExerciseRepository
from repositories.seance_repo import SeanceRepository
from ui.theme.colors import DARK_BG


class SessionLogModal(ctk.CTkToplevel):
    def __init__(
        self, parent, client_id: int, on_saved: Callable[[], None] | None = None
    ):
        super().__init__(parent)
        self.client_id = client_id
        self.on_saved = on_saved
        self.seance_repo = SeanceRepository()
        self.exercise_repo = ExerciseRepository()

        self.title("Enregistrer une séance")
        self.geometry("500x600")
        self.configure(fg_color=DARK_BG)
        self.resizable(False, False)

        self.title_var = ctk.StringVar()
        self.date_var = ctk.StringVar()

        self._build_form()
        self.exercise_entries: List[Dict] = []

    def _build_form(self):
        general = ctk.CTkFrame(self, fg_color="transparent")
        general.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(general, text="Titre de la séance").pack(anchor="w")
        ctk.CTkEntry(general, textvariable=self.title_var).pack(fill="x", pady=5)

        ctk.CTkLabel(general, text="Date (AAAA-MM-JJ)").pack(anchor="w")
        ctk.CTkEntry(general, textvariable=self.date_var).pack(fill="x", pady=5)

        ex_container = ctk.CTkFrame(self, fg_color="transparent")
        ex_container.pack(fill="both", expand=True, padx=20, pady=10)

        add_frame = ctk.CTkFrame(ex_container, fg_color="transparent")
        add_frame.pack(fill="x")

        exercices = self.exercise_repo.list_all_exercices()
        self.ex_map = {e.nom: e.id for e in exercices}
        values = list(self.ex_map.keys()) if self.ex_map else [""]
        self.option_var = ctk.StringVar(value=values[0] if values else "")
        ctk.CTkOptionMenu(add_frame, variable=self.option_var, values=values).pack(
            side="left", padx=(0, 10)
        )
        ctk.CTkButton(
            add_frame, text="Ajouter un exercice", command=self._add_exercise
        ).pack(side="left")

        self.ex_scroll = ctk.CTkScrollableFrame(ex_container, fg_color="transparent")
        self.ex_scroll.pack(fill="both", expand=True, pady=(10, 0))

        action = ctk.CTkFrame(self, fg_color="transparent")
        action.pack(pady=10)
        ctk.CTkButton(action, text="Enregistrer la séance", command=self._save).pack(
            side="left", padx=5
        )
        ctk.CTkButton(action, text="Annuler", command=self.destroy).pack(
            side="left", padx=5
        )

    def _add_exercise(self):
        name = self.option_var.get()
        if not name:
            return
        ex_id = self.ex_map[name]
        frame = ctk.CTkFrame(self.ex_scroll)
        frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(frame, text=name, width=150).grid(row=0, column=0, padx=5)
        series_var = ctk.StringVar()
        reps_var = ctk.StringVar()
        charge_var = ctk.StringVar()
        ctk.CTkEntry(
            frame, width=40, textvariable=series_var, placeholder_text="Séries"
        ).grid(row=0, column=1, padx=5)
        ctk.CTkEntry(
            frame, width=40, textvariable=reps_var, placeholder_text="Reps"
        ).grid(row=0, column=2, padx=5)
        ctk.CTkEntry(
            frame, width=60, textvariable=charge_var, placeholder_text="Charge"
        ).grid(row=0, column=3, padx=5)
        ctk.CTkButton(
            frame, text="X", width=20, command=lambda: self._remove_exercise(frame)
        ).grid(row=0, column=4, padx=5)

        self.exercise_entries.append(
            {
                "id": ex_id,
                "series": series_var,
                "reps": reps_var,
                "charge": charge_var,
                "frame": frame,
            }
        )

    def _remove_exercise(self, frame):
        for entry in list(self.exercise_entries):
            if entry["frame"] is frame:
                entry["frame"].destroy()
                self.exercise_entries.remove(entry)
                break

    def _save(self):
        seance = Seance(
            id=0,
            client_id=self.client_id,
            type_seance="manuel",
            titre=self.title_var.get(),
            date_creation=self.date_var.get(),
        )
        resultats: List[ResultatExercice] = []
        for e in self.exercise_entries:
            try:
                series = int(e["series"].get()) if e["series"].get() else None
            except ValueError:
                series = None
            try:
                reps = int(e["reps"].get()) if e["reps"].get() else None
            except ValueError:
                reps = None
            try:
                charge = float(e["charge"].get()) if e["charge"].get() else None
            except ValueError:
                charge = None
            resultats.append(
                ResultatExercice(
                    id=0,
                    seance_id=0,
                    exercice_id=e["id"],
                    series_effectuees=series,
                    reps_effectuees=reps,
                    charge_utilisee=charge,
                )
            )
        self.seance_repo.add_seance(seance, resultats)
        if self.on_saved:
            self.on_saved()
        self.destroy()
