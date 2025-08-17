import customtkinter as ctk

from repositories.client_repo import ClientRepository
from services.client_service import ClientService

OBJECTIFS = ["Volume", "Force", "Endurance", "Technique"]


class FormIndividuel(ctk.CTkFrame):
    """Formulaire pour le coaching individuel."""

    def __init__(
        self,
        parent,
        generate_callback,
        open_preview_callback,
        toggle_form_callback,
    ):
        super().__init__(parent, fg_color="#222", corner_radius=10)
        self.configure(width=360)
        self.grid_columnconfigure(0, weight=1)

        # Sélection du client
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        row1.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row1, text="Sélectionner un client").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.client_service = ClientService(ClientRepository())
        clients = self.client_service.get_all_clients()
        client_names = [f"{c.prenom} {c.nom}" for c in clients]
        self.client_var = ctk.StringVar(value=client_names[0] if client_names else "")
        ctk.CTkOptionMenu(row1, variable=self.client_var, values=client_names).grid(
            row=0, column=1, sticky="ew", padx=(0, 12)
        )

        # Objectif de la séance
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        row2.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row2, text="Objectif de la séance").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.goal_var = ctk.StringVar(value=OBJECTIFS[0])
        ctk.CTkOptionMenu(row2, variable=self.goal_var, values=OBJECTIFS).grid(
            row=0, column=1, sticky="ew", padx=(0, 12)
        )

        # Boutons d'action
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=98, column=0, sticky="ew", padx=12, pady=(6, 12))
        for c in range(2):
            btns.grid_columnconfigure(c, weight=1)

        ctk.CTkButton(
            btns, text="Générer la séance individuelle", command=generate_callback
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=4)
        ctk.CTkButton(
            btns, text="Agrandir l’aperçu", command=open_preview_callback
        ).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ctk.CTkButton(
            btns, text="Masquer le formulaire", command=toggle_form_callback
        ).grid(row=1, column=1, sticky="ew", padx=4, pady=4)

    def get_params(self) -> dict:
        """Retourne les paramètres sélectionnés."""
        return {"client": self.client_var.get(), "goal": self.goal_var.get()}
