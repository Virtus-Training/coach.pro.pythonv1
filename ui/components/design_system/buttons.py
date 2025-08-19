"""Button components for the design system."""

import customtkinter as ctk

from ui.theme.colors import NEUTRAL_100, NEUTRAL_700, PRIMARY
from ui.theme.fonts import H3_NORMAL


class PrimaryButton(ctk.CTkButton):
    """Bouton standard pour les actions principales."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=PRIMARY,
            hover_color="#007BBE",
            text_color=NEUTRAL_100,
            font=H3_NORMAL,
            corner_radius=8,
            height=40,
            **kwargs,
        )


class SecondaryButton(ctk.CTkButton):
    """Bouton pour les actions secondaires (retour, annuler, etc.)."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            hover_color=NEUTRAL_700,
            text_color=PRIMARY,
            border_width=2,
            border_color=PRIMARY,
            font=H3_NORMAL,
            corner_radius=8,
            height=40,
            **kwargs,
        )
