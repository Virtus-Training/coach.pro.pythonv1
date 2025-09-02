import customtkinter as ctk

from ui.pages.database_page_tabs.aliments_tab import AlimentsTab
from ui.pages.database_page_tabs.exercises_tab import ExercisesTab


class DatabasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.colors = ctk.ThemeManager.theme["color"]
        self.fonts = ctk.ThemeManager.theme["font"]
        self.configure(fg_color=self.colors["surface_dark"])

        # Header
        header = ctk.CTkFrame(self, fg_color=self.colors["primary"], corner_radius=10)
        header.pack(fill="x", padx=20, pady=20)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(
            title_row,
            text="🗃️",
            font=ctk.CTkFont(**self.fonts["H1"]),
        ).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(
            title_row,
            text="Bases de Données",
            font=ctk.CTkFont(**self.fonts["H1"]),
            text_color=self.colors["surface_dark"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Gérez vos bases de données d'exercices, d'aliments et de programmes.",
            font=ctk.CTkFont(**self.fonts["Body"]),
            text_color=self.colors["primary_text"],
        ).pack(anchor="w", padx=20, pady=(5, 15))

        # Tab view
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        exercises_tab = tabview.add("Exercices")
        ExercisesTab(exercises_tab).pack(fill="both", expand=True)

        foods_tab = tabview.add("Aliments")
        AlimentsTab(foods_tab).pack(fill="both", expand=True)

    def init_exercises_tab(self, frame):
        # Legacy placeholder removed; now handled by ExercisesTab
        pass
