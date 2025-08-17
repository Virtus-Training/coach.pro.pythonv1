"""UI components for individual session generation form."""

import customtkinter as ctk

from repositories.client_repo import ClientRepository
from services.client_service import ClientService
from ui.components.design_system.buttons import PrimaryButton
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle


class FormIndividuel(Card):
    """Formulaire pour la génération de séances individuelles."""

    def __init__(self, parent, generate_callback=None):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

        CardTitle(self, text="Séance Individuelle").grid(
            row=0, column=0, sticky="w", padx=16, pady=(16, 12)
        )

        # Sélection du client
        client_row = ctk.CTkFrame(self, fg_color="transparent")
        client_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        client_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(client_row, text="Client").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.client_service = ClientService(ClientRepository())
        clients = self.client_service.get_all_clients()
        client_names = [f"{c.prenom} {c.nom}" for c in clients]
        self.client_var = ctk.StringVar(value=client_names[0] if client_names else "")
        ctk.CTkOptionMenu(
            client_row, variable=self.client_var, values=client_names
        ).grid(row=0, column=1, sticky="ew")

        # Objectif de la séance
        objective_row = ctk.CTkFrame(self, fg_color="transparent")
        objective_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        objective_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(objective_row, text="Objectif").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.objective_var = ctk.StringVar()
        ctk.CTkEntry(objective_row, textvariable=self.objective_var).grid(
            row=0, column=1, sticky="ew"
        )

        # Action button
        PrimaryButton(
            self, text="Générer la séance", command=generate_callback
        ).grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))

    def get_params(self) -> dict:
        """Retourne les paramètres du formulaire."""
        return {
            "client": self.client_var.get(),
            "goal": self.objective_var.get(),
        }

