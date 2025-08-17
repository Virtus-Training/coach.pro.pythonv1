import customtkinter as ctk

from models.client import Client
from repositories.client_repo import ClientRepository
from ui.modals.client_form_modal import ClientFormModal
from ui.theme.colors import DARK_BG, DARK_PANEL, TEXT, TEXT_SECONDARY
from ui.theme.fonts import get_small_font, get_text_font, get_title_font


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

        ctk.CTkButton(
            actions, text="Ajouter un client", command=self._open_add_modal
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Rafraîchir", command=self._load_clients).pack(
            side="left"
        )

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self._load_clients()

    # -- Data loading -----------------------------------------------------
    def _load_clients(self) -> None:
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
        name_label = ctk.CTkLabel(
            info, text=full_name, font=get_text_font(), text_color=TEXT
        )
        name_label.pack(anchor="w")
        email = client.email or "Non renseigné"
        email_label = ctk.CTkLabel(
            info, text=email, font=get_small_font(), text_color=TEXT_SECONDARY
        )
        email_label.pack(anchor="w")

        ctk.CTkButton(
            card,
            text="Modifier",
            command=lambda c=client: self._open_edit_modal(c),
            width=100,
        ).pack(side="right", padx=10, pady=10)

        # Rendre la carte cliquable
        widgets_to_bind = [card, info, name_label, email_label]
        for widget in widgets_to_bind:
            widget.bind(
                "<Button-1>", lambda e, cid=client.id: self.on_client_selected(cid)
            )

    def on_client_selected(self, client_id: int) -> None:
        self.master.master.show_client_detail(client_id)

    # -- Modal handlers ---------------------------------------------------
    def _open_add_modal(self) -> None:
        modal = ClientFormModal(self)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()

    def _open_edit_modal(self, client: Client) -> None:
        modal = ClientFormModal(self, client)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()
