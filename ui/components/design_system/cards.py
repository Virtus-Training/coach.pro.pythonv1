# ui/components/design_system/cards.py

import customtkinter as ctk

from ui.theme.colors import BORDER_COLOR, DARK_PANEL


class Card(ctk.CTkFrame):
    """Conteneur de base pour les éléments sous forme de carte."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=DARK_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            **kwargs,
        )
