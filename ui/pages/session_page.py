"""Page contenant les formulaires de génération de séances."""

import customtkinter as ctk

from controllers.session_controller import SessionController
from repositories.client_repo import ClientRepository
from services.client_service import ClientService
from ui.components.design_system.typography import PageTitle

from .session_page_components.form_collectif import FormCollectif
from .session_page_components.form_individuel import FormIndividuel
from .session_page_components.session_preview import SessionPreview


class SessionPage(ctk.CTkFrame):
    """Page principale pour la génération de séances."""

    def __init__(self, parent, session_controller: SessionController):
        super().__init__(parent)
        self.session_controller = session_controller
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

        self.form_collectif = FormCollectif(
            collectif_tab, generate_callback=self.on_generate_collectif
        )
        self.form_collectif.pack(fill="both", expand=True, padx=16, pady=16)

        client_service = ClientService(ClientRepository())
        self.form_individuel = FormIndividuel(individuel_tab, client_service)
        self.form_individuel.pack(fill="both", expand=True, padx=16, pady=16)

        # Aperçu de la séance
        self.preview_panel = SessionPreview(self, self.session_controller)
        self.preview_panel.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=16)

    def on_generate_collectif(self) -> None:
        params = self.form_collectif.get_params()
        _, dto = self.session_controller.generate_session_preview(
            params, mode="collectif"
        )
        self.preview_panel.render_session(dto, client_id=None)
