from typing import Any, Dict, List

from dtos.tracking_dtos import ExerciseProgressionDTO, TrackedExerciseDTO
from repositories.resultat_exercice_repo import ResultatExerciceRepository


class TrackingService:
    def __init__(self, repo: ResultatExerciceRepository) -> None:
        self.repo = repo

    def save_session_results(
        self, session_id: str, results_data: List[Dict[str, Any]]
    ) -> None:
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

    def get_exercise_progression(
        self, client_id: int, exercice_id: int
    ) -> ExerciseProgressionDTO:
        results = self.repo.get_results_for_exercise(client_id, exercice_id)
        return ExerciseProgressionDTO(
            dates=[r.session_date or "" for r in results],
            poids=[r.charge_utilisee or 0 for r in results],
            repetitions=[r.reps_effectuees or 0 for r in results],
            rpe=[r.rpe or 0 for r in results],
        )

    def get_tracked_exercises(self, client_id: int) -> List[TrackedExerciseDTO]:
        rows = self.repo.get_tracked_exercises(client_id)
        return [TrackedExerciseDTO(id=r[0], name=r[1]) for r in rows]
