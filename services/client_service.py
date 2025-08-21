import re
from typing import List, Optional

from models.client import Client
from repositories.client_repo import ClientRepository


class ClientService:
    def __init__(self, repo: ClientRepository) -> None:
        self.repo = repo

    def get_all_clients(self) -> List[Client]:
        return self.repo.list_all()

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.repo.find_by_id(client_id)

    def validate_client_data(self, data: dict) -> None:
        if not data.get("prenom") or not data.get("nom"):
            raise ValueError("Le nom et le prénom sont obligatoires.")
        email = data.get("email")
        if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("L'email est invalide.")

    def add_client(self, client_data: dict) -> None:
        self.validate_client_data(client_data)
        client = Client(
            id=None,
            prenom=client_data["prenom"],
            nom=client_data["nom"],
            email=client_data.get("email"),
            date_naissance=client_data.get("date_naissance"),
        )
        self.repo.add(client)

    def update_client(self, client: Client, client_data: dict) -> None:
        self.validate_client_data(client_data)
        client.prenom = client_data["prenom"]
        client.nom = client_data["nom"]
        client.email = client_data.get("email")
        client.date_naissance = client_data.get("date_naissance")
        self.repo.update(client)

    def delete_client(self, client_id: int) -> None:
        self.repo.delete(client_id)

    def update_client_anamnese(
        self, client_id: int, objectifs: str, antecedents: str
    ) -> None:
        self.repo.update_anamnese(client_id, objectifs, antecedents)

    def get_client_exclusions(self, client_id: int) -> List[int]:
        return self.repo.get_exclusions(client_id)

    def update_client_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        self.repo.update_exclusions(client_id, exercice_ids)
