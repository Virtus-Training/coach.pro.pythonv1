from typing import List, Optional

from db.database_manager import db_manager
from models.aliment import Aliment
from models.portion import Portion


class AlimentRepository:

    def list_all(self) -> List[Aliment]:
        with db_manager.get_connection() as conn:
            rows = conn.execute("SELECT * FROM aliments ORDER BY nom").fetchall()
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

    def get_portions_for_aliment(self, aliment_id: int) -> List[Portion]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM portions WHERE aliment_id = ? ORDER BY id",
                (aliment_id,),
            ).fetchall()
        return [
            Portion(
                id=row["id"],
                aliment_id=row["aliment_id"],
                description=row["description"],
                grammes_equivalents=row["grammes_equivalents"],
            )
            for row in rows
        ]

    def get_portion_by_id(self, portion_id: int) -> Optional[Portion]:
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM portions WHERE id = ?", (portion_id,)
            ).fetchone()
        if not row:
            return None
        return Portion(
            id=row["id"],
            aliment_id=row["aliment_id"],
            description=row["description"],
            grammes_equivalents=row["grammes_equivalents"],
        )

    def search_by_name(self, query: str) -> List[Aliment]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM aliments WHERE nom LIKE ? ORDER BY nom",
                (f"%{query}%",),
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
