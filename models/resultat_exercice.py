from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultatExercice:
    id: int
    session_id: str
    exercice_id: int
    session_date: str | None = None
    series_effectuees: Optional[int] = None
    reps_effectuees: Optional[int] = None
    charge_utilisee: Optional[float] = None
    rpe: Optional[int] = None
    feedback_client: Optional[str] = None
