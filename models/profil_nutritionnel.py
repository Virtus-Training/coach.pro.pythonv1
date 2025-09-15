from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime


class ObjectifNutritif(Enum):
    """Objectifs nutritionnels disponibles"""
    PERTE_POIDS = "Perte de poids"
    PRISE_MUSCLE = "Prise de muscle"
    MAINTENANCE = "Maintenance"
    PERFORMANCE = "Performance sportive"
    SANTE_GENERALE = "Santé générale"


class NiveauActivite(Enum):
    """Niveaux d'activité physique"""
    SEDENTAIRE = "Sédentaire"
    LEGER = "Activité légère"
    MODERE = "Activité modérée"
    INTENSE = "Activité intense"
    TRES_INTENSE = "Très intense"


class RestrictionAlimentaire(Enum):
    """Restrictions alimentaires possibles"""
    AUCUNE = "Aucune"
    ALLERGIES_NOIX = "Allergies aux noix"
    ALLERGIES_LAIT = "Intolérance lactose"
    ALLERGIES_GLUTEN = "Intolérance gluten"
    DIABETE = "Diabète"
    HYPERTENSION = "Hypertension"
    CHOLESTEROL = "Hypercholestérolémie"


@dataclass
class ProfilNutritionnel:
    """Profil nutritionnel personnalisé pour un client"""
    id: Optional[int] = None
    client_id: int = 0
    
    # Données physiques
    age: int = 30
    sexe: str = "M"  # M/F
    poids_kg: float = 70.0
    taille_cm: float = 175.0
    
    # Objectifs et préférences
    objectif_principal: str = ObjectifNutritif.MAINTENANCE.value
    niveau_activite: str = NiveauActivite.MODERE.value
    restrictions_alimentaires: List[str] = field(default_factory=list)
    regimes_compatibles: List[str] = field(default_factory=list)
    
    # Préférences alimentaires
    aliments_preferes: List[int] = field(default_factory=list)  # IDs d'aliments
    aliments_exclus: List[int] = field(default_factory=list)  # IDs d'aliments
    nombre_repas_souhaite: int = 3
    
    # Calculs automatiques
    metabolism_basal: Optional[float] = None
    besoins_caloriques: Optional[float] = None
    repartition_macros: Dict[str, float] = field(default_factory=dict)
    
    # Méta-données
    date_creation: datetime = field(default_factory=datetime.now)
    date_mise_a_jour: datetime = field(default_factory=datetime.now)
    
    def calculer_metabolisme_basal(self) -> float:
        """Calcule le métabolisme basal avec la formule de Mifflin-St Jeor"""
        if self.sexe.upper() == "M":
            mb = 10 * self.poids_kg + 6.25 * self.taille_cm - 5 * self.age + 5
        else:
            mb = 10 * self.poids_kg + 6.25 * self.taille_cm - 5 * self.age - 161
        
        self.metabolism_basal = mb
        return mb
    
    def calculer_besoins_caloriques(self) -> float:
        """Calcule les besoins caloriques selon le niveau d'activité"""
        if not self.metabolism_basal:
            self.calculer_metabolisme_basal()
        
        facteurs_activite = {
            NiveauActivite.SEDENTAIRE.value: 1.2,
            NiveauActivite.LEGER.value: 1.375,
            NiveauActivite.MODERE.value: 1.55,
            NiveauActivite.INTENSE.value: 1.725,
            NiveauActivite.TRES_INTENSE.value: 1.9
        }
        
        facteur = facteurs_activite.get(self.niveau_activite, 1.55)
        besoins_maintenance = self.metabolism_basal * facteur
        
        # Ajustement selon l'objectif
        ajustements = {
            ObjectifNutritif.PERTE_POIDS.value: 0.85,  # -15% pour déficit modéré
            ObjectifNutritif.PRISE_MUSCLE.value: 1.1,  # +10% pour surplus léger
            ObjectifNutritif.MAINTENANCE.value: 1.0,
            ObjectifNutritif.PERFORMANCE.value: 1.05,
            ObjectifNutritif.SANTE_GENERALE.value: 1.0
        }
        
        ajustement = ajustements.get(self.objectif_principal, 1.0)
        self.besoins_caloriques = besoins_maintenance * ajustement
        return self.besoins_caloriques
    
    def calculer_repartition_macros(self) -> Dict[str, float]:
        """Calcule la répartition optimale des macronutriments"""
        if not self.besoins_caloriques:
            self.calculer_besoins_caloriques()
        
        # Répartitions selon l'objectif
        repartitions = {
            ObjectifNutritif.PERTE_POIDS.value: {"proteines": 0.30, "glucides": 0.35, "lipides": 0.35},
            ObjectifNutritif.PRISE_MUSCLE.value: {"proteines": 0.25, "glucides": 0.45, "lipides": 0.30},
            ObjectifNutritif.MAINTENANCE.value: {"proteines": 0.20, "glucides": 0.50, "lipides": 0.30},
            ObjectifNutritif.PERFORMANCE.value: {"proteines": 0.20, "glucides": 0.55, "lipides": 0.25},
            ObjectifNutritif.SANTE_GENERALE.value: {"proteines": 0.20, "glucides": 0.50, "lipides": 0.30}
        }
        
        repartition = repartitions.get(self.objectif_principal, repartitions[ObjectifNutritif.MAINTENANCE.value])
        
        # Conversion en grammes
        kcal_totales = self.besoins_caloriques
        self.repartition_macros = {
            "proteines_g": (kcal_totales * repartition["proteines"]) / 4,
            "glucides_g": (kcal_totales * repartition["glucides"]) / 4,
            "lipides_g": (kcal_totales * repartition["lipides"]) / 9,
            "proteines_pourcent": repartition["proteines"] * 100,
            "glucides_pourcent": repartition["glucides"] * 100,
            "lipides_pourcent": repartition["lipides"] * 100
        }
        
        return self.repartition_macros
    
    def obtenir_recommandations_hydratation(self) -> Dict[str, float]:
        """Calcule les besoins en hydratation"""
        base_hydratation = self.poids_kg * 35  # ml par kg
        
        ajustements_activite = {
            NiveauActivite.SEDENTAIRE.value: 1.0,
            NiveauActivite.LEGER.value: 1.1,
            NiveauActivite.MODERE.value: 1.2,
            NiveauActivite.INTENSE.value: 1.4,
            NiveauActivite.TRES_INTENSE.value: 1.6
        }
        
        facteur = ajustements_activite.get(self.niveau_activite, 1.2)
        besoins_ml = base_hydratation * facteur
        
        return {
            "besoins_ml_jour": besoins_ml,
            "verres_200ml": besoins_ml / 200,
            "litres": besoins_ml / 1000
        }
    
    def est_compatible_aliment(self, aliment_id: int) -> bool:
        """Vérifie si un aliment est compatible avec le profil"""
        if aliment_id in self.aliments_exclus:
            return False
        
        # TODO: Vérifier compatibilité avec restrictions et régimes
        return True
    
    def mettre_a_jour_profil(self):
        """Met à jour les calculs automatiques"""
        self.calculer_metabolisme_basal()
        self.calculer_besoins_caloriques()
        self.calculer_repartition_macros()
        self.date_mise_a_jour = datetime.now()


@dataclass
class ObjectifMacro:
    """Objectifs spécifiques pour les macronutriments"""
    proteines_g: float
    glucides_g: float
    lipides_g: float
    fibres_g: float = 25.0
    kcal_total: float = 0.0
    
    def __post_init__(self):
        if self.kcal_total == 0.0:
            self.kcal_total = (self.proteines_g * 4) + (self.glucides_g * 4) + (self.lipides_g * 9)
    
    def marge_tolerance(self, pourcentage: float = 5.0) -> "ObjectifMacro":
        """Retourne les objectifs avec une marge de tolérance"""
        marge = pourcentage / 100.0
        
        return ObjectifMacro(
            proteines_g=self.proteines_g * (1 + marge),
            glucides_g=self.glucides_g * (1 + marge),
            lipides_g=self.lipides_g * (1 + marge),
            fibres_g=self.fibres_g * (1 + marge),
            kcal_total=self.kcal_total * (1 + marge)
        )