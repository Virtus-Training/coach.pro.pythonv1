import customtkinter as ctk

from models.client import Client
from repositories.exercices_repo import ExerciseRepository
from controllers.client_controller import ClientController
from ui.components.design_system import Card, CardTitle, PrimaryButton
from ui.components.exclusion_selector import ExclusionSelector


class AnamneseTab(ctk.CTkFrame):
    def __init__(self, master, controller: ClientController, client: Client):
        super().__init__(master, fg_color="transparent")
        self.client = client
        self.controller = controller
        self.exercice_repo = ExerciseRepository()

        info_card = Card(self)
        info_card.pack(fill="x", padx=20, pady=(20, 10))

        CardTitle(info_card, text="Informations Clés").pack(
            anchor="w", padx=20, pady=(20, 10)
        )

        ctk.CTkLabel(info_card, text="Objectifs du client").pack(anchor="w", padx=20)
        self.objectifs_txt = ctk.CTkTextbox(info_card, height=80)
        self.objectifs_txt.pack(fill="x", padx=20, pady=(0, 10))
        if client.objectifs:
            self.objectifs_txt.insert("1.0", client.objectifs)

        ctk.CTkLabel(info_card, text="Antécédents & Notes").pack(anchor="w", padx=20)
        self.antecedents_txt = ctk.CTkTextbox(info_card, height=80)
        self.antecedents_txt.pack(fill="x", padx=20, pady=(0, 20))
        if client.antecedents_medicaux:
            self.antecedents_txt.insert("1.0", client.antecedents_medicaux)

        excl_card = Card(self)
        excl_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        CardTitle(excl_card, text="Exercices à Exclure").pack(
            anchor="w", padx=20, pady=(20, 10)
        )

        all_exercices = self.exercice_repo.list_all_exercices()
        excluded_ids = self.controller.get_client_exclusions(client.id)

        self.selector = ExclusionSelector(excl_card, all_exercices, excluded_ids)
        self.selector.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        PrimaryButton(
            self, text="Enregistrer les modifications", command=self._save
        ).pack(anchor="e", padx=20, pady=(0, 20))

    def _save(self):
        objectifs = self.objectifs_txt.get("1.0", "end").strip()
        antecedents = self.antecedents_txt.get("1.0", "end").strip()
        excluded_ids = self.selector.get_excluded_ids()
        self.controller.update_client_anamnese(
            self.client.id, objectifs, antecedents
        )
        self.controller.update_client_exclusions(self.client.id, excluded_ids)
