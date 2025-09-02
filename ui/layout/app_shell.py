# ui/layout/app_shell.py

import customtkinter as ctk

from ui.layout.header import Header
from ui.layout.sidebar import Sidebar


class AppShell(ctk.CTkFrame):
    """Main application shell with persistent sidebar and header."""

    def __init__(
        self,
        parent,
        switch_page_callback,
        page_registry: dict[str, dict],
        active_module: str = "dashboard",
    ):
        super().__init__(parent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.current_content = None  # <- Ligne à ajouter

        # Sidebar
        self.sidebar = Sidebar(
            self, switch_page_callback, page_registry, active_module=active_module
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")

        # Header
        self.header = Header(self)
        self.header.grid(row=0, column=1, sticky="ew")

        # Content area
        self.content_area = ctk.CTkFrame(
            self, fg_color=ctk.ThemeManager.theme["color"]["surface_dark"]
        )
        self.content_area.grid(row=1, column=1, sticky="nsew")

    def set_content(self, new_content):
        if self.current_content:
            self.current_content.pack_forget()

        self.current_content = new_content
        self.current_content.pack(fill="both", expand=True)
