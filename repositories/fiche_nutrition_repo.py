from typing import List, Optional

from db.database_manager import db_manager
from models.fiche_nutrition import FicheNutrition


class FicheNutritionRepository:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or db_manager

    def add(self, fiche: FicheNutrition) -> int:
        with db_manager.get_connection() as conn:
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
        with db_manager.get_connection() as conn:
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

    def get_all_for_client(self, client_id: int) -> List[FicheNutrition]:
        """Get all nutrition sheets for a client"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM fiches_nutrition WHERE client_id = ? ORDER BY date_creation DESC",
                (client_id,),
            ).fetchall()

        fiches = []
        for row in rows:
            fiches.append(FicheNutrition(
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
            ))
        return fiches

    def get_by_id(self, fiche_id: int) -> Optional[FicheNutrition]:
        """Get nutrition sheet by ID"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM fiches_nutrition WHERE id = ?",
                (fiche_id,),
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

    def delete(self, fiche_id: int) -> bool:
        """Delete nutrition sheet"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM fiches_nutrition WHERE id = ?", (fiche_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception:
            return False
