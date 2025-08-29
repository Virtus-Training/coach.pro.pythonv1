"""Generic modal window for forms."""

from typing import Any, Callable

import customtkinter as ctk

from exceptions.validation_error import ValidationError
from ui.components.design_system import PrimaryButton, SecondaryButton


class BaseFormModal(ctk.CTkToplevel):
    """Base modal handling form fields and save/cancel actions.

    Parameters
    ----------
    form_fields:
        Mapping of field identifiers to callables. Each callable receives the
        form frame as master and must return a widget exposing `get_value`,
        `set_value`, `show_error` and `hide_error` methods (like
        :class:`LabeledInput`).
    """

    def __init__(
        self,
        parent,
        title: str,
        form_fields: dict[str, Callable[[ctk.CTkFrame], Any]],
        save_callback: Callable[[dict[str, Any]], None],
    ) -> None:
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        fonts = ctk.ThemeManager.theme["font"]
        self.title(title)
        self.configure(fg_color=colors["surface_dark"])
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)

        self.form_fields: dict[str, Any] = {
            key: factory(form_frame) for key, factory in form_fields.items()
        }
        self.save_callback = save_callback

        for row, field in enumerate(self.form_fields.values()):
            field.grid(row=row, column=0, sticky="ew", pady=(0, 10))

        self.general_error_label = ctk.CTkLabel(
            self,
            text="",
            text_color=colors["error"],
            font=ctk.CTkFont(**fonts["Small"]),
        )
        self.general_error_label.pack(padx=20)
        self.general_error_label.pack_forget()

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        SecondaryButton(button_frame, text="Annuler", command=self.destroy).pack(
            side="left", padx=5
        )
        PrimaryButton(button_frame, text="Enregistrer", command=self._on_save).pack(
            side="left", padx=5
        )

        self.update_idletasks()
        self.geometry(f"400x{self.winfo_height()}")

    def _on_save(self) -> None:
        self._hide_general_error()
        data: dict[str, Any] = {}
        for key, field in self.form_fields.items():
            if hasattr(field, "hide_error"):
                field.hide_error()
            value = field.get_value()
            data[key] = value or None
        try:
            self.save_callback(data)
            self.destroy()
        except ValidationError as err:
            for field_id, message in err.errors.items():
                field = self.form_fields.get(field_id)
                if field and hasattr(field, "show_error"):
                    field.show_error(message)
        except Exception as exc:  # pylint: disable=broad-except
            self._show_general_error(str(exc))

    def _show_general_error(self, message: str) -> None:
        self.general_error_label.configure(text=message)
        self.general_error_label.pack(padx=20, pady=(0, 10))

    def _hide_general_error(self) -> None:
        self.general_error_label.pack_forget()
