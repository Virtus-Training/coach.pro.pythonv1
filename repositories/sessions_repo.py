import json

from db.database_manager import db_manager
from models.session import Block, BlockItem, Session


class SessionsRepository:
    def save(self, s: Session) -> None:
        with db_manager.get_connection() as conn:
            try:
                conn.execute("BEGIN")
                conn.execute(
                    "INSERT OR REPLACE INTO sessions("\
                    "session_id, client_id, mode, label, duration_sec, date_creation, is_template"\
                    ") VALUES (?,?,?,?,?,?,?)",
                    (
                        s.session_id,
                        s.client_id,
                        s.mode,
                        s.label,
                        s.duration_sec,
                        s.date_creation,
                        int(s.is_template),
                    ),
                )
                for b in s.blocks:
                    conn.execute(
                        """INSERT OR REPLACE INTO session_blocks
                        (block_id, session_id, type, duration_sec, rounds, work_sec, rest_sec, title, locked)
                        VALUES (?,?,?,?,?,?,?,?,?)""",
                        (
                            b.block_id,
                            s.session_id,
                            b.type,
                            b.duration_sec,
                            b.rounds,
                            b.work_sec,
                            b.rest_sec,
                            b.title,
                            int(b.locked),
                        ),
                    )
                    for it in b.items:
                        conn.execute(
                            """INSERT INTO session_items(block_id, exercise_id, prescription, notes)
                                        VALUES (?,?,?,?)""",
                            (
                                b.block_id,
                                it.exercise_id,
                                json.dumps(it.prescription, ensure_ascii=False),
                                it.notes or None,
                            ),
                        )
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def list_sessions_for_month(self, year: int, month: int) -> list[Session]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM sessions
                WHERE strftime('%Y', date_creation) = ?
                  AND strftime('%m', date_creation) = ?
                ORDER BY date_creation
                """,
                (str(year), f"{month:02d}"),
            ).fetchall()
            sessions: list[Session] = []
            for s in rows:
                block_rows = conn.execute(
                    "SELECT * FROM session_blocks WHERE session_id = ?",
                    (s["session_id"],),
                ).fetchall()
                blocks = []
                for b in block_rows:
                    item_rows = conn.execute(
                        "SELECT * FROM session_items WHERE block_id = ?",
                        (b["block_id"],),
                    ).fetchall()
                    items = [
                        BlockItem(
                            exercise_id=r["exercise_id"],
                            prescription=json.loads(r["prescription"]),
                            notes=r["notes"],
                        )
                        for r in item_rows
                    ]
                    blocks.append(
                        Block(
                            block_id=b["block_id"],
                            type=b["type"],
                            duration_sec=b["duration_sec"],
                            rounds=b["rounds"],
                            work_sec=b["work_sec"],
                            rest_sec=b["rest_sec"],
                            items=items,
                            title=b["title"],
                            locked=bool(b["locked"]),
                        )
                    )
                sessions.append(
                    Session(
                        session_id=s["session_id"],
                        mode=s["mode"],
                        label=s["label"],
                        duration_sec=s["duration_sec"],
                        date_creation=s["date_creation"],
                        client_id=s["client_id"],
                        is_template=bool(s["is_template"]),
                        blocks=blocks,
                        meta={},
                    )
                )
            return sessions

    def list_templates(self) -> list[Session]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM sessions WHERE is_template = 1 ORDER BY label"
            ).fetchall()
            return [
                Session(
                    session_id=r["session_id"],
                    mode=r["mode"],
                    label=r["label"],
                    duration_sec=r["duration_sec"],
                    date_creation=r["date_creation"],
                    client_id=r["client_id"],
                    is_template=bool(r["is_template"]),
                    blocks=[],
                    meta={},
                )
                for r in rows
            ]

    def get_by_id(self, session_id: str) -> Session | None:
        with db_manager.get_connection() as conn:
            s = conn.execute(
                "SELECT * FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            if not s:
                return None
            block_rows = conn.execute(
                "SELECT * FROM session_blocks WHERE session_id = ?",
                (session_id,),
            ).fetchall()
            blocks = []
            for b in block_rows:
                item_rows = conn.execute(
                    "SELECT * FROM session_items WHERE block_id = ?",
                    (b["block_id"],),
                ).fetchall()
                items = [
                    BlockItem(
                        exercise_id=r["exercise_id"],
                        prescription=json.loads(r["prescription"]),
                        notes=r["notes"],
                    )
                    for r in item_rows
                ]
                blocks.append(
                    Block(
                        block_id=b["block_id"],
                        type=b["type"],
                        duration_sec=b["duration_sec"],
                        rounds=b["rounds"],
                        work_sec=b["work_sec"],
                        rest_sec=b["rest_sec"],
                        items=items,
                        title=b["title"],
                        locked=bool(b["locked"]),
                    )
                )
            return Session(
                session_id=s["session_id"],
                mode=s["mode"],
                label=s["label"],
                duration_sec=s["duration_sec"],
                date_creation=s["date_creation"],
                client_id=s["client_id"],
                is_template=bool(s["is_template"]),
                blocks=blocks,
                meta={},
            )

    def count_sessions_this_month(self) -> int:
        with db_manager.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT COUNT(*)
                FROM sessions
                WHERE strftime('%Y-%m', date_creation) = strftime('%Y-%m', 'now')
                """
            )
            (count,) = cursor.fetchone()
        return count
