"""Typography components for the design system."""

import customtkinter as ctk

from ui.theme.colors import NEUTRAL_100
from ui.theme.fonts import H1_BOLD, H2_BOLD


class PageTitle(ctk.CTkLabel):
    """Titre principal pour les pages."""

    def __init__(self, master, **kwargs):
        super().__init__(master, font=H1_BOLD, text_color=NEUTRAL_100, **kwargs)


class CardTitle(ctk.CTkLabel):
    """Titre pour les cartes et sections."""

    def __init__(self, master, **kwargs):
        super().__init__(master, font=H2_BOLD, text_color=NEUTRAL_100, **kwargs)
