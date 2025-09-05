"""Button components for the design system.

Provides consistent button variants aligned with the app theme:
- PrimaryButton: solid accent for main actions
- SecondaryButton: outlined accent for secondary actions
- GhostButton: text-only subtle action for toolbars
- DangerButton: solid red for destructive actions
"""

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


class GhostButton(ctk.CTkButton):
    """Bouton discret (texte/ghost) idéal pour toolbars et actions peu
    prioritaires. Utilise la couleur de texte secondaire avec un hover subtil.
    """

    def __init__(self, master, **kwargs):
        colors = ctk.ThemeManager.theme["color"]
        super().__init__(
            master,
            fg_color="transparent",
            hover_color=colors.get("subtle_border", "#374151"),
            text_color=colors.get("secondary_text", "#9CA3AF"),
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
            corner_radius=6,
            height=34,
            **kwargs,
        )


class DangerButton(ctk.CTkButton):
    """Bouton pour actions destructives (supprimer…)."""

    def __init__(self, master, **kwargs):
        colors = ctk.ThemeManager.theme["color"]
        super().__init__(
            master,
            fg_color=colors.get("error", "#EF4444"),
            hover_color="#B91C1C",
            text_color="#111827",
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
            corner_radius=8,
            height=40,
            **kwargs,
        )
