import customtkinter as ctk

from ui.components.design_system import HeroBanner
from ui.pages.database_page_tabs.aliments_tab import AlimentsTab
from ui.pages.database_page_tabs.exercises_tab import ExercisesTab


class DatabasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.colors = ctk.ThemeManager.theme["color"]
        self.fonts = ctk.ThemeManager.theme["font"]
        self.configure(fg_color=self.colors["surface_dark"])

        # Header (SaaS-like hero banner)
        hero = HeroBanner(
            self,
            title="Bases de Données",
            subtitle="Gérez vos bases d'exercices, d'aliments et de programmes.",
            icon_path="assets/icons/database.png",
        )
        hero.pack(fill="x", padx=12, pady=(6, 8))

        # Tabs area
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        exercises_tab = tabview.add("Exercices")
        ExercisesTab(exercises_tab).pack(fill="both", expand=True)

        foods_tab = tabview.add("Aliments")
        AlimentsTab(foods_tab).pack(fill="both", expand=True)

    def init_exercises_tab(self, frame):
        # Legacy placeholder removed; now handled by ExercisesTab
        pass
