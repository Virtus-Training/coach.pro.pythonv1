from typing import Any, Dict, List, Optional

from db.database_manager import db_manager
from models.exercices import Exercise


def _split_csv(s: str | None) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()] if s else []


class ExerciseRepository:
    def list_all_exercices(self) -> List[Exercise]:
        with db_manager.get_connection() as conn:
            rows = conn.execute("SELECT * FROM exercices ORDER BY nom").fetchall()
        return [
            Exercise(
                id=row["id"],
                nom=row["nom"],
                groupe_musculaire_principal=row["groupe_musculaire_principal"],
                equipement=row["equipement"],
                tags=row["tags"],
                movement_pattern=row.get("movement_pattern")
                if isinstance(row, dict)
                else row["movement_pattern"],
                movement_category=(
                    row.get("movement_category")
                    if isinstance(row, dict)
                    else row["movement_category"]
                    if "movement_category" in row.keys()
                    else None
                ),
                type_effort=row["type_effort"],
                coefficient_volume=row["coefficient_volume"],
                est_chargeable=bool(row["est_chargeable"]),
            )
            for row in rows
        ]

    # Alias for consistency
    def list_all(self) -> List[Exercise]:
        return self.list_all_exercices()

    def get_by_name(self, name: str) -> Optional[Exercise]:
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM exercices WHERE nom = ?",
                (name,),
            ).fetchone()
        if not row:
            return None
        return Exercise(
            id=row["id"],
            nom=row["nom"],
            groupe_musculaire_principal=row["groupe_musculaire_principal"],
            equipement=row["equipement"],
            tags=row["tags"],
            movement_pattern=row["movement_pattern"],
            movement_category=row["movement_category"]
            if "movement_category" in row.keys()
            else None,
            type_effort=row["type_effort"],
            coefficient_volume=row["coefficient_volume"],
            est_chargeable=bool(row["est_chargeable"]),
        )

    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Retourne un exercice par son identifiant ou None s'il n'existe pas.

        Ajouté pour la compatibilité avec le SmartWorkoutGenerator qui
        consulte ponctuellement les métadonnées d'un exercice.
        """
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM exercices WHERE id = ?",
                (exercise_id,),
            ).fetchone()
        if not row:
            return None
        return Exercise(
            id=row["id"],
            nom=row["nom"],
            groupe_musculaire_principal=row["groupe_musculaire_principal"],
            equipement=row["equipement"],
            tags=row["tags"],
            movement_pattern=row["movement_pattern"],
            movement_category=row["movement_category"]
            if "movement_category" in row.keys()
            else None,
            type_effort=row["type_effort"],
            coefficient_volume=row["coefficient_volume"],
            est_chargeable=bool(row["est_chargeable"]),
        )

    def create(self, e: Exercise) -> int:
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                (
                    "INSERT INTO exercices (nom, groupe_musculaire_principal, equipement, tags, "
                    "movement_pattern, movement_category, type_effort, coefficient_volume, est_chargeable) "
                    "VALUES (?,?,?,?,?,?,?,?,?)"
                ),
                (
                    e.nom,
                    e.groupe_musculaire_principal,
                    e.equipement,
                    e.tags,
                    e.movement_pattern,
                    e.movement_category,
                    e.type_effort,
                    e.coefficient_volume,
                    1 if e.est_chargeable else 0,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def update(self, e: Exercise) -> None:
        with db_manager.get_connection() as conn:
            conn.execute(
                (
                    "UPDATE exercices SET nom=?, groupe_musculaire_principal=?, equipement=?, tags=?, "
                    "movement_pattern=?, movement_category=?, type_effort=?, coefficient_volume=?, est_chargeable=? WHERE id = ?"
                ),
                (
                    e.nom,
                    e.groupe_musculaire_principal,
                    e.equipement,
                    e.tags,
                    e.movement_pattern,
                    e.movement_category,
                    e.type_effort,
                    e.coefficient_volume,
                    1 if e.est_chargeable else 0,
                    e.id,
                ),
            )
            conn.commit()

    def delete(self, exercise_id: int) -> None:
        with db_manager.get_connection() as conn:
            conn.execute("DELETE FROM exercices WHERE id = ?", (exercise_id,))
            conn.commit()

    def cleanup_normalize(self) -> int:
        """Normalise les valeurs redondantes/incohérentes.

        - movement_pattern: 'plyo'/'saut'/'jump' -> 'Jump'
        - movement_category: NULL si hors {Polyarticulaire, Isolation, Gainage}
        - tags: 'Plyo' -> 'Explosif', 'Isometrie' -> 'Isométrie'

        Returns: nombre approximatif de changements.
        """
        with db_manager.get_connection() as conn:
            before = conn.total_changes
            conn.execute(
                "UPDATE exercices SET movement_pattern='Jump' "
                "WHERE LOWER(movement_pattern) IN ('plyo','saut','jump')"
            )
            conn.execute(
                (
                    "UPDATE exercices SET movement_category = NULL "
                    "WHERE movement_category IS NOT NULL "
                    "AND movement_category NOT IN ('Polyarticulaire','Isolation','Gainage')"
                )
            )
            conn.execute(
                "UPDATE exercices SET tags=REPLACE(tags,'Plyo','Explosif') WHERE tags LIKE '%Plyo%'"
            )
            conn.execute(
                "UPDATE exercices SET tags=REPLACE(tags,'Isometrie','Isométrie') WHERE tags LIKE '%Isometrie%'"
            )
            conn.commit()
            after = conn.total_changes
            return max(0, after - before)

    def get_names_by_ids(self, ids: List[int]) -> Dict[int, str]:
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = f"SELECT id, nom FROM exercices WHERE id IN ({placeholders})"
        with db_manager.get_connection() as conn:
            rows = conn.execute(q, unique_ids).fetchall()
        return {r["id"]: r["nom"] for r in rows}

    def get_name_equipment_by_ids(self, ids: List[int]) -> Dict[int, Dict[str, Any]]:
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = f"SELECT id, nom, equipement FROM exercices WHERE id IN ({placeholders})"
        with db_manager.get_connection() as conn:
            rows = conn.execute(q, unique_ids).fetchall()
        out: Dict[int, Dict[str, Any]] = {}
        for r in rows:
            out[r["id"]] = {
                "name": r["nom"],
                "equipment": _split_csv(r["equipement"]),
            }
        return out

    def get_meta_by_ids(self, ids: List[int]) -> Dict[int, Dict[str, Any]]:
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = (
            "SELECT id, nom, groupe_musculaire_principal, equipement "
            f"FROM exercices WHERE id IN ({placeholders})"
        )
        with db_manager.get_connection() as conn:
            rows = conn.execute(q, unique_ids).fetchall()
        out: Dict[int, Dict[str, Any]] = {}
        for r in rows:
            out[r["id"]] = {
                "name": r["nom"],
                "primary_muscle": r["groupe_musculaire_principal"],
                "equipment": _split_csv(r["equipement"]),
            }
        return out

    def filter(
        self,
        equipment: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Exercise]:
        """Return exercises filtered by equipment and/or tags."""
        query = "SELECT * FROM exercices"
        conditions: List[str] = []
        params: List[str] = []

        if equipment:
            equipment_conditions = []
            for eq in equipment:
                equipment_conditions.append("equipement LIKE ?")
                params.append(f"%{eq}%")
            conditions.append("(" + " OR ".join(equipment_conditions) + ")")

        if tags:
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
            conditions.append("(" + " OR ".join(tag_conditions) + ")")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY nom"

        with db_manager.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            Exercise(
                id=row["id"],
                nom=row["nom"],
                groupe_musculaire_principal=row["groupe_musculaire_principal"],
                equipement=row["equipement"],
                tags=row["tags"],
                movement_pattern=row["movement_pattern"],
                movement_category=row["movement_category"]
                if "movement_category" in row.keys()
                else None,
                type_effort=row["type_effort"],
                coefficient_volume=row["coefficient_volume"],
                est_chargeable=bool(row["est_chargeable"]),
            )
            for row in rows
        ]
