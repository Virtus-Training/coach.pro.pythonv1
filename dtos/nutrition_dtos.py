from dataclasses import dataclass
from typing import List, Optional

from models.client import Client
from models.fiche_nutrition import FicheNutrition


@dataclass
class ItemDTO:
    id: int
    aliment_id: int
    nom: str
    quantite: float
    unite: str
    kcal: float
    proteines: float
    glucides: float
    lipides: float


@dataclass
class RepasDTO:
    id: int
    nom: str
    items: List[ItemDTO]
    totals_kcal: float
    totals_proteines: float
    totals_glucides: float
    totals_lipides: float


@dataclass
class PlanAlimentaireDTO:
    id: int
    repas: List[RepasDTO]
    totals_kcal: float
    totals_proteines: float
    totals_glucides: float
    totals_lipides: float


@dataclass
class NutritionPageDTO:
    client: Client
    fiche: Optional[FicheNutrition]
    plan: PlanAlimentaireDTO
