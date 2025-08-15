import sqlite3
from typing import List

from models.aliment import Aliment

DB_PATH = "coach.db"


class AlimentRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def list_all(self) -> List[Aliment]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM aliments ORDER BY nom"
            ).fetchall()
        return [
            Aliment(
                id=row["id"],
                nom=row["nom"],
                categorie=row["categorie"],
                type_alimentation=row["type_alimentation"],
                kcal_100g=row["kcal_100g"],
                proteines_100g=row["proteines_100g"],
                glucides_100g=row["glucides_100g"],
                lipides_100g=row["lipides_100g"],
                fibres_100g=row["fibres_100g"],
                unite_base=row["unite_base"],
                indice_healthy=row["indice_healthy"],
                indice_commun=row["indice_commun"],
            )
            for row in rows
        ]
