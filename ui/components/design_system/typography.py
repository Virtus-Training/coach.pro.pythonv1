"""Typography components for the design system."""

import customtkinter as ctk


class PageTitle(ctk.CTkLabel):
    """Titre principal pour les pages."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H1"]),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            **kwargs,
        )


class CardTitle(ctk.CTkLabel):
    """Titre pour les cartes et sections."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H2"]),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            **kwargs,
        )
