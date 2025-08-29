"""Card components for the design system."""

from typing import Callable, Iterable, Optional, Tuple

import customtkinter as ctk
from PIL import Image

from .buttons import SecondaryButton


class Card(ctk.CTkFrame):
    """Conteneur de base pour les éléments sous forme de carte."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
            corner_radius=16,
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"]["subtle_border"],
            **kwargs,
        )


class InfoCard(ctk.CTkFrame):
    """Reusable information card with icon, text and actions."""

    def __init__(
        self,
        master,
        icon_path: Optional[str] = None,
        title: str = "",
        subtitle: str = "",
        tags: Optional[Iterable[str]] = None,
        actions: Optional[Iterable[Tuple[str, Callable[[], None]]]] = None,
        on_click_callback: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
            corner_radius=16,
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"]["subtle_border"],
            **kwargs,
        )

        self.on_click_callback = on_click_callback
        colors = ctk.ThemeManager.theme["color"]
        self._default_fg = colors["surface_light"]
        self._hover_fg = colors["surface_dark"]

        self.grid_columnconfigure(1, weight=1)

        # -- Icon ---------------------------------------------------------
        if icon_path:
            image = ctk.CTkImage(Image.open(icon_path), size=(48, 48))
            icon_label = ctk.CTkLabel(self, text="", image=image)
            icon_label.image = image
        else:
            icon_label = ctk.CTkLabel(self, text="")
        icon_label.grid(row=0, column=0, padx=(16, 12), pady=16)

        # -- Main information -------------------------------------------
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", pady=16)
        info_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            info_frame,
            text=title,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H3"]),
            text_color=colors["primary_text"],
        )
        title_label.grid(row=0, column=0, sticky="w")

        subtitle_label = ctk.CTkLabel(
            info_frame,
            text=subtitle,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
            text_color=colors["secondary_text"],
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        tags_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        tags_frame.grid(row=2, column=0, sticky="w", pady=(8, 0))
        if tags:
            for tag in tags:
                tag_label = ctk.CTkLabel(
                    tags_frame,
                    text=tag,
                    font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Small"]),
                    text_color=colors["surface_dark"],
                    fg_color=colors["primary"],
                    corner_radius=8,
                    padx=6,
                    pady=2,
                )
                tag_label.pack(side="left", padx=(0, 6))
                tag_label.bind("<Button-1>", lambda e: "break")

        # -- Actions -----------------------------------------------------
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=2, padx=16, pady=16)
        if actions:
            actions_list = list(actions)
            for idx, (name, callback) in enumerate(actions_list):
                btn = SecondaryButton(
                    actions_frame, text=name, command=callback, width=100
                )
                btn.pack(side="left", padx=(0, 6) if idx < len(actions_list) - 1 else 0)

        # -- Click bindings ---------------------------------------------
        if on_click_callback:
            for widget in [self, title_label, subtitle_label]:
                widget.bind("<Button-1>", lambda e: on_click_callback())
        if actions:
            for child in actions_frame.winfo_children():
                child.bind("<Button-1>", lambda e: "break")

        self._bind_hover_recursive(self)

    # -- Hover handling -------------------------------------------------
    def _bind_hover_recursive(self, widget) -> None:
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        for child in widget.winfo_children():
            self._bind_hover_recursive(child)

    def _on_enter(self, _event) -> None:
        self.configure(fg_color=self._hover_fg)

    def _on_leave(self, _event) -> None:
        self.configure(fg_color=self._default_fg)
