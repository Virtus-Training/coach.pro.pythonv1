"""UI components for individual session generation form."""

from typing import List

import customtkinter as ctk

from models.client import Client
from ui.components.design_system.buttons import PrimaryButton
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle


class FormIndividuel(Card):
    """Formulaire pour la génération de séances individuelles."""

    def __init__(self, parent, clients: List[Client], generate_callback=None):
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
        self._client_map = {f"{c.prenom} {c.nom}": c.id for c in clients}
        client_names = list(self._client_map.keys())
        self.client_var = ctk.StringVar(value=client_names[0] if client_names else "")
        ctk.CTkComboBox(
            client_row, variable=self.client_var, values=client_names
        ).grid(row=0, column=1, sticky="ew")

        # Objectif de la séance
        objective_row = ctk.CTkFrame(self, fg_color="transparent")
        objective_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
        objective_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(objective_row, text="Objectif").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.objective_var = ctk.StringVar()
        ctk.CTkEntry(objective_row, textvariable=self.objective_var).grid(
            row=0, column=1, sticky="ew"
        )

        # Durée de la séance
        duration_row = ctk.CTkFrame(self, fg_color="transparent")
        duration_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
        duration_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(duration_row, text="Durée").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        duration_values = [
            "30 minutes",
            "45 minutes",
            "60 minutes",
            "75 minutes",
            "90 minutes",
        ]
        self.duration_var = ctk.StringVar(value=duration_values[0])
        ctk.CTkOptionMenu(
            duration_row, variable=self.duration_var, values=duration_values
        ).grid(row=0, column=1, sticky="ew")

        # Action button
        PrimaryButton(self, text="Générer la séance", command=generate_callback).grid(
            row=4, column=0, sticky="ew", padx=16, pady=(0, 16)
        )

    def get_params(self) -> dict:
        """Retourne les paramètres du formulaire."""
        return {
            "client_id": self._client_map.get(self.client_var.get()),
            "objectif": self.objective_var.get(),
            "duree_minutes": int(self.duration_var.get().split()[0]),
        }
