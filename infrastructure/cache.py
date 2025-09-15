"""
Async Cache Infrastructure.

Provides async caching implementations with memory and Redis support,
including cache warming, eviction policies, and performance monitoring.
"""

from __future__ import annotations

import asyncio
import json
import pickle
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class CacheConfig:
    """Cache configuration settings."""

    max_size: int = 1000
    default_ttl: int = 300  # 5 minutes
    cleanup_interval: int = 60  # 1 minute
    enable_metrics: bool = True
    serialization_method: str = "pickle"  # "pickle" or "json"


@dataclass
class CacheMetrics:
    """Cache performance metrics."""

    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    total_operations: int = 0
    avg_access_time_ms: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total_reads = self.hits + self.misses
        return (self.hits / total_reads) * 100 if total_reads > 0 else 0.0

    @property
    def miss_rate(self) -> float:
        """Calculate cache miss rate."""
        return 100.0 - self.hit_rate

    def reset(self) -> None:
        """Reset all metrics."""
        self.hits = 0
        self.misses = 0
        self.sets = 0
        self.deletes = 0
        self.evictions = 0
        self.total_operations = 0
        self.avg_access_time_ms = 0.0


@dataclass
class CacheEntry:
    """Cache entry with metadata."""

    value: Any
    created_at: float
    ttl: int
    access_count: int = 0
    last_accessed: float = 0.0

    def __post_init__(self):
        """Initialize timestamps."""
        if self.last_accessed == 0.0:
            self.last_accessed = self.created_at

    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl <= 0:
            return False
        return time.time() > (self.created_at + self.ttl)

    @property
    def age_seconds(self) -> float:
        """Get entry age in seconds."""
        return time.time() - self.created_at

    def touch(self) -> None:
        """Update access information."""
        self.access_count += 1
        self.last_accessed = time.time()


