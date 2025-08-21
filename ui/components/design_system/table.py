"""Reusable DataTable component for the design system."""

from __future__ import annotations

from typing import Any, Iterable, List

import customtkinter as ctk

from ui.theme.colors import (
    TABLE_HEADER_BG,
    TABLE_ROW_EVEN_BG,
    TABLE_ROW_ODD_BG,
    TEXT,
)
from ui.theme.fonts import FONT_FAMILY


class DataTable(ctk.CTkFrame):
    """Generic table widget with sortable columns and filtering."""

    def __init__(self, master, headers: List[str], data: Iterable[Iterable[Any]]):
        super().__init__(master, fg_color="transparent")

        self.headers = list(headers)
        self.original_data = [list(row) for row in data]
        self.data = list(self.original_data)
        self.sort_column: int | None = None
        self.sort_reverse = False

        header_font = (FONT_FAMILY, 14, "bold")

        self.header_frame = ctk.CTkFrame(self, fg_color=TABLE_HEADER_BG)
        self.header_frame.pack(fill="x")

        self.body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure(0, weight=1)

        self.header_buttons: list[ctk.CTkButton] = []
        for idx, title in enumerate(self.headers):
            btn = ctk.CTkButton(
                self.header_frame,
                text=title,
                fg_color=TABLE_HEADER_BG,
                hover_color=TABLE_HEADER_BG,
                text_color=TEXT,
                font=header_font,
                corner_radius=0,
                command=lambda c=idx: self._on_header_click(c),
                height=30,
            )
            btn.grid(row=0, column=idx, sticky="nsew", padx=1, pady=1)
            self.header_frame.grid_columnconfigure(idx, weight=1)
            self.header_buttons.append(btn)

        self._render_rows()

    # ------------------------------------------------------------------
    def _render_rows(self) -> None:
        for child in self.body.winfo_children():
            child.destroy()

        for r, row in enumerate(self.data):
            bg = TABLE_ROW_EVEN_BG if r % 2 == 0 else TABLE_ROW_ODD_BG
            row_frame = ctk.CTkFrame(self.body, fg_color=bg)
            row_frame.grid(row=r, column=0, sticky="ew")
            for c, value in enumerate(row):
                lbl = ctk.CTkLabel(row_frame, text=str(value), text_color=TEXT)
                lbl.grid(row=0, column=c, padx=5, pady=2, sticky="w")
                row_frame.grid_columnconfigure(c, weight=1)

    # ------------------------------------------------------------------
    def _on_header_click(self, column: int) -> None:
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        self._sort_data()
        self._update_header_arrows()
        self._render_rows()

    def _sort_data(self) -> None:
        if self.sort_column is None:
            return

        col = self.sort_column

        def sort_key(row: List[Any]):
            value = row[col]
            if isinstance(value, (int, float)):
                return value
            try:
                return float(value)
            except (TypeError, ValueError):
                return str(value).lower()

        self.data.sort(key=sort_key, reverse=self.sort_reverse)

    def _update_header_arrows(self) -> None:
        for idx, btn in enumerate(self.header_buttons):
            text = self.headers[idx]
            if self.sort_column == idx:
                text += " ▲" if not self.sort_reverse else " ▼"
            btn.configure(text=text)

    # ------------------------------------------------------------------
    def filter(self, search_term: str) -> None:
        term = search_term.lower().strip()
        if not term:
            self.data = list(self.original_data)
        else:
            self.data = [
                row
                for row in self.original_data
                if any(term in str(cell).lower() for cell in row)
            ]

        if self.sort_column is not None:
            self._sort_data()

        self._update_header_arrows()
        self._render_rows()


__all__ = ["DataTable"]

