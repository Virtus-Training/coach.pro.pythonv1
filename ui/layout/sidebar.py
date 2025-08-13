# ui/layout/sidebar.py

import customtkinter as ctk
from PIL import Image
import os

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, switch_page_callback, active_module="dashboard"):
        super().__init__(parent, width=220, corner_radius=0)
        self.switch_page_callback = switch_page_callback
        self.active_module = active_module
        self.configure(fg_color="#1a1a1a")  # Dark theme

        self.menu_items = [
            ("dashboard", "Tableau de bord", "layout-dashboard.png"),
            ("programs", "Programmes", "dumbbell.png"),
            ("calendar", "Calendrier", "calendar.png"),
            ("sessions", "Séances", "clock.png"),
            ("progress", "Progression", "chart.png"),
            ("pdf", "PDF", "pdf.png"),
            ("nutrition", "Nutrition", "apple.png"),
            ("database", "Base de données", "database.png"),
            ("clients", "Clients", "users.png"),
            ("messaging", "Messagerie", "chat.png"),
            ("billing", "Facturation", "billing.png"),
            ("settings", "Paramètres", "settings.png"),
        ]

        self.create_sidebar()

    def create_sidebar(self):
        title = ctk.CTkLabel(self, text="CoachPro", text_color="#3b82f6",
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 10))

        for item_id, item_name, icon_file in self.menu_items:
            self.add_menu_button(item_id, item_name, icon_file)

    def add_menu_button(self, item_id, label, icon_filename):
        image_path = os.path.join("assets", "icons", icon_filename)
        icon = ctk.CTkImage(Image.open(image_path), size=(18, 18))

        button = ctk.CTkButton(
            self,
            text=label,
            image=icon,
            anchor="w",
            command=lambda: self.on_menu_click(item_id),
            fg_color="#1a1a1a" if self.active_module != item_id else "#3b82f6",
            text_color="#f5f5f5" if self.active_module != item_id else "#ffffff",
            hover_color="#333333",
            corner_radius=0,
            font=ctk.CTkFont(size=14),
            height=40
        )
        button.pack(fill="x", padx=10, pady=2)

    def on_menu_click(self, module_id):
        self.active_module = module_id
        self.switch_page_callback(module_id)
        for widget in self.winfo_children():
            widget.destroy()
        self.create_sidebar()

