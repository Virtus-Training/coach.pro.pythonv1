import sqlite3
from typing import List, Dict, Any

from models.exercices import Exercise

DB_PATH = "coach.db"


def _split_csv(s: str | None) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()] if s else []


class ExerciseRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def list_all_exercices(self) -> List[Exercise]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM exercices ORDER BY nom"
            ).fetchall()
        return [
            Exercise(
                id=row["id"],
                nom=row["nom"],
                groupe_musculaire_principal=row["groupe_musculaire_principal"],
                equipement=row["equipement"],
                type_effort=row["type_effort"],
                coefficient_volume=row["coefficient_volume"],
                est_chargeable=bool(row["est_chargeable"]),
            )
            for row in rows
        ]

    def get_names_by_ids(self, ids: List[int]) -> Dict[int, str]:
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = f"SELECT id, nom FROM exercices WHERE id IN ({placeholders})"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(q, unique_ids).fetchall()
        return {r["id"]: r["nom"] for r in rows}

    def get_name_equipment_by_ids(self, ids: List[int]) -> Dict[int, Dict[str, Any]]:
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = (
            "SELECT id, nom, equipement FROM exercices "
            f"WHERE id IN ({placeholders})"
        )
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
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
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(q, unique_ids).fetchall()
        out: Dict[int, Dict[str, Any]] = {}
        for r in rows:
            out[r["id"]] = {
                "name": r["nom"],
                "primary_muscle": r["groupe_musculaire_principal"],
                "equipment": _split_csv(r["equipement"]),
            }
        return out
