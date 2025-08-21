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

    def add_client(self, client_data: dict) -> None:
        client = Client(
            id=None,
            prenom=client_data["prenom"],
            nom=client_data["nom"],
            email=client_data["email"],
            date_naissance=client_data["date_naissance"],
        )
        self.repo.add(client)

    def update_client(self, client: Client, client_data: dict) -> None:
        client.prenom = client_data["prenom"]
        client.nom = client_data["nom"]
        client.email = client_data["email"]
        client.date_naissance = client_data["date_naissance"]
        self.repo.update(client)

    def update_client_anamnese(
        self, client_id: int, objectifs: str, antecedents: str
    ) -> None:
        self.repo.update_anamnese(client_id, objectifs, antecedents)

    def get_client_exclusions(self, client_id: int) -> List[int]:
        return self.repo.get_exclusions(client_id)

    def update_client_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        self.repo.update_exclusions(client_id, exercice_ids)
