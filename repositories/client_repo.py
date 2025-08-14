import sqlite3
from typing import List, Optional

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
                objectifs=row.get("objectifs"),
                antecedents_medicaux=row.get("antecedents_medicaux"),
            )
            for row in rows
        ]

    def add(self, client: Client) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                (
                    "INSERT INTO clients (nom, prenom, email, date_naissance, objectifs, antecedents_medicaux) "
                    "VALUES (?, ?, ?, ?, ?, ?)"
                ),
                (
                    client.nom,
                    client.prenom,
                    client.email,
                    client.date_naissance,
                    client.objectifs,
                    client.antecedents_medicaux,
                ),
            )
            conn.commit()

    def update(self, client: Client) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                (
                    "UPDATE clients SET nom = ?, prenom = ?, email = ?, date_naissance = ?, objectifs = ?, antecedents_medicaux = ? "
                    "WHERE id = ?"
                ),
                (
                    client.nom,
                    client.prenom,
                    client.email,
                    client.date_naissance,
                    client.objectifs,
                    client.antecedents_medicaux,
                    client.id,
                ),
            )
            conn.commit()

    def find_by_id(self, client_id: int) -> Optional[Client]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM clients WHERE id = ?",
                (client_id,),
            ).fetchone()
        if row is None:
            return None
        return Client(
            id=row["id"],
            nom=row["nom"],
            prenom=row["prenom"],
            email=row["email"],
            date_naissance=row["date_naissance"],
            objectifs=row["objectifs"],
            antecedents_medicaux=row["antecedents_medicaux"],
        )

    def update_anamnese(self, client_id: int, objectifs: str, antecedents: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE clients SET objectifs = ?, antecedents_medicaux = ? WHERE id = ?",
                (objectifs, antecedents, client_id),
            )
            conn.commit()

    def update_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM client_exercice_exclusions WHERE client_id = ?",
                (client_id,),
            )
            conn.executemany(
                "INSERT INTO client_exercice_exclusions (client_id, exercice_id) VALUES (?, ?)",
                [(client_id, eid) for eid in exercice_ids],
            )
            conn.commit()

    def get_exclusions(self, client_id: int) -> List[int]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT exercice_id FROM client_exercice_exclusions WHERE client_id = ?",
                (client_id,),
            ).fetchall()
        return [r["exercice_id"] for r in rows]
