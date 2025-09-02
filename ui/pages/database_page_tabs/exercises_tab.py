from __future__ import annotations

from typing import List, Optional

import tkinter as tk
import customtkinter as ctk

from models.exercices import Exercise
from repositories.exercices_repo import ExerciseRepository
from ui.components.design_system import LabeledInput


class ExerciseForm(ctk.CTkToplevel):
    """Formulaire d'exercice unique pour ajout et modification."""

    def __init__(self, master, on_submit, exercise: Optional[Exercise] = None) -> None:
        super().__init__(master, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])  # fallback if CTkToplevel not themed
        self.title("Exercice")
        self.geometry("520x520")
        self.resizable(False, False)
        self._on_submit = on_submit

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        self.in_nom = LabeledInput(frame, label="Nom")
        self.in_nom.pack(fill="x", pady=(0, 8))

        self.in_groupe = LabeledInput(frame, label="Groupe musculaire principal")
        self.in_groupe.pack(fill="x", pady=(0, 8))

        self.in_equip = LabeledInput(frame, label="Équipements (séparés par ,)")
        self.in_equip.pack(fill="x", pady=(0, 8))

        self.in_tags = LabeledInput(frame, label="Tags (séparés par ,)")
        self.in_tags.pack(fill="x", pady=(0, 8))

        self.in_pattern = LabeledInput(frame, label="Pattern (push/pull/squat/hinge/carry...)")
        self.in_pattern.pack(fill="x", pady=(0, 8))

        self.in_type = LabeledInput(frame, label="Type d'effort (Force/Cardio/Technique...)")
        self.in_type.pack(fill="x", pady=(0, 8))

        self.in_coeff = LabeledInput(frame, label="Coeff. volume (ex: 1.0)")
        self.in_coeff.pack(fill="x", pady=(0, 8))

        self.var_charge = ctk.BooleanVar(value=False)
        self.sw_charge = ctk.CTkSwitch(frame, text="Chargeable", variable=self.var_charge)
        self.sw_charge.pack(anchor="w", pady=(4, 12))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(btn_row, text="Annuler", command=self.destroy).pack(side="right")
        ctk.CTkButton(btn_row, text="Enregistrer", command=self._submit).pack(side="right", padx=(0, 8))

        if exercise:
            self.in_nom.set_value(exercise.nom)
            self.in_groupe.set_value(exercise.groupe_musculaire_principal)
            self.in_equip.set_value(exercise.equipement or "")
            self.in_tags.set_value(exercise.tags or "")
            self.in_pattern.set_value(exercise.movement_pattern or "")
            self.in_type.set_value(exercise.type_effort or "")
            self.in_coeff.set_value(str(exercise.coefficient_volume or 1.0))
            self.var_charge.set(bool(exercise.est_chargeable))

        self.lift()
        self.focus()

    def _submit(self) -> None:
        nom = self.in_nom.get_value()
        if not nom:
            self.in_nom.show_error("Nom requis")
            return
        try:
            coeff = float(self.in_coeff.get_value() or 1.0)
        except ValueError:
            self.in_coeff.show_error("Nombre invalide")
            return
        payload = {
            "nom": nom,
            "groupe": self.in_groupe.get_value(),
            "equip": self.in_equip.get_value() or None,
            "tags": self.in_tags.get_value() or None,
            "pattern": self.in_pattern.get_value() or None,
            "type_effort": self.in_type.get_value() or "",
            "coeff": coeff,
            "charge": bool(self.var_charge.get()),
        }
        self._on_submit(payload)
        self.destroy()


