from typing import Dict

import customtkinter as ctk

from models.plan_alimentaire import Repas, RepasItem
from repositories.aliment_repo import AlimentRepository
from repositories.client_repo import ClientRepository
from repositories.fiche_nutrition_repo import FicheNutritionRepository
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository
from services.client_service import ClientService
from services.nutrition_service import NutritionService
from services.plan_alimentaire_service import PlanAlimentaireService
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle
from ui.components.food_search_bar import FoodSearchBar
from ui.components.meal_card import MealCard


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent, client_id: int):
        super().__init__(parent)
        self.client_id = client_id

        self.plan_repo = PlanAlimentaireRepository()
        self.plan_service = PlanAlimentaireService(self.plan_repo)
        self.aliment_repo = AlimentRepository()
        self.client_service = ClientService(ClientRepository())
        self.nutrition_service = NutritionService(FicheNutritionRepository())

        self.client = self.client_service.get_client_by_id(client_id)
        self.fiche = self.nutrition_service.get_last_sheet_for_client(client_id)
        self.plan = self.plan_service.get_or_create_plan_for_client(client_id)
        self.active_repas_id = self.plan.repas[0].id if self.plan.repas else None

        self.aliments = self.aliment_repo.list_all()
        self.aliments_by_id = {a.id: a for a in self.aliments}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        self._create_left_panel()
        self._create_center_panel()
        self._create_right_panel()
        self._refresh()

    # Left panel
    def _create_left_panel(self) -> None:
        self.left_card = Card(self)
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
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
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
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
        self.search_bar = FoodSearchBar(self, self._on_food_selected)
        self.search_bar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

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
        self.plan_repo.delete_item(item_id)
        self.plan = self.plan_repo.get_plan(self.plan.id)
        self._refresh()

    # Add item popup
    def _open_add_item_popup(self, aliment) -> None:
        portions = self.aliment_repo.get_portions_for_aliment(aliment.id)
        popup = ctk.CTkToplevel(self)
        popup.title(aliment.nom)
        popup.grab_set()

        gram_var = ctk.StringVar(value="100")
        gram_entry = ctk.CTkEntry(popup, textvariable=gram_var)
        gram_entry.pack(padx=10, pady=10)

        portion_names = [p.description for p in portions]
        portion_var = ctk.StringVar(value=portion_names[0])

        def on_portion_change(choice):
            idx = portion_names.index(choice)
            gram_var.set(str(portions[idx].grammes_equivalents))

        portion_menu = ctk.CTkOptionMenu(
            popup, values=portion_names, variable=portion_var, command=on_portion_change
        )
        portion_menu.pack(padx=10, pady=10)

        def add_action():
            try:
                grams = float(gram_var.get())
            except ValueError:
                grams = 0.0
            idx = portion_names.index(portion_var.get())
            portion = portions[idx]
            quantite = grams / portion.grammes_equivalents if portion.grammes_equivalents else 1.0
            item = RepasItem(
                id=0,
                repas_id=self.active_repas_id,
                aliment_id=aliment.id,
                portion_id=portion.id,
                quantite=quantite,
            )
            self.plan_repo.add_item(self.active_repas_id, item)
            self.plan = self.plan_repo.get_plan(self.plan.id)
            self._refresh()
            popup.destroy()

        ctk.CTkButton(popup, text="Ajouter", command=add_action).pack(pady=10)

    # Refresh UI
    def _refresh(self) -> None:
        for repas in self.plan.repas:
            items = []
            for item in repas.items:
                aliment = self.aliments_by_id.get(item.aliment_id)
                portion = self.aliment_repo.get_portion_by_id(item.portion_id)
                grams = (portion.grammes_equivalents * item.quantite) if portion else 0
                items.append({
                    "id": item.id,
                    "label": f"{aliment.nom} - {grams:.0f}g" if aliment else "?",
                })
            totals = self._compute_meal_totals(repas)
            card = self.meal_cards.get(repas.id)
            if card:
                card.update(items, totals)
                card.set_active(repas.id == self.active_repas_id)
        self._update_totals()

    def _compute_meal_totals(self, repas: Repas) -> Dict[str, float]:
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for item in repas.items:
            it = self.plan_repo.compute_item_totals(item)
            for k in totals:
                totals[k] += it[k]
        return totals

    def _update_totals(self) -> None:
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for repas in self.plan.repas:
            mt = self._compute_meal_totals(repas)
            for k in totals:
                totals[k] += mt[k]
        cible_kcal = self.fiche.objectif_kcal if self.fiche else 0
        cible_p = self.fiche.proteines_g if self.fiche else 0
        cible_g = self.fiche.glucides_g if self.fiche else 0
        cible_l = self.fiche.lipides_g if self.fiche else 0
        self.cal_lbl.configure(text=f"Calories: {totals['kcal']:.0f} / {cible_kcal}")
        self.prot_lbl.configure(text=f"Protéines: {totals['proteines']:.1f} / {cible_p}")
        self.carb_lbl.configure(text=f"Glucides: {totals['glucides']:.1f} / {cible_g}")
        self.fat_lbl.configure(text=f"Lipides: {totals['lipides']:.1f} / {cible_l}")
