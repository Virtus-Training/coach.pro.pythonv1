# repositories/client_repo.py (CORRIGÉ)

import sqlite3
from typing import List, Optional
from models.client import Client

class ClientRepository:
    def __init__(self, db_path="coach.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def list_all(self) -> List[Client]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY nom, prenom")
        rows = cursor.fetchall()
        conn.close()

        clients = []
        for row in rows:
            clients.append(
                Client(
                    id=row["id"],
                    nom=row["nom"],
                    prenom=row["prenom"],
                    email=row["email"],
                    date_naissance=row["date_naissance"],
                    objectifs=row["objectifs"],
                    antecedents_medicaux=row["antecedents_medicaux"],
                )
            )
        return clients

    def find_by_id(self, client_id: int) -> Optional[Client]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Client(
                id=row["id"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                date_naissance=row["date_naissance"],
                objectifs=row["objectifs"],
                antecedents_medicaux=row["antecedents_medicaux"],
            )
        return None

    def add(self, client: Client) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (prenom, nom, email, date_naissance) VALUES (?, ?, ?, ?)",
            (client.prenom, client.nom, client.email, client.date_naissance),
        )
        conn.commit()
        conn.close()

    def update(self, client: Client) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE clients
            SET prenom = ?, nom = ?, email = ?, date_naissance = ?
            WHERE id = ?
            """,
            (client.prenom, client.nom, client.email, client.date_naissance, client.id),
        )
        conn.commit()
        conn.close()

    def update_anamnese(
        self, client_id: int, objectifs: str, antecedents: str
    ) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE clients
            SET objectifs = ?, antecedents_medicaux = ?
            WHERE id = ?
            """,
            (objectifs, antecedents, client_id),
        )
        conn.commit()
        conn.close()

    def update_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM client_exercice_exclusions WHERE client_id = ?", (client_id,)
        )
        if exercice_ids:
            values = [(client_id, ex_id) for ex_id in exercice_ids]
            cursor.executemany(
                "INSERT INTO client_exercice_exclusions (client_id, exercice_id) VALUES (?, ?)",
                values,
            )
        conn.commit()
        conn.close()

    def get_exclusions(self, client_id: int) -> List[int]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT exercice_id FROM client_exercice_exclusions WHERE client_id = ?",
            (client_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [row["exercice_id"] for row in rows]
