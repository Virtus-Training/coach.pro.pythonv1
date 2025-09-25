"""
Advanced Nutrition Calculator Service
====================================

Professional-grade nutrition calculations using evidence-based formulas:
- Mifflin-St Jeor BMR (gold standard)
- Harris-Benedict BMR (classic fallback)
- Activity factor adjustments (PAL values)
- Macro distribution optimization
- Body composition considerations
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math
from enum import Enum


class BMRMethod(Enum):
    """BMR calculation methods"""
    MIFFLIN_ST_JEOR = "mifflin_st_jeor"  # Most accurate for modern populations
    HARRIS_BENEDICT = "harris_benedict"  # Classic formula


class ActivityLevel(Enum):
    """Physical activity levels with PAL (Physical Activity Level) values"""
    SEDENTARY = ("Sédentaire", 1.2, "Bureau, peu d'exercice")
    LIGHTLY_ACTIVE = ("Légèrement actif", 1.375, "Exercice léger 1-3j/semaine")
    MODERATELY_ACTIVE = ("Modérément actif", 1.55, "Exercice modéré 3-5j/semaine")
    VERY_ACTIVE = ("Très actif", 1.725, "Exercice intense 6-7j/semaine")
    EXTREMELY_ACTIVE = ("Extrêmement actif", 1.9, "Exercice/travail physique intense")

    def __init__(self, label: str, factor: float, description: str):
        self.label = label
        self.factor = factor
        self.description = description


class NutritionGoal(Enum):
    """Nutrition objectives with caloric adjustments"""
    MAINTENANCE = ("Maintenance", 0, "Maintien du poids actuel")
    FAT_LOSS_MILD = ("Perte légère", -200, "Déficit modéré -200 kcal")
    FAT_LOSS_MODERATE = ("Perte modérée", -400, "Déficit standard -400 kcal")
    FAT_LOSS_AGGRESSIVE = ("Perte rapide", -600, "Déficit important -600 kcal")
    LEAN_GAIN_SLOW = ("Prise lente", +200, "Surplus modéré +200 kcal")
    LEAN_GAIN_MODERATE = ("Prise modérée", +400, "Surplus standard +400 kcal")
    LEAN_GAIN_AGGRESSIVE = ("Prise rapide", +600, "Surplus important +600 kcal")

    def __init__(self, label: str, adjustment: int, description: str):
        self.label = label
        self.adjustment = adjustment
        self.description = description


@dataclass
class PersonalData:
    """Personal data for nutrition calculations"""
    nom: str
    prenom: str
    age: int
    sexe: str  # "Homme" or "Femme"
    taille_cm: float
    poids_kg: float
    masse_grasse_pct: Optional[float] = None
    niveau_activite: ActivityLevel = ActivityLevel.SEDENTARY
    objectif: NutritionGoal = NutritionGoal.MAINTENANCE


@dataclass
class MacroTargets:
    """Macronutrient targets with detailed breakdown"""
    proteines_g_par_kg: float = 1.6
    glucides_pct: float = 40.0  # % of remaining calories after protein
    lipides_pct: float = 30.0   # % of remaining calories after protein

    def validate(self) -> List[str]:
        """Validate macro distribution coherence"""
        errors = []
        if self.glucides_pct + self.lipides_pct != 100.0:
            errors.append("Glucides + Lipides doit égaler 100%")
        if self.proteines_g_par_kg < 0.8 or self.proteines_g_par_kg > 4.0:
            errors.append("Protéines/kg doit être entre 0.8g et 4.0g")
        return errors


@dataclass
class NutritionResults:
    """Complete nutrition calculation results"""
    # Métabolisme de base
    bmr_kcal: float
    bmr_method: BMRMethod

    # Dépense énergétique totale
    tdee_kcal: float
    activite_factor: float

    # Objectifs caloriques
    objectif_kcal: float
    deficit_surplus: int

    # Macronutriments (grammes)
    proteines_g: int
    glucides_g: int
    lipides_g: int

    # Macronutriments (calories)
    proteines_kcal: int
    glucides_kcal: int
    lipides_kcal: int

    # Distribution (pourcentages)
    proteines_pct: float
    glucides_pct: float
    lipides_pct: float

    # Méta-données
    personal_data: PersonalData
    macro_targets: MacroTargets


class AdvancedNutritionCalculator:
    """
    Professional nutrition calculator with scientific accuracy.

    Features:
    - Multiple BMR formulas with automatic selection
    - Precision activity factor adjustments
    - Body composition considerations
    - Evidence-based macro distributions
    - Goal-specific recommendations
    """

    @staticmethod
    def calculate_bmr(
        age: int,
        sexe: str,
        taille_cm: float,
        poids_kg: float,
        method: BMRMethod = BMRMethod.MIFFLIN_ST_JEOR,
        masse_grasse_pct: Optional[float] = None
    ) -> float:
        """
        Calculate Basal Metabolic Rate using specified method.

        Args:
            age: Age in years
            sexe: "Homme" or "Femme"
            taille_cm: Height in centimeters
            poids_kg: Weight in kilograms
            method: BMR calculation method
            masse_grasse_pct: Body fat percentage (optional)

        Returns:
            BMR in kcal/day
        """
        if method == BMRMethod.MIFFLIN_ST_JEOR:
            # Mifflin-St Jeor (1990) - Most accurate for modern populations
            bmr = 10 * poids_kg + 6.25 * taille_cm - 5 * age
            if sexe.lower().startswith('h'):  # Homme
                bmr += 5
            else:  # Femme
                bmr -= 161

        elif method == BMRMethod.HARRIS_BENEDICT:
            # Harris-Benedict (1984 revision) - Classic formula
            if sexe.lower().startswith('h'):  # Homme
                bmr = 88.362 + (13.397 * poids_kg) + (4.799 * taille_cm) - (5.677 * age)
            else:  # Femme
                bmr = 447.593 + (9.247 * poids_kg) + (3.098 * taille_cm) - (4.330 * age)

        # Katch-McArdle adjustment si masse grasse connue
        if masse_grasse_pct is not None and 5 <= masse_grasse_pct <= 50:
            lean_mass_kg = poids_kg * (1 - masse_grasse_pct / 100)
            # Katch-McArdle: BMR = 370 + (21.6 × lean body mass in kg)
            bmr_katch = 370 + (21.6 * lean_mass_kg)
            # Moyenne pondérée (70% formule standard, 30% Katch-McArdle)
            bmr = 0.7 * bmr + 0.3 * bmr_katch

        return max(bmr, 800)  # Minimum physiologique

    @staticmethod
    def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
        """
        Calculate Total Daily Energy Expenditure.

        Args:
            bmr: Basal Metabolic Rate in kcal/day
            activity_level: Physical activity level

        Returns:
            TDEE in kcal/day
        """
        return bmr * activity_level.factor

    @staticmethod
    def calculate_macro_distribution(
        target_calories: float,
        poids_kg: float,
        macro_targets: MacroTargets
    ) -> Tuple[int, int, int, int, int, int]:
        """
        Calculate macro distribution in grams and calories.

        Args:
            target_calories: Target daily calories
            poids_kg: Body weight in kg
            macro_targets: Macro distribution preferences

        Returns:
            Tuple of (prot_g, carb_g, fat_g, prot_kcal, carb_kcal, fat_kcal)
        """
        # Protéines (priorité absolue)
        proteines_g = max(int(poids_kg * macro_targets.proteines_g_par_kg), 50)
        proteines_kcal = proteines_g * 4

        # Calories restantes pour glucides et lipides
        remaining_kcal = max(target_calories - proteines_kcal, 400)

        # Distribution glucides/lipides sur calories restantes
        glucides_kcal = int(remaining_kcal * (macro_targets.glucides_pct / 100))
        lipides_kcal = int(remaining_kcal - glucides_kcal)

        # Conversion en grammes
        glucides_g = max(int(glucides_kcal / 4), 50)  # Minimum 50g glucides
        lipides_g = max(int(lipides_kcal / 9), 20)    # Minimum 20g lipides

        return proteines_g, glucides_g, lipides_g, proteines_kcal, glucides_kcal, lipides_kcal

    @classmethod
    def calculate_complete_nutrition(
        self,
        personal_data: PersonalData,
        macro_targets: MacroTargets,
        bmr_method: BMRMethod = BMRMethod.MIFFLIN_ST_JEOR
    ) -> NutritionResults:
        """
        Complete nutrition calculation with all parameters.

        Args:
            personal_data: Personal information
            macro_targets: Macro distribution preferences
            bmr_method: BMR calculation method

        Returns:
            Complete nutrition results
        """
        # Validation des données
        if personal_data.age < 10 or personal_data.age > 120:
            raise ValueError("Âge doit être entre 10 et 120 ans")
        if personal_data.poids_kg < 30 or personal_data.poids_kg > 300:
            raise ValueError("Poids doit être entre 30 et 300 kg")
        if personal_data.taille_cm < 100 or personal_data.taille_cm > 250:
            raise ValueError("Taille doit être entre 100 et 250 cm")

        # Calcul BMR
        bmr = self.calculate_bmr(
            personal_data.age,
            personal_data.sexe,
            personal_data.taille_cm,
            personal_data.poids_kg,
            bmr_method,
            personal_data.masse_grasse_pct
        )

        # Calcul TDEE
        tdee = self.calculate_tdee(bmr, personal_data.niveau_activite)

        # Calories objectif
        objectif_kcal = tdee + personal_data.objectif.adjustment
        objectif_kcal = max(objectif_kcal, bmr * 1.1)  # Jamais moins de 110% BMR

        # Distribution macronutriments
        prot_g, carb_g, fat_g, prot_kcal, carb_kcal, fat_kcal = self.calculate_macro_distribution(
            objectif_kcal, personal_data.poids_kg, macro_targets
        )

        # Calcul pourcentages
        total_kcal = prot_kcal + carb_kcal + fat_kcal
        prot_pct = (prot_kcal / total_kcal * 100) if total_kcal > 0 else 0
        carb_pct = (carb_kcal / total_kcal * 100) if total_kcal > 0 else 0
        fat_pct = (fat_kcal / total_kcal * 100) if total_kcal > 0 else 0

        return NutritionResults(
            # Métabolisme
            bmr_kcal=round(bmr),
            bmr_method=bmr_method,

            # TDEE
            tdee_kcal=round(tdee),
            activite_factor=personal_data.niveau_activite.factor,

            # Objectifs
            objectif_kcal=round(objectif_kcal),
            deficit_surplus=personal_data.objectif.adjustment,

            # Macros (grammes)
            proteines_g=prot_g,
            glucides_g=carb_g,
            lipides_g=fat_g,

            # Macros (calories)
            proteines_kcal=prot_kcal,
            glucides_kcal=carb_kcal,
            lipides_kcal=fat_kcal,

            # Distribution (%)
            proteines_pct=round(prot_pct, 1),
            glucides_pct=round(carb_pct, 1),
            lipides_pct=round(fat_pct, 1),

            # Méta
            personal_data=personal_data,
            macro_targets=macro_targets
        )

    @staticmethod
    def get_personalized_recommendations(results: NutritionResults) -> List[str]:
        """
        Generate personalized recommendations based on goals and profile.

        Args:
            results: Complete nutrition calculation results

        Returns:
            List of personalized recommendations
        """
        recommendations = []
        goal = results.personal_data.objectif
        age = results.personal_data.age
        poids = results.personal_data.poids_kg

        # Recommandations de base
        recommendations.extend([
            f"💧 Hydratation : {int(poids * 35)} mL/jour (eau + boissons)",
            "😴 Sommeil : 7-9h par nuit pour optimiser la récupération",
            "🥗 Privilégier les aliments bruts et minimalement transformés",
            "⏰ Respecter des horaires de repas réguliers (±1h)"
        ])

        # Recommandations spécifiques à l'objectif
        if goal in [NutritionGoal.FAT_LOSS_MILD, NutritionGoal.FAT_LOSS_MODERATE, NutritionGoal.FAT_LOSS_AGGRESSIVE]:
            recommendations.extend([
                "🥬 Augmenter les légumes pour la satiété (fibres + volume)",
                "🐟 Prioriser les protéines maigres à chaque repas",
                "⚖️ Déficit progressif : surveiller la balance 2x/semaine",
                "🚶 Ajouter 30min de marche quotidienne",
                "💤 Le sommeil influence les hormones de faim (ghréline/leptine)"
            ])

        elif goal in [NutritionGoal.LEAN_GAIN_SLOW, NutritionGoal.LEAN_GAIN_MODERATE, NutritionGoal.LEAN_GAIN_AGGRESSIVE]:
            recommendations.extend([
                "🍌 Glucides autour des entraînements (pré/post-workout)",
                "🥛 Collation post-entraînement : protéines + glucides dans l'heure",
                "📈 Prise de poids cible : 200-400g/semaine maximum",
                "🏋️ Entraînement résistance 3-4x/semaine minimum",
                "🕐 Répartir les repas : 4-6 prises alimentaires/jour"
            ])

        # Recommandations par âge
        if age >= 50:
            recommendations.extend([
                "🦴 Calcium et vitamine D : laitages + exposition solaire",
                "💪 Protéines élevées : 1.2-1.6g/kg pour préserver masse musculaire"
            ])
        elif age <= 25:
            recommendations.append("⚡ Métabolisme élevé : ne pas sous-estimer les besoins caloriques")

        # Recommandations par genre
        if results.personal_data.sexe.lower().startswith('f'):
            recommendations.extend([
                "🩸 Fer : viandes rouges, légumineuses (besoins accrus)",
                "🦴 Calcium : 1000-1200mg/jour (prévention ostéoporose)"
            ])

        return recommendations[:12]  # Max 12 recommandations

    @staticmethod
    def estimate_timeline(results: NutritionResults) -> Dict[str, str]:
        """
        Estimate realistic timeline for goal achievement.

        Args:
            results: Nutrition calculation results

        Returns:
            Timeline estimates dict
        """
        goal = results.personal_data.objectif
        deficit_surplus = results.deficit_surplus

        if deficit_surplus == 0:
            return {"timeline": "Maintenance continue", "rate": "0 kg/mois"}

        # 1 kg de graisse ≈ 7700 kcal
        kcal_per_kg = 7700
        monthly_kcal_change = deficit_surplus * 30
        monthly_weight_change = monthly_kcal_change / kcal_per_kg

        timeline = {}

        if deficit_surplus < 0:  # Perte de poids
            monthly_loss = abs(monthly_weight_change)
            timeline = {
                "timeline": "2-6 mois selon objectif",
                "rate": f"-{monthly_loss:.1f} kg/mois",
                "target_5kg": f"{5/monthly_loss:.1f} mois" if monthly_loss > 0 else "N/A",
                "target_10kg": f"{10/monthly_loss:.1f} mois" if monthly_loss > 0 else "N/A"
            }
        else:  # Prise de poids
            monthly_gain = monthly_weight_change
            timeline = {
                "timeline": "3-6 mois pour adaptation",
                "rate": f"+{monthly_gain:.1f} kg/mois",
                "target_5kg": f"{5/monthly_gain:.1f} mois" if monthly_gain > 0 else "N/A",
                "target_10kg": f"{10/monthly_gain:.1f} mois" if monthly_gain > 0 else "N/A"
            }

        return timeline