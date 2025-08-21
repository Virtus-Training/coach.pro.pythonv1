import os

import customtkinter as ctk

from controllers.client_controller import ClientController
from models.client import Client
from ui.components.design_system import (
    InfoCard,
    PageTitle,
    PrimaryButton,
    SecondaryButton,
)
from ui.modals.client_form_modal import ClientFormModal
from ui.theme.colors import NEUTRAL_900


class ClientsPage(ctk.CTkFrame):
    """Page de gestion des clients."""

    def __init__(self, parent, controller: ClientController):
        super().__init__(parent)
        self.configure(fg_color=NEUTRAL_900)

        self.controller = controller

        PageTitle(self, text="Gestion des Clients").pack(
            anchor="w", padx=20, pady=(20, 24)
        )

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 24))

        PrimaryButton(
            actions, text="Ajouter un client", command=self._open_add_modal
        ).pack(side="left", padx=(0, 10))
        SecondaryButton(actions, text="Rafraîchir", command=self._load_clients).pack(
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

        clients = self.controller.get_all_clients_for_view()
        for client in clients:
            self._create_client_card(client)

    def _create_client_card(self, client: Client) -> None:
        actions = [
            ("Modifier", lambda c=client: self._open_edit_modal(c)),
            ("Supprimer", lambda cid=client.id: self._delete_client(cid)),
        ]
        tags = [client.objectifs] if client.objectifs else []
        card = InfoCard(
            self.scroll,
            icon_path=os.path.join("assets", "icons", "user1.png"),
            title=f"{client.prenom} {client.nom}",
            subtitle=client.email or "Non renseigné",
            tags=tags,
            actions=actions,
            on_click_callback=lambda cid=client.id: self.on_client_selected(cid),
        )
        card.pack(fill="x", padx=5, pady=5)

    def _delete_client(self, client_id: int) -> None:
        self.controller.delete_client(client_id)
        self._load_clients()

    def on_client_selected(self, client_id: int) -> None:
        self.master.master.show_client_detail(client_id)

    # -- Modal handlers ---------------------------------------------------
    def _open_add_modal(self) -> None:
        modal = ClientFormModal(self, self.controller)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()

    def _open_edit_modal(self, client: Client) -> None:
        modal = ClientFormModal(self, self.controller, client)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()
