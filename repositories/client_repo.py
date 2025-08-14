import sqlite3
from typing import List

from models.client import Client

DB_PATH = "coach.db"


class ClientRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def list_all(self) -> List[Client]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM clients ORDER BY nom, prenom"
            ).fetchall()
        return [
            Client(
                id=row["id"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                date_naissance=row["date_naissance"],
            )
            for row in rows
        ]
