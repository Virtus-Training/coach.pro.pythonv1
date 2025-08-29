from typing import Any, Dict, List

from dtos.tracking_dtos import ExerciseProgressionDTO, TrackedExerciseDTO
from repositories.exercices_repo import ExerciseRepository
from services.session_service import SessionService
from services.tracking_service import TrackingService


class TrackingController:
    def __init__(
        self,
        tracking_service: TrackingService,
        session_service: SessionService,
        exercise_repo: ExerciseRepository,
    ) -> None:
        self.tracking_service = tracking_service
        self.session_service = session_service
        self.exercise_repo = exercise_repo

    def get_session_for_logging(self, session_id: str) -> Dict[str, Any]:
        session = self.session_service.get_session_by_id(session_id)
        if not session:
            return {"session": None, "exercises": []}
        exercise_ids: List[int] = []
        for blk in session.blocks:
            for it in blk.items:
                eid = int(it.exercise_id)
                if eid not in exercise_ids:
                    exercise_ids.append(eid)
        names = self.exercise_repo.get_names_by_ids(exercise_ids)
        existing = self.tracking_service.get_results_for_session(session_id)
        exercises = []
        for eid in exercise_ids:
            exercises.append(
                {
                    "id": eid,
                    "name": names.get(eid, f"Exercice {eid}"),
                    "result": existing.get(eid, {}),
                }
            )
        return {"session": session, "exercises": exercises}

    def save_session_results(
        self, session_id: str, results_data: List[Dict[str, Any]]
    ) -> None:
        self.tracking_service.save_session_results(session_id, results_data)

    def get_exercise_progression(
        self, client_id: int, exercice_id: int
    ) -> ExerciseProgressionDTO:
        return self.tracking_service.get_exercise_progression(client_id, exercice_id)

    def get_tracked_exercises(self, client_id: int) -> List[TrackedExerciseDTO]:
        return self.tracking_service.get_tracked_exercises(client_id)
