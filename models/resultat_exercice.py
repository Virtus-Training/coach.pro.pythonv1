from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultatExercice:
    id: int
    seance_id: int
    exercice_id: int
    series_effectuees: Optional[int] = None
    reps_effectuees: Optional[int] = None
    charge_utilisee: Optional[float] = None
    feedback_client: Optional[str] = None
