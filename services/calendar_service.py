from __future__ import annotations

import uuid
from typing import List

from models.session import Block, BlockItem, Session
from repositories.sessions_repo import SessionsRepository


class CalendarService:
    def __init__(self, repo: SessionsRepository) -> None:
        self.repo = repo

    def get_sessions_for_month(self, year: int, month: int) -> List[Session]:
        return self.repo.list_sessions_for_month(year, month)

    def get_unscheduled_sessions(self) -> List[Session]:
        return self.repo.list_templates()

    def schedule_session(self, template_id: str, year: int, month: int, day: int) -> None:
        template = self.repo.get_by_id(template_id)
        if not template:
            return
        new_session_id = uuid.uuid4().hex
        new_blocks = []
        for idx, blk in enumerate(template.blocks, start=1):
            new_block_id = f"{new_session_id}-b{idx}"
            items = [
                BlockItem(
                    exercise_id=it.exercise_id,
                    prescription=it.prescription.copy(),
                    notes=it.notes,
                )
                for it in blk.items
            ]
            new_blocks.append(
                Block(
                    block_id=new_block_id,
                    type=blk.type,
                    duration_sec=blk.duration_sec,
                    rounds=blk.rounds,
                    work_sec=blk.work_sec,
                    rest_sec=blk.rest_sec,
                    items=items,
                    title=blk.title,
                    locked=blk.locked,
                )
            )
        date_str = f"{year:04d}-{month:02d}-{day:02d} 12:00:00"
        new_session = Session(
            session_id=new_session_id,
            mode=template.mode,
            label=template.label,
            duration_sec=template.duration_sec,
            date_creation=date_str,
            client_id=None,
            is_template=False,
            blocks=new_blocks,
            meta={},
        )
        self.repo.save(new_session)
