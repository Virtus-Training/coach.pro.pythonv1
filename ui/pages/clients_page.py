import customtkinter as ctk
from ui.theme.fonts import get_title_font, get_text_font, get_small_font
from ui.theme.colors import DARK_BG, DARK_PANEL, TEXT, TEXT_SECONDARY
from repositories.client_repo import ClientRepository
from models.client import Client
from ui.modals.client_form_modal import ClientFormModal


class ClientsPage(ctk.CTkFrame):
    """Page de gestion des clients."""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=DARK_BG)

        self.repo = ClientRepository()

        ctk.CTkLabel(
            self,
            text="Gestion des Clients",
            font=get_title_font(),
            text_color=TEXT,
        ).pack(anchor="w", padx=20, pady=(20, 10))

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20)

        ctk.CTkButton(actions, text="Ajouter un client", command=self._open_add_modal).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Rafraîchir", command=self.load_clients).pack(side="left")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_clients()

    # -- Data loading -----------------------------------------------------
    def load_clients(self) -> None:
        """Charge et affiche les clients dans le scroll frame."""
        for widget in self.scroll.winfo_children():
            widget.destroy()

        clients = self.repo.list_all()
        for client in clients:
            self._create_client_card(client)

    def _create_client_card(self, client: Client) -> None:
        card = ctk.CTkFrame(self.scroll, fg_color=DARK_PANEL, corner_radius=8)
        card.pack(fill="x", padx=5, pady=5)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=10, pady=10)

        full_name = f"{client.prenom} {client.nom}"
        ctk.CTkLabel(info, text=full_name, font=get_text_font(), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(info, text=client.email or "", font=get_small_font(), text_color=TEXT_SECONDARY).pack(anchor="w")

        ctk.CTkButton(
            card,
            text="Modifier",
            command=lambda c=client: self._open_edit_modal(c),
            width=100,
        ).pack(side="right", padx=10, pady=10)

    # -- Modal handlers ---------------------------------------------------
    def _open_add_modal(self) -> None:
        modal = ClientFormModal(self)
        modal.grab_set()
        self.wait_window(modal)
        self.load_clients()

    def _open_edit_modal(self, client: Client) -> None:
        modal = ClientFormModal(self, client)
        modal.grab_set()
        self.wait_window(modal)
        self.load_clients()
