from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from models.session import Session
from services.calendar_service import CalendarService
from services.session_service import SessionService


class CalendarController:
    def __init__(
        self, calendar_service: CalendarService, session_service: SessionService
    ) -> None:
        self.calendar_service = calendar_service
        self.session_service = session_service

    def get_calendar_data(self, year: int, month: int) -> Dict[int, List[Session]]:
        sessions = self.calendar_service.get_sessions_for_month(year, month)
        data: Dict[int, List[Session]] = {}
        for s in sessions:
            day = datetime.fromisoformat(s.date_creation).day
            data.setdefault(day, []).append(s)
        return data

    def get_session_details(self, session_id: str) -> Session | None:
        return self.session_service.get_session_by_id(session_id)

    def get_unscheduled_sessions(self) -> list[Session]:
        return self.calendar_service.get_unscheduled_sessions()

    def schedule_session(self, session_id: str, year: int, month: int, day: int) -> None:
        self.calendar_service.schedule_session(session_id, year, month, day)
