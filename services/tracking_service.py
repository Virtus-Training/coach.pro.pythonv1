from typing import Any, Dict, List

from repositories.resultat_exercice_repo import ResultatExerciceRepository


class TrackingService:
    def __init__(self, repo: ResultatExerciceRepository) -> None:
        self.repo = repo

    def save_session_results(self, session_id: str, results_data: List[Dict[str, Any]]) -> None:
        for res in results_data:
            self.repo.upsert(
                session_id=session_id,
                exercice_id=int(res.get("exercise_id")),
                poids=res.get("poids"),
                repetitions=res.get("repetitions"),
                rpe=res.get("rpe"),
                series_effectuees=res.get("series_effectuees"),
            )

    def get_results_for_session(self, session_id: str) -> Dict[int, Dict[str, Any]]:
        return self.repo.get_results_for_session(session_id)
