import customtkinter as ctk

from controllers.client_controller import ClientController
from models.client import Client
from ui.components.design_system import (
    Card,
    CardTitle,
    PageTitle,
    PrimaryButton,
    SecondaryButton,
)
from ui.modals.client_form_modal import ClientFormModal
from ui.theme.colors import NEUTRAL_300, NEUTRAL_900
from ui.theme.fonts import LABEL_NORMAL


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
        card = Card(self.scroll)
        card.pack(fill="x", padx=5, pady=5)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=20, pady=20)

        full_name = f"{client.prenom} {client.nom}"
        name_label = CardTitle(info, text=full_name)
        name_label.pack(anchor="w", pady=(0, 16))
        email = client.email or "Non renseigné"
        email_label = ctk.CTkLabel(
            info, text=email, font=LABEL_NORMAL, text_color=NEUTRAL_300
        )
        email_label.pack(anchor="w")

        SecondaryButton(
            card,
            text="Modifier",
            command=lambda c=client: self._open_edit_modal(c),
            width=100,
        ).pack(side="right", padx=20, pady=20)

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
        modal = ClientFormModal(self, self.controller)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()

    def _open_edit_modal(self, client: Client) -> None:
        modal = ClientFormModal(self, self.controller, client)
        modal.grab_set()
        self.wait_window(modal)
        self._load_clients()
