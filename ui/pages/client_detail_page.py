import customtkinter as ctk

from repositories.client_repo import ClientRepository
from ui.theme.fonts import get_title_font
from ui.theme.colors import DARK_BG, TEXT
from ui.pages.client_detail_page_components.anamnese_tab import AnamneseTab


class ClientDetailPage(ctk.CTkFrame):
    """Page affichant les détails d'un client."""

    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color=DARK_BG)
        self.client_id = client_id
        repo = ClientRepository()
        client = repo.find_by_id(client_id)

        ctk.CTkButton(
            self,
            text="< Retour",
            command=self.master.master.show_clients_page,
            width=100,
        ).pack(anchor="w", padx=20, pady=(20, 10))

        if client:
            title = f"{client.prenom} {client.nom}"
        else:
            title = "Client introuvable"

        ctk.CTkLabel(
            self,
            text=title,
            font=get_title_font(),
            text_color=TEXT,
        ).pack(anchor="w", padx=20, pady=(0, 20))

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        anam_tab = tabview.add("Anamnèse")
        if client:
            AnamneseTab(anam_tab, client).pack(fill="both", expand=True, padx=10, pady=10)

