import sqlite3, json
from typing import List
from models.session import Session, Block, BlockItem

DB_PATH = "coach.db"

class SessionsRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def save(self, s: Session) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO sessions(session_id, mode, label, duration_sec) VALUES (?,?,?,?)",
                         (s.session_id, s.mode, s.label, s.duration_sec))
            for b in s.blocks:
                conn.execute("""INSERT OR REPLACE INTO session_blocks
                    (block_id, session_id, type, duration_sec, rounds, work_sec, rest_sec, title, locked)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (b.block_id, s.session_id, b.type, b.duration_sec, b.rounds, b.work_sec, b.rest_sec, b.title, int(b.locked)))
                for it in b.items:
                    conn.execute("""INSERT INTO session_items(block_id, exercise_id, prescription, notes)
                                    VALUES (?,?,?,?)""",
                                 (b.block_id, it.exercise_id, json.dumps(it.prescription, ensure_ascii=False), it.notes or None))
            conn.commit()
