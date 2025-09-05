from __future__ import annotations

from typing import Callable, List

import customtkinter as ctk

from models.session import Session


class DraggableList(ctk.CTkFrame):
    def __init__(self, parent, on_drag_start: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.on_drag_start = on_drag_start
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

    def set_sessions(self, sessions: List[Session]) -> None:
        for w in self.container.winfo_children():
            w.destroy()
        for sess in sorted(sessions, key=lambda s: s.label.lower()):
            btn = ctk.CTkButton(
                self.container,
                text=sess.label,
                anchor="w",
                fg_color="transparent",
                hover_color="#333333",
                font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
            )
            btn.pack(fill="x", pady=2, padx=2)
            btn.bind(
                "<ButtonPress-1>",
                lambda e, sid=sess.session_id: self.on_drag_start(sid),
            )

