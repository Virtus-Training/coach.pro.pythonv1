from __future__ import annotations

import logging
import re
import uuid
from datetime import date
from typing import Any, Dict, Optional

from models.session import Block, BlockItem, Session
from repositories.sessions_repo import SessionsRepository


class SessionService:
    def __init__(self, repo: SessionsRepository) -> None:
        self.repo = repo

    def save_session_from_dto(
        self, session_dto: Dict[str, Any], client_id: Optional[int]
    ) -> None:
        session = self._dto_to_session(session_dto, client_id)
        self.repo.save(session)

    def get_session_by_id(self, session_id: str) -> Session | None:
        return self.repo.get_by_id(session_id)

    def _dto_to_session(self, dto: Dict[str, Any], client_id: Optional[int]) -> Session:
        session_id = uuid.uuid4().hex
        meta = dto.get("meta", {})
        label = meta.get("title", "Séance")
        duration_sec = self._parse_minutes(meta.get("duration")) * 60
        mode = "INDIVIDUEL" if client_id else "COLLECTIF"
        session = Session(
            session_id=session_id,
            mode=mode,
            label=label,
            duration_sec=duration_sec,
            date_creation=meta.get("date") or date.today().isoformat(),
            client_id=client_id,
            blocks=[],
            meta=meta,
        )
        for idx, blk in enumerate(dto.get("blocks", []), start=1):
            block_id = f"{session_id}-b{idx}"
            block = Block(
                block_id=block_id,
                type=blk.get("format", ""),
                duration_sec=self._parse_minutes(blk.get("duration")) * 60,
                title=blk.get("title"),
                items=[],
            )
            for ex in blk.get("exercises", []):
                prescription: Dict[str, Any] = {}
                reps = ex.get("reps")
                if isinstance(reps, str):
                    if "reps" in reps:
                        prescription["reps"] = self._parse_int(reps)
                    elif reps.endswith("s"):
                        prescription["work_sec"] = self._parse_int(reps)
                rest = ex.get("repos_s")
                if rest is not None:
                    prescription["rest_sec"] = rest
                item = BlockItem(
                    exercise_id=str(ex.get("id")),
                    prescription=prescription,
                )
                block.items.append(item)
            session.blocks.append(block)
        return session

    @staticmethod
    def _parse_minutes(text: Optional[str]) -> int:
        if not text:
            return 0
        match = re.search(r"\d+", text)
        if not match:
            logging.warning("Unable to parse minutes from %r", text)
            return 0
        try:
            return int(match.group(0))
        except (ValueError, TypeError):
            logging.warning("Invalid minutes value %r", text)
            return 0

    @staticmethod
    def _parse_int(text: str) -> int:
        match = re.search(r"\d+", text)
        if not match:
            logging.warning("Unable to parse integer from %r", text)
            return 0
        try:
            return int(match.group(0))
        except (ValueError, TypeError):
            logging.warning("Invalid integer value %r", text)
            return 0
