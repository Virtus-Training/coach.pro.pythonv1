from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Exercise:
    exercise_id: str
    name: str
    primary_muscle: str
    secondary_muscles: List[str]
    movement_pattern: str
    equipment: List[str]
    unilateral: bool
    plane: str
    category: str
    level: List[str]
    default_rep_range: str
    default_sets: int
    default_rest_sec: int
    avg_rep_time_sec: float
    cues: str
    contraindications: List[str]
    tags: List[str]
    variants_of: Optional[str] = None
    image_path: Optional[str] = None
