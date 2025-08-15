from dataclasses import dataclass
from typing import Optional


@dataclass
class Exercise:
    id: int
    nom: str
    groupe_musculaire_principal: str
    equipement: Optional[str] = None
    tags: Optional[str] = None
    type_effort: str = ""
    coefficient_volume: float = 1.0
    est_chargeable: bool = False
