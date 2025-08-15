import customtkinter as ctk

from ui.pages.database_page_tabs.aliments_tab import AlimentsTab
from ui.theme.fonts import get_title_font, get_text_font
from ui.theme.colors import PRIMARY, DARK_BG, DARK_PANEL, TEXT


class DatabasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=DARK_BG)

        # Header
        header = ctk.CTkFrame(self, fg_color=PRIMARY, corner_radius=10)
        header.pack(fill="x", padx=20, pady=20)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(title_row, text="🗃️", font=get_title_font()).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_row, text="Bases de Données", font=get_title_font(), text_color="white").pack(side="left")

        ctk.CTkLabel(
            header,
            text="Gérez vos bases de données d'exercices, d'aliments et de programmes.",
            font=get_text_font(),
            text_color="#dbeafe",
        ).pack(anchor="w", padx=20, pady=(5, 15))

        # Tab view
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        exercises_tab = tabview.add("Exercices")
        self.init_exercises_tab(exercises_tab)

        foods_tab = tabview.add("Aliments")
        AlimentsTab(foods_tab).pack(fill="both", expand=True)

    def init_exercises_tab(self, frame):
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for i in range(10):
            row = ctk.CTkFrame(scroll, fg_color=DARK_PANEL, corner_radius=8)
            row.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(row, text=f"Exercice {i+1}", font=get_text_font(), text_color=TEXT).pack(side="left", padx=10)
