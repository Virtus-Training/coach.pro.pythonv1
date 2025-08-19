"""Card container component."""

import customtkinter as ctk

from ui.theme.colors import NEUTRAL_700, NEUTRAL_800


class Card(ctk.CTkFrame):
    """Conteneur de base pour les éléments sous forme de carte."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=NEUTRAL_800,
            corner_radius=16,
            border_width=1,
            border_color=NEUTRAL_700,
            **kwargs,
        )
