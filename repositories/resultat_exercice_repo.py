from typing import Any, Dict, List, Tuple

from db.database_manager import db_manager
from models.resultat_exercice import ResultatExercice


class ResultatExerciceRepository:
    """Interact with the ``resultats_exercices`` table."""

    def upsert(
        self,
        session_id: str,
        exercice_id: int,
        poids: float | None,
        repetitions: int | None,
        rpe: int | None,
        series_effectuees: int | None,
    ) -> None:
        with db_manager.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO resultats_exercices (
                    session_id, exercice_id, charge_utilisee, reps_effectuees, rpe, series_effectuees
                ) VALUES (?,?,?,?,?,?)
                ON CONFLICT(session_id, exercice_id) DO UPDATE SET
                    charge_utilisee=excluded.charge_utilisee,
                    reps_effectuees=excluded.reps_effectuees,
                    rpe=excluded.rpe,
                    series_effectuees=excluded.series_effectuees
                """,
                (session_id, exercice_id, poids, repetitions, rpe, series_effectuees),
            )

    def get_results_for_session(self, session_id: str) -> Dict[int, Dict[str, Any]]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM resultats_exercices WHERE session_id = ?",
                (session_id,),
            ).fetchall()
        out: Dict[int, Dict[str, Any]] = {}
        for r in rows:
            out[r["exercice_id"]] = {
                "poids": r["charge_utilisee"],
                "repetitions": r["reps_effectuees"],
                "rpe": r["rpe"],
                "series_effectuees": r["series_effectuees"],
            }
        return out

    def get_results_for_exercise(
        self, client_id: int, exercice_id: int
    ) -> List[ResultatExercice]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT r.id, r.session_id, r.exercice_id, r.series_effectuees,
                       r.reps_effectuees, r.charge_utilisee, r.rpe,
                       r.feedback_client, s.date_creation
                FROM resultats_exercices r
                JOIN sessions s ON r.session_id = s.session_id
                WHERE s.client_id = ? AND r.exercice_id = ?
                ORDER BY s.date_creation
                """,
                (client_id, exercice_id),
            ).fetchall()
        return [
            ResultatExercice(
                id=row["id"],
                session_id=row["session_id"],
                exercice_id=row["exercice_id"],
                session_date=row["date_creation"],
                series_effectuees=row["series_effectuees"],
                reps_effectuees=row["reps_effectuees"],
                charge_utilisee=row["charge_utilisee"],
                rpe=row["rpe"],
                feedback_client=row["feedback_client"],
            )
            for row in rows
        ]

    def get_tracked_exercises(self, client_id: int) -> List[Tuple[int, str]]:
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT DISTINCT e.id, e.nom
                FROM resultats_exercices r
                JOIN sessions s ON r.session_id = s.session_id
                JOIN exercices e ON r.exercice_id = e.id
                WHERE s.client_id = ?
                ORDER BY e.nom
                """,
                (client_id,),
            ).fetchall()
        return [(row["id"], row["nom"]) for row in rows]
