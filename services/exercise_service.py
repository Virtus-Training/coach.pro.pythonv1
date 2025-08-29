from typing import Any, Dict, List

from repositories.exercices_repo import ExerciseRepository


class ExerciseService:
    def __init__(self, repo: ExerciseRepository) -> None:
        self.repo = repo

    def get_meta_by_ids(self, ids: List[Any]) -> Dict[int, Dict[str, Any]]:
        int_ids = [int(i) for i in ids]
        return self.repo.get_meta_by_ids(int_ids)
