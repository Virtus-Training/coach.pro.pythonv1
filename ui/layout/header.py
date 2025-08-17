# ui/layout/header.py

import os

import customtkinter as ctk
from PIL import Image


class Header(ctk.CTkFrame):
    def __init__(self, parent, title="CoachPro"):
        super().__init__(parent, height=60, fg_color="#121212")
        self.pack_propagate(False)

        # Logo (optionnel)
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(64, 64))
            logo_label = ctk.CTkLabel(self, image=logo_image, text="")
            logo_label.pack(side="left", padx=20)

        # Titre
        self.title_label = ctk.CTkLabel(
            self,
            text="CoachPro",
            text_color="#3b82f6",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.pack(side="left", padx=10)

        # Profil (optionnel)
        user_label = ctk.CTkLabel(self, text="👤 Virtus Training", text_color="#bbbbbb")
        user_label.pack(side="right", padx=20)

    def update_title(self, new_title):
        self.title_label.configure(text=new_title)
