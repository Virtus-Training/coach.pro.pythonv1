from typing import Any, Dict

from db.database_manager import db_manager


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
