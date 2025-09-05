# ui/components/card.py

import customtkinter as ctk
from PIL import Image


class IconCard(ctk.CTkFrame):
    def __init__(self, parent, text: str, icon_path: str = None, command=None):
        super().__init__(
            parent,
            height=80,
            corner_radius=10,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
        )
        self.pack_propagate(False)

        self.button = ctk.CTkButton(
            self,
            text=text,
            image=ctk.CTkImage(Image.open(icon_path), size=(26, 26))
            if icon_path
            else None,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H3"]),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            anchor="w",
            command=command,
        )
        self.button.pack(fill="both", padx=10, pady=10)

