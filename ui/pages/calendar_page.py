from __future__ import annotations

import datetime

import customtkinter as ctk

from controllers.calendar_controller import CalendarController
from controllers.session_controller import SessionController
from controllers.tracking_controller import TrackingController
from ui.components.calendar_view import CalendarView
from ui.components.design_system import HeroBanner
from ui.components.draggable_list import DraggableList
from ui.modals.session_detail_modal import SessionDetailModal
from ui.modals.session_log_modal import SessionLogModal


class CalendarPage(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        controller: CalendarController,
        session_controller: SessionController,
        tracking_controller: TrackingController,
    ):
        super().__init__(parent)
        self.controller = controller
        self.session_controller = session_controller
        self.tracking_controller = tracking_controller
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        hero = HeroBanner(
            self,
            title="Calendrier",
            subtitle="Planifiez et suivez vos séances.",
            icon_path="assets/icons/calendar.png",
        )
        hero.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))

        left = ctk.CTkFrame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        right = ctk.CTkFrame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.dragging_session_id: str | None = None
        self.draggable = DraggableList(left, self.on_drag_start)
        self.draggable.pack(fill="both", expand=True)
        self.calendar = CalendarView(
            right,
            self.on_previous_month,
            self.on_next_month,
            self.on_session_click,
            self.get_dragged_session_id,
            self.on_session_drop,
            self.on_log_session,
        )
        self.calendar.pack(fill="both", expand=True)
        self._refresh()

    def on_drag_start(self, session_id: str) -> None:
        self.dragging_session_id = session_id

    def get_dragged_session_id(self) -> str | None:
        return self.dragging_session_id

    def on_session_drop(self, session_id: str, year: int, month: int, day: int) -> None:
        self.controller.schedule_session(session_id, year, month, day)
        self.dragging_session_id = None
        self._refresh()

    def _refresh(self) -> None:
        data = self.controller.get_calendar_data(self.year, self.month)
        self.calendar.set_data(self.year, self.month, data)
        sessions = self.controller.get_unscheduled_sessions()
        self.draggable.set_sessions(sessions)

    def on_session_click(self, session_id: str) -> None:
        session = self.controller.get_session_details(session_id)
        if session:
            SessionDetailModal(self, session, self.session_controller)

    def on_log_session(self, session_id: str) -> None:
        SessionLogModal(self, session_id, self.tracking_controller)

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

