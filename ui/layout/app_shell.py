import customtkinter as ctk

from ui.layout.header import Header
from ui.layout.sidebar import Sidebar
from .content_area import ContentArea

class AppShell(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback, page_registry, active_module="dashboard"):
        super().__init__(master)
        self.master = master
        self.switch_page_callback = switch_page_callback
        self.page_registry = page_registry
        self.active_module = active_module
        self.current_content = None # Laissez cette ligne pour éviter de futures erreurs

        # Configuration de la grille
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Création des widgets
        self.sidebar = Sidebar(
            self,
            self.switch_page_callback,
            self.page_registry,
            self.active_module,
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.header = Header(self)
        self.header.grid(row=0, column=1, sticky="nsew")

        self.content_area = ContentArea(self)
        self.content_area.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

    def set_content(self, new_content):
        if self.current_content:
            self.current_content.pack_forget()

        self.current_content = new_content
        self.current_content.pack(fill="both", expand=True)

    def set_sidebar_active(self, page_name: str):
        self.sidebar.set_active(page_name)
