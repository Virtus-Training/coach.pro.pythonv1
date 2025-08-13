# ui/components/button.py

import customtkinter as ctk
from ui.theme.colors import PRIMARY, SECONDARY, TEXT

class ButtonPrimary(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None):
        super().__init__(
            parent,
            text=text,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color=TEXT,
            command=command,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )

