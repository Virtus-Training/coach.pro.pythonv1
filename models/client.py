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
