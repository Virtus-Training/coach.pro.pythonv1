# ui/components/design_system/buttons.py

import customtkinter as ctk

from ui.theme.colors import PRIMARY, SECONDARY, TEXT_ON_PRIMARY
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

