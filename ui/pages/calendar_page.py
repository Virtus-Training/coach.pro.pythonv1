from __future__ import annotations

import datetime
import customtkinter as ctk

from controllers.calendar_controller import CalendarController
from controllers.session_controller import SessionController
from ui.components.calendar_view import CalendarView
from ui.modals.session_detail_modal import SessionDetailModal
from ui.theme.fonts import get_section_font


class CalendarPage(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        controller: CalendarController,
        session_controller: SessionController,
    ):
        super().__init__(parent)
        self.controller = controller
        self.session_controller = session_controller
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month

        ctk.CTkLabel(self, text="Planning", font=get_section_font()).pack(pady=5)
        self.calendar = CalendarView(
            self, self.on_previous_month, self.on_next_month, self.on_session_click
        )
        self.calendar.pack(fill="both", expand=True)
        self._refresh()

    def _refresh(self) -> None:
        data = self.controller.get_calendar_data(self.year, self.month)
        self.calendar.set_data(self.year, self.month, data)

    def on_session_click(self, session_id: str) -> None:
        session = self.controller.get_session_details(session_id)
        if session:
            SessionDetailModal(self, session, self.session_controller)

    def on_previous_month(self) -> None:
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._refresh()

    def on_next_month(self) -> None:
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._refresh()
