from dataclasses import dataclass


@dataclass
class Portion:
    id: int
    aliment_id: int
    description: str
    grammes_equivalents: float
