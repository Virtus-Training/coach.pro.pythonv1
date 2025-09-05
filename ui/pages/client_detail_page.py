import customtkinter as ctk

from controllers.client_controller import ClientController
from controllers.nutrition_controller import NutritionController
from ui.components.design_system import HeroBanner, SecondaryButton
from ui.pages.client_detail_page_components.anamnese_tab import AnamneseTab
from ui.pages.client_detail_page_components.fiche_nutrition_tab import (
    FicheNutritionTab,
)
from ui.pages.client_detail_page_components.stats_tab import StatsTab
from ui.pages.client_detail_page_components.suivi_tab import SuiviTab


class ClientDetailPage(ctk.CTkFrame):
    """Page affichant les détails d'un client."""

    def __init__(
        self,
        master,
        controller: ClientController,
        nutrition_controller: NutritionController,
        client_id: int,
    ):
        super().__init__(
            master, fg_color=ctk.ThemeManager.theme["color"]["surface_dark"]
        )
        self.client_id = client_id
        self.controller = controller
        self.nutrition_controller = nutrition_controller
        client = self.controller.get_client_by_id(client_id)

        # Header with back button + hero
        back_bar = ctk.CTkFrame(self, fg_color="transparent")
        back_bar.pack(fill="x", padx=20, pady=(20, 0))
        SecondaryButton(
            back_bar,
            text="< Retour",
            command=self.master.master.show_clients_page,
            width=100,
        ).pack(side="left")

        title = (
            f"{client.prenom} {client.nom}" if client else "Client introuvable"
        )
        hero = HeroBanner(
            self,
            title=title,
            subtitle="Fiche client, suivi, statistiques et nutrition",
            icon_path="assets/icons/users.png",
        )
        hero.pack(fill="x", padx=20, pady=16)

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        anam_tab = tabview.add("Anamnèse")
        if client:
            AnamneseTab(anam_tab, self.controller, client).pack(
                fill="both", expand=True, padx=10, pady=10
            )
        suivi_tab = tabview.add("Suivi & Séances")
        SuiviTab(suivi_tab, self.client_id).pack(
            fill="both", expand=True, padx=10, pady=10
        )
        stats_tab = tabview.add("Progression & Stats")
        StatsTab(stats_tab, self.client_id).pack(
            fill="both", expand=True, padx=10, pady=10
        )
        fiche_tab = tabview.add("Fiche Nutrition")
        FicheNutritionTab(
            fiche_tab,
            self.controller,
            self.nutrition_controller,
            self.client_id,
        ).pack(fill="both", expand=True, padx=10, pady=10)
