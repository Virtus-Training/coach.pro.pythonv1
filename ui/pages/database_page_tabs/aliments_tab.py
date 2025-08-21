from typing import List

import customtkinter as ctk

from models.aliment import Aliment
from repositories.aliment_repo import AlimentRepository
from ui.components.design_system import DataTable


class AlimentsTab(ctk.CTkFrame):
    def __init__(self, parent, repo: AlimentRepository | None = None):
        super().__init__(parent, fg_color="transparent")
        self.repo = repo or AlimentRepository()

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_search)

        search_entry = ctk.CTkEntry(
            self, textvariable=self.search_var, placeholder_text="Rechercher..."
        )
        search_entry.pack(fill="x", padx=10, pady=10)

        self.aliments: List[Aliment] = self.repo.list_all()
        data = [
            [
                a.nom,
                a.kcal_100g,
                a.proteines_100g,
                a.glucides_100g,
                a.lipides_100g,
            ]
            for a in self.aliments
        ]
        headers = ["Nom", "Kcal", "Protéines", "Glucides", "Lipides"]
        self.table = DataTable(self, headers=headers, data=data)
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _on_search(self, *_):
        self.table.filter(self.search_var.get())
