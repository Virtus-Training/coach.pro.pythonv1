# ui/components/design_system/buttons.py

import customtkinter as ctk

from ui.theme.colors import PRIMARY, SECONDARY, TEXT_ON_PRIMARY, DARK_SOFT
from ui.theme.fonts import get_button_font


class PrimaryButton(ctk.CTkButton):
    """Bouton standard pour les actions principales."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color=TEXT_ON_PRIMARY,
            font=get_button_font(),
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
            hover_color=DARK_SOFT,
            text_color=PRIMARY,
            border_width=1,
            border_color=PRIMARY,
            font=get_button_font(),
            corner_radius=8,
            height=40,
            **kwargs,
        )

