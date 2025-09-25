"""Client Controller with dependency injection and async support."""

from __future__ import annotations

import asyncio
from functools import wraps
from typing import List, Optional, Dict, Any, Callable, TypeVar, Awaitable

from core.container import Injectable, ServiceLifetime
from core.events import IEventBus
from core.exceptions import (
    BusinessRuleViolationError,
    ValidationError,
    ControllerError,
)
from models.client import Client
from repositories.interfaces import QueryOptions, QueryResult
from services.client_service import ClientService

T = TypeVar('T')


def handle_async_in_sync(func: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """Decorator to handle async operations in sync context (for UI compatibility)."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, create a new thread
                import concurrent.futures
                import threading

                def run_in_thread():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(func(*args, **kwargs))
                    finally:
                        new_loop.close()

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    return future.result()
            else:
                return loop.run_until_complete(func(*args, **kwargs))
        except RuntimeError:
            # No event loop running, create one
            return asyncio.run(func(*args, **kwargs))
        except Exception as e:
            # Re-raise domain exceptions, wrap others
            if isinstance(e, (ValidationError, BusinessRuleViolationError)):
                raise
            raise ControllerError(f"Error in {func.__name__}: {str(e)}") from e

    return wrapper


@Injectable(ServiceLifetime.TRANSIENT)
class ClientController:
    """Controller providing CRUD operations for clients with enterprise patterns."""

    def __init__(
        self,
        client_service: ClientService,
        event_bus: Optional[IEventBus] = None,
    ) -> None:
        self._client_service = client_service
        self._event_bus = event_bus

    # Sync wrapper methods for UI compatibility

    @handle_async_in_sync
    async def get_all_clients_for_view(
        self,
        page: int = 1,
        page_size: int = 50,
        sort_by: Optional[str] = None,
        sort_desc: bool = False
    ) -> List[Client]:
        """Get all clients for view with optional pagination and sorting."""
        options = QueryOptions(
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_desc=sort_desc
        )
        result = await self._client_service.get_all_clients(options)
        return result.data

    @handle_async_in_sync
    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Get client by ID."""
        return await self._client_service.get_client_by_id(client_id)

    @handle_async_in_sync
    async def add_client(self, data: Dict[str, Any]) -> Client:
        """Add new client with validation."""
        return await self._client_service.create_client(data)

    @handle_async_in_sync
    async def update_client(self, client_id: int, data: Dict[str, Any]) -> Client:
        """Update existing client."""
        return await self._client_service.update_client(client_id, data)

    @handle_async_in_sync
    async def delete_client(self, client_id: int) -> bool:
        """Delete client by ID."""
        return await self._client_service.delete_client(client_id)

    @handle_async_in_sync
    async def update_client_anamnese(
        self, client_id: int, objectifs: str, antecedents: str
    ) -> Client:
        """Update client anamnesis."""
        return await self._client_service.update_client_anamnese(
            client_id, objectifs, antecedents
        )

    @handle_async_in_sync
    async def get_client_exclusions(self, client_id: int) -> List[int]:
        """Get client exercise exclusions."""
        return await self._client_service.get_client_exclusions(client_id)

    @handle_async_in_sync
    async def update_client_exclusions(
        self, client_id: int, exercise_ids: List[int]
    ) -> Client:
        """Update client exercise exclusions."""
        return await self._client_service.update_client_exclusions(
            client_id, exercise_ids
        )

    # Legacy compatibility methods

    def get_all_clients_for_view_legacy(self) -> List[Client]:
        """Legacy method for backward compatibility."""
        return self.get_all_clients_for_view()

    def add_client_legacy(self, data: dict) -> None:
        """Legacy method that converts old data format."""
        # Convert old format to new format
        new_data = {
            "first_name": data.get("prenom", ""),
            "last_name": data.get("nom", ""),
            "email": data.get("email"),
            "birth_date": data.get("date_naissance"),
            "weight_kg": data.get("poids_kg"),
            "height_cm": data.get("taille_cm"),
            "objectives": data.get("objectifs"),
            "medical_history": data.get("antecedents_medicaux"),
        }
        self.add_client(new_data)

    def update_client_legacy(self, client_id: int, data: dict) -> None:
        """Legacy method that converts old data format."""
        # Convert old format to new format
        new_data = {
            "first_name": data.get("prenom"),
            "last_name": data.get("nom"),
            "email": data.get("email"),
            "birth_date": data.get("date_naissance"),
            "weight_kg": data.get("poids_kg"),
            "height_cm": data.get("taille_cm"),
            "objectives": data.get("objectifs"),
            "medical_history": data.get("antecedents_medicaux"),
        }
        # Remove None values
        new_data = {k: v for k, v in new_data.items() if v is not None}
        self.update_client(client_id, new_data)

    def delete_client_legacy(self, client_id: int) -> None:
        """Legacy method for backward compatibility."""
        self.delete_client(client_id)

    @property
    def service(self) -> ClientService:
        """Legacy property access to service."""
        return self._client_service
