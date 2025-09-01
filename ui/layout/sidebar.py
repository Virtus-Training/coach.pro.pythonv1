# ui/layout/sidebar.py

import os

import customtkinter as ctk
from PIL import Image

from utils.icon_loader import load_icon


class Sidebar(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        switch_page_callback,
        page_registry: dict[str, dict],
        active_module: str = "dashboard",
    ):
        super().__init__(
            parent,
            width=220,
            corner_radius=0,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
        )
        self.switch_page_callback = switch_page_callback
        self.active_module = active_module
        self.page_registry = page_registry

        self._build()

    def _build(self) -> None:
        """Create sidebar content."""
        # Logo
        logo_path = os.path.join("assets", "Logo.png")
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(160, 40))
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="CoachPro",
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H2"]),
            text_color=ctk.ThemeManager.theme["color"]["primary"],
        ).pack(pady=(0, 20))

        for item_id, data in self.page_registry.items():
            self._add_button(item_id, data["label"], data["icon"])

    def _add_button(self, item_id: str, label: str, icon_filename: str) -> None:
        icon = load_icon(icon_filename, 18)
        is_active = self.active_module == item_id
        theme = ctk.ThemeManager.theme["color"]
        button = ctk.CTkButton(
            self,
            text=label,
            image=icon,
            anchor="w",
            command=lambda i=item_id: self._on_click(i),
            fg_color=theme["primary"] if is_active else "transparent",
            text_color=theme["surface_dark"] if is_active else theme["primary_text"],
            hover_color=theme["primary"] if is_active else theme["surface_light"],
            corner_radius=0,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
            height=40,
        )
        button.pack(fill="x", padx=10, pady=2)

    def _on_click(self, module_id: str) -> None:
        if module_id == self.active_module:
            return
        self.active_module = module_id
        self.switch_page_callback(module_id)
        self.refresh()

    def refresh(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
        self._build()

    def set_active(self, module_id: str) -> None:
        self.active_module = module_id
        self.refresh()
