import sqlite3
from typing import List

from models.seance import Seance
from models.resultat_exercice import ResultatExercice

DB_PATH = "coach.db"


class SeanceRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_by_client_id(self, client_id: int) -> List[Seance]:
        """Return all sessions for a client ordered from most recent to oldest."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
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
        with sqlite3.connect(self.db_path) as conn:
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
