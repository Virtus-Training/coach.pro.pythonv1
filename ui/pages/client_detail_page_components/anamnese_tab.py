import customtkinter as ctk

from models.client import Client
from repositories.client_repo import ClientRepository
from repositories.exercices_repo import ExerciseRepository
from ui.components.exclusion_selector import ExclusionSelector


class AnamneseTab(ctk.CTkFrame):
    def __init__(self, master, client: Client):
        super().__init__(master, fg_color="transparent")
        self.client = client
        self.client_repo = ClientRepository()
        self.exercice_repo = ExerciseRepository()

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(info_frame, text="Objectifs du client").pack(anchor="w")
        self.objectifs_txt = ctk.CTkTextbox(info_frame, height=80)
        self.objectifs_txt.pack(fill="x", pady=(0,10))
        if client.objectifs:
            self.objectifs_txt.insert("1.0", client.objectifs)

        ctk.CTkLabel(info_frame, text="Antécédents & Notes").pack(anchor="w")
        self.antecedents_txt = ctk.CTkTextbox(info_frame, height=80)
        self.antecedents_txt.pack(fill="x")
        if client.antecedents_medicaux:
            self.antecedents_txt.insert("1.0", client.antecedents_medicaux)

        excl_frame = ctk.CTkFrame(self, fg_color="transparent")
        excl_frame.pack(fill="both", expand=True, padx=10, pady=10)

        all_exercices = self.exercice_repo.list_all_exercices()
        excluded_ids = self.client_repo.get_exclusions(client.id)

        self.selector = ExclusionSelector(excl_frame, all_exercices, excluded_ids)
        self.selector.pack(fill="both", expand=True)

        ctk.CTkButton(self, text="Enregistrer les modifications", command=self._save).pack(pady=10)

    def _save(self):
        objectifs = self.objectifs_txt.get("1.0", "end").strip()
        antecedents = self.antecedents_txt.get("1.0", "end").strip()
        excluded_ids = self.selector.get_excluded_ids()
        self.client_repo.update_anamnese(self.client.id, objectifs, antecedents)
        self.client_repo.update_exclusions(self.client.id, excluded_ids)
