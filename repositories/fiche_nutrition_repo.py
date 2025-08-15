import sqlite3
from typing import Optional

from models.fiche_nutrition import FicheNutrition

DB_PATH = "coach.db"


class FicheNutritionRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, fiche: FicheNutrition) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO fiches_nutrition (
                    client_id, poids_kg_mesure, objectif,
                    proteines_cible_g_par_kg, ratio_glucides_lipides_cible,
                    maintenance_kcal, objectif_kcal,
                    proteines_g, glucides_g, lipides_g
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fiche.client_id,
                    fiche.poids_kg_mesure,
                    fiche.objectif,
                    fiche.proteines_cible_g_par_kg,
                    fiche.ratio_glucides_lipides_cible,
                    fiche.maintenance_kcal,
                    fiche.objectif_kcal,
                    fiche.proteines_g,
                    fiche.glucides_g,
                    fiche.lipides_g,
                ),
            )
            conn.commit()
            return cur.lastrowid

    def get_last_for_client(self, client_id: int) -> Optional[FicheNutrition]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM fiches_nutrition WHERE client_id = ? ORDER BY date_creation DESC LIMIT 1",
                (client_id,),
            ).fetchone()
            if not row:
                return None
            return FicheNutrition(
                id=row["id"],
                client_id=row["client_id"],
                date_creation=row["date_creation"],
                poids_kg_mesure=row["poids_kg_mesure"],
                objectif=row["objectif"],
                proteines_cible_g_par_kg=row["proteines_cible_g_par_kg"],
                ratio_glucides_lipides_cible=row["ratio_glucides_lipides_cible"],
                maintenance_kcal=row["maintenance_kcal"],
                objectif_kcal=row["objectif_kcal"],
                proteines_g=row["proteines_g"],
                glucides_g=row["glucides_g"],
                lipides_g=row["lipides_g"],
            )
