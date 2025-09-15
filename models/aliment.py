from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CategorieAliment(Enum):
    """Catégories d'aliments standardisées"""

    LEGUMES = "Légumes"
    FRUITS = "Fruits"
    CEREALES = "Céréales et dérivés"
    LEGUMINEUSES = "Légumineuses"
    VIANDES = "Viandes"
    POISSONS = "Poissons et fruits de mer"
    OEUFS = "Œufs"
    LAITAGES = "Produits laitiers"
    MATIERES_GRASSES = "Matières grasses"
    SUCRES = "Sucres et produits sucrés"
    BOISSONS = "Boissons"
    CONDIMENTS = "Condiments et épices"
    AUTRES = "Autres"


class TypeAlimentation(Enum):
    """Types d'alimentation/régimes compatibles"""

    OMNIVORE = "Omnivore"
    VEGETARIEN = "Végétarien"
    VEGAN = "Vegan"
    SANS_GLUTEN = "Sans gluten"
    CETOGENE = "Cétogène"
    PALEO = "Paléo"


@dataclass
class Aliment:
    """Modèle d'aliment enrichi avec calculs nutritionnels"""

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

    @property
    def indice_glycemique_estime(self) -> int:
        """Estimation de l'indice glycémique basée sur la composition"""
        if self.glucides_100g < 1:
            return 0

        # Logique d'estimation basée sur la catégorie et les fibres
        base_ig = 50
        if self.categorie == CategorieAliment.FRUITS.value:
            base_ig = 35
        elif self.categorie == CategorieAliment.LEGUMES.value:
            base_ig = 15
        elif self.categorie == CategorieAliment.CEREALES.value:
            base_ig = 70
        elif self.categorie == CategorieAliment.SUCRES.value:
            base_ig = 85

        # Ajustement pour les fibres
        if self.fibres_100g and self.fibres_100g > 3:
            base_ig = max(10, base_ig - int(self.fibres_100g * 2))

        return min(100, max(0, base_ig))

    @property
    def densite_nutritionnelle(self) -> float:
        """Score de densité nutritionnelle (protéines + fibres) / kcal"""
        if self.kcal_100g <= 0:
            return 0.0

        score_proteines = self.proteines_100g * 4  # 4 kcal/g
        score_fibres = (self.fibres_100g or 0) * 2  # Bonus fibres

        return (score_proteines + score_fibres) / self.kcal_100g

    @property
    def ratio_macro_optimal(self) -> bool:
        """Vérifie si l'aliment a un ratio macro équilibré pour la satiété"""
        total_macro = self.proteines_100g + self.glucides_100g + self.lipides_100g
        if total_macro <= 0:
            return False

        ratio_prot = self.proteines_100g / total_macro
        ratio_lipides = self.lipides_100g / total_macro

        # Aliment équilibré si protéines > 15% et lipides entre 20-35%
        return ratio_prot >= 0.15 and 0.20 <= ratio_lipides <= 0.35

    def calculer_valeurs_nutritionnelles(self, quantite_g: float) -> dict:
        """Calcule les valeurs nutritionnelles pour une quantité donnée"""
        facteur = quantite_g / 100.0

        return {
            "quantite_g": quantite_g,
            "kcal": self.kcal_100g * facteur,
            "proteines_g": self.proteines_100g * facteur,
            "glucides_g": self.glucides_100g * facteur,
            "lipides_g": self.lipides_100g * facteur,
            "fibres_g": (self.fibres_100g or 0) * facteur,
            "densite_nutritionnelle": self.densite_nutritionnelle,
            "ig_estime": self.indice_glycemique_estime,
        }

    def est_compatible_regime(self, regime: str) -> bool:
        """Vérifie si l'aliment est compatible avec un régime donné"""
        if not self.type_alimentation:
            return True  # Compatible par défaut si non spécifié

        compatibilities = {
            TypeAlimentation.VEGAN.value: [TypeAlimentation.VEGAN.value],
            TypeAlimentation.VEGETARIEN.value: [
                TypeAlimentation.VEGETARIEN.value,
                TypeAlimentation.VEGAN.value,
            ],
            TypeAlimentation.OMNIVORE.value: [t.value for t in TypeAlimentation],
        }

        return regime in compatibilities.get(self.type_alimentation, [])
