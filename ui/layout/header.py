# ui/layout/header.py

import customtkinter as ctk

from utils.icon_loader import load_icon
from ui.theme import colors, fonts


class Header(ctk.CTkFrame):
    def __init__(self, parent, title: str = ""):
        super().__init__(parent, height=60, fg_color=colors.NEUTRAL_800)
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            text_color=colors.TEXT,
            font=fonts.get_title_font(),
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        user_frame = ctk.CTkFrame(self, fg_color="transparent")
        user_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        user_icon = load_icon("user1.png", 24)
        ctk.CTkLabel(
            user_frame,
            text="Coach",
            image=user_icon,
            compound="left",
            text_color=colors.TEXT_SECONDARY,
            font=fonts.get_text_font(),
        ).pack()

    def update_title(self, new_title: str) -> None:
        self.title_label.configure(text=new_title)
