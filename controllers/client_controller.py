from typing import List, Optional

from models.client import Client
from services.client_service import ClientService


class ClientController:
    """Controller providing CRUD operations for clients."""

    def __init__(self, service: ClientService) -> None:
        self.service = service

    def get_all_clients_for_view(self) -> List[Client]:
        return self.service.get_all_clients()

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.service.get_client_by_id(client_id)

    def add_client(self, data: dict) -> None:
        self.service.add_client(data)

    def update_client(self, client_id: int, data: dict) -> None:
        client = self.service.get_client_by_id(client_id)
        if not client:
            raise ValueError("Client introuvable")
        self.service.update_client(client, data)

    def delete_client(self, client_id: int) -> None:
        self.service.delete_client(client_id)

    def update_client_anamnese(
        self, client_id: int, objectifs: str, antecedents: str
    ) -> None:
        self.service.update_client_anamnese(client_id, objectifs, antecedents)

    def get_client_exclusions(self, client_id: int) -> List[int]:
        return self.service.get_client_exclusions(client_id)

    def update_client_exclusions(self, client_id: int, exercice_ids: List[int]) -> None:
        self.service.update_client_exclusions(client_id, exercice_ids)
