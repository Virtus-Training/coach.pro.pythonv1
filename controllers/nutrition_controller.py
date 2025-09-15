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

# Import des nouveaux services intelligents
from services.meal_plan_generator_service import MealPlanGeneratorService
from services.food_search_service import FoodSearchService, FiltreRecherche
# from repositories.profil_nutritionnel_repo import ProfilNutritionnelRepository


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
        
        # Nouveaux services intelligents
        self.meal_generator = MealPlanGeneratorService()
        self.food_search = FoodSearchService()
        # self.profil_repo = ProfilNutritionnelRepository()

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

    # --- Nouvelles fonctionnalités intelligentes ---
    
    def search_aliments_advanced(self, query: str, filters: dict = None) -> List[Aliment]:
        """Recherche avancée d'aliments avec filtres"""
        try:
            if filters:
                filtre = FiltreRecherche(
                    nom=query,
                    categories=filters.get("categories"),
                    proteines_min=filters.get("proteines_min"),
                    kcal_max=filters.get("kcal_max"),
                    limit=filters.get("limit", 20)
                )
                resultat = self.food_search.recherche_avancee(filtre)
                return resultat.aliments
            else:
                resultat = self.food_search.recherche_simple(query, limit=20)
                return resultat.aliments
        except Exception as e:
            print(f"Erreur recherche avancée: {e}")
            # Fallback sur la recherche classique
            return self.nutrition_service.search_aliments(query)
    
    def get_food_suggestions(self, client_id: int, limit: int = 5) -> List[Aliment]:
        """Obtient des suggestions d'aliments personnalisées"""
        try:
            # Pour l'instant, suggestions génériques sans profil
            return self.food_search.obtenir_top_aliments("proteines_100g", limit=limit)
                
        except Exception as e:
            print(f"Erreur suggestions: {e}")
            # Fallback : retour des premiers aliments trouvés
            return self.nutrition_service.search_aliments("")[:limit]
    
    def generate_automatic_meal_plan(self, client_id: int, nom_plan: str = None, duree_jours: int = 1) -> PlanAlimentaireDTO:
        """Génère automatiquement un plan alimentaire intelligent"""
        try:
            # Pour l'instant, génération simple sans profil nutritionnel
            if not nom_plan:
                from datetime import datetime
                nom_plan = f"Plan auto - {datetime.now().strftime('%d/%m/%Y')}"
            
            # Utiliser le générateur simple
            plan_simple = self.meal_generator.generer_plan_simple(
                client_id=client_id,
                objectif_kcal=2000,  # Valeur par défaut
                nom_plan=nom_plan
            )
            
            print(f"Plan généré: {plan_simple['nom']} avec {len(plan_simple['repas'])} repas")
            
            # Retourner le plan existant (pour l'instant)
            plan_existant = self.plan_service.get_or_create_plan_for_client(client_id)
            return self._plan_to_dto(plan_existant)
            
        except Exception as e:
            print(f"Erreur génération automatique: {e}")
            # Fallback : retourner le plan existant ou un nouveau
            plan_existant = self.plan_service.get_or_create_plan_for_client(client_id)
            return self._plan_to_dto(plan_existant)
    
    def analyze_current_plan(self, client_id: int) -> Dict:
        """Analyse le plan alimentaire actuel du client"""
        try:
            plan = self.plan_service.get_or_create_plan_for_client(client_id)
            
            # Analyse basique avec les totaux existants
            totals = self.plan_service.compute_plan_totals(plan)
            return {
                "totaux": totals,
                "nombre_repas": len(plan.repas),
                "score_equilibre": 75  # Score par défaut
            }
                
        except Exception as e:
            print(f"Erreur analyse plan: {e}")
            return {"erreur": f"Impossible d'analyser le plan: {e}"}
    
    def get_nutritional_profile(self, client_id: int):
        """Récupère le profil nutritionnel d'un client"""
        # Pour l'instant, pas de profil nutritionnel
        return None
    
    def create_or_update_nutritional_profile(self, client_id: int, profile_data: dict):
        """Crée ou met à jour un profil nutritionnel"""
        # Pour l'instant, simulation de création de profil
        print(f"Profil nutritionnel simulé créé pour client {client_id}: {profile_data}")
        return {"id": client_id, **profile_data}
