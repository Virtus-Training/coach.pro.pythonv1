from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RepasItem:
    id: int
    repas_id: int
    aliment_id: int
    portion_id: int
    quantite: float = 1.0


@dataclass
class Repas:
    id: int
    plan_id: int
    nom: str
    ordre: int = 0
    items: List[RepasItem] = field(default_factory=list)


@dataclass
class PlanAlimentaire:
    id: int
    nom: str
    description: Optional[str] = None
    tags: Optional[str] = None
    repas: List[Repas] = field(default_factory=list)
