from __future__ import annotations

from typing import Dict


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


def calculate_nutrition_targets(data: Dict) -> Dict:
    proteines_g_par_kg = float(data.get("proteines_g_par_kg", 1.8))
    ratio_glucides = data.get("ratio_glucides")

    bmr = _bmr(data)
    factor = ACTIVITY_FACTORS.get(data["niveau_activite"], 1.2)
    maintenance = bmr * factor

    adj = OBJECTIVE_ADJUST.get(data["objectif"], 0)
    objectif_kcal = maintenance + adj

    # Proteins
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
        ratio_glucides = (carbs_cal / remaining_total * 100) if remaining_total > 0 else 0

    return {
        "maintenance_kcal": round(maintenance),
        "objectif_kcal": round(objectif_kcal),
        "proteines_g": proteines_g,
        "glucides_g": glucides_g,
        "lipides_g": lipides_g,
        "proteines_cible_g_par_kg": proteines_g_par_kg,
        "ratio_glucides_lipides_cible": round(ratio_glucides, 2),
    }
