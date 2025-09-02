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
            type_effort=row["type_effort"],
            coefficient_volume=row["coefficient_volume"],
            est_chargeable=bool(row["est_chargeable"]),
        )

    def create(self, e: Exercise) -> int:
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                (
                    "INSERT INTO exercices (nom, groupe_musculaire_principal, equipement, tags, "
                    "movement_pattern, type_effort, coefficient_volume, est_chargeable) "
                    "VALUES (?,?,?,?,?,?,?,?)"
                ),
                (
                    e.nom,
                    e.groupe_musculaire_principal,
                    e.equipement,
                    e.tags,
                    e.movement_pattern,
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
                    "movement_pattern=?, type_effort=?, coefficient_volume=?, est_chargeable=? WHERE id = ?"
                ),
                (
                    e.nom,
                    e.groupe_musculaire_principal,
                    e.equipement,
                    e.tags,
                    e.movement_pattern,
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
                type_effort=row["type_effort"],
                coefficient_volume=row["coefficient_volume"],
                est_chargeable=bool(row["est_chargeable"]),
            )
            for row in rows
        ]
