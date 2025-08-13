import sqlite3
from typing import List, Dict, Any
from models.exercices import Exercise

DB_PATH = "coach.db"

def _split_csv(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()] if s else []

class ExerciseRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def filter(self, *, equipment: List[str], tags: List[str] | None = None) -> List[Exercise]:
        q = "SELECT * FROM exercises"
        where, params = [], []
        if equipment:
            where.append("(" + " OR ".join(["equipment LIKE ?"] * len(equipment)) + ")")
            params += [f"%{e}%" for e in equipment]
        if tags:
            where.append("(" + " OR ".join(["tags LIKE ?"] * len(tags)) + ")")
            params += [f"%{t}%" for t in tags]
        if where:
            q += " WHERE " + " AND ".join(where)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(q, params).fetchall()

        out: List[Exercise] = []
        for r in rows:
            out.append(Exercise(
                exercise_id=r["exercise_id"],
                name=r["name"],
                primary_muscle=r["primary_muscle"],
                secondary_muscles=_split_csv(r["secondary_muscles"]),
                movement_pattern=r["movement_pattern"],
                equipment=_split_csv(r["equipment"]),
                unilateral=bool(r["unilateral"]),
                plane=r["plane"],
                category=r["category"],
                level=_split_csv(r["level"]),
                default_rep_range=r["default_rep_range"],
                default_sets=r["default_sets"],
                default_rest_sec=r["default_rest_sec"],
                avg_rep_time_sec=r["avg_rep_time_sec"],
                cues=r["cues"],
                contraindications=_split_csv(r["contraindications"]),
                tags=_split_csv(r["tags"]),
                variants_of=r["variants_of"],
                image_path=r["image_path"],
            ))
        return out

    def get_names_by_ids(self, ids: list[str]) -> dict[str, str]:
        """Retourne {exercise_id: name}."""
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = f"SELECT exercise_id, name FROM exercises WHERE exercise_id IN ({placeholders})"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(q, unique_ids).fetchall()
        return {r["exercise_id"]: r["name"] for r in rows}

    def get_name_equipment_by_ids(self, ids: list[str]) -> dict[str, Dict[str, Any]]:
        """
        Retourne { exercise_id: { 'name': str, 'equipment': [str, ...] } }.
        """
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        placeholders = ",".join(["?"] * len(unique_ids))
        q = f"SELECT exercise_id, name, equipment FROM exercises WHERE exercise_id IN ({placeholders})"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(q, unique_ids).fetchall()
        out: dict[str, Dict[str, Any]] = {}
        for r in rows:
            out[r["exercise_id"]] = {
                "name": r["name"],
                "equipment": _split_csv(r["equipment"]),
            }
        return out
