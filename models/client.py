from dataclasses import dataclass
from typing import Optional


@dataclass
class Client:
    id: int
    nom: str
    prenom: str
    email: Optional[str] = None
    date_naissance: Optional[str] = None
