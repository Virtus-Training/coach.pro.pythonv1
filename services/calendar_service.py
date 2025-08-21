from __future__ import annotations

from typing import List

from models.session import Session
from repositories.sessions_repo import SessionsRepository


class CalendarService:
    def __init__(self, repo: SessionsRepository) -> None:
        self.repo = repo

    def get_sessions_for_month(self, year: int, month: int) -> List[Session]:
        return self.repo.list_sessions_for_month(year, month)
