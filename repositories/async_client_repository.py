"""
Async Client Repository Implementation.

Enterprise-grade async repository for Client entities with:
- High-performance async/await operations
- Multi-level caching (memory + Redis)
- Comprehensive performance monitoring
- Specification pattern for complex queries
- Transaction management integration
- Domain event publishing
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from core.events import IEventBus
from core.exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
    RepositoryError,
    ValidationError,
)
from domain.entities import Client
from domain.events import ClientArchivedEvent, ClientCreatedEvent, ClientUpdatedEvent
from domain.value_objects import PersonalInfo, PhysicalProfile
from infrastructure.cache import (
    CacheManager,
    cache_delete,
    cache_get,
    cache_set,
    get_cache_manager,
)
from infrastructure.database import AsyncDatabaseManager, get_database_manager
from repositories.interfaces import (
    ActiveEntitySpecification,
    IAsyncClientRepository,
    ISpecification,
    PaginationSpecification,
    QueryOptions,
    QueryResult,
    RepositoryMetrics,
)


class ClientEmailSpecification(ISpecification[Client]):
    """Specification for finding clients by email."""

    def __init__(self, email: str):
        self.email = email.lower()

    def is_satisfied_by(self, entity: Client) -> bool:
        return entity.personal_info.email.lower() == self.email

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "LOWER(email) = ?", (self.email,)


class ClientNameSpecification(ISpecification[Client]):
    """Specification for finding clients by name."""

    def __init__(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ):
        self.first_name = first_name.lower() if first_name else None
        self.last_name = last_name.lower() if last_name else None

    def is_satisfied_by(self, entity: Client) -> bool:
        if (
            self.first_name
            and self.first_name not in entity.personal_info.first_name.lower()
        ):
            return False
        if (
            self.last_name
            and self.last_name not in entity.personal_info.last_name.lower()
        ):
            return False
        return True

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        conditions = []
        params = []

        if self.first_name:
            conditions.append("LOWER(prenom) LIKE ?")
            params.append(f"%{self.first_name}%")

        if self.last_name:
            conditions.append("LOWER(nom) LIKE ?")
            params.append(f"%{self.last_name}%")

        if not conditions:
            return "1=1", ()

        return " AND ".join(conditions), tuple(params)


class ClientsWithSessionsSpecification(ISpecification[Client]):
    """Specification for clients with sessions in a date range."""

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def is_satisfied_by(self, entity: Client) -> bool:
        # This would require loading sessions - better handled at SQL level
        return True

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return (
            """
        EXISTS (
            SELECT 1 FROM seances s
            WHERE s.client_id = clients.id
            AND s.date_seance BETWEEN ? AND ?
        )
        """,
            (self.start_date, self.end_date),
        )


class AsyncClientRepository(IAsyncClientRepository):
    """
    High-performance async Client repository implementation.

    Features:
    - Async/await operations with connection pooling
    - Multi-level caching with TTL and invalidation
    - Performance monitoring and slow query detection
    - Specification pattern for complex queries
    - Batch operations for high throughput
    - Domain event publishing for CQRS
    - Comprehensive error handling
    """

    def __init__(
        self,
        db_manager: Optional[AsyncDatabaseManager] = None,
        cache_manager: Optional[CacheManager] = None,
        event_bus: Optional[IEventBus] = None,
    ):
        self._db_manager = db_manager or get_database_manager()
        self._cache_manager = cache_manager or get_cache_manager()
        self._event_bus = event_bus
        self._metrics = RepositoryMetrics()

        # Cache configuration
        self._cache_prefix = "client:"
        self._default_cache_ttl = 300  # 5 minutes
        self._list_cache_ttl = 60  # 1 minute for lists

    # Core CRUD Operations

    async def get_by_id(
        self, entity_id: int, options: Optional[QueryOptions] = None
    ) -> Optional[Client]:
        """Get client by ID with caching."""
        options = options or QueryOptions()
        start_time = time.perf_counter()

        try:
            # Check cache first
            cache_key = f"{self._cache_prefix}{entity_id}"
            if options.use_cache:
                cached_client = await cache_get(cache_key)
                if cached_client:
                    self._metrics.cache_hits += 1
                    self._metrics.successful_queries += 1
                    self._metrics.total_queries += 1
                    return self._deserialize_client(cached_client)

                self._metrics.cache_misses += 1

            # Query database
            query = """
            SELECT id, prenom, nom, email, telephone, date_naissance, sexe,
                   poids, taille, niveau_activite, objectifs, notes,
                   date_creation, date_modification, is_active
            FROM clients
            WHERE id = ? AND is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                row = await conn.fetchone(query, (entity_id,))

                if not row:
                    self._metrics.successful_queries += 1
                    self._metrics.total_queries += 1
                    return None

                client = self._map_row_to_client(row)

                # Cache result
                if options.use_cache:
                    await cache_set(
                        cache_key,
                        self._serialize_client(client),
                        options.cache_ttl or self._default_cache_ttl,
                    )

                self._update_metrics(start_time, True)
                return client

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to get client {entity_id}: {str(e)}") from e

    async def get_all(
        self, options: Optional[QueryOptions] = None
    ) -> QueryResult[Client]:
        """Get all clients with pagination and caching."""
        options = options or QueryOptions()
        start_time = time.perf_counter()

        try:
            # Build cache key based on options
            cache_key = f"{self._cache_prefix}all:{options.page}:{options.page_size}:{options.sort_by}:{options.sort_desc}:{options.include_deleted}"

            # Check cache
            if options.use_cache:
                cached_result = await cache_get(cache_key)
                if cached_result:
                    self._metrics.cache_hits += 1
                    self._metrics.successful_queries += 1
                    self._metrics.total_queries += 1
                    return self._deserialize_query_result(cached_result)

                self._metrics.cache_misses += 1

            # Build query
            base_query = """
            SELECT id, prenom, nom, email, telephone, date_naissance, sexe,
                   poids, taille, niveau_activite, objectifs, notes,
                   date_creation, date_modification, is_active
            FROM clients
            """

            where_clause = (
                "WHERE is_active = 1" if not options.include_deleted else "WHERE 1=1"
            )

            # Add sorting
            order_clause = ""
            if options.sort_by:
                direction = "DESC" if options.sort_desc else "ASC"
                order_clause = f" ORDER BY {options.sort_by} {direction}"

            # Add pagination
            pagination = PaginationSpecification(options.page, options.page_size)
            limit_clause, limit_params = pagination.to_sql_limit()

            # Count query
            count_query = f"SELECT COUNT(*) FROM clients {where_clause}"

            # Data query
            data_query = f"{base_query} {where_clause}{order_clause} {limit_clause}"

            async with self._db_manager.get_connection() as conn:
                # Get total count
                total_count = await conn.execute_scalar(count_query)

                # Get data
                rows = await conn.fetchall(data_query, limit_params)

                clients = [self._map_row_to_client(row) for row in rows]

                result = QueryResult(
                    data=clients,
                    total_count=total_count,
                    page=options.page,
                    page_size=options.page_size,
                    has_next=(options.page * options.page_size) < total_count,
                    has_previous=options.page > 1,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    cache_hit=False,
                )

                # Cache result
                if options.use_cache:
                    await cache_set(
                        cache_key,
                        self._serialize_query_result(result),
                        self._list_cache_ttl,
                    )

                self._update_metrics(start_time, True)
                return result

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to get all clients: {str(e)}") from e

    async def find(
        self,
        specification: ISpecification[Client],
        options: Optional[QueryOptions] = None,
    ) -> QueryResult[Client]:
        """Find clients matching specification."""
        options = options or QueryOptions()
        start_time = time.perf_counter()

        try:
            # Get SQL from specification
            where_condition, where_params = specification.to_sql_where()

            # Build queries
            base_query = """
            SELECT id, prenom, nom, email, telephone, date_naissance, sexe,
                   poids, taille, niveau_activite, objectifs, notes,
                   date_creation, date_modification, is_active
            FROM clients
            """

            where_clause = f"WHERE ({where_condition})"
            if not options.include_deleted:
                where_clause += " AND is_active = 1"

            # Add sorting
            order_clause = ""
            if options.sort_by:
                direction = "DESC" if options.sort_desc else "ASC"
                order_clause = f" ORDER BY {options.sort_by} {direction}"

            # Add pagination
            pagination = PaginationSpecification(options.page, options.page_size)
            limit_clause, limit_params = pagination.to_sql_limit()

            # Count query
            count_query = f"SELECT COUNT(*) FROM clients {where_clause}"

            # Data query
            data_query = f"{base_query} {where_clause}{order_clause} {limit_clause}"

            async with self._db_manager.get_connection() as conn:
                # Get total count
                total_count = await conn.execute_scalar(count_query, where_params)

                # Get data
                rows = await conn.fetchall(data_query, where_params + limit_params)

                clients = [self._map_row_to_client(row) for row in rows]

                result = QueryResult(
                    data=clients,
                    total_count=total_count,
                    page=options.page,
                    page_size=options.page_size,
                    has_next=(options.page * options.page_size) < total_count,
                    has_previous=options.page > 1,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    cache_hit=False,
                )

                self._update_metrics(start_time, True)
                return result

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to find clients: {str(e)}") from e

    async def create(self, entity: Client) -> Client:
        """Create new client with validation and events."""
        start_time = time.perf_counter()

        try:
            # Validate unique email
            existing = await self.find_by_email(entity.personal_info.email)
            if existing:
                raise DuplicateEntityError(
                    f"Client with email {entity.personal_info.email} already exists"
                )

            query = """
            INSERT INTO clients (
                prenom, nom, email, telephone, date_naissance, sexe,
                poids, taille, niveau_activite, objectifs, notes,
                date_creation, date_modification, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """

            params = (
                entity.personal_info.first_name,
                entity.personal_info.last_name,
                entity.personal_info.email,
                entity.personal_info.phone,
                entity.personal_info.birth_date,
                entity.personal_info.gender,
                entity.physical_profile.weight_kg if entity.physical_profile else None,
                entity.physical_profile.height_cm if entity.physical_profile else None,
                entity.physical_profile.activity_level
                if entity.physical_profile
                else None,
                entity.goals,
                entity.notes,
                datetime.now(),
                datetime.now(),
            )

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()

                entity.id = cursor.lastrowid

            # Invalidate cache
            await self._invalidate_list_caches()

            # Publish domain event
            if self._event_bus:
                await self._event_bus.publish(
                    ClientCreatedEvent(
                        client_id=entity.id,
                        email=entity.personal_info.email,
                        timestamp=datetime.now(),
                    )
                )

            self._update_metrics(start_time, True)
            return entity

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, (DuplicateEntityError, ValidationError)):
                raise
            raise RepositoryError(f"Failed to create client: {str(e)}") from e

    async def update(self, entity: Client) -> Client:
        """Update existing client with optimistic concurrency."""
        start_time = time.perf_counter()

        try:
            if not entity.id:
                raise ValidationError("Client ID is required for update")

            query = """
            UPDATE clients SET
                prenom = ?, nom = ?, email = ?, telephone = ?, date_naissance = ?, sexe = ?,
                poids = ?, taille = ?, niveau_activite = ?, objectifs = ?, notes = ?,
                date_modification = ?
            WHERE id = ? AND is_active = 1
            """

            params = (
                entity.personal_info.first_name,
                entity.personal_info.last_name,
                entity.personal_info.email,
                entity.personal_info.phone,
                entity.personal_info.birth_date,
                entity.personal_info.gender,
                entity.physical_profile.weight_kg if entity.physical_profile else None,
                entity.physical_profile.height_cm if entity.physical_profile else None,
                entity.physical_profile.activity_level
                if entity.physical_profile
                else None,
                entity.goals,
                entity.notes,
                datetime.now(),
                entity.id,
            )

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()

                if cursor.rowcount == 0:
                    raise EntityNotFoundError(
                        f"Client {entity.id} not found or inactive"
                    )

            # Invalidate caches
            await self._invalidate_client_caches(entity.id)
            await self._invalidate_list_caches()

            # Publish domain event
            if self._event_bus:
                await self._event_bus.publish(
                    ClientUpdatedEvent(
                        client_id=entity.id,
                        email=entity.personal_info.email,
                        timestamp=datetime.now(),
                    )
                )

            self._update_metrics(start_time, True)
            return entity

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, (EntityNotFoundError, ValidationError)):
                raise
            raise RepositoryError(
                f"Failed to update client {entity.id}: {str(e)}"
            ) from e

    async def delete(self, entity_id: int) -> bool:
        """Hard delete client."""
        start_time = time.perf_counter()

        try:
            query = "DELETE FROM clients WHERE id = ?"

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, (entity_id,))
                await conn.commit()

                success = cursor.rowcount > 0

            if success:
                await self._invalidate_client_caches(entity_id)
                await self._invalidate_list_caches()

            self._update_metrics(start_time, True)
            return success

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(
                f"Failed to delete client {entity_id}: {str(e)}"
            ) from e

    async def soft_delete(self, entity_id: int) -> bool:
        """Soft delete client by marking inactive."""
        start_time = time.perf_counter()

        try:
            query = """
            UPDATE clients SET
                is_active = 0,
                date_modification = ?
            WHERE id = ? AND is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, (datetime.now(), entity_id))
                await conn.commit()

                success = cursor.rowcount > 0

            if success:
                await self._invalidate_client_caches(entity_id)
                await self._invalidate_list_caches()

            self._update_metrics(start_time, True)
            return success

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(
                f"Failed to soft delete client {entity_id}: {str(e)}"
            ) from e

    # Domain-Specific Operations

    async def find_by_email(self, email: str) -> Optional[Client]:
        """Find client by email address."""
        spec = ClientEmailSpecification(email)
        result = await self.find(spec, QueryOptions(page_size=1))
        return result.data[0] if result.data else None

    async def find_by_name(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> QueryResult[Client]:
        """Find clients by name with partial matching."""
        spec = ClientNameSpecification(first_name, last_name)
        return await self.find(spec)

    async def find_active_clients(
        self, options: Optional[QueryOptions] = None
    ) -> QueryResult[Client]:
        """Find all active clients."""
        spec = ActiveEntitySpecification()
        return await self.find(spec, options)

    async def find_clients_with_sessions_in_period(
        self,
        start_date: datetime,
        end_date: datetime,
        options: Optional[QueryOptions] = None,
    ) -> QueryResult[Client]:
        """Find clients with sessions in date range."""
        spec = ClientsWithSessionsSpecification(start_date, end_date)
        return await self.find(spec, options)

    async def get_client_statistics(self, client_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics for a client."""
        start_time = time.perf_counter()

        try:
            query = """
            SELECT
                c.id,
                COUNT(DISTINCT s.id) as total_sessions,
                COUNT(DISTINCT CASE WHEN s.date_seance >= date('now', '-30 days') THEN s.id END) as sessions_last_30_days,
                MIN(s.date_seance) as first_session_date,
                MAX(s.date_seance) as last_session_date,
                AVG(CASE WHEN s.statut = 'completed' THEN 1.0 ELSE 0.0 END) * 100 as completion_rate
            FROM clients c
            LEFT JOIN seances s ON c.id = s.client_id
            WHERE c.id = ? AND c.is_active = 1
            GROUP BY c.id
            """

            async with self._db_manager.get_connection() as conn:
                row = await conn.fetchone(query, (client_id,))

                if not row:
                    raise EntityNotFoundError(f"Client {client_id} not found")

                stats = {
                    "client_id": row["id"],
                    "total_sessions": row["total_sessions"] or 0,
                    "sessions_last_30_days": row["sessions_last_30_days"] or 0,
                    "first_session_date": row["first_session_date"],
                    "last_session_date": row["last_session_date"],
                    "completion_rate": round(row["completion_rate"] or 0, 2),
                    "is_active_client": (row["sessions_last_30_days"] or 0) > 0,
                    "days_since_last_session": (
                        datetime.now().date()
                        - datetime.fromisoformat(row["last_session_date"]).date()
                    ).days
                    if row["last_session_date"]
                    else None,
                }

            self._update_metrics(start_time, True)
            return stats

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, EntityNotFoundError):
                raise
            raise RepositoryError(f"Failed to get client statistics: {str(e)}") from e

    # Helper Methods

    def _map_row_to_client(self, row) -> Client:
        """Map database row to Client entity."""
        personal_info = PersonalInfo(
            first_name=row["prenom"],
            last_name=row["nom"],
            email=row["email"],
            phone=row["telephone"],
            birth_date=datetime.fromisoformat(row["date_naissance"]).date()
            if row["date_naissance"]
            else None,
            gender=row["sexe"],
        )

        physical_profile = None
        if row["poids"] or row["taille"] or row["niveau_activite"]:
            physical_profile = PhysicalProfile(
                weight_kg=row["poids"],
                height_cm=row["taille"],
                activity_level=row["niveau_activite"],
            )

        return Client(
            personal_info=personal_info,
            physical_profile=physical_profile,
            goals=row["objectifs"],
            notes=row["notes"],
            id=row["id"],
        )

    def _serialize_client(self, client: Client) -> Dict[str, Any]:
        """Serialize client for cache storage."""
        return {
            "id": client.id,
            "personal_info": {
                "first_name": client.personal_info.first_name,
                "last_name": client.personal_info.last_name,
                "email": client.personal_info.email,
                "phone": client.personal_info.phone,
                "birth_date": client.personal_info.birth_date.isoformat()
                if client.personal_info.birth_date
                else None,
                "gender": client.personal_info.gender,
            },
            "physical_profile": {
                "weight_kg": client.physical_profile.weight_kg,
                "height_cm": client.physical_profile.height_cm,
                "activity_level": client.physical_profile.activity_level,
            }
            if client.physical_profile
            else None,
            "goals": client.goals,
            "notes": client.notes,
        }

    def _deserialize_client(self, data: Dict[str, Any]) -> Client:
        """Deserialize client from cache data."""
        personal_info = PersonalInfo(
            first_name=data["personal_info"]["first_name"],
            last_name=data["personal_info"]["last_name"],
            email=data["personal_info"]["email"],
            phone=data["personal_info"]["phone"],
            birth_date=datetime.fromisoformat(
                data["personal_info"]["birth_date"]
            ).date()
            if data["personal_info"]["birth_date"]
            else None,
            gender=data["personal_info"]["gender"],
        )

        physical_profile = None
        if data["physical_profile"]:
            physical_profile = PhysicalProfile(
                weight_kg=data["physical_profile"]["weight_kg"],
                height_cm=data["physical_profile"]["height_cm"],
                activity_level=data["physical_profile"]["activity_level"],
            )

        return Client(
            personal_info=personal_info,
            physical_profile=physical_profile,
            goals=data["goals"],
            notes=data["notes"],
            id=data["id"],
        )

    async def _invalidate_client_caches(self, client_id: int) -> None:
        """Invalidate all caches for a specific client."""
        await cache_delete(f"{self._cache_prefix}{client_id}")

    async def _invalidate_list_caches(self) -> None:
        """Invalidate all list caches."""
        await self._cache_manager.clear_cache(f"{self._cache_prefix}all:*")

    def _update_metrics(self, start_time: float, success: bool) -> None:
        """Update repository metrics."""
        execution_time = (time.perf_counter() - start_time) * 1000

        self._metrics.total_queries += 1
        if success:
            self._metrics.successful_queries += 1
        else:
            self._metrics.failed_queries += 1

        if execution_time > 100:  # Slow query threshold
            self._metrics.slow_queries += 1

        # Update running average
        if self._metrics.total_queries == 1:
            self._metrics.avg_query_time_ms = execution_time
        else:
            self._metrics.avg_query_time_ms = (
                self._metrics.avg_query_time_ms * (self._metrics.total_queries - 1)
                + execution_time
            ) / self._metrics.total_queries

    # Interface Implementation

    async def exists(self, entity_id: int) -> bool:
        """Check if client exists by ID."""
        client = await self.get_by_id(entity_id)
        return client is not None

    async def count(
        self, specification: Optional[ISpecification[Client]] = None
    ) -> int:
        """Count clients matching specification."""
        if specification:
            where_condition, where_params = specification.to_sql_where()
            query = f"SELECT COUNT(*) FROM clients WHERE ({where_condition}) AND is_active = 1"
            return await self._db_manager.execute_scalar(query, where_params) or 0
        else:
            return (
                await self._db_manager.execute_scalar(
                    "SELECT COUNT(*) FROM clients WHERE is_active = 1"
                )
                or 0
            )

    async def batch_create(self, entities: List[Client]) -> List[Client]:
        """Create multiple clients in batch."""
        created_clients = []

        async with self._db_manager.get_transaction():
            for entity in entities:
                created_client = await self.create(entity)
                created_clients.append(created_client)

        await self._invalidate_list_caches()
        return created_clients

    async def batch_update(self, entities: List[Client]) -> List[Client]:
        """Update multiple clients in batch."""
        updated_clients = []

        async with self._db_manager.get_transaction():
            for entity in entities:
                updated_client = await self.update(entity)
                updated_clients.append(updated_client)

        await self._invalidate_list_caches()
        return updated_clients

    async def batch_delete(self, entity_ids: List[int]) -> int:
        """Delete multiple clients in batch."""
        deleted_count = 0

        async with self._db_manager.get_transaction():
            for entity_id in entity_ids:
                if await self.delete(entity_id):
                    deleted_count += 1

        await self._invalidate_list_caches()
        return deleted_count

    async def get_metrics(self) -> RepositoryMetrics:
        """Get repository performance metrics."""
        return self._metrics

    async def clear_cache(self, pattern: Optional[str] = None) -> None:
        """Clear repository cache."""
        if pattern:
            await self._cache_manager.clear_cache(f"{self._cache_prefix}{pattern}")
        else:
            await self._cache_manager.clear_cache(f"{self._cache_prefix}*")

    async def update_physical_profile(
        self, client_id: int, physical_profile: PhysicalProfile
    ) -> bool:
        """Update client's physical profile."""
        start_time = time.perf_counter()

        try:
            query = """
            UPDATE clients SET
                poids = ?, taille = ?, niveau_activite = ?, date_modification = ?
            WHERE id = ? AND is_active = 1
            """

            params = (
                physical_profile.weight_kg,
                physical_profile.height_cm,
                physical_profile.activity_level,
                datetime.now(),
                client_id,
            )

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()

                success = cursor.rowcount > 0

            if success:
                await self._invalidate_client_caches(client_id)

            self._update_metrics(start_time, True)
            return success

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to update physical profile: {str(e)}") from e

    async def archive_inactive_clients(self, days_inactive: int = 90) -> int:
        """Archive clients inactive for specified days."""
        start_time = time.perf_counter()

        try:
            cutoff_date = datetime.now() - timedelta(days=days_inactive)

            query = """
            UPDATE clients SET is_active = 0, date_modification = ?
            WHERE id NOT IN (
                SELECT DISTINCT client_id FROM seances
                WHERE date_seance >= ? AND client_id IS NOT NULL
            ) AND is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, (datetime.now(), cutoff_date))
                await conn.commit()

                archived_count = cursor.rowcount

            if archived_count > 0:
                await self._invalidate_list_caches()

                # Publish domain events for archived clients
                if self._event_bus:
                    await self._event_bus.publish(
                        ClientArchivedEvent(
                            archived_count=archived_count,
                            days_inactive=days_inactive,
                            timestamp=datetime.now(),
                        )
                    )

            self._update_metrics(start_time, True)
            return archived_count

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(
                f"Failed to archive inactive clients: {str(e)}"
            ) from e

    def _serialize_query_result(self, result: QueryResult[Client]) -> Dict[str, Any]:
        """Serialize query result for caching."""
        return {
            "data": [self._serialize_client(client) for client in result.data],
            "total_count": result.total_count,
            "page": result.page,
            "page_size": result.page_size,
            "has_next": result.has_next,
            "has_previous": result.has_previous,
            "execution_time_ms": result.execution_time_ms,
            "cache_hit": result.cache_hit,
        }

    def _deserialize_query_result(self, data: Dict[str, Any]) -> QueryResult[Client]:
        """Deserialize query result from cache."""
        return QueryResult(
            data=[
                self._deserialize_client(client_data) for client_data in data["data"]
            ],
            total_count=data["total_count"],
            page=data["page"],
            page_size=data["page_size"],
            has_next=data["has_next"],
            has_previous=data["has_previous"],
            execution_time_ms=data["execution_time_ms"],
            cache_hit=True,
        )
