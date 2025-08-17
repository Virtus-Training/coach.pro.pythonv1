"""Page contenant les formulaires de génération de séances."""

import customtkinter as ctk

from ui.components.design_system.typography import PageTitle
from .session_page_components.form_collectif import FormCollectif
from .session_page_components.form_individuel import FormIndividuel


class SessionPage(ctk.CTkFrame):
    """Page principale pour la génération de séances."""

    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        PageTitle(self, text="Séances").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8)
        )

        # Onglets pour les formulaires
        tabs = ctk.CTkTabview(self)
        tabs.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=16)

        collectif_tab = tabs.add("Cours Collectif")
        individuel_tab = tabs.add("Individuel")

        self.form_collectif = FormCollectif(collectif_tab)
        self.form_collectif.pack(fill="both", expand=True, padx=16, pady=16)

        self.form_individuel = FormIndividuel(individuel_tab)
        self.form_individuel.pack(fill="both", expand=True, padx=16, pady=16)

        # Aperçu de la séance
        preview = ctk.CTkFrame(self)
        preview.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=16)
        ctk.CTkLabel(preview, text="Aperçu de la séance").pack(
            padx=16, pady=16
        )

