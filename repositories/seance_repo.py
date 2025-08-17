from datetime import datetime
from typing import Dict, List

from db.database_manager import db_manager
from models.resultat_exercice import ResultatExercice
from models.seance import Seance


class SeanceRepository:
    def get_by_client_id(self, client_id: int) -> List[Seance]:
        """Return all sessions for a client ordered from most recent to oldest."""
        with db_manager._get_connection() as conn:
            seance_rows = conn.execute(
                "SELECT * FROM seances WHERE client_id = ? ORDER BY date_creation DESC",
                (client_id,),
            ).fetchall()
            seances: List[Seance] = []
            for s in seance_rows:
                res_rows = conn.execute(
                    "SELECT * FROM resultats_exercices WHERE seance_id = ?",
                    (s["id"],),
                ).fetchall()
                resultats = [
                    ResultatExercice(
                        id=r["id"],
                        seance_id=r["seance_id"],
                        exercice_id=r["exercice_id"],
                        series_effectuees=r["series_effectuees"],
                        reps_effectuees=r["reps_effectuees"],
                        charge_utilisee=r["charge_utilisee"],
                        feedback_client=r["feedback_client"],
                    )
                    for r in res_rows
                ]
                seances.append(
                    Seance(
                        id=s["id"],
                        client_id=s["client_id"],
                        type_seance=s["type_seance"],
                        titre=s["titre"],
                        date_creation=s["date_creation"],
                        resultats=resultats,
                    )
                )
            return seances

    def add_seance(self, seance: Seance, resultats: List[ResultatExercice]) -> None:
        """Insert a new session and all its exercise results in a single transaction."""
        with db_manager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO seances (client_id, type_seance, titre, date_creation) VALUES (?, ?, ?, ?)",
                (
                    seance.client_id,
                    seance.type_seance,
                    seance.titre,
                    seance.date_creation,
                ),
            )
            seance_id = cur.lastrowid
            for r in resultats:
                cur.execute(
                    """
                    INSERT INTO resultats_exercices (
                        seance_id, exercice_id, series_effectuees, reps_effectuees, charge_utilisee, feedback_client
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        seance_id,
                        r.exercice_id,
                        r.series_effectuees,
                        r.reps_effectuees,
                        r.charge_utilisee,
                        r.feedback_client,
                    ),
                )
            conn.commit()

    def get_exercice_history(self, client_id: int, exercice_id: int) -> List[Dict]:
        """Return max load per session for a given client and exercise.

        Dates are returned as ``datetime`` objects and results are ordered from
        oldest to newest session.
        """
        with db_manager._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT s.date_creation AS date, MAX(r.charge_utilisee) AS max_charge
                FROM seances s
                JOIN resultats_exercices r ON s.id = r.seance_id
                WHERE s.client_id = ? AND r.exercice_id = ?
                GROUP BY s.date_creation
                ORDER BY s.date_creation ASC
                """,
                (client_id, exercice_id),
            ).fetchall()
        history: List[Dict] = []
        for r in rows:
            history.append(
                {
                    "date": datetime.strptime(r["date"], "%Y-%m-%d"),
                    "max_charge": r["max_charge"],
                }
            )
        return history
