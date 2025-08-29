from typing import Optional

from controllers.client_controller import ClientController
from models.client import Client
from ui.components.design_system import LabeledInput
from ui.modals.base_modal import BaseFormModal


class ClientFormModal(BaseFormModal):
    """Modal for creating or editing a client."""

    def __init__(
        self,
        parent,
        controller: ClientController,
        client: Optional[Client] = None,
    ) -> None:
        self.controller = controller
        self.client = client

        fields = {
            "prenom": lambda master: LabeledInput(master, "Prénom"),
            "nom": lambda master: LabeledInput(master, "Nom"),
            "email": lambda master: LabeledInput(master, "Email"),
            "date_naissance": lambda master: LabeledInput(
                master, "Date de Naissance (AAAA-MM-JJ)"
            ),
        }

        if client:

            def save_callback(data):
                controller.update_client(client.id, data)

            title = "Modifier un client"
        else:
            save_callback = controller.add_client
            title = "Ajouter un client"

        super().__init__(parent, title, fields, save_callback)

        if client:
            self.form_fields["prenom"].set_value(client.prenom)
            self.form_fields["nom"].set_value(client.nom)
            self.form_fields["email"].set_value(client.email or "")
            self.form_fields["date_naissance"].set_value(client.date_naissance or "")
