import customtkinter as ctk

from ui.components.design_system import Card, CardTitle, HeroBanner


class BillingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        self.configure(fg_color=colors["surface_dark"])

        hero = HeroBanner(
            self,
            title="Facturation",
            subtitle="Paiements, abonnements et reçus (à venir).",
            icon_path="assets/icons/billing.png",
        )
        hero.pack(fill="x", padx=12, pady=(6, 8))

        card = Card(self)
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        CardTitle(card, text="Bientôt disponible").pack(anchor="w", padx=12, pady=12)
