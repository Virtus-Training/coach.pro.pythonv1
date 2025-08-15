from dataclasses import dataclass, field
from typing import List, Optional

from .resultat_exercice import ResultatExercice


@dataclass
class Seance:
    """Représente une séance d'entraînement ainsi que ses résultats."""

    id: int
    client_id: Optional[int]
    type_seance: str
    titre: str
    date_creation: str
    resultats: List[ResultatExercice] = field(default_factory=list)
