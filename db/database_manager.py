import sqlite3

DB_PATH = "coach.db"


class DatabaseManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


db_manager = DatabaseManager(DB_PATH)
