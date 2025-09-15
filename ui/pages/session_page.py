"""Page contenant les formulaires de génération de séances."""

import customtkinter as ctk

from controllers.client_controller import ClientController
from repositories.client_repo import ClientRepository
from services.client_service import ClientService
from ui.components.design_system.typography import PageTitle
from ui.components.layout import two_columns

from .session_page_components.form_collectif_v2 import (
    FormCollectif as FormCollectifV2,
)
from .session_page_components.form_individuel import FormIndividuel
from .session_page_components.session_preview import SessionPreview


class SessionPage(ctk.CTkFrame):
    """Page principale pour la génération de séances."""

    def __init__(self, parent, session_controller):
        super().__init__(parent)
        self.session_controller = session_controller
        self.grid_rowconfigure(1, weight=1)
        # Ensure the single grid column stretches so the right pane can expand fully
        self.grid_columnconfigure(0, weight=1)

        PageTitle(self, text="Séances").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8)
        )

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, columnspan=2, sticky="nsew")
        left_col, right_col = two_columns(container, left_width=480, fixed_side="left")
        left_col.grid(row=0, column=0, sticky="nsew")
        right_col.grid(row=0, column=1, sticky="nsew")

        # Aperçu de la séance
        # (Initialisation déplacée ici pour que right_col soit définie)
        self.preview_panel = SessionPreview(right_col, self.session_controller)
        self.preview_panel.pack(fill="both", expand=True, padx=16, pady=16)

        # Onglets pour les formulaires (avec contenu scrollable)
        tabs = ctk.CTkTabview(left_col)
        tabs.pack(fill="both", expand=True, padx=16, pady=16)

        collectif_tab = tabs.add("Cours Collectif")
        individuel_tab = tabs.add("Individuel")

        # Structure avec bouton fixe en bas
        collectif_tab.grid_rowconfigure(0, weight=1)
        collectif_tab.grid_columnconfigure(0, weight=1)

        # Zone scrollable pour le formulaire
        collectif_scroll = ctk.CTkScrollableFrame(collectif_tab, fg_color="transparent")
        collectif_scroll.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 0))

        # Zone fixe pour le bouton
        button_frame = ctk.CTkFrame(collectif_tab, fg_color="transparent", height=60)
        button_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        button_frame.grid_propagate(False)

        self.form_collectif = FormCollectifV2(
            collectif_scroll,
            button_parent=button_frame,
            generate_callback=self.on_generate_collectif,
        )
        self.form_collectif.pack(fill="both", expand=True, padx=8, pady=8)

        client_controller = ClientController(ClientService(ClientRepository()))
        clients = client_controller.get_all_clients_for_view()

        # Structure similaire pour l'onglet individuel
        individuel_tab.grid_rowconfigure(0, weight=1)
        individuel_tab.grid_columnconfigure(0, weight=1)

        individuel_scroll = ctk.CTkScrollableFrame(
            individuel_tab, fg_color="transparent"
        )
        individuel_scroll.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 0))

        # Zone fixe pour le bouton individuel
        button_frame_indiv = ctk.CTkFrame(
            individuel_tab, fg_color="transparent", height=60
        )
        button_frame_indiv.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        button_frame_indiv.grid_propagate(False)

        self.form_individuel = FormIndividuel(
            individuel_scroll,
            clients,
            button_parent=button_frame_indiv,
            generate_callback=self.on_generate_individual,
        )
        self.form_individuel.pack(fill="both", expand=True, padx=8, pady=8)

    def on_generate_collectif(self) -> None:
        params = self.form_collectif.get_params()
        _, dto = self.session_controller.generate_session_preview(
            params, mode="collectif"
        )
        self.preview_panel.render_session(dto, client_id=None)

    def on_generate_individual(self) -> None:
        params = self.form_individuel.get_params()
        _, dto = self.session_controller.generate_individual_session(
            params["client_id"], params["objectif"], params["duree_minutes"]
        )
        self.preview_panel.render_session(dto, client_id=params["client_id"])
