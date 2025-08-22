import customtkinter as ctk


class PdfPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(
            self,
            text="Ma Section",
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["H2"]),
        ).pack()
