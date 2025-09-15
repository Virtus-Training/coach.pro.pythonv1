"""
Service de génération intelligente de plans alimentaires

Ce service utilise l'IA et les données nutritionnelles pour créer des plans
alimentaires personnalisés basés sur les profils et objectifs des clients.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import random

from models.aliment import Aliment, CategorieAliment
from models.plan_alimentaire import PlanAlimentaire, Repas, RepasItem
from repositories.aliment_repo import AlimentRepository


@dataclass
class RepasTemplate:
    """Template pour générer un repas"""
    nom: str
    type_repas: str
    pourcentage_kcal: float
    categories_principales: List[str]
    categories_secondaires: Optional[List[str]] = None
    ratio_macro_cible: Optional[Dict[str, float]] = None
    nombre_aliments_min: int = 2
    nombre_aliments_max: int = 4


class MealPlanGeneratorService:
    """Service de génération intelligente de plans alimentaires"""
    
    def __init__(self):
        self.aliment_repo = AlimentRepository()
        self.templates_repas = self._creer_templates_repas()
    
    def _creer_templates_repas(self) -> Dict[int, List[RepasTemplate]]:
        """Crée les templates de repas pour différents nombres de repas par jour"""
        
        # Templates pour 3 repas/jour
        trois_repas = [
            RepasTemplate(
                nom="Petit-déjeuner",
                type_repas="petit_dejeuner",
                pourcentage_kcal=0.25,
                categories_principales=["Cereales", "Laitages"],
                categories_secondaires=["Fruits"],
                ratio_macro_cible={"proteines": 0.20, "glucides": 0.55, "lipides": 0.25},
                nombre_aliments_min=2,
                nombre_aliments_max=3
            ),
            RepasTemplate(
                nom="Déjeuner",
                type_repas="dejeuner",
                pourcentage_kcal=0.40,
                categories_principales=["Viandes", "Cereales"],
                categories_secondaires=["Legumes"],
                ratio_macro_cible={"proteines": 0.25, "glucides": 0.45, "lipides": 0.30},
                nombre_aliments_min=3,
                nombre_aliments_max=4
            ),
            RepasTemplate(
                nom="Dîner",
                type_repas="diner",
                pourcentage_kcal=0.35,
                categories_principales=["Poissons", "Legumes"],
                categories_secondaires=["Cereales"],
                ratio_macro_cible={"proteines": 0.30, "glucides": 0.35, "lipides": 0.35},
                nombre_aliments_min=3,
                nombre_aliments_max=4
            )
        ]
        
        # Templates pour 4 repas/jour (avec collation)
        quatre_repas = trois_repas.copy()
        # Ajustement des pourcentages
        quatre_repas[0].pourcentage_kcal = 0.20  # Petit-déjeuner
        quatre_repas[1].pourcentage_kcal = 0.35  # Déjeuner
        quatre_repas[2].pourcentage_kcal = 0.30  # Dîner
        
        # Ajout de la collation
        quatre_repas.append(RepasTemplate(
            nom="Collation",
            type_repas="collation",
            pourcentage_kcal=0.15,
            categories_principales=["Fruits", "Laitages"],
            categories_secondaires=["Cereales"],
            ratio_macro_cible={"proteines": 0.25, "glucides": 0.50, "lipides": 0.25},
            nombre_aliments_min=1,
            nombre_aliments_max=2
        ))
        
        # Templates pour 5-6 repas/jour
        six_repas = [
            RepasTemplate(
                nom="Petit-déjeuner",
                type_repas="petit_dejeuner",
                pourcentage_kcal=0.15,
                categories_principales=["Cereales"],
                categories_secondaires=["Fruits"]
            ),
            RepasTemplate(
                nom="Collation matinale",
                type_repas="collation_matin",
                pourcentage_kcal=0.10,
                categories_principales=["Fruits"]
            ),
            RepasTemplate(
                nom="Déjeuner",
                type_repas="dejeuner",
                pourcentage_kcal=0.30,
                categories_principales=["Viandes", "Cereales", "Legumes"]
            ),
            RepasTemplate(
                nom="Collation après-midi",
                type_repas="collation_aprem",
                pourcentage_kcal=0.15,
                categories_principales=["Laitages", "Fruits"]
            ),
            RepasTemplate(
                nom="Dîner",
                type_repas="diner",
                pourcentage_kcal=0.25,
                categories_principales=["Poissons", "Legumes"]
            ),
            RepasTemplate(
                nom="Collation soirée",
                type_repas="collation_soir",
                pourcentage_kcal=0.05,
                categories_principales=["Laitages"]
            )
        ]
        
        return {
            3: trois_repas,
            4: quatre_repas,
            5: six_repas[:5],  # Sans la collation soirée
            6: six_repas
        }
    
    def generer_plan_simple(self, client_id: int, objectif_kcal: float = 2000, nom_plan: str = "Plan généré") -> Dict[str, Any]:
        """Génère un plan alimentaire simple pour test d'intégration"""
        
        # Pour l'instant, on retourne un plan basique pour tester l'intégration
        return {
            "nom": nom_plan,
            "client_id": client_id,
            "objectif_kcal": objectif_kcal,
            "repas": [
                {
                    "nom": "Petit-déjeuner",
                    "kcal_cible": objectif_kcal * 0.25,
                    "aliments_suggeres": ["Flocons d'avoine", "Lait", "Banane"]
                },
                {
                    "nom": "Déjeuner", 
                    "kcal_cible": objectif_kcal * 0.40,
                    "aliments_suggeres": ["Poulet", "Riz", "Légumes"]
                },
                {
                    "nom": "Dîner",
                    "kcal_cible": objectif_kcal * 0.35,
                    "aliments_suggeres": ["Saumon", "Quinoa", "Salade"]
                }
            ]
        }
    
    def analyser_plan_nutritionnel_simple(self, plan_data: Dict) -> Dict[str, Any]:
        """Analyse nutritionnelle simple d'un plan"""
        
        # Analyse basique pour test d'intégration
        total_kcal = plan_data.get("objectif_kcal", 2000)
        
        return {
            "totaux": {
                "kcal": total_kcal,
                "proteines_g": total_kcal * 0.15 / 4,  # 15% protéines
                "glucides_g": total_kcal * 0.55 / 4,   # 55% glucides  
                "lipides_g": total_kcal * 0.30 / 9     # 30% lipides
            },
            "ratios_macros": {
                "proteines_pourcent": 15.0,
                "glucides_pourcent": 55.0,
                "lipides_pourcent": 30.0
            },
            "nombre_repas": len(plan_data.get("repas", [])),
            "score_equilibre": 85  # Score par défaut
        }
    
    def obtenir_suggestions_aliments(self, objectif: str = "maintenance", limit: int = 10) -> List[Aliment]:
        """Obtient des suggestions d'aliments selon l'objectif"""
        
        try:
            if "perte" in objectif.lower():
                # Aliments faibles en calories
                return self.aliment_repo.search_advanced(max_kcal=150, limit=limit)
            elif "muscle" in objectif.lower():
                # Aliments riches en protéines
                return self.aliment_repo.search_advanced(min_proteines=15, limit=limit)
            else:
                # Aliments équilibrés
                return self.aliment_repo.get_top_by_nutrition("indice_healthy", limit=limit)
        except Exception as e:
            print(f"Erreur suggestions aliments: {e}")
            # Fallback: retourner tous les aliments disponibles
            return self.aliment_repo.list_all()[:limit]