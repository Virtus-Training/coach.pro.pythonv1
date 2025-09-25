"""
Fallback Database Implementation using synchronous SQLite.

This is a temporary implementation to get the application running
without aiosqlite dependency.
"""

from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ContextManager, Dict, List, Optional, Tuple


@dataclass
class DatabaseConfig:
    """Database configuration settings."""

    database_path: str = "coach.db"
    connection_timeout: float = 30.0
    enable_wal_mode: bool = True
    enable_foreign_keys: bool = True


@dataclass
class QueryMetrics:
    """Query performance metrics."""

    query: str
    parameters: Tuple[Any, ...]
    execution_time_ms: float
    rows_affected: int
    timestamp: float

    def is_slow_query(self, threshold_ms: float = 100.0) -> bool:
        """Check if query is considered slow."""
        return self.execution_time_ms > threshold_ms


class SyncConnection:
    """Synchronous database connection wrapper."""

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._query_metrics: List[QueryMetrics] = []

    def execute(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> sqlite3.Cursor:
        """Execute a query with parameters."""
        start_time = time.perf_counter()

        try:
            cursor = self._connection.execute(query, parameters)
            execution_time = (time.perf_counter() - start_time) * 1000

            # Record metrics
            metrics = QueryMetrics(
                query=query,
                parameters=parameters,
                execution_time_ms=execution_time,
                rows_affected=cursor.rowcount or 0,
                timestamp=time.time(),
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

    def executemany(
        self,
        query: str,
        parameters_list: List[Tuple[Any, ...]],
    ) -> sqlite3.Cursor:
        """Execute query with multiple parameter sets."""
        start_time = time.perf_counter()

        try:
            cursor = self._connection.executemany(query, parameters_list)
            execution_time = (time.perf_counter() - start_time) * 1000

            # Record metrics
            metrics = QueryMetrics(
                query=f"{query} (batch of {len(parameters_list)})",
                parameters=(),
                execution_time_ms=execution_time,
                rows_affected=cursor.rowcount or 0,
                timestamp=time.time(),
            )
            self._query_metrics.append(metrics)

            return cursor

        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            print(f"BATCH QUERY ERROR ({execution_time:.2f}ms): {e}")
            raise

    def commit(self) -> None:
        """Commit current transaction."""
        self._connection.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        self._connection.rollback()

    def close(self) -> None:
        """Close the connection."""
        self._connection.close()

    def get_query_metrics(self) -> List[QueryMetrics]:
        """Get query performance metrics."""
        return self._query_metrics.copy()


class SyncDatabaseManager:
    """Synchronous database manager."""

    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._connection: Optional[sqlite3.Connection] = None

    def get_connection(self) -> SyncConnection:
        """Get database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(
                self._config.database_path,
                timeout=self._config.connection_timeout,
            )

            # Configure connection
            if self._config.enable_foreign_keys:
                self._connection.execute("PRAGMA foreign_keys = ON")

            if self._config.enable_wal_mode:
                self._connection.execute("PRAGMA journal_mode = WAL")

        return SyncConnection(self._connection)

    @contextmanager
    def transaction(self) -> ContextManager[SyncConnection]:
        """Context manager for database transactions."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def close(self) -> None:
        """Close database manager."""
        if self._connection:
            self._connection.close()
            self._connection = None


# For compatibility with async interface
class AsyncConnection:
    """Async-compatible wrapper around sync connection."""

    def __init__(self, sync_conn: SyncConnection):
        self._sync_conn = sync_conn

    async def execute(self, query: str, parameters: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """Execute query asynchronously (actually sync)."""
        return self._sync_conn.execute(query, parameters)

    async def executemany(self, query: str, parameters_list: List[Tuple[Any, ...]]) -> sqlite3.Cursor:
        """Execute many queries asynchronously (actually sync)."""
        return self._sync_conn.executemany(query, parameters_list)

    async def commit(self) -> None:
        """Commit transaction."""
        self._sync_conn.commit()

    async def rollback(self) -> None:
        """Rollback transaction."""
        self._sync_conn.rollback()

    async def close(self) -> None:
        """Close connection."""
        self._sync_conn.close()


class AsyncDatabaseManager:
    """Async-compatible wrapper around sync database manager."""

    def __init__(self, config: DatabaseConfig):
        self._sync_manager = SyncDatabaseManager(config)

    async def get_connection(self) -> AsyncConnection:
        """Get async-compatible connection."""
        sync_conn = self._sync_manager.get_connection()
        return AsyncConnection(sync_conn)

    async def transaction(self) -> AsyncConnection:
        """Get connection for transaction."""
        return await self.get_connection()

    async def get_transaction(self) -> AsyncTransaction:
        """Get transaction context manager."""
        connection = await self.get_connection()
        return AsyncTransaction(connection)

    async def close(self) -> None:
        """Close database manager."""
        self._sync_manager.close()


class AsyncTransaction:
    """Async-compatible transaction wrapper."""

    def __init__(self, connection: AsyncConnection):
        self._connection = connection
        self._committed = False
        self._rolled_back = False

    async def __aenter__(self) -> AsyncConnection:
        """Enter transaction context."""
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit transaction context."""
        if exc_type is not None and not self._rolled_back:
            await self._connection.rollback()
        elif not self._committed and not self._rolled_back:
            await self._connection.commit()

    async def commit(self) -> None:
        """Commit transaction."""
        if not self._committed and not self._rolled_back:
            await self._connection.commit()
            self._committed = True

    async def rollback(self) -> None:
        """Rollback transaction."""
        if not self._committed and not self._rolled_back:
            await self._connection.rollback()
            self._rolled_back = True


# Global database manager instance
_global_db_manager: Optional[AsyncDatabaseManager] = None


def get_database_manager() -> AsyncDatabaseManager:
    """Get global database manager instance."""
    global _global_db_manager
    if _global_db_manager is None:
        config = DatabaseConfig()
        _global_db_manager = AsyncDatabaseManager(config)
    return _global_db_manager


def initialize_database(db_path: str = "coach.db") -> None:
    """Initialize global database manager."""
    global _global_db_manager
    config = DatabaseConfig(database_path=db_path)
    _global_db_manager = AsyncDatabaseManager(config)