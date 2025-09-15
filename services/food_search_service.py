"""
Service de recherche avancée d'aliments

Service intelligent pour rechercher des aliments avec filtres,
synonymes, et suggestions personnalisées.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from models.aliment import Aliment
from repositories.aliment_repo import AlimentRepository


@dataclass
class FiltreRecherche:
    """Filtre de recherche d'aliments"""

    nom: Optional[str] = None
    categories: Optional[List[str]] = None
    proteines_min: Optional[float] = None
    proteines_max: Optional[float] = None
    kcal_min: Optional[float] = None
    kcal_max: Optional[float] = None
    limit: int = 20


@dataclass
class ResultatRecherche:
    """Résultat d'une recherche d'aliments"""

    aliments: List[Aliment]
    nombre_total: int
    temps_recherche_ms: float
    criteres_appliques: Dict[str, Any]
    suggestions: Optional[List[str]] = None


class FoodSearchService:
    """Service de recherche intelligente d'aliments"""

    def __init__(self):
        self.aliment_repo = AlimentRepository()
        self.synonymes = {
            # Viandes
            "boeuf": ["bœuf", "beef", "steak"],
            "porc": ["cochon", "jambon"],
            "volaille": ["poulet", "dinde"],
            # Poissons
            "poisson": ["saumon", "thon", "truite"],
            # Légumes
            "légume": ["légumes", "salade"],
            # Fruits
            "fruit": ["fruits", "compote"],
            # Produits laitiers
            "laitage": ["lait", "yaourt", "fromage"],
            # Céréales
            "céréale": ["céréales", "blé", "avoine", "riz"],
            # Termes nutritionnels
            "protéine": ["protéines", "protein"],
            "glucide": ["glucides", "sucre"],
            "lipide": ["lipides", "graisse"],
        }

    def recherche_simple(self, query: str, limit: int = 20) -> ResultatRecherche:
        """Recherche simple par nom d'aliment"""

        import time

        start_time = time.time()

        # Nettoyage de la requête
        query = query.strip().lower()

        # Recherche directe
        aliments = self.aliment_repo.search_by_name(query)

        # Extension avec synonymes si peu de résultats
        if len(aliments) < 5:
            aliments.extend(self._recherche_avec_synonymes(query))

        # Suppression des doublons
        aliments = self._supprimer_doublons(aliments)

        # Limitation
        aliments = aliments[:limit]

        temps_recherche = (time.time() - start_time) * 1000

        return ResultatRecherche(
            aliments=aliments,
            nombre_total=len(aliments),
            temps_recherche_ms=round(temps_recherche, 2),
            criteres_appliques={"query": query, "limit": limit},
        )

    def recherche_avancee(self, filtre: FiltreRecherche) -> ResultatRecherche:
        """Recherche avancée avec filtres"""

        import time

        start_time = time.time()

        # Recherche de base
        if filtre.nom:
            aliments = self.aliment_repo.search_by_name(filtre.nom)
        else:
            aliments = self.aliment_repo.list_all()

        # Application des filtres
        if filtre.proteines_min is not None:
            aliments = [a for a in aliments if a.proteines_100g >= filtre.proteines_min]

        if filtre.kcal_max is not None:
            aliments = [a for a in aliments if a.kcal_100g <= filtre.kcal_max]

        if filtre.categories:
            aliments = [a for a in aliments if a.categorie in filtre.categories]

        # Limitation
        aliments = aliments[: filtre.limit]

        temps_recherche = (time.time() - start_time) * 1000

        return ResultatRecherche(
            aliments=aliments,
            nombre_total=len(aliments),
            temps_recherche_ms=round(temps_recherche, 2),
            criteres_appliques=self._filtre_to_dict(filtre),
        )

    def obtenir_top_aliments(
        self,
        critere: str = "proteines_100g",
        limit: int = 20,
        exclude_categories: Optional[List[str]] = None,
    ) -> List[Aliment]:
        """Obtient le top des aliments selon un critère nutritionnel"""

        return self.aliment_repo.get_top_by_nutrition(
            metric=critere, limit=limit, exclude_categories=exclude_categories
        )

    def _recherche_avec_synonymes(self, query: str) -> List[Aliment]:
        """Étend la recherche avec des synonymes"""

        aliments_synonymes = []

        for mot_cle, synonymes in self.synonymes.items():
            if query in mot_cle or mot_cle in query:
                for synonyme in synonymes:
                    aliments = self.aliment_repo.search_by_name(synonyme)
                    aliments_synonymes.extend(aliments)

        return aliments_synonymes

    def _supprimer_doublons(self, aliments: List[Aliment]) -> List[Aliment]:
        """Supprime les doublons dans une liste d'aliments"""

        aliments_uniques = []
        ids_vus = set()

        for aliment in aliments:
            if aliment.id not in ids_vus:
                aliments_uniques.append(aliment)
                ids_vus.add(aliment.id)

        return aliments_uniques

    def _filtre_to_dict(self, filtre: FiltreRecherche) -> Dict[str, Any]:
        """Convertit un filtre en dictionnaire"""

        return {k: v for k, v in filtre.__dict__.items() if v is not None}
