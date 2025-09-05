"""Hero banner and toolbar-like containers for page headers.

The `HeroBanner` provides a visually distinctive header similar to SaaS apps
with a colored background, title, subtitle and optional icon.
"""

from __future__ import annotations

import os
from typing import Optional

import customtkinter as ctk
from PIL import Image


class HeroBanner(ctk.CTkFrame):
    """Prominent page header with accent background.

    Parameters
    ----------
    master: widget parent
    title: main title text
    subtitle: optional subtitle text
    icon_path: optional path to an image to render at left (48x48)
    """

    def __init__(
        self,
        master,
        title: str,
        subtitle: str = "",
        icon_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        colors = ctk.ThemeManager.theme["color"]
        super().__init__(master, fg_color=colors.get("primary", "#22D3EE"), **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # Optional icon
        if icon_path and os.path.exists(icon_path):
            try:
                img = ctk.CTkImage(Image.open(icon_path), size=(48, 48))
            except Exception:
                img = None
        else:
            img = None

        if img is not None:
            ctk.CTkLabel(self, text="", image=img).grid(
                row=0, column=0, rowspan=2, padx=(16, 12), pady=16
            )

        # Title + subtitle
        title_lbl = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H1"]),
            text_color=colors.get("surface_dark", "#111827"),
        )
        title_lbl.grid(row=0, column=1, sticky="w", padx=(16 if img is None else 0, 16), pady=(14, 0))

        if subtitle:
            sub_lbl = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
                text_color=colors.get("surface_dark", "#111827"),
            )
            sub_lbl.grid(row=1, column=1, sticky="w", padx=(16 if img is None else 0, 16), pady=(2, 14))

        # Decorative right overlay (subtle)
        # A small translucent stripe adds a modern touch without images
        deco = ctk.CTkFrame(self, fg_color="#ffffff", width=8, corner_radius=0)
        try:
            deco.configure(fg_color="#a5f3fc")  # light cyan
        except Exception:
            pass
        deco.grid(row=0, column=2, rowspan=2, sticky="ns", padx=(0, 0))

