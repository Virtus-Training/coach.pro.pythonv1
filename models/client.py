from dataclasses import dataclass
from typing import Optional


@dataclass
class Client:
    id: int
    nom: str
    prenom: str
    email: Optional[str] = None
    date_naissance: Optional[str] = None
    objectifs: Optional[str] = None
    antecedents_medicaux: Optional[str] = None
    sexe: Optional[str] = None
    poids_kg: Optional[float] = None
    taille_cm: Optional[float] = None
    niveau_activite: Optional[str] = None
