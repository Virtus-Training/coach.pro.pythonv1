import customtkinter as ctk

from ui.components.design_system import HeroBanner, Card, CardTitle


class ProgramPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        self.configure(fg_color=colors["surface_dark"])

        hero = HeroBanner(
            self,
            title="Programmes",
            subtitle="Créez et organisez vos plans d’entraînement.",
            icon_path="assets/icons/dumbbell.png",
        )
        hero.pack(fill="x", padx=20, pady=20)

        placeholder = Card(self)
        placeholder.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        CardTitle(placeholder, text="Bientôt disponible").pack(anchor="w", padx=12, pady=12)