class ICache(ABC):
    """Abstract cache interface."""

    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache entries."""
        pass

    @abstractmethod
    async def get_metrics(self) -> CacheMetrics:
        """Get cache metrics."""
        pass


class AsyncMemoryCache(ICache):
    """
    Async in-memory cache with LRU eviction and TTL support.

    Features:
    - TTL (Time To Live) support
    - LRU (Least Recently Used) eviction
    - Automatic cleanup of expired entries
    - Performance metrics
    - Thread-safe operations
    """

    def __init__(self, config: CacheConfig):
        self.config = config
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: List[str] = []
        self._lock = asyncio.Lock()
        self._metrics = CacheMetrics()
        self._cleanup_task: Optional[asyncio.Task] = None

        # Start cleanup task
        if config.cleanup_interval > 0:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        start_time = time.perf_counter()

        async with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._metrics.misses += 1
                self._metrics.total_operations += 1
                return None

            if entry.is_expired:
                # Remove expired entry
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)

                self._metrics.misses += 1
                self._metrics.evictions += 1
                self._metrics.total_operations += 1
                return None

            # Update access information
            entry.touch()

            # Update LRU order
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            self._metrics.hits += 1
            self._metrics.total_operations += 1

            # Update average access time
            access_time = (time.perf_counter() - start_time) * 1000
            self._update_avg_access_time(access_time)

            return self._deserialize(entry.value)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if ttl is None:
            ttl = self.config.default_ttl

        async with self._lock:
            # Serialize value
            serialized_value = self._serialize(value)

            # Create cache entry
            entry = CacheEntry(
                value=serialized_value,
                created_at=time.time(),
                ttl=ttl,
            )

            # Check if we need to evict entries
            if len(self._cache) >= self.config.max_size and key not in self._cache:
                await self._evict_lru()

            # Store entry
            self._cache[key] = entry

            # Update LRU order
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            self._metrics.sets += 1
            self._metrics.total_operations += 1

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)

                self._metrics.deletes += 1
                self._metrics.total_operations += 1
                return True

            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        async with self._lock:
            entry = self._cache.get(key)
            return entry is not None and not entry.is_expired

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._metrics.reset()

    async def get_metrics(self) -> CacheMetrics:
        """Get cache metrics."""
        return self._metrics

    async def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information."""
        async with self._lock:
            total_entries = len(self._cache)
            expired_entries = sum(
                1 for entry in self._cache.values() if entry.is_expired
            )

            return {
                "total_entries": total_entries,
                "expired_entries": expired_entries,
                "valid_entries": total_entries - expired_entries,
                "max_size": self.config.max_size,
                "utilization_percent": (total_entries / self.config.max_size) * 100,
                "metrics": self._metrics,
            }

    async def warm_cache(
        self, warm_data: Dict[str, Any], ttl: Optional[int] = None
    ) -> None:
        """Warm cache with initial data."""
        for key, value in warm_data.items():
            await self.set(key, value, ttl)

    def _serialize(self, value: Any) -> bytes:
        """Serialize value for storage."""
        if self.config.serialization_method == "json":
            try:
                return json.dumps(value).encode("utf-8")
            except (TypeError, ValueError):
                # Fallback to pickle for non-JSON serializable objects
                return pickle.dumps(value)
        else:
            return pickle.dumps(value)

    def _deserialize(self, data: bytes) -> Any:
        """Deserialize value from storage."""
        if self.config.serialization_method == "json":
            try:
                return json.loads(data.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Fallback to pickle
                return pickle.loads(data)
        else:
            return pickle.loads(data)

    async def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self._access_order:
            return

        # Remove oldest entry
        oldest_key = self._access_order.pop(0)
        if oldest_key in self._cache:
            del self._cache[oldest_key]
            self._metrics.evictions += 1

    async def _cleanup_expired(self) -> int:
        """Clean up expired entries."""
        expired_keys = []

        for key, entry in self._cache.items():
            if entry.is_expired:
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)

        if expired_keys:
            self._metrics.evictions += len(expired_keys)

        return len(expired_keys)

    async def _cleanup_loop(self) -> None:
        """Background cleanup task."""
        while True:
            try:
                await asyncio.sleep(self.config.cleanup_interval)
                async with self._lock:
                    cleaned = await self._cleanup_expired()
                    if cleaned > 0:
                        print(f"Cache cleanup: removed {cleaned} expired entries")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Cache cleanup error: {e}")
                await asyncio.sleep(self.config.cleanup_interval)

    def _update_avg_access_time(self, access_time_ms: float) -> None:
        """Update average access time."""
        if self._metrics.total_operations == 1:
            self._metrics.avg_access_time_ms = access_time_ms
        else:
            # Running average
            self._metrics.avg_access_time_ms = (
                self._metrics.avg_access_time_ms * (self._metrics.total_operations - 1)
                + access_time_ms
            ) / self._metrics.total_operations

    async def close(self) -> None:
        """Close cache and cleanup resources."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        await self.clear()


class AsyncRedisCache(ICache):
    """
    Async Redis cache implementation.

    Note: This is a simplified implementation. In production,
    you would use a library like aioredis.
    """

    def __init__(self, config: CacheConfig, redis_url: str = "redis://localhost:6379"):
        self.config = config
        self.redis_url = redis_url
        self._metrics = CacheMetrics()
        self._redis = None  # Would be actual Redis connection

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        # Simplified implementation - would use actual Redis operations
        self._metrics.total_operations += 1
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in Redis cache."""
        # Simplified implementation
        self._metrics.sets += 1
        self._metrics.total_operations += 1

    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        # Simplified implementation
        self._metrics.deletes += 1
        self._metrics.total_operations += 1
        return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache."""
        self._metrics.total_operations += 1
        return False

    async def clear(self) -> None:
        """Clear all Redis cache entries."""
        self._metrics.reset()

    async def get_metrics(self) -> CacheMetrics:
        """Get Redis cache metrics."""
        return self._metrics


class CacheManager:
    """
    Cache manager that coordinates multiple cache implementations.

    Supports cache hierarchies (L1 memory cache + L2 Redis cache).
    """

    def __init__(
        self,
        primary_cache: ICache,
        secondary_cache: Optional[ICache] = None,
    ):
        self.primary_cache = primary_cache
        self.secondary_cache = secondary_cache

    async def get(self, key: str) -> Optional[Any]:
        """Get value with cache hierarchy."""
        # Try primary cache first
        value = await self.primary_cache.get(key)
        if value is not None:
            return value

        # Try secondary cache if available
        if self.secondary_cache:
            value = await self.secondary_cache.get(key)
            if value is not None:
                # Populate primary cache
                await self.primary_cache.set(key, value)
                return value

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in both cache layers."""
        # Set in primary cache
        await self.primary_cache.set(key, value, ttl)

        # Set in secondary cache if available
        if self.secondary_cache:
            await self.secondary_cache.set(key, value, ttl)

    async def delete(self, key: str) -> bool:
        """Delete value from both cache layers."""
        primary_deleted = await self.primary_cache.delete(key)
        secondary_deleted = True

        if self.secondary_cache:
            secondary_deleted = await self.secondary_cache.delete(key)

        return primary_deleted or secondary_deleted

    async def exists(self, key: str) -> bool:
        """Check if key exists in either cache layer."""
        exists_primary = await self.primary_cache.exists(key)
        if exists_primary:
            return True

        if self.secondary_cache:
            return await self.secondary_cache.exists(key)

        return False

    async def clear(self) -> None:
        """Clear both cache layers."""
        await self.primary_cache.clear()
        if self.secondary_cache:
            await self.secondary_cache.clear()

    async def get_combined_metrics(self) -> Dict[str, CacheMetrics]:
        """Get metrics from both cache layers."""
        metrics = {"primary": await self.primary_cache.get_metrics()}

        if self.secondary_cache:
            metrics["secondary"] = await self.secondary_cache.get_metrics()

        return metrics


# Cache decorators for easy use
def cache_result(cache_key_func, ttl: Optional[int] = None):
    """Decorator to cache function results."""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would implement caching logic
            # For now, just call the function
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Global cache instances
_memory_cache: Optional[AsyncMemoryCache] = None
_cache_manager: Optional[CacheManager] = None


def get_memory_cache(config: Optional[CacheConfig] = None) -> AsyncMemoryCache:
    """Get global memory cache instance."""
    global _memory_cache

    if _memory_cache is None:
        if config is None:
            config = CacheConfig()
        _memory_cache = AsyncMemoryCache(config)

    return _memory_cache


def get_cache_manager(
    primary_config: Optional[CacheConfig] = None,
    use_redis: bool = False,
) -> CacheManager:
    """Get global cache manager instance."""
    global _cache_manager

    if _cache_manager is None:
        primary_cache = get_memory_cache(primary_config)
        secondary_cache = None

        if use_redis:
            # In production, you would configure Redis here
            secondary_cache = AsyncRedisCache(primary_config or CacheConfig())

        _cache_manager = CacheManager(primary_cache, secondary_cache)

    return _cache_manager


# Convenience functions
async def cache_get(key: str) -> Optional[Any]:
    """Get from global cache."""
    manager = get_cache_manager()
    return await manager.get(key)


async def cache_set(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """Set in global cache."""
    manager = get_cache_manager()
    await manager.set(key, value, ttl)


async def cache_delete(key: str) -> bool:
    """Delete from global cache."""
    manager = get_cache_manager()
    return await manager.delete(key)
