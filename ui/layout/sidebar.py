# ui/layout/sidebar.py

import os

import customtkinter as ctk
from PIL import Image

from ui.theme import colors, fonts
from utils.icon_loader import load_icon


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, switch_page_callback, active_module: str = "dashboard"):
        super().__init__(
            parent, width=220, corner_radius=0, fg_color=colors.NEUTRAL_900
        )
        self.switch_page_callback = switch_page_callback
        self.active_module = active_module

        self.menu_items = [
            ("dashboard", "Tableau de bord", "layout-dashboard.png"),
            ("programs", "Programmes", "dumbbell.png"),
            ("calendar", "Calendrier", "calendar.png"),
            ("sessions", "Séances", "clock.png"),
            ("progress", "Progression", "chart.png"),
            ("pdf", "PDF", "pdf.png"),
            ("nutrition", "Nutrition", "meal-plan.png"),
            ("database", "Base de données", "database.png"),
            ("clients", "Clients", "users.png"),
            ("messaging", "Messagerie", "chat.png"),
            ("billing", "Facturation", "billing.png"),
            ("settings", "Paramètres", "settings.png"),
        ]

        self._build()

    def _build(self) -> None:
        """Create sidebar content."""
        # Logo
        logo_path = os.path.join("assets", "Logo.png")
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(160, 40))
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="CoachPro",
            font=fonts.get_title_font(),
            text_color=colors.PRIMARY,
        ).pack(pady=(0, 20))

        for item_id, item_name, icon_file in self.menu_items:
            self._add_button(item_id, item_name, icon_file)

    def _add_button(self, item_id: str, label: str, icon_filename: str) -> None:
        icon = load_icon(icon_filename, 18)
        is_active = self.active_module == item_id
        button = ctk.CTkButton(
            self,
            text=label,
            image=icon,
            anchor="w",
            command=lambda i=item_id: self._on_click(i),
            fg_color=colors.PRIMARY if is_active else "transparent",
            text_color=colors.NEUTRAL_100 if is_active else colors.TEXT,
            hover_color=colors.PRIMARY if is_active else colors.NEUTRAL_800,
            corner_radius=0,
            font=ctk.CTkFont(size=14),
            height=40,
        )
        button.pack(fill="x", padx=10, pady=2)

    def _on_click(self, module_id: str) -> None:
        if module_id == self.active_module:
            return
        self.active_module = module_id
        self.switch_page_callback(module_id)
        self.refresh()

    def refresh(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
        self._build()

    def set_active(self, module_id: str) -> None:
        self.active_module = module_id
        self.refresh()
