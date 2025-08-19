from dataclasses import dataclass
from typing import Optional


@dataclass
class FicheNutrition:
    id: Optional[int]
    client_id: int
    date_creation: Optional[str]
    poids_kg_mesure: float
    objectif: str
    proteines_cible_g_par_kg: float
    ratio_glucides_lipides_cible: float
    maintenance_kcal: int
    objectif_kcal: int
    proteines_g: int
    glucides_g: int
    lipides_g: int
