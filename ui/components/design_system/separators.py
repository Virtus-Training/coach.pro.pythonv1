import customtkinter as ctk


class Divider(ctk.CTkFrame):
    """Fine horizontal divider using theme subtle border color."""

    def __init__(self, master, pad_y: tuple[int, int] | None = (8, 8)):
        color = ctk.ThemeManager.theme["color"].get("subtle_border", "#374151")
        super().__init__(master, height=1, fg_color=color, corner_radius=0)
        self.pack_propagate(False)
        if pad_y is not None:
            self._default_pad = pad_y
        else:
            self._default_pad = (0, 0)

    def pack(self, *args, **kwargs):  # type: ignore[override]
        if "fill" not in kwargs:
            kwargs["fill"] = "x"
        if "padx" not in kwargs:
            kwargs["padx"] = 0
        if "pady" not in kwargs:
            kwargs["pady"] = self._default_pad
        return super().pack(*args, **kwargs)
