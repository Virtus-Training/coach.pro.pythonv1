"""
Async Database Infrastructure.

Provides async database operations with connection pooling,
transaction management, and performance monitoring.
"""

from __future__ import annotations

import asyncio
import sqlite3
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncContextManager, Dict, List, Optional, Tuple

import aiosqlite


@dataclass
class DatabaseConfig:
    """Database configuration settings."""

    database_path: str = "coach.db"
    pool_size: int = 5
    max_connections: int = 10
    connection_timeout: float = 30.0
    command_timeout: float = 30.0
    enable_wal_mode: bool = True
    enable_foreign_keys: bool = True
    enable_query_logging: bool = False
    query_log_threshold_ms: float = 100.0


@dataclass
class QueryMetrics:
    """Query performance metrics."""

    query: str
    parameters: Tuple[Any, ...] = ()
    execution_time_ms: float = 0.0
    rows_affected: int = 0
    timestamp: float = 0.0
    connection_id: Optional[str] = None

    def is_slow_query(self, threshold_ms: float = 100.0) -> bool:
        """Check if query is considered slow."""
        return self.execution_time_ms > threshold_ms


class AsyncConnection:
    """
    Async database connection wrapper with performance monitoring.
    """

    def __init__(self, connection: aiosqlite.Connection, connection_id: str):
        self._connection = connection
        self._connection_id = connection_id
        self._is_closed = False
        self._query_metrics: List[QueryMetrics] = []

    @property
    def connection_id(self) -> str:
        """Get connection ID."""
        return self._connection_id

    @property
    def is_closed(self) -> bool:
        """Check if connection is closed."""
        return self._is_closed

    async def execute(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> aiosqlite.Cursor:
        """Execute a query with performance monitoring."""
        if self._is_closed:
            raise RuntimeError("Connection is closed")

        start_time = time.perf_counter()

        try:
            cursor = await self._connection.execute(query, parameters)
            execution_time = (time.perf_counter() - start_time) * 1000

            # Record metrics
            metrics = QueryMetrics(
                query=query,
                parameters=parameters,
                execution_time_ms=execution_time,
                rows_affected=cursor.rowcount or 0,
                timestamp=time.time(),
                connection_id=self._connection_id,
            )
            self._query_metrics.append(metrics)

            # Log slow queries
            if metrics.is_slow_query():
                print(f"SLOW QUERY ({execution_time:.2f}ms): {query[:100]}...")

            return cursor

        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            print(f"QUERY ERROR ({execution_time:.2f}ms): {e}")
            raise

    async def executemany(
        self,
        query: str,
        parameters_list: List[Tuple[Any, ...]],
    ) -> aiosqlite.Cursor:
        """Execute query with multiple parameter sets."""
        if self._is_closed:
            raise RuntimeError("Connection is closed")

        start_time = time.perf_counter()

        try:
            cursor = await self._connection.executemany(query, parameters_list)
            execution_time = (time.perf_counter() - start_time) * 1000

            # Record metrics
            metrics = QueryMetrics(
                query=f"{query} (batch of {len(parameters_list)})",
                parameters=(),
                execution_time_ms=execution_time,
                rows_affected=cursor.rowcount or 0,
                timestamp=time.time(),
                connection_id=self._connection_id,
            )
            self._query_metrics.append(metrics)

            return cursor

        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            print(f"BATCH QUERY ERROR ({execution_time:.2f}ms): {e}")
            raise

    async def fetchall(
        self, query: str, parameters: Tuple[Any, ...] = ()
    ) -> List[sqlite3.Row]:
        """Execute query and fetch all results."""
        cursor = await self.execute(query, parameters)
        return await cursor.fetchall()

    async def fetchone(
        self, query: str, parameters: Tuple[Any, ...] = ()
    ) -> Optional[sqlite3.Row]:
        """Execute query and fetch one result."""
        cursor = await self.execute(query, parameters)
        return await cursor.fetchone()

    async def commit(self) -> None:
        """Commit current transaction."""
        if not self._is_closed:
            await self._connection.commit()

    async def rollback(self) -> None:
        """Rollback current transaction."""
        if not self._is_closed:
            await self._connection.rollback()

    async def close(self) -> None:
        """Close the connection."""
        if not self._is_closed:
            await self._connection.close()
            self._is_closed = True

    def get_query_metrics(self, limit: int = 100) -> List[QueryMetrics]:
        """Get recent query metrics."""
        return self._query_metrics[-limit:] if limit else self._query_metrics

    def get_slow_queries(self, threshold_ms: float = 100.0) -> List[QueryMetrics]:
        """Get slow queries above threshold."""
        return [m for m in self._query_metrics if m.is_slow_query(threshold_ms)]


class AsyncTransaction:
    """
    Async transaction context manager.
    """

    def __init__(self, connection: AsyncConnection):
        self._connection = connection
        self._committed = False
        self._rolled_back = False

    async def __aenter__(self) -> AsyncTransaction:
        """Start transaction."""
        await self._connection.execute("BEGIN")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """End transaction."""
        if exc_type is not None and not self._rolled_back:
            await self.rollback()
        elif not self._committed and not self._rolled_back:
            await self.commit()

    async def commit(self) -> None:
        """Commit transaction."""
        if not self._committed and not self._rolled_back:
            await self._connection.commit()
            self._committed = True

    async def rollback(self) -> None:
        """Rollback transaction."""
        if not self._rolled_back and not self._committed:
            await self._connection.rollback()
            self._rolled_back = True


class AsyncDatabaseManager:
    """
    Async database manager with connection pooling.

    Provides high-performance async database operations with:
    - Connection pooling
    - Transaction management
    - Query performance monitoring
    - Automatic connection health checks
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connections: asyncio.Queue[AsyncConnection] = asyncio.Queue(
            maxsize=config.max_connections
        )
        self._total_connections = 0
        self._connection_counter = 0
        self._lock = asyncio.Lock()
        self._is_initialized = False

    async def initialize(self) -> None:
        """Initialize the database manager."""
        if self._is_initialized:
            return

        async with self._lock:
            if self._is_initialized:
                return

            # Create initial connection pool
            for _ in range(self.config.pool_size):
                connection = await self._create_connection()
                await self._connections.put(connection)

            self._is_initialized = True

    async def _create_connection(self) -> AsyncConnection:
        """Create a new database connection."""
        self._connection_counter += 1
        connection_id = f"conn_{self._connection_counter}"

        # Open connection
        conn = await aiosqlite.connect(self.config.database_path)
        conn.row_factory = aiosqlite.Row

        # Configure connection
        if self.config.enable_wal_mode:
            await conn.execute("PRAGMA journal_mode=WAL")

        if self.config.enable_foreign_keys:
            await conn.execute("PRAGMA foreign_keys=ON")

        # Performance optimizations
        await conn.execute("PRAGMA synchronous=NORMAL")
        await conn.execute("PRAGMA cache_size=10000")
        await conn.execute("PRAGMA temp_store=MEMORY")

        self._total_connections += 1
        return AsyncConnection(conn, connection_id)

    @asynccontextmanager
    async def get_connection(self) -> AsyncContextManager[AsyncConnection]:
        """Get a connection from the pool."""
        if not self._is_initialized:
            await self.initialize()

        connection = None
        try:
            # Try to get connection from pool with timeout
            connection = await asyncio.wait_for(
                self._connections.get(),
                timeout=self.config.connection_timeout,
            )

            # Health check
            if connection.is_closed:
                connection = await self._create_connection()

            yield connection

        except asyncio.TimeoutError:
            # Pool is exhausted, create new connection if under limit
            if self._total_connections < self.config.max_connections:
                connection = await self._create_connection()
                yield connection
            else:
                raise RuntimeError("Database connection pool exhausted")

        finally:
            # Return connection to pool
            if connection and not connection.is_closed:
                try:
                    await self._connections.put_nowait(connection)
                except asyncio.QueueFull:
                    # Pool is full, close the connection
                    await connection.close()

    @asynccontextmanager
    async def get_transaction(self) -> AsyncContextManager[AsyncTransaction]:
        """Get a transactional connection."""
        async with self.get_connection() as connection:
            async with AsyncTransaction(connection) as transaction:
                yield transaction

    async def execute_query(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> List[sqlite3.Row]:
        """Execute a query and return all results."""
        async with self.get_connection() as connection:
            return await connection.fetchall(query, parameters)

    async def execute_scalar(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> Any:
        """Execute a query and return single value."""
        async with self.get_connection() as connection:
            row = await connection.fetchone(query, parameters)
            return row[0] if row else None

    async def execute_non_query(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> int:
        """Execute a non-query command and return rows affected."""
        async with self.get_connection() as connection:
            cursor = await connection.execute(query, parameters)
            await connection.commit()
            return cursor.rowcount or 0

    async def execute_batch(
        self,
        query: str,
        parameters_list: List[Tuple[Any, ...]],
    ) -> int:
        """Execute batch command."""
        async with self.get_connection() as connection:
            cursor = await connection.executemany(query, parameters_list)
            await connection.commit()
            return cursor.rowcount or 0

    async def health_check(self) -> Dict[str, Any]:
        """Perform database health check."""
        try:
            start_time = time.perf_counter()

            async with self.get_connection() as connection:
                # Test query
                await connection.fetchone("SELECT 1")
                response_time = (time.perf_counter() - start_time) * 1000

                # Get connection metrics
                metrics = connection.get_query_metrics(limit=10)
                slow_queries = connection.get_slow_queries()

                return {
                    "status": "healthy",
                    "response_time_ms": response_time,
                    "total_connections": self._total_connections,
                    "pool_size": self._connections.qsize(),
                    "recent_queries": len(metrics),
                    "slow_queries": len(slow_queries),
                }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "total_connections": self._total_connections,
                "pool_size": self._connections.qsize(),
            }

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get database performance metrics."""
        all_metrics = []

        # Collect metrics from pool
        temp_connections = []
        while not self._connections.empty():
            try:
                conn = self._connections.get_nowait()
                all_metrics.extend(conn.get_query_metrics())
                temp_connections.append(conn)
            except asyncio.QueueEmpty:
                break

        # Put connections back
        for conn in temp_connections:
            await self._connections.put(conn)

        if not all_metrics:
            return {"error": "No metrics available"}

        # Calculate statistics
        execution_times = [m.execution_time_ms for m in all_metrics]
        slow_queries = [m for m in all_metrics if m.is_slow_query()]

        return {
            "total_queries": len(all_metrics),
            "slow_queries": len(slow_queries),
            "avg_execution_time_ms": sum(execution_times) / len(execution_times),
            "max_execution_time_ms": max(execution_times),
            "min_execution_time_ms": min(execution_times),
            "total_connections": self._total_connections,
            "active_connections": self.config.max_connections
            - self._connections.qsize(),
        }

    async def close_all(self) -> None:
        """Close all connections and cleanup."""
        async with self._lock:
            connections_to_close = []

            # Collect all connections from pool
            while not self._connections.empty():
                try:
                    conn = self._connections.get_nowait()
                    connections_to_close.append(conn)
                except asyncio.QueueEmpty:
                    break

            # Close all connections
            for conn in connections_to_close:
                await conn.close()

            self._total_connections = 0
            self._is_initialized = False

    def __del__(self):
        """Cleanup when object is destroyed."""
        # Note: In real production code, you'd want to ensure proper cleanup
        # This is simplified for the demo
        pass


# Singleton instance for global use
_db_manager: Optional[AsyncDatabaseManager] = None


def get_database_manager(
    config: Optional[DatabaseConfig] = None,
) -> AsyncDatabaseManager:
    """Get the global database manager instance."""
    global _db_manager

    if _db_manager is None:
        if config is None:
            config = DatabaseConfig()
        _db_manager = AsyncDatabaseManager(config)

    return _db_manager


async def initialize_database_manager(
    config: Optional[DatabaseConfig] = None,
) -> AsyncDatabaseManager:
    """Initialize the global database manager."""
    manager = get_database_manager(config)
    await manager.initialize()
    return manager


# Convenience functions for common operations
async def execute_query(
    query: str, parameters: Tuple[Any, ...] = ()
) -> List[sqlite3.Row]:
    """Execute query using global manager."""
    manager = get_database_manager()
    return await manager.execute_query(query, parameters)


async def execute_scalar(query: str, parameters: Tuple[Any, ...] = ()) -> Any:
    """Execute scalar query using global manager."""
    manager = get_database_manager()
    return await manager.execute_scalar(query, parameters)


async def execute_non_query(query: str, parameters: Tuple[Any, ...] = ()) -> int:
    """Execute non-query using global manager."""
    manager = get_database_manager()
    return await manager.execute_non_query(query, parameters)
