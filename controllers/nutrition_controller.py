from typing import Dict, List

from dtos.nutrition_dtos import (
    ItemDTO,
    NutritionPageDTO,
    PlanAlimentaireDTO,
    RepasDTO,
)
from models.aliment import Aliment
from models.plan_alimentaire import Repas
from models.portion import Portion
from services.client_service import ClientService
from services.nutrition_service import NutritionService
from services.pdf_generator import generate_nutrition_pdf
from services.plan_alimentaire_service import PlanAlimentaireService


class NutritionController:
    def __init__(
        self,
        nutrition_service: NutritionService,
        plan_service: PlanAlimentaireService,
        client_service: ClientService,
    ) -> None:
        self.nutrition_service = nutrition_service
        self.plan_service = plan_service
        self.client_service = client_service

    # --- Data fetchers ---
    def search_aliments(self, query: str) -> List[Aliment]:
        return self.nutrition_service.search_aliments(query)

    def get_portions_for_aliment(self, aliment_id: int) -> List[Portion]:
        return self.nutrition_service.get_portions_for_aliment(aliment_id)

    # --- Page data ---
    def get_nutrition_page_data(self, client_id: int) -> NutritionPageDTO:
        client = self.client_service.get_client_by_id(client_id)
        fiche = self.nutrition_service.get_last_sheet_for_client(client_id)
        plan = self.plan_service.get_or_create_plan_for_client(client_id)
        plan_dto = self._plan_to_dto(plan)
        return NutritionPageDTO(client=client, fiche=fiche, plan=plan_dto)

    def add_aliment_to_repas(
        self, repas_id: int, aliment_id: int, quantite: float
    ) -> PlanAlimentaireDTO:
        plan = self.plan_service.add_aliment_to_repas(repas_id, aliment_id, quantite)
        return self._plan_to_dto(plan)

    def delete_item_from_repas(self, item_id: int) -> PlanAlimentaireDTO:
        plan = self.plan_service.delete_item_from_repas(item_id)
        return self._plan_to_dto(plan)

    # --- Fiche nutritionnelle helpers ---
    def get_last_sheet_for_client(self, client_id: int):
        return self.nutrition_service.get_last_sheet_for_client(client_id)

    def generate_nutrition_sheet(self, client_id: int, data: Dict):
        return self.nutrition_service.generate_nutrition_sheet(client_id, data)

    def calculate_nutrition_targets(self, data: Dict) -> Dict:
        return self.nutrition_service.calculate_nutrition_targets(data)

    def export_sheet_to_pdf(
        self, fiche_data: Dict, client_data, file_path: str
    ) -> None:
        self.nutrition_service.export_sheet_to_pdf(fiche_data, client_data, file_path)

    def export_plan_to_pdf(
        self, nutrition_dto: NutritionPageDTO, file_path: str
    ) -> None:
        generate_nutrition_pdf(nutrition_dto, file_path)

    # --- Internal helpers ---
    def _plan_to_dto(self, plan) -> PlanAlimentaireDTO:
        repas_dtos: List[RepasDTO] = []
        for repas in plan.repas:
            repas_dtos.append(self._repas_to_dto(repas))
        totals = self.plan_service.compute_plan_totals(plan)
        return PlanAlimentaireDTO(
            id=plan.id,
            repas=repas_dtos,
            totals_kcal=totals["kcal"],
            totals_proteines=totals["proteines"],
            totals_glucides=totals["glucides"],
            totals_lipides=totals["lipides"],
        )

    def _repas_to_dto(self, repas: Repas) -> RepasDTO:
        items: List[ItemDTO] = []
        for item in repas.items:
            aliment = self.nutrition_service.get_aliment_by_id(item.aliment_id)
            totals = self.plan_service.compute_item_totals(item)
            items.append(
                ItemDTO(
                    id=item.id,
                    aliment_id=item.aliment_id,
                    nom=aliment.nom if aliment else "",
                    quantite=item.quantite,
                    unite="g",
                    kcal=totals["kcal"],
                    proteines=totals["proteines"],
                    glucides=totals["glucides"],
                    lipides=totals["lipides"],
                )
            )
        mt = self.plan_service.compute_meal_totals(repas)
        return RepasDTO(
            id=repas.id,
            nom=repas.nom,
            items=items,
            totals_kcal=mt["kcal"],
            totals_proteines=mt["proteines"],
            totals_glucides=mt["glucides"],
            totals_lipides=mt["lipides"],
        )
