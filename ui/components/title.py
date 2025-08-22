# ui/components/title.py

import customtkinter as ctk


class SectionTitle(ctk.CTkLabel):
    def __init__(self, parent, text: str):
        super().__init__(
            parent,
            text=text,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H2"]),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
