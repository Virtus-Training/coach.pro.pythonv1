from __future__ import annotations

from typing import Dict, List, Optional

from models.aliment import Aliment
from models.client import Client
from models.fiche_nutrition import FicheNutrition
from models.portion import Portion
from repositories.aliment_repo import AlimentRepository
from repositories.fiche_nutrition_repo import FicheNutritionRepository
from services.pdf_generator import generate_nutrition_sheet_pdf

ACTIVITY_FACTORS = {
    "Sédentaire": 1.2,
    "Activité légère": 1.375,
    "Activité modérée": 1.55,
    "Très actif": 1.725,
    "Extrêmement actif": 1.9,
}

OBJECTIVE_ADJUST = {
    "Perte de poids": -300,
    "Maintenance": 0,
    "Prise de masse": 300,
}


class NutritionService:
    def __init__(
        self,
        fiche_repo: FicheNutritionRepository,
        aliment_repo: AlimentRepository,
    ) -> None:
        self.repo = fiche_repo
        self.aliment_repo = aliment_repo

    @staticmethod
    def _bmr(data: Dict) -> float:
        poids = data["poids_kg"]
        taille = data["taille_cm"]
        age = data["age"]
        sexe = data["sexe"].lower()
        base = 10 * poids + 6.25 * taille - 5 * age
        if sexe.startswith("h"):
            base += 5
        else:
            base -= 161
        return base

    def calculate_nutrition_targets(self, data: Dict) -> Dict:
        proteines_g_par_kg = float(data.get("proteines_g_par_kg", 1.8))
        ratio_glucides = data.get("ratio_glucides")

        bmr = self._bmr(data)
        factor = ACTIVITY_FACTORS.get(data["niveau_activite"], 1.2)
        maintenance = bmr * factor

        adj = OBJECTIVE_ADJUST.get(data["objectif"], 0)
        objectif_kcal = maintenance + adj

        proteines_g = round(proteines_g_par_kg * data["poids_kg"])
        protein_cal = proteines_g * 4

        if ratio_glucides is not None:
            ratio_glucides = float(ratio_glucides)
            remaining = objectif_kcal - protein_cal
            carbs_cal = remaining * (ratio_glucides / 100)
            lipids_cal = remaining - carbs_cal
            glucides_g = round(carbs_cal / 4)
            lipides_g = round(lipids_cal / 9)
        else:
            lipides_g = round(data["poids_kg"])
            lipids_cal = lipides_g * 9
            remaining = objectif_kcal - protein_cal - lipids_cal
            glucides_g = round(remaining / 4)
            carbs_cal = glucides_g * 4
            remaining_total = objectif_kcal - protein_cal
            ratio_glucides = (
                (carbs_cal / remaining_total * 100) if remaining_total > 0 else 0
            )

        return {
            "maintenance_kcal": round(maintenance),
            "objectif_kcal": round(objectif_kcal),
            "proteines_g": proteines_g,
            "glucides_g": glucides_g,
            "lipides_g": lipides_g,
            "proteines_cible_g_par_kg": proteines_g_par_kg,
            "ratio_glucides_lipides_cible": round(ratio_glucides, 2),
        }

    def generate_nutrition_sheet(self, client_id: int, data: Dict) -> FicheNutrition:
        targets = self.calculate_nutrition_targets(data)
        fiche = FicheNutrition(
            id=None,
            client_id=client_id,
            date_creation=None,
            poids_kg_mesure=data["poids_kg"],
            objectif=data["objectif"],
            proteines_cible_g_par_kg=targets["proteines_cible_g_par_kg"],
            ratio_glucides_lipides_cible=targets["ratio_glucides_lipides_cible"],
            maintenance_kcal=targets["maintenance_kcal"],
            objectif_kcal=targets["objectif_kcal"],
            proteines_g=targets["proteines_g"],
            glucides_g=targets["glucides_g"],
            lipides_g=targets["lipides_g"],
        )
        self.repo.add(fiche)
        return self.get_last_sheet_for_client(client_id)

    def get_last_sheet_for_client(self, client_id: int) -> Optional[FicheNutrition]:
        return self.repo.get_last_for_client(client_id)

    def export_sheet_to_pdf(
        self, fiche_data: Dict, client_data: Client, file_path: str
    ) -> None:
        generate_nutrition_sheet_pdf(fiche_data, client_data, file_path)

    # --- Simple data fetchers for controller ---
    def search_aliments(self, query: str) -> List[Aliment]:
        return self.aliment_repo.search_by_name(query)

    def get_portions_for_aliment(self, aliment_id: int) -> List[Portion]:
        return self.aliment_repo.get_portions_for_aliment(aliment_id)

    def get_aliment_by_id(self, aliment_id: int) -> Optional[Aliment]:
        for a in self.aliment_repo.list_all():
            if a.id == aliment_id:
                return a
        return None
