import customtkinter as ctk

from repositories.client_repo import ClientRepository
from services.client_service import ClientService
from ui.components.design_system import PageTitle, SecondaryButton
from ui.pages.client_detail_page_components.anamnese_tab import AnamneseTab
from ui.pages.client_detail_page_components.fiche_nutrition_tab import (
    FicheNutritionTab,
)
from ui.pages.client_detail_page_components.stats_tab import StatsTab
from ui.pages.client_detail_page_components.suivi_tab import SuiviTab
from ui.theme.colors import NEUTRAL_900


class ClientDetailPage(ctk.CTkFrame):
    """Page affichant les détails d'un client."""

    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color=NEUTRAL_900)
        self.client_id = client_id
        self.client_service = ClientService(ClientRepository())
        client = self.client_service.get_client_by_id(client_id)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)

        SecondaryButton(
            header,
            text="< Retour",
            command=self.master.master.show_clients_page,
            width=100,
        ).pack(side="left")

        if client:
            title = f"{client.prenom} {client.nom}"
        else:
            title = "Client introuvable"

        PageTitle(header, text=title).pack(side="left", padx=20)

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        anam_tab = tabview.add("Anamnèse")
        if client:
            AnamneseTab(anam_tab, client).pack(
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
        FicheNutritionTab(fiche_tab, self.client_id).pack(
            fill="both", expand=True, padx=10, pady=10
        )
