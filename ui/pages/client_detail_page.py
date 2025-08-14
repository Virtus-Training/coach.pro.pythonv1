import customtkinter as ctk

from repositories.client_repo import ClientRepository
from ui.theme.fonts import get_title_font, get_text_font
from ui.theme.colors import DARK_BG, TEXT


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
            email = client.email or "Non renseigné"
            birth = client.date_naissance or "Non renseigné"
        else:
            title = "Client introuvable"
            email = "Non renseigné"
            birth = "Non renseigné"

        ctk.CTkLabel(
            self,
            text=title,
            font=get_title_font(),
            text_color=TEXT,
        ).pack(anchor="w", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            self,
            text=f"Email : {email}",
            font=get_text_font(),
            text_color=TEXT,
        ).pack(anchor="w", padx=20, pady=(0, 5))

        ctk.CTkLabel(
            self,
            text=f"Date de naissance : {birth}",
            font=get_text_font(),
            text_color=TEXT,
        ).pack(anchor="w", padx=20)

