import customtkinter as ctk

from ui.components.design_system import Card, CardTitle, HeroBanner


class ProgressPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        self.configure(fg_color=colors["surface_dark"])

        hero = HeroBanner(
            self,
            title="Progression",
            subtitle="Suivi et statistiques (à venir).",
            icon_path="assets/icons/chart.png",
        )
        hero.pack(fill="x", padx=12, pady=(6, 8))

        card = Card(self)
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        CardTitle(card, text="Bientôt disponible").pack(anchor="w", padx=12, pady=12)
