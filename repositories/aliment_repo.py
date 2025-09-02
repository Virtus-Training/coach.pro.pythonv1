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

    def get_by_name(self, name: str) -> Optional[Aliment]:
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM aliments WHERE nom = ?",
                (name,),
            ).fetchone()
        if not row:
            return None
        return Aliment(
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

    def create(self, a: Aliment) -> int:
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                (
                    "INSERT INTO aliments (nom, categorie, type_alimentation, kcal_100g, "
                    "proteines_100g, glucides_100g, lipides_100g, fibres_100g, unite_base, "
                    "indice_healthy, indice_commun) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
                ),
                (
                    a.nom,
                    a.categorie,
                    a.type_alimentation,
                    a.kcal_100g,
                    a.proteines_100g,
                    a.glucides_100g,
                    a.lipides_100g,
                    a.fibres_100g,
                    a.unite_base,
                    a.indice_healthy,
                    a.indice_commun,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def update(self, a: Aliment) -> None:
        with db_manager.get_connection() as conn:
            conn.execute(
                (
                    "UPDATE aliments SET nom=?, categorie=?, type_alimentation=?, kcal_100g=?, "
                    "proteines_100g=?, glucides_100g=?, lipides_100g=?, fibres_100g=?, unite_base=?, "
                    "indice_healthy=?, indice_commun=? WHERE id = ?"
                ),
                (
                    a.nom,
                    a.categorie,
                    a.type_alimentation,
                    a.kcal_100g,
                    a.proteines_100g,
                    a.glucides_100g,
                    a.lipides_100g,
                    a.fibres_100g,
                    a.unite_base,
                    a.indice_healthy,
                    a.indice_commun,
                    a.id,
                ),
            )
            conn.commit()

    def delete(self, aliment_id: int) -> None:
        with db_manager.get_connection() as conn:
            conn.execute("DELETE FROM portions WHERE aliment_id = ?", (aliment_id,))
            conn.execute("DELETE FROM aliments WHERE id = ?", (aliment_id,))
            conn.commit()

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
