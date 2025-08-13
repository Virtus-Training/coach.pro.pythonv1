# ui/components/tabbar.py (modifié)

import customtkinter as ctk
from ui.theme.colors import PRIMARY, TEXT, TEXT_SECONDARY, DARK_SOFT, DARK_PANEL
from ui.theme.fonts import get_text_font, get_small_font
from PIL import Image
import os

class CustomTabBar(ctk.CTkFrame):
    def __init__(self, parent, tabs, on_tab_selected, active_tab):
        super().__init__(parent, fg_color=DARK_PANEL)
        self.tabs = tabs
        self.on_tab_selected = on_tab_selected
        self.active_tab = active_tab
        self.buttons = {}
        self.build()

    def build(self):
        for tab in self.tabs:
            tab_id = tab["id"]
            button = ctk.CTkFrame(self, fg_color=self.get_tab_color(tab_id), corner_radius=0, height=60)
            button.pack(side="left", fill="y", expand=True, padx=1)

            icon_path = os.path.join("assets", "icons", tab["icon"])
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(20, 20))

            inner = ctk.CTkButton(
                button,
                text=f"{tab['name']}\n{tab['count']}",
                anchor="center",
                image=icon_image,
                compound="left",
                fg_color="transparent",
                hover_color=DARK_SOFT,
                font=get_text_font(),
                text_color=PRIMARY if tab_id == self.active_tab else TEXT_SECONDARY,
                command=lambda tid=tab_id: self.select_tab(tid)
            )
            inner.pack(fill="both", expand=True, padx=2)
            self.buttons[tab_id] = (button, inner)

    def select_tab(self, tab_id):
        if tab_id == self.active_tab:
            return
        self.active_tab = tab_id
        self.on_tab_selected(tab_id)
        self.refresh()

    def refresh(self):
        for tab_id, (frame, button) in self.buttons.items():
            frame.configure(fg_color=self.get_tab_color(tab_id))
            button.configure(
                text_color=PRIMARY if tab_id == self.active_tab else TEXT_SECONDARY
            )

    def get_tab_color(self, tab_id):
        return "#1e293b" if tab_id == self.active_tab else DARK_PANEL
