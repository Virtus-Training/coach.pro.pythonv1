from __future__ import annotations

import calendar
from datetime import date
from typing import Callable, Dict, List

import customtkinter as ctk

from models.session import Session


MONTHS_FR = [
    "",
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


class CalendarView(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_previous_month: Callable[[], None],
        on_next_month: Callable[[], None],
        on_session_click: Callable[[str], None] | None = None,
        get_dragged_session_id: Callable[[], str | None] | None = None,
        on_session_drop: Callable[[str, int, int, int], None] | None = None,
        on_log_session: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.on_session_click = on_session_click
        self.get_dragged_session_id = get_dragged_session_id
        self.on_session_drop = on_session_drop
        self.on_log_session = on_log_session

        header = ctk.CTkFrame(self)
        header.pack(fill="x", pady=5)
        ctk.CTkButton(header, text="<", width=40, command=on_previous_month).pack(
            side="left", padx=5
        )
        self.month_label = ctk.CTkLabel(header, text="")
        self.month_label.pack(side="left", expand=True)
        ctk.CTkButton(header, text=">", width=40, command=on_next_month).pack(
            side="right", padx=5
        )

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True)

        for i, name in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            lbl = ctk.CTkLabel(self.grid_frame, text=name)
            lbl.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        self.cells: List[List[ctk.CTkFrame]] = []
        for r in range(1, 7):
            row_cells = []
            for c in range(7):
                cell = ctk.CTkFrame(self.grid_frame, border_width=1, corner_radius=0)
                cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_cells.append(cell)
            self.cells.append(row_cells)

        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(1, 7):
            self.grid_frame.grid_rowconfigure(i, weight=1)

    def set_data(self, year: int, month: int, data: Dict[int, List[Session]]) -> None:
        self.current_year = year
        self.current_month = month
        self.month_label.configure(text=f"{MONTHS_FR[month]} {year}")
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(year, month)
        for r in range(6):
            for c in range(7):
                cell = self.cells[r][c]
                for w in cell.winfo_children():
                    w.destroy()
                day = weeks[r][c] if r < len(weeks) else 0
                cell.unbind("<ButtonRelease-1>")
                if day == 0:
                    continue
                cell.bind("<ButtonRelease-1>", lambda e, d=day: self._handle_drop(d))
                ctk.CTkLabel(cell, text=str(day)).pack(anchor="ne", padx=2, pady=2)
                for sess in data.get(day, []):
                    row = ctk.CTkFrame(cell, fg_color="transparent")
                    row.pack(anchor="w", padx=2, pady=1, fill="x")
                    ctk.CTkButton(
                        row,
                        text=sess.label,
                        anchor="w",
                        command=lambda sid=sess.session_id: self._handle_session_click(
                            sid
                        ),
                    ).pack(side="left", fill="x", expand=True)
                    sess_date = date(year, month, day)
                    if self.on_log_session and sess_date <= date.today():
                        ctk.CTkButton(
                            row,
                            text="+",
                            width=20,
                            command=lambda sid=sess.session_id: self.on_log_session(sid),
                        ).pack(side="left", padx=2)

    def _handle_session_click(self, session_id: str) -> None:
        if self.on_session_click:
            self.on_session_click(session_id)

    def _handle_drop(self, day: int) -> None:
        if not (self.on_session_drop and self.get_dragged_session_id):
            return
        session_id = self.get_dragged_session_id()
        if session_id:
            self.on_session_drop(session_id, self.current_year, self.current_month, day)
