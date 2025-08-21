from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from models.session import Session
from services.calendar_service import CalendarService


class CalendarController:
    def __init__(self, service: CalendarService) -> None:
        self.service = service

    def get_calendar_data(self, year: int, month: int) -> Dict[int, List[Session]]:
        sessions = self.service.get_sessions_for_month(year, month)
        data: Dict[int, List[Session]] = {}
        for s in sessions:
            day = datetime.fromisoformat(s.date_creation).day
            data.setdefault(day, []).append(s)
        return data
