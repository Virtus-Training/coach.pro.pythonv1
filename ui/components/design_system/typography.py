# ui/components/design_system/typography.py

import customtkinter as ctk

from ui.theme.colors import TEXT
from ui.theme.fonts import get_title_font, get_section_font


class PageTitle(ctk.CTkLabel):
    """Titre principal pour les pages."""

    def __init__(self, master, **kwargs):
        super().__init__(master, font=get_title_font(), text_color=TEXT, **kwargs)


class CardTitle(ctk.CTkLabel):
    """Titre pour les cartes et sections."""

    def __init__(self, master, **kwargs):
        super().__init__(master, font=get_section_font(), text_color=TEXT, **kwargs)
