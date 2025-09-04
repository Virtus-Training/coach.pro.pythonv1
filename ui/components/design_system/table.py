"""Reusable DataTable component for the design system."""

from __future__ import annotations

from typing import Any, Iterable, List

import customtkinter as ctk


class DataTable(ctk.CTkFrame):
    """Generic table widget with sortable columns, filtering and selection.

    Optional callback on row selection can be provided via `on_select`.
    """

    def __init__(
        self,
        master,
        headers: List[str],
        data: Iterable[Iterable[Any]],
        on_select: callable | None = None,
    ):
        super().__init__(master, fg_color="transparent")

        self.headers = list(headers)
        self.original_data = [list(row) for row in data]
        self.data = list(self.original_data)
        self.sort_column: int | None = None
        self.sort_reverse = False
        self.on_select = on_select
        self.selected_index: int | None = None

        self.theme = ctk.ThemeManager.theme["DataTable"]
        header_font = ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])

        self.header_frame = ctk.CTkFrame(self, fg_color=self.theme["header_fg_color"])
        self.header_frame.pack(fill="x")

        self.body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure(0, weight=1)

        self.header_buttons: list[ctk.CTkButton] = []
        for idx, title in enumerate(self.headers):
            btn = ctk.CTkButton(
                self.header_frame,
                text=title,
                fg_color=self.theme["header_fg_color"],
                hover_color=self.theme["header_fg_color"],
                text_color=self.theme["header_text_color"],
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
            bg = (
                self.theme["row_even_fg_color"]
                if r % 2 == 0
                else self.theme["row_odd_fg_color"]
            )
            sel_bg = self.theme.get(
                "row_selected_fg_color", self.theme["row_hover_fg_color"]
            )
            is_selected = self.selected_index == r
            row_frame = ctk.CTkFrame(
                self.body, fg_color=(sel_bg if is_selected else bg)
            )
            row_frame.grid(row=r, column=0, sticky="ew")
            row_frame.bind(
                "<Enter>",
                lambda _e, f=row_frame: f.configure(
                    fg_color=self.theme["row_hover_fg_color"]
                ),
            )
            row_frame.bind(
                "<Leave>",
                lambda _e,
                f=row_frame,
                color=(sel_bg if is_selected else bg): f.configure(fg_color=color),
            )
            if self.on_select is not None:

                def _make_click(idx: int, rf: ctk.CTkFrame):
                    def _cb(_e=None):
                        self.selected_index = idx
                        # re-render to update selection highlighting
                        self._render_rows()
                        try:
                            self.on_select(idx, self.data[idx])
                        except Exception:
                            pass

                    return _cb

                row_frame.bind("<Button-1>", _make_click(r, row_frame))
            for c, value in enumerate(row):
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    text_color=self.theme["row_text_color"],
                )
                lbl.grid(row=0, column=c, padx=5, pady=2, sticky="w")
                row_frame.grid_columnconfigure(c, weight=1)
                if self.on_select is not None:
                    lbl.bind("<Button-1>", _make_click(r, row_frame))

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

        try:
            [float(row[col]) for row in self.data]
        except (TypeError, ValueError):

            def key(row):
                return str(row[col]).lower()
        else:

            def key(row):
                return float(row[col])

        self.data.sort(key=key, reverse=self.sort_reverse)

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

        self.selected_index = None
        self._update_header_arrows()
        self._render_rows()


__all__ = ["DataTable"]
