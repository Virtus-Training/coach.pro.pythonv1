"""Form components for the design system."""

import customtkinter as ctk


class LabeledInput(ctk.CTkFrame):
    """Input field with a label and error management."""

    def __init__(self, master, label: str, **entry_kwargs):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)

        colors = ctk.ThemeManager.theme["color"]
        fonts = ctk.ThemeManager.theme["font"]

        self._label = ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(**fonts["Body"]),
            text_color=colors["primary_text"],
        )
        self._label.grid(row=0, column=0, sticky="w")

        self.entry = ctk.CTkEntry(
            self,
            border_color=colors["subtle_border"],
            **entry_kwargs,
        )
        self.entry.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(**fonts["Small"]),
            text_color=colors["error"],
        )
        self.error_label.grid(row=2, column=0, sticky="w")
        self.error_label.grid_remove()

    def get_value(self) -> str:
        return self.entry.get().strip()

    def set_value(self, value: str) -> None:
        self.entry.delete(0, "end")
        if value is not None:
            self.entry.insert(0, value)

    def show_error(self, message: str) -> None:
        self.error_label.configure(text=message)
        self.error_label.grid()
        self.entry.configure(border_color=colors["error"])

    def hide_error(self) -> None:
        self.error_label.grid_remove()
        self.entry.configure(border_color=colors["subtle_border"])
