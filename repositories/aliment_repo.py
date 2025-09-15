from typing import Dict, List, Optional, Tuple

from db.database_manager import db_manager
from models.aliment import Aliment
from models.portion import Portion


class AlimentRepository:
    def _row_to_aliment(self, row) -> Aliment:
        """Convertit une ligne de base de données en objet Aliment"""
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

    def list_all(self) -> List[Aliment]:
        with db_manager.get_connection() as conn:
            rows = conn.execute("SELECT * FROM aliments ORDER BY nom").fetchall()
        return [self._row_to_aliment(row) for row in rows]

    def get_by_id(self, aliment_id: int) -> Optional[Aliment]:
        """Récupère un aliment par son ID"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM aliments WHERE id = ?",
                (aliment_id,),
            ).fetchone()
        return self._row_to_aliment(row) if row else None

    def get_by_name(self, name: str) -> Optional[Aliment]:
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM aliments WHERE nom = ?",
                (name,),
            ).fetchone()
        return self._row_to_aliment(row) if row else None

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
        """Recherche d'aliments par nom (recherche floue)"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM aliments WHERE nom LIKE ? ORDER BY nom",
                (f"%{query}%",),
            ).fetchall()
        return [self._row_to_aliment(row) for row in rows]

    def search_advanced(
        self,
        query: Optional[str] = None,
        categorie: Optional[str] = None,
        min_proteines: Optional[float] = None,
        max_kcal: Optional[float] = None,
        min_fibres: Optional[float] = None,
        regime_compatible: Optional[str] = None,
        limit: int = 50,
    ) -> List[Aliment]:
        """Recherche avancée avec filtres multiples"""

        conditions = []
        params = []

        if query:
            conditions.append("nom LIKE ?")
            params.append(f"%{query}%")

        if categorie:
            conditions.append("categorie = ?")
            params.append(categorie)

        if min_proteines is not None:
            conditions.append("proteines_100g >= ?")
            params.append(min_proteines)

        if max_kcal is not None:
            conditions.append("kcal_100g <= ?")
            params.append(max_kcal)

        if min_fibres is not None:
            conditions.append("fibres_100g >= ?")
            params.append(min_fibres)

        if regime_compatible:
            conditions.append("(type_alimentation = ? OR type_alimentation IS NULL)")
            params.append(regime_compatible)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query_sql = f"""
            SELECT * FROM aliments
            WHERE {where_clause}
            ORDER BY indice_healthy DESC, indice_commun DESC, nom
            LIMIT ?
        """

        params.append(limit)

        with db_manager.get_connection() as conn:
            rows = conn.execute(query_sql, params).fetchall()

        return [self._row_to_aliment(row) for row in rows]

    def get_by_categories(self, categories: List[str]) -> Dict[str, List[Aliment]]:
        """Récupère les aliments groupés par catégories"""
        result = {cat: [] for cat in categories}

        placeholders = ",".join("?" * len(categories))

        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM aliments WHERE categorie IN ({placeholders}) ORDER BY categorie, nom",
                categories,
            ).fetchall()

        for row in rows:
            aliment = self._row_to_aliment(row)
            if aliment.categorie in result:
                result[aliment.categorie].append(aliment)

        return result

    def get_top_by_nutrition(
        self,
        metric: str = "proteines_100g",
        limit: int = 20,
        exclude_categories: Optional[List[str]] = None,
    ) -> List[Aliment]:
        """Récupère le top des aliments selon un critère nutritionnel"""

        allowed_metrics = ["proteines_100g", "fibres_100g", "indice_healthy"]
        if metric not in allowed_metrics:
            raise ValueError(f"Metric must be one of {allowed_metrics}")

        conditions = [f"{metric} > 0"]
        params = []

        if exclude_categories:
            placeholders = ",".join("?" * len(exclude_categories))
            conditions.append(f"categorie NOT IN ({placeholders})")
            params.extend(exclude_categories)

        where_clause = " AND ".join(conditions)

        query_sql = f"""
            SELECT * FROM aliments
            WHERE {where_clause}
            ORDER BY {metric} DESC
            LIMIT ?
        """

        params.append(limit)

        with db_manager.get_connection() as conn:
            rows = conn.execute(query_sql, params).fetchall()

        return [self._row_to_aliment(row) for row in rows]

    def get_complementary_foods(
        self, base_aliment_id: int, objectif_macros: Dict[str, float]
    ) -> List[Tuple[Aliment, float]]:
        """Trouve des aliments complémentaires pour équilibrer les macros"""
        base_aliment = self.get_by_id(base_aliment_id)
        if not base_aliment:
            return []

        # Calcul des déficits en macronutriments
        deficit_proteines = max(
            0, objectif_macros.get("proteines_g", 0) - base_aliment.proteines_100g
        )
        deficit_glucides = max(
            0, objectif_macros.get("glucides_g", 0) - base_aliment.glucides_100g
        )
        deficit_lipides = max(
            0, objectif_macros.get("lipides_g", 0) - base_aliment.lipides_100g
        )

        # Recherche d'aliments complémentaires
        with db_manager.get_connection() as conn:
            query = """
                SELECT *,
                       ABS(proteines_100g - ?) +
                       ABS(glucides_100g - ?) +
                       ABS(lipides_100g - ?) as score_complementaire
                FROM aliments
                WHERE id != ?
                ORDER BY score_complementaire ASC
                LIMIT 10
            """

            rows = conn.execute(
                query,
                (deficit_proteines, deficit_glucides, deficit_lipides, base_aliment_id),
            ).fetchall()

        results = []
        for row in rows:
            aliment = self._row_to_aliment(row)
            score = row["score_complementaire"]
            results.append((aliment, score))

        return results

    def get_statistics(self) -> Dict[str, any]:
        """Retourne des statistiques sur la base d'aliments"""
        with db_manager.get_connection() as conn:
            stats = {
                "total_aliments": conn.execute(
                    "SELECT COUNT(*) FROM aliments"
                ).fetchone()[0],
                "categories": [
                    row[0]
                    for row in conn.execute(
                        "SELECT DISTINCT categorie FROM aliments WHERE categorie IS NOT NULL ORDER BY categorie"
                    ).fetchall()
                ],
                "avg_kcal": conn.execute(
                    "SELECT AVG(kcal_100g) FROM aliments"
                ).fetchone()[0],
                "avg_proteines": conn.execute(
                    "SELECT AVG(proteines_100g) FROM aliments"
                ).fetchone()[0],
                "aliments_riches_proteines": conn.execute(
                    "SELECT COUNT(*) FROM aliments WHERE proteines_100g > 15"
                ).fetchone()[0],
                "aliments_riches_fibres": conn.execute(
                    "SELECT COUNT(*) FROM aliments WHERE fibres_100g > 5"
                ).fetchone()[0],
            }

        return stats
