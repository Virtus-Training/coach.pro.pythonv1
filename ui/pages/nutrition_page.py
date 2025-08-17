from typing import Dict, Optional

import customtkinter as ctk

from models.plan_alimentaire import PlanAlimentaire, Repas, RepasItem
from repositories.aliment_repo import AlimentRepository
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository
from ui.theme.colors import PRIMARY


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.plan_repo = PlanAlimentaireRepository()
        self.aliment_repo = AlimentRepository()
        self.selected_plan: Optional[PlanAlimentaire] = None
        self.active_repas_id: Optional[int] = None
        self.aliments = self.aliment_repo.list_all()
        self.aliments_by_id = {a.id: a for a in self.aliments}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        self._create_left_panel()
        self._create_center_panel()
        self._create_right_panel()
        self._load_plans_list()

    # ----- Left panel -----
    def _create_left_panel(self) -> None:
        self.plans_frame = ctk.CTkScrollableFrame(self)
        self.plans_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        add_btn = ctk.CTkButton(
            self.plans_frame, text="+", width=40, command=self._create_plan
        )
        add_btn.pack(pady=5)

    def _load_plans_list(self) -> None:
        for widget in self.plans_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") != "+":
                widget.destroy()
        plans = self.plan_repo.list_plans()
        for p in plans:
            btn = ctk.CTkButton(
                self.plans_frame,
                text=p.nom,
                anchor="w",
                command=lambda pid=p.id: self._load_plan(pid),
            )
            btn.pack(fill="x", padx=5, pady=2)

    def _create_plan(self) -> None:
        new_plan = PlanAlimentaire(id=0, nom="Nouveau plan")
        plan_id = self.plan_repo.create_plan(new_plan)
        self._load_plans_list()
        self._load_plan(plan_id)

    # ----- Center panel -----
    def _create_center_panel(self) -> None:
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.editor_frame.columnconfigure(0, weight=1)

        self.name_entry = ctk.CTkEntry(self.editor_frame)
        self.name_entry.grid(row=0, column=0, sticky="ew", pady=(5, 0), padx=5)
        self.name_entry.bind("<FocusOut>", lambda e: self._save_plan())

        self.desc_text = ctk.CTkTextbox(self.editor_frame, height=80)
        self.desc_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.desc_text.bind("<FocusOut>", lambda e: self._save_plan())

        self.totals_label = ctk.CTkLabel(self.editor_frame, text="Totaux: 0 kcal")
        self.totals_label.grid(row=2, column=0, sticky="w", padx=5)

        self.meals_frame = ctk.CTkScrollableFrame(self.editor_frame)
        self.meals_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.editor_frame.rowconfigure(3, weight=1)

        self.add_meal_btn = ctk.CTkButton(
            self.editor_frame, text="Ajouter un repas", command=self._add_meal
        )
        self.add_meal_btn.grid(row=4, column=0, pady=5)

    def _load_plan(self, plan_id: int) -> None:
        self.selected_plan = self.plan_repo.get_plan(plan_id)
        self.active_repas_id = None
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.selected_plan.nom)
        self.desc_text.delete("1.0", "end")
        if self.selected_plan.description:
            self.desc_text.insert("1.0", self.selected_plan.description)
        self._refresh_meals()
        self._update_totals()

    def _save_plan(self) -> None:
        if not self.selected_plan:
            return
        self.selected_plan.nom = self.name_entry.get()
        self.selected_plan.description = self.desc_text.get("1.0", "end").strip()
        self.plan_repo.update_plan(self.selected_plan)
        self._load_plans_list()

    def _refresh_meals(self) -> None:
        for widget in self.meals_frame.winfo_children():
            widget.destroy()
        if not self.selected_plan:
            return
        for repas in self.selected_plan.repas:
            self._create_meal_card(repas)

    def _create_meal_card(self, repas: Repas) -> None:
        frame = ctk.CTkFrame(self.meals_frame, border_width=2)
        frame.pack(fill="x", pady=5, padx=5)
        frame.bind(
            "<Button-1>", lambda e, rid=repas.id: self._set_active_meal(rid, frame)
        )

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x")
        name_lbl = ctk.CTkLabel(header, text=repas.nom)
        name_lbl.pack(side="left", padx=5)
        totals = self._compute_meal_totals(repas)
        totals_lbl = ctk.CTkLabel(
            header,
            text=f"{totals['kcal']:.0f} kcal P{totals['proteines']:.1f} G{totals['glucides']:.1f} L{totals['lipides']:.1f}",
        )
        totals_lbl.pack(side="left", padx=5)
        add_btn = ctk.CTkButton(
            header,
            text="+",
            width=30,
            command=lambda rid=repas.id: self._set_active_meal(rid, frame),
        )
        add_btn.pack(side="right", padx=5)

        items_frame = ctk.CTkFrame(frame, fg_color="transparent")
        items_frame.pack(fill="x", padx=10, pady=5)
        for item in repas.items:
            aliment = self.aliments_by_id.get(item.aliment_id)
            portion = self.aliment_repo.get_portion_by_id(item.portion_id)
            desc = portion.description if portion else "?"
            item_lbl = ctk.CTkLabel(
                items_frame,
                text=f"{aliment.nom} - {desc} x{item.quantite}",
                anchor="w",
            )
            item_lbl.pack(fill="x")

    def _set_active_meal(self, repas_id: int, frame: ctk.CTkFrame) -> None:
        self.active_repas_id = repas_id
        for child in self.meals_frame.winfo_children():
            child.configure(border_color=self.meals_frame.cget("fg_color"))
        frame.configure(border_color=PRIMARY)

    def _add_meal(self) -> None:
        if not self.selected_plan:
            return
        repas = Repas(
            id=0,
            plan_id=self.selected_plan.id,
            nom="Nouveau repas",
            ordre=len(self.selected_plan.repas),
        )
        self.plan_repo.add_repas(self.selected_plan.id, repas)
        self._load_plan(self.selected_plan.id)

    # ----- Right panel -----
    def _create_right_panel(self) -> None:
        self.library_frame = ctk.CTkFrame(self)
        self.library_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.library_frame.columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.library_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.search_var.trace_add("write", lambda *args: self._update_library())

        self.results_frame = ctk.CTkScrollableFrame(self.library_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.library_frame.rowconfigure(1, weight=1)
        self._update_library()

    def _update_library(self) -> None:
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        query = self.search_var.get().lower()
        for aliment in self.aliments:
            if query and query not in aliment.nom.lower():
                continue
            btn = ctk.CTkButton(
                self.results_frame,
                text=aliment.nom,
                anchor="w",
                command=lambda a=aliment: self._open_add_item_popup(a),
            )
            btn.pack(fill="x", padx=5, pady=2)

    def _open_add_item_popup(self, aliment) -> None:
        if self.active_repas_id is None:
            return
        portions = self.aliment_repo.get_portions_for_aliment(aliment.id)
        popup = ctk.CTkToplevel(self)
        popup.title(aliment.nom)
        popup.grab_set()

        portion_var = ctk.StringVar(value=str(portions[0].id))
        portion_menu = ctk.CTkOptionMenu(
            popup,
            values=[f"{p.description} ({p.grammes_equivalents}g)" for p in portions],
            variable=portion_var,
        )
        portion_menu.pack(padx=10, pady=10)

        qty_entry = ctk.CTkEntry(popup)
        qty_entry.insert(0, "1.0")
        qty_entry.pack(padx=10, pady=10)

        def add_action():
            try:
                qty = float(qty_entry.get())
            except ValueError:
                qty = 1.0
            portion = portions[portion_menu._current_index]
            item = RepasItem(
                id=0,
                repas_id=self.active_repas_id,
                aliment_id=aliment.id,
                portion_id=portion.id,
                quantite=qty,
            )
            self.plan_repo.add_item(self.active_repas_id, item)
            self._load_plan(self.selected_plan.id)
            popup.destroy()

        add_btn = ctk.CTkButton(popup, text="Ajouter", command=add_action)
        add_btn.pack(pady=10)

    # ----- Totals -----

    def _compute_meal_totals(self, repas: Repas) -> Dict[str, float]:
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for item in repas.items:
            it = self.plan_repo.compute_item_totals(item)
            for k in totals:
                totals[k] += it[k]
        return totals

    def _update_totals(self) -> None:
        if not self.selected_plan:
            self.totals_label.configure(text="Totaux: 0 kcal")
            return
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for repas in self.selected_plan.repas:
            mt = self._compute_meal_totals(repas)
            for k in totals:
                totals[k] += mt[k]
        self.totals_label.configure(
            text=(
                f"Totaux: {totals['kcal']:.0f} kcal "
                f"P{totals['proteines']:.1f} "
                f"G{totals['glucides']:.1f} "
                f"L{totals['lipides']:.1f}"
            )
        )
