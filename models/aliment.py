from dataclasses import dataclass
from typing import Optional


@dataclass
class Aliment:
    id: int
    nom: str
    categorie: Optional[str] = None
    type_alimentation: Optional[str] = None
    kcal_100g: float = 0.0
    proteines_100g: float = 0.0
    glucides_100g: float = 0.0
    lipides_100g: float = 0.0
    fibres_100g: Optional[float] = None
    unite_base: str = "g"
    indice_healthy: Optional[int] = None
    indice_commun: Optional[int] = None
