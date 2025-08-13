# ui/components/card.py

import customtkinter as ctk
from PIL import Image
import os
from ui.theme.fonts import get_section_font
from ui.theme.colors import DARK_PANEL, TEXT

class IconCard(ctk.CTkFrame):
    def __init__(self, parent, text: str, icon_path: str = None, command=None):
        super().__init__(parent, height=80, corner_radius=10, fg_color=DARK_PANEL)
        self.pack_propagate(False)

        self.button = ctk.CTkButton(
            self,
            text=text,
            image=ctk.CTkImage(Image.open(icon_path), size=(26, 26)) if icon_path else None,
            font=get_section_font(),
            text_color=TEXT,
            fg_color="transparent",
            hover_color="#333333",
            anchor="w",
            command=command
        )
        self.button.pack(fill="both", padx=10, pady=10)

