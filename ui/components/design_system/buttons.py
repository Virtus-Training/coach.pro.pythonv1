"""Button components for the design system."""

import customtkinter as ctk


class PrimaryButton(ctk.CTkButton):
    """Bouton standard pour les actions principales."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=ctk.ThemeManager.theme["color"]["primary"],
            hover_color="#06B6D4",
            text_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
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
            hover_color=ctk.ThemeManager.theme["color"]["subtle_border"],
            text_color=ctk.ThemeManager.theme["color"]["primary"],
            border_width=2,
            border_color=ctk.ThemeManager.theme["color"]["primary"],
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
            corner_radius=8,
            height=40,
            **kwargs,
        )
