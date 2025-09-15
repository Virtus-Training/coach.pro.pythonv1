"""
Async Session Repository Implementation.

Enterprise-grade async repository for Session entities with:
- High-performance async/await operations
- Advanced transaction management
- Comprehensive caching with invalidation strategies
- Complex query specifications for workout analytics
- Bulk operations for scheduling and management
- Domain event publishing for session lifecycle
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, date
from typing import Any, Dict, List, Optional, Tuple

from domain.entities import Session, Exercise
from domain.events import SessionCreatedEvent, SessionUpdatedEvent, SessionCompletedEvent
from infrastructure.database import AsyncDatabaseManager, get_database_manager
from infrastructure.cache import CacheManager, get_cache_manager, cache_get, cache_set, cache_delete
from repositories.interfaces import (
    IAsyncSessionRepository,
    QueryResult,
    QueryOptions,
    RepositoryMetrics,
    ISpecification,
    ActiveEntitySpecification,
    DateRangeSpecification,
    PaginationSpecification,
)
from core.events import IEventBus
from core.exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
    RepositoryError,
    ValidationError,
    BusinessRuleViolationError,
)


class SessionByClientSpecification(ISpecification[Session]):
    """Specification for finding sessions by client ID."""

    def __init__(self, client_id: int):
        self.client_id = client_id

    def is_satisfied_by(self, entity: Session) -> bool:
        return entity.client_id == self.client_id

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "client_id = ?", (self.client_id,)


class SessionByStatusSpecification(ISpecification[Session]):
    """Specification for finding sessions by status."""

    def __init__(self, status: str):
        self.status = status

    def is_satisfied_by(self, entity: Session) -> bool:
        return entity.status == self.status

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        return "statut = ?", (self.status,)


class UpcomingSessionsSpecification(ISpecification[Session]):
    """Specification for upcoming sessions."""

    def __init__(self, days_ahead: int = 7, client_id: Optional[int] = None):
        self.start_date = datetime.now().date()
        self.end_date = (datetime.now() + timedelta(days=days_ahead)).date()
        self.client_id = client_id

    def is_satisfied_by(self, entity: Session) -> bool:
        session_date = entity.date_seance.date() if isinstance(entity.date_seance, datetime) else entity.date_seance
        date_match = self.start_date <= session_date <= self.end_date
        client_match = self.client_id is None or entity.client_id == self.client_id
        return date_match and client_match

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        conditions = ["date_seance BETWEEN ? AND ?"]
        params = [self.start_date, self.end_date]

        if self.client_id:
            conditions.append("client_id = ?")
            params.append(self.client_id)

        return " AND ".join(conditions), tuple(params)


class CompletedSessionsSpecification(ISpecification[Session]):
    """Specification for completed sessions."""

    def __init__(self, client_id: Optional[int] = None):
        self.client_id = client_id

    def is_satisfied_by(self, entity: Session) -> bool:
        status_match = entity.status == 'completed'
        client_match = self.client_id is None or entity.client_id == self.client_id
        return status_match and client_match

    def to_sql_where(self) -> tuple[str, tuple[Any, ...]]:
        conditions = ["statut = 'completed'"]
        params = []

        if self.client_id:
            conditions.append("client_id = ?")
            params.append(self.client_id)

        return " AND ".join(conditions), tuple(params)


class AsyncSessionRepository(IAsyncSessionRepository):
    """
    High-performance async Session repository implementation.

    Features:
    - Complex workout analytics queries
    - Advanced transaction management
    - Multi-level caching with smart invalidation
    - Bulk scheduling operations
    - Session cloning and templating
    - Performance monitoring with detailed metrics
    - Domain event integration
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
        self._cache_prefix = "session:"
        self._default_cache_ttl = 300  # 5 minutes
        self._list_cache_ttl = 60  # 1 minute for lists
        self._analytics_cache_ttl = 600  # 10 minutes for analytics

    # Core CRUD Operations

    async def get_by_id(
        self,
        entity_id: int,
        options: Optional[QueryOptions] = None
    ) -> Optional[Session]:
        """Get session by ID with caching."""
        options = options or QueryOptions()
        start_time = time.perf_counter()

        try:
            # Check cache first
            cache_key = f"{self._cache_prefix}{entity_id}"
            if options.use_cache:
                cached_session = await cache_get(cache_key)
                if cached_session:
                    self._metrics.cache_hits += 1
                    self._metrics.successful_queries += 1
                    self._metrics.total_queries += 1
                    return self._deserialize_session(cached_session)

                self._metrics.cache_misses += 1

            # Query database with JOIN for client info
            query = """
            SELECT s.id, s.client_id, s.date_seance, s.heure_debut, s.heure_fin,
                   s.type_seance, s.statut, s.exercices_json, s.notes,
                   s.date_creation, s.date_modification, s.is_active,
                   c.prenom as client_prenom, c.nom as client_nom
            FROM seances s
            LEFT JOIN clients c ON s.client_id = c.id
            WHERE s.id = ? AND s.is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                row = await conn.fetchone(query, (entity_id,))

                if not row:
                    self._metrics.successful_queries += 1
                    self._metrics.total_queries += 1
                    return None

                session = self._map_row_to_session(row)

                # Cache result
                if options.use_cache:
                    await cache_set(cache_key, self._serialize_session(session), options.cache_ttl or self._default_cache_ttl)

                self._update_metrics(start_time, True)
                return session

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to get session {entity_id}: {str(e)}") from e

    async def get_all(
        self,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Get all sessions with pagination and caching."""
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

            # Build query with JOIN
            base_query = """
            SELECT s.id, s.client_id, s.date_seance, s.heure_debut, s.heure_fin,
                   s.type_seance, s.statut, s.exercices_json, s.notes,
                   s.date_creation, s.date_modification, s.is_active,
                   c.prenom as client_prenom, c.nom as client_nom
            FROM seances s
            LEFT JOIN clients c ON s.client_id = c.id
            """

            where_clause = "WHERE s.is_active = 1" if not options.include_deleted else "WHERE 1=1"

            # Add sorting (default by date descending)
            sort_field = options.sort_by or "s.date_seance"
            direction = "DESC" if options.sort_desc else "ASC"
            order_clause = f" ORDER BY {sort_field} {direction}"

            # Add pagination
            pagination = PaginationSpecification(options.page, options.page_size)
            limit_clause, limit_params = pagination.to_sql_limit()

            # Count query
            count_query = f"SELECT COUNT(*) FROM seances s {where_clause}"

            # Data query
            data_query = f"{base_query} {where_clause}{order_clause} {limit_clause}"

            async with self._db_manager.get_connection() as conn:
                # Get total count
                total_count = await conn.execute_scalar(count_query)

                # Get data
                rows = await conn.fetchall(data_query, limit_params)

                sessions = [self._map_row_to_session(row) for row in rows]

                result = QueryResult(
                    data=sessions,
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
                    await cache_set(cache_key, self._serialize_query_result(result), self._list_cache_ttl)

                self._update_metrics(start_time, True)
                return result

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to get all sessions: {str(e)}") from e

    async def find(
        self,
        specification: ISpecification[Session],
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find sessions matching specification."""
        options = options or QueryOptions()
        start_time = time.perf_counter()

        try:
            # Get SQL from specification
            where_condition, where_params = specification.to_sql_where()

            # Build queries with JOIN
            base_query = """
            SELECT s.id, s.client_id, s.date_seance, s.heure_debut, s.heure_fin,
                   s.type_seance, s.statut, s.exercices_json, s.notes,
                   s.date_creation, s.date_modification, s.is_active,
                   c.prenom as client_prenom, c.nom as client_nom
            FROM seances s
            LEFT JOIN clients c ON s.client_id = c.id
            """

            where_clause = f"WHERE ({where_condition})"
            if not options.include_deleted:
                where_clause += " AND s.is_active = 1"

            # Add sorting
            sort_field = options.sort_by or "s.date_seance"
            direction = "DESC" if options.sort_desc else "ASC"
            order_clause = f" ORDER BY {sort_field} {direction}"

            # Add pagination
            pagination = PaginationSpecification(options.page, options.page_size)
            limit_clause, limit_params = pagination.to_sql_limit()

            # Count query
            count_query = f"SELECT COUNT(*) FROM seances s LEFT JOIN clients c ON s.client_id = c.id {where_clause}"

            # Data query
            data_query = f"{base_query} {where_clause}{order_clause} {limit_clause}"

            async with self._db_manager.get_connection() as conn:
                # Get total count
                total_count = await conn.execute_scalar(count_query, where_params)

                # Get data
                rows = await conn.fetchall(data_query, where_params + limit_params)

                sessions = [self._map_row_to_session(row) for row in rows]

                result = QueryResult(
                    data=sessions,
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
            raise RepositoryError(f"Failed to find sessions: {str(e)}") from e

    async def create(self, entity: Session) -> Session:
        """Create new session with validation and events."""
        start_time = time.perf_counter()

        try:
            # Validate business rules
            await self._validate_session_creation(entity)

            query = """
            INSERT INTO seances (
                client_id, date_seance, heure_debut, heure_fin,
                type_seance, statut, exercices_json, notes,
                date_creation, date_modification, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """

            # Serialize exercises to JSON
            exercices_json = json.dumps(entity.exercices) if entity.exercices else None

            params = (
                entity.client_id,
                entity.date_seance,
                entity.heure_debut,
                entity.heure_fin,
                entity.type_seance,
                entity.status,
                exercices_json,
                entity.notes,
                datetime.now(),
                datetime.now(),
            )

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()

                entity.id = cursor.lastrowid

            # Invalidate cache
            await self._invalidate_session_caches(entity.client_id)

            # Publish domain event
            if self._event_bus:
                await self._event_bus.publish(SessionCreatedEvent(
                    session_id=entity.id,
                    client_id=entity.client_id,
                    session_date=entity.date_seance,
                    session_type=entity.type_seance,
                    timestamp=datetime.now()
                ))

            self._update_metrics(start_time, True)
            return entity

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, (ValidationError, BusinessRuleViolationError)):
                raise
            raise RepositoryError(f"Failed to create session: {str(e)}") from e

    async def update(self, entity: Session) -> Session:
        """Update existing session with validation."""
        start_time = time.perf_counter()

        try:
            if not entity.id:
                raise ValidationError("Session ID is required for update")

            # Check if status changed to completed
            old_session = await self.get_by_id(entity.id)
            status_changed_to_completed = (
                old_session and
                old_session.status != 'completed' and
                entity.status == 'completed'
            )

            query = """
            UPDATE seances SET
                client_id = ?, date_seance = ?, heure_debut = ?, heure_fin = ?,
                type_seance = ?, statut = ?, exercices_json = ?, notes = ?,
                date_modification = ?
            WHERE id = ? AND is_active = 1
            """

            # Serialize exercises to JSON
            exercices_json = json.dumps(entity.exercices) if entity.exercices else None

            params = (
                entity.client_id,
                entity.date_seance,
                entity.heure_debut,
                entity.heure_fin,
                entity.type_seance,
                entity.status,
                exercices_json,
                entity.notes,
                datetime.now(),
                entity.id,
            )

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()

                if cursor.rowcount == 0:
                    raise EntityNotFoundError(f"Session {entity.id} not found or inactive")

            # Invalidate caches
            await self._invalidate_single_session_cache(entity.id)
            await self._invalidate_session_caches(entity.client_id)

            # Publish domain events
            if self._event_bus:
                await self._event_bus.publish(SessionUpdatedEvent(
                    session_id=entity.id,
                    client_id=entity.client_id,
                    session_date=entity.date_seance,
                    timestamp=datetime.now()
                ))

                # Publish completion event if status changed
                if status_changed_to_completed:
                    await self._event_bus.publish(SessionCompletedEvent(
                        session_id=entity.id,
                        client_id=entity.client_id,
                        completion_date=datetime.now(),
                        duration_minutes=self._calculate_session_duration(entity),
                        timestamp=datetime.now()
                    ))

            self._update_metrics(start_time, True)
            return entity

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, (EntityNotFoundError, ValidationError)):
                raise
            raise RepositoryError(f"Failed to update session {entity.id}: {str(e)}") from e

    # Domain-Specific Operations

    async def find_by_client(
        self,
        client_id: int,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find sessions by client ID."""
        spec = SessionByClientSpecification(client_id)
        return await self.find(spec, options)

    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        client_id: Optional[int] = None,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find sessions in date range."""
        date_spec = DateRangeSpecification(start_date, end_date, 'date_seance')

        if client_id:
            client_spec = SessionByClientSpecification(client_id)
            combined_spec = date_spec.and_specification(client_spec)
        else:
            combined_spec = date_spec

        return await self.find(combined_spec, options)

    async def find_upcoming_sessions(
        self,
        client_id: Optional[int] = None,
        days_ahead: int = 7,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find upcoming sessions."""
        spec = UpcomingSessionsSpecification(days_ahead, client_id)
        return await self.find(spec, options)

    async def find_completed_sessions(
        self,
        client_id: Optional[int] = None,
        options: Optional[QueryOptions] = None
    ) -> QueryResult[Session]:
        """Find completed sessions."""
        spec = CompletedSessionsSpecification(client_id)
        return await self.find(spec, options)

    async def get_session_analytics(
        self,
        client_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get comprehensive session analytics and metrics."""
        start_time = time.perf_counter()

        try:
            # Build cache key for analytics
            cache_key = f"{self._cache_prefix}analytics:{client_id}:{start_date}:{end_date}"

            # Check cache
            cached_analytics = await cache_get(cache_key)
            if cached_analytics:
                self._metrics.cache_hits += 1
                return cached_analytics

            self._metrics.cache_misses += 1

            # Default date range (last 30 days)
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()

            # Build query conditions
            date_conditions = "s.date_seance BETWEEN ? AND ?"
            params = [start_date, end_date]

            if client_id:
                date_conditions += " AND s.client_id = ?"
                params.append(client_id)

            query = f"""
            SELECT
                COUNT(*) as total_sessions,
                COUNT(CASE WHEN s.statut = 'completed' THEN 1 END) as completed_sessions,
                COUNT(CASE WHEN s.statut = 'cancelled' THEN 1 END) as cancelled_sessions,
                COUNT(CASE WHEN s.statut = 'scheduled' THEN 1 END) as scheduled_sessions,
                COUNT(DISTINCT s.client_id) as unique_clients,
                AVG(CASE WHEN s.statut = 'completed' THEN
                    (JULIANDAY(s.heure_fin) - JULIANDAY(s.heure_debut)) * 24 * 60
                END) as avg_session_duration_minutes,
                COUNT(CASE WHEN s.type_seance = 'individuel' THEN 1 END) as individual_sessions,
                COUNT(CASE WHEN s.type_seance = 'collectif' THEN 1 END) as group_sessions,
                MIN(s.date_seance) as first_session_date,
                MAX(s.date_seance) as last_session_date
            FROM seances s
            WHERE {date_conditions} AND s.is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                row = await conn.fetchone(query, params)

                # Calculate additional metrics
                completion_rate = 0.0
                if row['total_sessions'] > 0:
                    completion_rate = (row['completed_sessions'] / row['total_sessions']) * 100

                cancellation_rate = 0.0
                if row['total_sessions'] > 0:
                    cancellation_rate = (row['cancelled_sessions'] / row['total_sessions']) * 100

                # Get most popular session times
                time_query = f"""
                SELECT
                    strftime('%H', s.heure_debut) as hour,
                    COUNT(*) as session_count
                FROM seances s
                WHERE {date_conditions} AND s.is_active = 1 AND s.statut = 'completed'
                GROUP BY strftime('%H', s.heure_debut)
                ORDER BY session_count DESC
                LIMIT 5
                """

                time_rows = await conn.fetchall(time_query, params)
                popular_times = [
                    {'hour': f"{row['hour']}:00", 'count': row['session_count']}
                    for row in time_rows
                ]

                # Get session trends (by day of week)
                trends_query = f"""
                SELECT
                    strftime('%w', s.date_seance) as day_of_week,
                    COUNT(*) as session_count
                FROM seances s
                WHERE {date_conditions} AND s.is_active = 1
                GROUP BY strftime('%w', s.date_seance)
                ORDER BY day_of_week
                """

                trends_rows = await conn.fetchall(trends_query, params)
                day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                weekly_trends = [
                    {'day': day_names[int(row['day_of_week'])], 'count': row['session_count']}
                    for row in trends_rows
                ]

                analytics = {
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'days': (end_date - start_date).days
                    },
                    'totals': {
                        'total_sessions': row['total_sessions'] or 0,
                        'completed_sessions': row['completed_sessions'] or 0,
                        'cancelled_sessions': row['cancelled_sessions'] or 0,
                        'scheduled_sessions': row['scheduled_sessions'] or 0,
                        'unique_clients': row['unique_clients'] or 0
                    },
                    'metrics': {
                        'completion_rate': round(completion_rate, 2),
                        'cancellation_rate': round(cancellation_rate, 2),
                        'avg_session_duration_minutes': round(row['avg_session_duration_minutes'] or 0, 1)
                    },
                    'session_types': {
                        'individual_sessions': row['individual_sessions'] or 0,
                        'group_sessions': row['group_sessions'] or 0
                    },
                    'trends': {
                        'popular_times': popular_times,
                        'weekly_distribution': weekly_trends
                    },
                    'date_range': {
                        'first_session': row['first_session_date'],
                        'last_session': row['last_session_date']
                    }
                }

            # Cache analytics result
            await cache_set(cache_key, analytics, self._analytics_cache_ttl)

            self._update_metrics(start_time, True)
            return analytics

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to get session analytics: {str(e)}") from e

    async def clone_session(
        self,
        session_id: int,
        new_date: datetime
    ) -> Session:
        """Clone existing session for new date."""
        start_time = time.perf_counter()

        try:
            # Get original session
            original_session = await self.get_by_id(session_id)
            if not original_session:
                raise EntityNotFoundError(f"Session {session_id} not found")

            # Create cloned session
            cloned_session = Session(
                client_id=original_session.client_id,
                date_seance=new_date.date() if isinstance(new_date, datetime) else new_date,
                heure_debut=original_session.heure_debut,
                heure_fin=original_session.heure_fin,
                type_seance=original_session.type_seance,
                exercices=original_session.exercices.copy() if original_session.exercices else None,
                notes=f"Cloned from session {session_id}. {original_session.notes or ''}".strip(),
                status='scheduled'
            )

            # Save cloned session
            created_session = await self.create(cloned_session)

            self._update_metrics(start_time, True)
            return created_session

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, EntityNotFoundError):
                raise
            raise RepositoryError(f"Failed to clone session {session_id}: {str(e)}") from e

    async def bulk_schedule_sessions(
        self,
        template_session_id: int,
        dates: List[datetime],
        client_id: Optional[int] = None
    ) -> List[Session]:
        """Bulk schedule sessions from template."""
        start_time = time.perf_counter()
        created_sessions = []

        try:
            # Get template session
            template_session = await self.get_by_id(template_session_id)
            if not template_session:
                raise EntityNotFoundError(f"Template session {template_session_id} not found")

            # Use transaction for bulk operation
            async with self._db_manager.get_transaction() as transaction:
                for session_date in dates:
                    # Create session from template
                    new_session = Session(
                        client_id=client_id or template_session.client_id,
                        date_seance=session_date.date() if isinstance(session_date, datetime) else session_date,
                        heure_debut=template_session.heure_debut,
                        heure_fin=template_session.heure_fin,
                        type_seance=template_session.type_seance,
                        exercices=template_session.exercices.copy() if template_session.exercices else None,
                        notes=f"Scheduled from template {template_session_id}",
                        status='scheduled'
                    )

                    # Create without individual transaction (using existing transaction)
                    created_session = await self._create_session_in_transaction(new_session, transaction)
                    created_sessions.append(created_session)

            # Invalidate caches after bulk operation
            affected_client_id = client_id or template_session.client_id
            await self._invalidate_session_caches(affected_client_id)

            self._update_metrics(start_time, True)
            return created_sessions

        except Exception as e:
            self._update_metrics(start_time, False)
            if isinstance(e, EntityNotFoundError):
                raise
            raise RepositoryError(f"Failed to bulk schedule sessions: {str(e)}") from e

    # Helper Methods

    def _map_row_to_session(self, row) -> Session:
        """Map database row to Session entity."""
        # Deserialize exercises JSON
        exercices = None
        if row['exercices_json']:
            try:
                exercices = json.loads(row['exercices_json'])
            except json.JSONDecodeError:
                exercices = None

        session = Session(
            client_id=row['client_id'],
            date_seance=datetime.fromisoformat(row['date_seance']).date() if row['date_seance'] else None,
            heure_debut=row['heure_debut'],
            heure_fin=row['heure_fin'],
            type_seance=row['type_seance'],
            exercices=exercices,
            notes=row['notes'],
            status=row['statut'],
            id=row['id']
        )

        # Add client info if available from JOIN
        if 'client_prenom' in row and row['client_prenom']:
            session._client_name = f"{row['client_prenom']} {row['client_nom']}"

        return session

    def _serialize_session(self, session: Session) -> Dict[str, Any]:
        """Serialize session for cache storage."""
        return {
            'id': session.id,
            'client_id': session.client_id,
            'date_seance': session.date_seance.isoformat() if session.date_seance else None,
            'heure_debut': session.heure_debut,
            'heure_fin': session.heure_fin,
            'type_seance': session.type_seance,
            'exercices': session.exercices,
            'notes': session.notes,
            'status': session.status,
            '_client_name': getattr(session, '_client_name', None)
        }

    def _deserialize_session(self, data: Dict[str, Any]) -> Session:
        """Deserialize session from cache data."""
        session = Session(
            client_id=data['client_id'],
            date_seance=datetime.fromisoformat(data['date_seance']).date() if data['date_seance'] else None,
            heure_debut=data['heure_debut'],
            heure_fin=data['heure_fin'],
            type_seance=data['type_seance'],
            exercices=data['exercices'],
            notes=data['notes'],
            status=data['status'],
            id=data['id']
        )

        if data.get('_client_name'):
            session._client_name = data['_client_name']

        return session

    async def _validate_session_creation(self, entity: Session) -> None:
        """Validate business rules for session creation."""
        if not entity.client_id:
            raise ValidationError("Client ID is required")

        if not entity.date_seance:
            raise ValidationError("Session date is required")

        if entity.heure_debut and entity.heure_fin:
            if entity.heure_debut >= entity.heure_fin:
                raise ValidationError("Start time must be before end time")

        # Check for scheduling conflicts
        if entity.date_seance and entity.heure_debut and entity.heure_fin:
            conflicts = await self._check_scheduling_conflicts(
                entity.date_seance,
                entity.heure_debut,
                entity.heure_fin,
                entity.client_id
            )

            if conflicts:
                raise BusinessRuleViolationError(
                    f"Scheduling conflict: overlapping session exists for client {entity.client_id}"
                )

    async def _check_scheduling_conflicts(
        self,
        session_date: date,
        start_time: str,
        end_time: str,
        client_id: int
    ) -> bool:
        """Check for scheduling conflicts with existing sessions."""
        query = """
        SELECT COUNT(*) FROM seances
        WHERE client_id = ? AND date_seance = ?
        AND statut NOT IN ('cancelled', 'completed')
        AND is_active = 1
        AND (
            (heure_debut < ? AND heure_fin > ?) OR
            (heure_debut < ? AND heure_fin > ?) OR
            (heure_debut >= ? AND heure_fin <= ?)
        )
        """

        params = (
            client_id, session_date,
            end_time, start_time,  # Existing session starts before new ends and ends after new starts
            start_time, end_time,  # Existing session starts before new ends and ends after new starts
            start_time, end_time   # New session completely contains existing session
        )

        conflict_count = await self._db_manager.execute_scalar(query, params)
        return conflict_count > 0

    def _calculate_session_duration(self, session: Session) -> int:
        """Calculate session duration in minutes."""
        if not session.heure_debut or not session.heure_fin:
            return 0

        try:
            start = datetime.strptime(session.heure_debut, "%H:%M").time()
            end = datetime.strptime(session.heure_fin, "%H:%M").time()

            start_dt = datetime.combine(date.today(), start)
            end_dt = datetime.combine(date.today(), end)

            duration = end_dt - start_dt
            return int(duration.total_seconds() / 60)
        except ValueError:
            return 0

    async def _create_session_in_transaction(self, entity: Session, transaction) -> Session:
        """Create session within existing transaction."""
        query = """
        INSERT INTO seances (
            client_id, date_seance, heure_debut, heure_fin,
            type_seance, statut, exercices_json, notes,
            date_creation, date_modification, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """

        exercices_json = json.dumps(entity.exercices) if entity.exercices else None

        params = (
            entity.client_id,
            entity.date_seance,
            entity.heure_debut,
            entity.heure_fin,
            entity.type_seance,
            entity.status,
            exercices_json,
            entity.notes,
            datetime.now(),
            datetime.now(),
        )

        async with self._db_manager.get_connection() as conn:
            cursor = await conn.execute(query, params)
            entity.id = cursor.lastrowid

        return entity

    async def _invalidate_single_session_cache(self, session_id: int) -> None:
        """Invalidate cache for a specific session."""
        await cache_delete(f"{self._cache_prefix}{session_id}")

    async def _invalidate_session_caches(self, client_id: Optional[int] = None) -> None:
        """Invalidate all session-related caches."""
        # Invalidate list caches
        await self._cache_manager.clear_cache(f"{self._cache_prefix}all:*")

        # Invalidate analytics caches
        if client_id:
            await self._cache_manager.clear_cache(f"{self._cache_prefix}analytics:{client_id}:*")
        else:
            await self._cache_manager.clear_cache(f"{self._cache_prefix}analytics:*")

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
                (self._metrics.avg_query_time_ms * (self._metrics.total_queries - 1) + execution_time)
                / self._metrics.total_queries
            )

    # Interface Implementation

    async def exists(self, entity_id: int) -> bool:
        """Check if session exists by ID."""
        session = await self.get_by_id(entity_id)
        return session is not None

    async def count(
        self,
        specification: Optional[ISpecification[Session]] = None
    ) -> int:
        """Count sessions matching specification."""
        if specification:
            where_condition, where_params = specification.to_sql_where()
            query = f"SELECT COUNT(*) FROM seances WHERE ({where_condition}) AND is_active = 1"
            return await self._db_manager.execute_scalar(query, where_params) or 0
        else:
            return await self._db_manager.execute_scalar("SELECT COUNT(*) FROM seances WHERE is_active = 1") or 0

    async def delete(self, entity_id: int) -> bool:
        """Hard delete session."""
        start_time = time.perf_counter()

        try:
            # Get session first to invalidate proper caches
            session = await self.get_by_id(entity_id)

            query = "DELETE FROM seances WHERE id = ?"

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, (entity_id,))
                await conn.commit()

                success = cursor.rowcount > 0

            if success and session:
                await self._invalidate_single_session_cache(entity_id)
                await self._invalidate_session_caches(session.client_id)

            self._update_metrics(start_time, True)
            return success

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to delete session {entity_id}: {str(e)}") from e

    async def soft_delete(self, entity_id: int) -> bool:
        """Soft delete session by marking inactive."""
        start_time = time.perf_counter()

        try:
            # Get session first to invalidate proper caches
            session = await self.get_by_id(entity_id)

            query = """
            UPDATE seances SET
                is_active = 0,
                date_modification = ?
            WHERE id = ? AND is_active = 1
            """

            async with self._db_manager.get_connection() as conn:
                cursor = await conn.execute(query, (datetime.now(), entity_id))
                await conn.commit()

                success = cursor.rowcount > 0

            if success and session:
                await self._invalidate_single_session_cache(entity_id)
                await self._invalidate_session_caches(session.client_id)

            self._update_metrics(start_time, True)
            return success

        except Exception as e:
            self._update_metrics(start_time, False)
            raise RepositoryError(f"Failed to soft delete session {entity_id}: {str(e)}") from e

    async def batch_create(self, entities: List[Session]) -> List[Session]:
        """Create multiple sessions in batch."""
        created_sessions = []

        async with self._db_manager.get_transaction() as transaction:
            for entity in entities:
                created_session = await self.create(entity)
                created_sessions.append(created_session)

        # Invalidate caches after bulk operation
        unique_clients = set(session.client_id for session in created_sessions if session.client_id)
        for client_id in unique_clients:
            await self._invalidate_session_caches(client_id)

        return created_sessions

    async def batch_update(self, entities: List[Session]) -> List[Session]:
        """Update multiple sessions in batch."""
        updated_sessions = []

        async with self._db_manager.get_transaction() as transaction:
            for entity in entities:
                updated_session = await self.update(entity)
                updated_sessions.append(updated_session)

        # Invalidate caches after bulk operation
        unique_clients = set(session.client_id for session in updated_sessions if session.client_id)
        for client_id in unique_clients:
            await self._invalidate_session_caches(client_id)

        return updated_sessions

    async def batch_delete(self, entity_ids: List[int]) -> int:
        """Delete multiple sessions in batch."""
        deleted_count = 0

        async with self._db_manager.get_transaction() as transaction:
            for entity_id in entity_ids:
                if await self.delete(entity_id):
                    deleted_count += 1

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

    def _serialize_query_result(self, result: QueryResult[Session]) -> Dict[str, Any]:
        """Serialize query result for caching."""
        return {
            'data': [self._serialize_session(session) for session in result.data],
            'total_count': result.total_count,
            'page': result.page,
            'page_size': result.page_size,
            'has_next': result.has_next,
            'has_previous': result.has_previous,
            'execution_time_ms': result.execution_time_ms,
            'cache_hit': result.cache_hit
        }

    def _deserialize_query_result(self, data: Dict[str, Any]) -> QueryResult[Session]:
        """Deserialize query result from cache."""
        return QueryResult(
            data=[self._deserialize_session(session_data) for session_data in data['data']],
            total_count=data['total_count'],
            page=data['page'],
            page_size=data['page_size'],
            has_next=data['has_next'],
            has_previous=data['has_previous'],
            execution_time_ms=data['execution_time_ms'],
            cache_hit=True
        )