import customtkinter as ctk
from ui.theme.fonts import get_section_font

class BillingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Ma Section", font=get_section_font()).pack()

