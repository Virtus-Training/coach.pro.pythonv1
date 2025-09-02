# ui/layout/sidebar.py

import customtkinter as ctk

from utils.icon_loader import load_icon, load_square_image


class Sidebar(ctk.CTkScrollableFrame):
    """The application sidebar with navigation buttons."""

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
        self.grid_rowconfigure(20, weight=1)
        self.switch_page_callback = switch_page_callback
        self.page_registry = page_registry
        self.active_module = active_module
        self._button_map = {}

        self._build()

    def _build(self) -> None:
        """Builds the widgets of the sidebar."""
        # Logo (square)
        # Use square-padding helper to avoid distortion and enforce square size
        logo = load_square_image("assets/Logo.png", 48)
        logo_label = ctk.CTkLabel(self, image=logo, text="", anchor="center")
        logo_label.pack(pady=(20, 10))

        # Buttons
        for item_id, data in self.page_registry.items():
            button = self._add_button(item_id, data["label"], data["icon"])
            self._button_map[item_id] = button

    def _add_button(self, item_id: str, label: str, icon_name: str) -> ctk.CTkButton:
        """Adds a navigation button to the sidebar."""
        # Use icon loader with explicit size and pass CTkImage directly to button
        icon = load_icon(icon_name, 20)
        button = ctk.CTkButton(
            self,
            image=icon,
            text=f"  {label}",
            height=40,
            compound="left",
            anchor="w",
            corner_radius=4,
            command=lambda i=item_id: self._on_click(i),
        )
        button.pack(fill="x", padx=10, pady=2)
        return button

    def _on_click(self, module_id: str) -> None:
        """Handles button clicks."""
        self.switch_page_callback(module_id)

    def set_active(self, module_id: str) -> None:
        """Sets the active state of a navigation button."""
        for item_id, button in self._button_map.items():
            if item_id == module_id:
                button.configure(
                    fg_color=ctk.ThemeManager.theme["color"]["primary"],
                    text_color=ctk.ThemeManager.theme["color"]["surface_dark"],
                )
            else:
                button.configure(
                    fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
                    text_color=ctk.ThemeManager.theme["color"]["primary_text"],
                )