class _Listbox(ctk.CTkFrame):
    """Listbox à hautes performances pour grandes listes.

    Utilise tkinter.Listbox pour minimiser le nombre de widgets.
    """

    def __init__(self, master, on_select=None):
        super().__init__(master, fg_color="transparent")
        self.on_select = on_select

        colors = ctk.ThemeManager.theme["color"]
        bg = colors.get("surface_light", "#1F2937")
        fg = colors.get("primary_text", "#E5E7EB")
        sel_bg = ctk.ThemeManager.theme.get("DataTable", {}).get("row_hover_fg_color", "#374151")
        sel_fg = fg

        self._lb = tk.Listbox(
            self,
            activestyle="dotbox",
            exportselection=False,
            background=bg,
            foreground=fg,
            selectbackground=sel_bg,
            selectforeground=sel_fg,
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        self._lb.pack(fill="both", expand=True)
        self._lb.bind("<<ListboxSelect>>", self._on_select)

        # Backing store (text = key = exercise name)
        self._items_all: list[str] = []
        self._items_visible: list[str] = []

    def set_items(self, items: list[str]):
        self._items_all = list(items)
        self._items_visible = list(items)
        self._refresh()

    def _refresh(self):
        self._lb.delete(0, tk.END)
        for text in self._items_visible:
            self._lb.insert(tk.END, text)

    def filter(self, term: str):
        t = (term or "").strip().lower()
        if not t:
            self._items_visible = list(self._items_all)
        else:
            self._items_visible = [it for it in self._items_all if t in it.lower()]
        self._refresh()

    def current_key(self) -> Optional[str]:
        cur = self._lb.curselection()
        if not cur:
            return None
        idx = int(cur[0])
        if 0 <= idx < len(self._items_visible):
            return self._items_visible[idx]
        return None

    def _on_select(self, _e=None):
        if self.on_select:
            self.on_select(self.current_key())


class ExercisesTab(ctk.CTkFrame):
    """Version légère de l'onglet Exercices (ajout/suppression uniquement)."""

    def __init__(self, parent, repo: ExerciseRepository | None = None):
        super().__init__(parent, fg_color="transparent")
        self.repo = repo or ExerciseRepository()

        self.selected_name: Optional[str] = None
        self.colors = ctk.ThemeManager.theme["color"]
        self.fonts = ctk.ThemeManager.theme["font"]

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=12, pady=(12, 0))

        self.search_entry = ctk.CTkEntry(toolbar, placeholder_text="Rechercher un exercice...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.btn_add = ctk.CTkButton(toolbar, text="Ajouter", command=self._on_add)
        self.btn_add.pack(side="right", padx=(8, 0))
        self.btn_edit = ctk.CTkButton(toolbar, text="Modifier", command=self._on_edit, state="disabled")
        self.btn_edit.pack(side="right", padx=(8, 0))
        self.btn_del = ctk.CTkButton(toolbar, text="Supprimer", command=self._on_delete, state="disabled")
        self.btn_del.pack(side="right")

        # Body: list + helper
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=12, pady=(10, 12))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="Liste des exercices",
            font=ctk.CTkFont(**self.fonts["BodyBold"]) if "BodyBold" in self.fonts else ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors.get("primary_text", None),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.listbox = _Listbox(body, on_select=self._on_select)
        self.listbox.grid(row=1, column=0, sticky="nsew")

        self._load()

    # ------------------------------------------------------------------
    def _load(self) -> None:
        self.exercises: List[Exercise] = self.repo.list_all()
        # Only display names for compactness
        names: list[str] = [e.nom for e in self.exercises]
        self.listbox.set_items(names)
        self.selected_name = None
        self.btn_del.configure(state="disabled")
        self.btn_edit.configure(state="disabled")

    def _on_select(self, name: Optional[str]) -> None:
        self.selected_name = name
        state = ("normal" if name else "disabled")
        self.btn_del.configure(state=state)
        self.btn_edit.configure(state=state)

    def _on_search(self, _event=None):
        self.listbox.filter(self.search_entry.get())

    def _on_add(self) -> None:
        def handle_submit(payload: dict):
            e = Exercise(
                id=0,
                nom=payload["nom"],
                groupe_musculaire_principal=payload["groupe"],
                equipement=payload["equip"],
                tags=payload["tags"],
                movement_pattern=payload["pattern"],
                type_effort=payload["type_effort"],
                coefficient_volume=payload["coeff"],
                est_chargeable=payload["charge"],
            )
            self.repo.create(e)
            self._load()

        ExerciseForm(self, on_submit=handle_submit)

    def _on_edit(self) -> None:
        if not self.selected_name:
            return
        e = self.repo.get_by_name(self.selected_name)
        if not e:
            return

        def handle_submit(payload: dict):
            e.nom = payload["nom"]
            e.groupe_musculaire_principal = payload["groupe"]
            e.equipement = payload["equip"]
            e.tags = payload["tags"]
            e.movement_pattern = payload["pattern"]
            e.type_effort = payload["type_effort"]
            e.coefficient_volume = payload["coeff"]
            e.est_chargeable = payload["charge"]
            self.repo.update(e)
            self._load()

        ExerciseForm(self, on_submit=handle_submit, exercise=e)

    def _on_delete(self) -> None:
        if not self.selected_name:
            return
        e = self.repo.get_by_name(self.selected_name)
        if not e:
            return
        # Confirmation
        confirm = ctk.CTkToplevel(self, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])  # fallback if CTkToplevel not themed
        confirm.title("Confirmer la suppression")
        ctk.CTkLabel(confirm, text=f"Supprimer '{e.nom}' ?").pack(padx=16, pady=16)
        row = ctk.CTkFrame(confirm, fg_color="transparent")
        row.pack(pady=(0, 12))

        def do_del():
            self.repo.delete(int(e.id))
            confirm.destroy()
            self._load()

        ctk.CTkButton(row, text="Annuler", command=confirm.destroy).pack(side="left", padx=8)
        ctk.CTkButton(row, text="Supprimer", fg_color="#B00020", hover_color="#8E001A", command=do_del).pack(side="left")
