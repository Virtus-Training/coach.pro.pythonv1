from typing import Dict

import customtkinter as ctk
from tkinter import filedialog

from controllers.nutrition_controller import NutritionController
from dtos.nutrition_dtos import NutritionPageDTO, PlanAlimentaireDTO
from ui.components.design_system import Card, CardTitle, PrimaryButton
from ui.components.food_search_bar import FoodSearchBar
from ui.components.meal_card import MealCard


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent, controller: NutritionController, client_id: int):
        super().__init__(parent)
        self.controller = controller
        self.client_id = client_id

        data = self.controller.get_nutrition_page_data(client_id)
        self.client = data.client
        self.fiche = data.fiche
        self.plan: PlanAlimentaireDTO = data.plan
        self.active_repas_id = self.plan.repas[0].id if self.plan.repas else None

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        self._create_top_bar()
        self._create_left_panel()
        self._create_center_panel()
        self._create_right_panel()
        self._refresh()

    # Left panel
    def _create_left_panel(self) -> None:
        self.left_card = Card(self)
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        name = f"{self.client.prenom} {self.client.nom}" if self.client else "Client"
        CardTitle(self.left_card, text=name).pack(padx=10, pady=(10, 5))
        self.cal_lbl = ctk.CTkLabel(self.left_card, text="Calories: 0 / 0")
        self.prot_lbl = ctk.CTkLabel(self.left_card, text="Protéines: 0 / 0")
        self.carb_lbl = ctk.CTkLabel(self.left_card, text="Glucides: 0 / 0")
        self.fat_lbl = ctk.CTkLabel(self.left_card, text="Lipides: 0 / 0")
        for lbl in [self.cal_lbl, self.prot_lbl, self.carb_lbl, self.fat_lbl]:
            lbl.pack(anchor="w", padx=10)

    # Center panel
    def _create_center_panel(self) -> None:
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.center_frame.columnconfigure(0, weight=1)
        self.meal_cards: Dict[int, MealCard] = {}
        for repas in self.plan.repas:
            card = MealCard(
                self.center_frame,
                repas.nom,
                on_select=lambda rid=repas.id: self._set_active_meal(rid),
                on_delete_item=self._delete_item,
            )
            card.pack(fill="x", pady=5)
            self.meal_cards[repas.id] = card

    # Right panel
    def _create_right_panel(self) -> None:
        self.search_bar = FoodSearchBar(
            self, self.controller, self._on_food_selected
        )
        self.search_bar.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

    def _create_top_bar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, columnspan=3, sticky="e", padx=5, pady=5)
        PrimaryButton(bar, text="Exporter en PDF", command=self._export_pdf).pack(
            anchor="e"
        )

    # Callbacks
    def _set_active_meal(self, repas_id: int) -> None:
        self.active_repas_id = repas_id
        for rid, card in self.meal_cards.items():
            card.set_active(rid == repas_id)

    def _on_food_selected(self, aliment) -> None:
        if self.active_repas_id is None:
            return
        self._open_add_item_popup(aliment)

    def _delete_item(self, item_id: int) -> None:
        self.plan = self.controller.delete_item_from_repas(item_id)
        self._refresh()

    # Add item popup
    def _open_add_item_popup(self, aliment) -> None:
        portions = self.controller.get_portions_for_aliment(aliment.id)
        popup = ctk.CTkToplevel(self)
        popup.title(aliment.nom)
        popup.grab_set()

        gram_var = ctk.StringVar(value="100")
        gram_entry = ctk.CTkEntry(popup, textvariable=gram_var)
        gram_entry.pack(padx=10, pady=10)

        portion_names = [p.description for p in portions]
        portion_var = ctk.StringVar(value=portion_names[0] if portion_names else "")

        def on_portion_change(choice):
            idx = portion_names.index(choice)
            gram_var.set(str(portions[idx].grammes_equivalents))

        if portion_names:
            portion_menu = ctk.CTkOptionMenu(
                popup, values=portion_names, variable=portion_var, command=on_portion_change
            )
            portion_menu.pack(padx=10, pady=10)

        def add_action():
            try:
                grams = float(gram_var.get())
            except ValueError:
                grams = 0.0
            self.plan = self.controller.add_aliment_to_repas(
                self.active_repas_id, aliment.id, grams
            )
            self._refresh()
            popup.destroy()

        ctk.CTkButton(popup, text="Ajouter", command=add_action).pack(pady=10)

    def _export_pdf(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if path:
            dto = NutritionPageDTO(client=self.client, fiche=self.fiche, plan=self.plan)
            self.controller.export_plan_to_pdf(dto, path)

    # Refresh UI
    def _refresh(self) -> None:
        for repas in self.plan.repas:
            items = [
                {
                    "id": item.id,
                    "label": f"{item.nom} - {item.quantite:.0f}{item.unite}",
                }
                for item in repas.items
            ]
            totals = {
                "kcal": repas.totals_kcal,
                "proteines": repas.totals_proteines,
                "glucides": repas.totals_glucides,
                "lipides": repas.totals_lipides,
            }
            card = self.meal_cards.get(repas.id)
            if card:
                card.update(items, totals)
                card.set_active(repas.id == self.active_repas_id)
        self._update_totals()

    def _update_totals(self) -> None:
        totals = {
            "kcal": self.plan.totals_kcal,
            "proteines": self.plan.totals_proteines,
            "glucides": self.plan.totals_glucides,
            "lipides": self.plan.totals_lipides,
        }
        cible_kcal = self.fiche.objectif_kcal if self.fiche else 0
        cible_p = self.fiche.proteines_g if self.fiche else 0
        cible_g = self.fiche.glucides_g if self.fiche else 0
        cible_l = self.fiche.lipides_g if self.fiche else 0
        self.cal_lbl.configure(text=f"Calories: {totals['kcal']:.0f} / {cible_kcal}")
        self.prot_lbl.configure(
            text=f"Protéines: {totals['proteines']:.1f} / {cible_p}"
        )
        self.carb_lbl.configure(
            text=f"Glucides: {totals['glucides']:.1f} / {cible_g}"
        )
        self.fat_lbl.configure(text=f"Lipides: {totals['lipides']:.1f} / {cible_l}")
