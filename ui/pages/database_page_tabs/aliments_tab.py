import customtkinter as ctk
from typing import List

from models.aliment import Aliment
from repositories.aliment_repo import AlimentRepository
from ui.theme.fonts import get_text_font, get_small_font
from ui.theme.colors import DARK_PANEL, TEXT, TEXT_SECONDARY


class AlimentsTab(ctk.CTkFrame):
    def __init__(self, parent, repo: AlimentRepository | None = None):
        super().__init__(parent, fg_color="transparent")
        self.repo = repo or AlimentRepository()
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_list)

        search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Rechercher...")
        search_entry.pack(fill="x", padx=10, pady=10)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.aliments: List[Aliment] = self.repo.list_all()
        self._show_aliments(self.aliments)

    def _show_aliments(self, aliments: List[Aliment]) -> None:
        for widget in self.scroll.winfo_children():
            widget.destroy()

        for aliment in aliments:
            card = ctk.CTkFrame(self.scroll, fg_color=DARK_PANEL, corner_radius=8)
            card.pack(fill="x", padx=5, pady=4)

            ctk.CTkLabel(card, text=aliment.nom, font=get_text_font(), text_color=TEXT).pack(anchor="w", padx=10, pady=(5, 0))
            info = (
                f"{aliment.categorie or ''} – "
                f"P:{aliment.proteines_100g:.1f}g | G:{aliment.glucides_100g:.1f}g | L:{aliment.lipides_100g:.1f}g"
            )
            ctk.CTkLabel(card, text=info, font=get_small_font(), text_color=TEXT_SECONDARY).pack(anchor="w", padx=10, pady=(0, 5))

    def update_list(self, *_) -> None:
        query = self.search_var.get().lower()
        if not query:
            filtered = self.aliments
        else:
            filtered = [
                a
                for a in self.aliments
                if query in a.nom.lower()
                or (a.categorie and query in a.categorie.lower())
                or (a.type_alimentation and query in a.type_alimentation.lower())
            ]
        self._show_aliments(filtered)
