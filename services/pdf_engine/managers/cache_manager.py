"""
Cache Manager - High-performance caching for PDF generation
Implements intelligent caching with size limits and TTL
"""

from __future__ import annotations

import hashlib
import pickle
import time
from pathlib import Path
from typing import Any, Dict, Optional


class CacheManager:
    """
    Intelligent caching system for PDF generation
    Features: TTL, size limits, LRU eviction, statistics
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        max_size_mb: int = 100,
        default_ttl: int = 3600,  # 1 hour
    ):
        self.cache_dir = Path(cache_dir) if cache_dir else self._get_default_cache_dir()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl

        # In-memory index for fast lookups
        self.index = self._load_index()
        self.stats = {"hits": 0, "misses": 0, "evictions": 0}

    def get(self, key: str) -> Optional[bytes]:
        """Get cached PDF data"""
        cache_file = self.cache_dir / f"{key}.cache"

        if not cache_file.exists():
            self.stats["misses"] += 1
            return None

        # Check TTL
        if self._is_expired(key):
            self._delete_entry(key)
            self.stats["misses"] += 1
            return None

        try:
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)

            # Update access time for LRU
            self.index[key]["accessed_at"] = time.time()
            self._save_index()

            self.stats["hits"] += 1
            return cached_data["content"]

        except Exception:
            # Corrupted cache file
            self._delete_entry(key)
            self.stats["misses"] += 1
            return None

    def set(self, key: str, content: bytes, ttl: Optional[int] = None) -> None:
        """Set cached PDF data"""
        if ttl is None:
            ttl = self.default_ttl

        cache_file = self.cache_dir / f"{key}.cache"

        # Check if we need to free space
        content_size = len(content)
        if self._get_total_size() + content_size > self.max_size_bytes:
            self._evict_lru(content_size)

        # Save cached data
        cached_data = {
            "content": content,
            "created_at": time.time(),
            "ttl": ttl,
            "size": content_size,
        }

        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f)

            # Update index
            self.index[key] = {
                "created_at": time.time(),
                "accessed_at": time.time(),
                "expires_at": time.time() + ttl,
                "size": content_size,
            }
            self._save_index()

        except Exception:
            # Cleanup on failure
            if cache_file.exists():
                cache_file.unlink()

    def delete(self, key: str) -> bool:
        """Delete cached entry"""
        return self._delete_entry(key)

    def clear(self) -> None:
        """Clear all cached entries"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

        self.index.clear()
        self._save_index()

        self.stats["evictions"] += len(self.index)

    def cleanup_expired(self) -> int:
        """Remove expired entries and return count"""
        expired_count = 0
        current_time = time.time()

        expired_keys = [
            key for key, meta in self.index.items()
            if current_time > meta["expires_at"]
        ]

        for key in expired_keys:
            if self._delete_entry(key):
                expired_count += 1

        return expired_count

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests) if total_requests > 0 else 0

        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": hit_rate,
            "evictions": self.stats["evictions"],
            "entries": len(self.index),
            "total_size_mb": self._get_total_size() / (1024 * 1024),
            "max_size_mb": self.max_size_bytes / (1024 * 1024),
        }

    def _get_default_cache_dir(self) -> Path:
        """Get default cache directory"""
        return Path.home() / ".coachpro" / "pdf_cache"

    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """Load cache index from disk"""
        index_file = self.cache_dir / "index.json"
        if index_file.exists():
            try:
                import json
                with open(index_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_index(self) -> None:
        """Save cache index to disk"""
        index_file = self.cache_dir / "index.json"
        try:
            import json
            with open(index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception:
            pass

    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired"""
        if key not in self.index:
            return True

        current_time = time.time()
        return current_time > self.index[key]["expires_at"]

    def _delete_entry(self, key: str) -> bool:
        """Delete cache entry and update index"""
        cache_file = self.cache_dir / f"{key}.cache"

        try:
            if cache_file.exists():
                cache_file.unlink()

            if key in self.index:
                del self.index[key]
                self._save_index()

            return True

        except Exception:
            return False

    def _get_total_size(self) -> int:
        """Get total cache size in bytes"""
        return sum(meta["size"] for meta in self.index.values())

    def _evict_lru(self, needed_space: int) -> None:
        """Evict least recently used entries to free space"""
        # Sort by access time (oldest first)
        sorted_entries = sorted(
            self.index.items(),
            key=lambda x: x[1]["accessed_at"]
        )

        freed_space = 0
        for key, meta in sorted_entries:
            if freed_space >= needed_space:
                break

            if self._delete_entry(key):
                freed_space += meta["size"]
                self.stats["evictions"] += 1