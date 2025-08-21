from __future__ import annotations

import calendar
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
    ) -> None:
        super().__init__(parent)
        self.on_session_click = on_session_click

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
        self.month_label.configure(text=f"{MONTHS_FR[month]} {year}")
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(year, month)
        for r in range(6):
            for c in range(7):
                cell = self.cells[r][c]
                for w in cell.winfo_children():
                    w.destroy()
                day = weeks[r][c] if r < len(weeks) else 0
                if day == 0:
                    continue
                ctk.CTkLabel(cell, text=str(day)).pack(anchor="ne", padx=2, pady=2)
                for sess in data.get(day, []):
                    ctk.CTkButton(
                        cell,
                        text=sess.label,
                        anchor="w",
                        command=lambda sid=sess.session_id: self._handle_session_click(
                            sid
                        ),
                    ).pack(anchor="w", padx=2)

    def _handle_session_click(self, session_id: str) -> None:
        if self.on_session_click:
            self.on_session_click(session_id)
