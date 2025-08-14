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

    def add(self, client: Client) -> None:
        """Insère un nouveau client dans la base de données."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO clients (nom, prenom, email, date_naissance) VALUES (?, ?, ?, ?)",
                (client.nom, client.prenom, client.email, client.date_naissance),
            )
            conn.commit()

    def update(self, client: Client) -> None:
        """Met à jour un client existant basé sur son identifiant."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE clients SET nom = ?, prenom = ?, email = ?, date_naissance = ? WHERE id = ?",
                (client.nom, client.prenom, client.email, client.date_naissance, client.id),
            )
            conn.commit()
