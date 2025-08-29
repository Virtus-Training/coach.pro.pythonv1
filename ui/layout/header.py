# ui/layout/header.py

import customtkinter as ctk

from utils.icon_loader import load_icon


class Header(ctk.CTkFrame):
    def __init__(self, parent, title: str = ""):
        super().__init__(
            parent,
            height=60,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
        )
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H1"]),
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
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
        ).pack()

    def update_title(self, new_title: str) -> None:
        self.title_label.configure(text=new_title)
