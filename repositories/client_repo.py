# repositories/client_repo.py (CORRIGÉ)

from typing import List, Optional

from db.database_manager import db_manager
from models.client import Client


class ClientRepository:
    def count_all(self) -> int:
        with db_manager.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM clients")
            (count,) = cursor.fetchone()
        return count

    def list_all(self) -> List[Client]:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY nom, prenom")
            rows = cursor.fetchall()

        clients: List[Client] = []
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
                    sexe=row["sexe"],
                    poids_kg=row["poids_kg"],
                    taille_cm=row["taille_cm"],
                    niveau_activite=row["niveau_activite"],
                )
            )
        return clients

    def find_by_id(self, client_id: int) -> Optional[Client]:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            row = cursor.fetchone()

        if row:
            return Client(
                id=row["id"],
                nom=row["nom"],
                prenom=row["prenom"],
                email=row["email"],
                date_naissance=row["date_naissance"],
                objectifs=row["objectifs"],
                antecedents_medicaux=row["antecedents_medicaux"],
                sexe=row["sexe"],
                poids_kg=row["poids_kg"],
                taille_cm=row["taille_cm"],
                niveau_activite=row["niveau_activite"],
            )
        return None

    def add(self, client: Client) -> None:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clients (prenom, nom, email, date_naissance) VALUES (?, ?, ?, ?)",
                (client.prenom, client.nom, client.email, client.date_naissance),
            )
            conn.commit()

    def update(self, client: Client) -> None:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE clients
                SET prenom = ?, nom = ?, email = ?, date_naissance = ?
                WHERE id = ?
                """,
                (
                    client.prenom,
                    client.nom,
                    client.email,
                    client.date_naissance,
                    client.id,
                ),
            )
            conn.commit()

    def delete(self, client_id: int) -> None:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()

    def update_anamnese(self, client_id: int, objectifs: str, antecedents: str) -> None:
        with db_manager.get_connection() as conn:
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

    def update_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM client_exercice_exclusions WHERE client_id = ?",
                (client_id,),
            )
            if exercice_ids:
                values = [(client_id, ex_id) for ex_id in exercice_ids]
                cursor.executemany(
                    "INSERT INTO client_exercice_exclusions (client_id, exercice_id) VALUES (?, ?)",
                    values,
                )
            conn.commit()

    def get_exclusions(self, client_id: int) -> List[int]:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT exercice_id FROM client_exercice_exclusions WHERE client_id = ?",
                (client_id,),
            )
            rows = cursor.fetchall()
        return [row["exercice_id"] for row in rows]
