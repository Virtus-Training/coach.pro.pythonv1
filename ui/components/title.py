# ui/components/title.py

import customtkinter as ctk
from ui.theme.fonts import get_section_font
from ui.theme.colors import TEXT

class SectionTitle(ctk.CTkLabel):
    def __init__(self, parent, text: str):
        super().__init__(parent, text=text, font=get_section_font(), text_color=TEXT)

