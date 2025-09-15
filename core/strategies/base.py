"""
Base Strategy Pattern Implementation

Enterprise-grade strategy pattern with performance monitoring,
validation, and comprehensive error handling.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar


class StrategyPriority(Enum):
    """Strategy execution priority levels"""

    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    FALLBACK = 5


class StrategyExecutionMode(Enum):
    """Strategy execution modes"""

    SYNC = "sync"
    ASYNC = "async"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"


@dataclass
class StrategyMetrics:
    """Performance and execution metrics for strategies"""

    execution_count: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    success_rate: float = 1.0
    error_count: int = 0
    last_execution: Optional[datetime] = None
    peak_memory_usage: float = 0.0
    cpu_usage_percent: float = 0.0
    cache_hit_rate: float = 0.0

    def update_execution(
        self, execution_time: float, success: bool = True, memory_usage: float = 0.0
    ):
        """Update metrics after strategy execution"""
        self.execution_count += 1
        self.total_execution_time += execution_time
        self.average_execution_time = self.total_execution_time / self.execution_count

        if not success:
            self.error_count += 1

        self.success_rate = 1.0 - (self.error_count / self.execution_count)
        self.last_execution = datetime.utcnow()

        if memory_usage > self.peak_memory_usage:
            self.peak_memory_usage = memory_usage

    def get_performance_score(self) -> float:
        """Calculate overall performance score (0-100)"""
        if self.execution_count == 0:
            return 0.0

        # Weighted scoring: success_rate (40%), speed (30%), reliability (30%)
        speed_score = max(
            0, 100 - (self.average_execution_time * 10)
        )  # Lower is better
        reliability_score = self.success_rate * 100
        consistency_score = min(100, self.cache_hit_rate * 100)

        return reliability_score * 0.4 + speed_score * 0.3 + consistency_score * 0.3


@dataclass
class StrategyConfig:
    """Configuration for strategy execution"""

    name: str
    version: str = "1.0.0"
    priority: StrategyPriority = StrategyPriority.NORMAL
    execution_mode: StrategyExecutionMode = StrategyExecutionMode.SYNC
    timeout_seconds: float = 30.0
    retry_attempts: int = 3
    fallback_strategies: List[str] = field(default_factory=list)
    feature_flags: Dict[str, bool] = field(default_factory=dict)
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300
    max_memory_mb: float = 500.0
    enable_monitoring: bool = True
    ab_test_enabled: bool = False
    ab_test_percentage: float = 10.0

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature flag is enabled"""
        return self.feature_flags.get(feature, False)


T = TypeVar("T")


@dataclass
class StrategyContext(Generic[T]):
    """Context passed to strategy execution"""

    data: T
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    config_overrides: Dict[str, Any] = field(default_factory=dict)
    execution_start: Optional[datetime] = None

    def __post_init__(self):
        if self.execution_start is None:
            self.execution_start = datetime.utcnow()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value with default"""
        return self.metadata.get(key, default)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value"""
        self.metadata[key] = value


@dataclass
class StrategyResult(Generic[T]):
    """Result returned by strategy execution"""

    data: T
    success: bool = True
    execution_time_ms: float = 0.0
    strategy_name: str = ""
    strategy_version: str = ""
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Optional[Dict[str, float]] = None
    cache_hit: bool = False
    fallback_used: bool = False

    @property
    def is_success(self) -> bool:
        """Check if execution was successful"""
        return self.success and self.error_message is None

    def add_warning(self, message: str) -> None:
        """Add a warning message"""
        self.warnings.append(message)

    def set_error(self, message: str) -> None:
        """Set error state with message"""
        self.success = False
        self.error_message = message


class StrategyError(Exception):
    """Base exception for strategy-related errors"""

    def __init__(
        self, message: str, strategy_name: str = "", cause: Optional[Exception] = None
    ):
        super().__init__(message)
        self.strategy_name = strategy_name
        self.cause = cause


class StrategyValidationError(StrategyError):
    """Exception raised when strategy validation fails"""

    pass


class StrategyExecutionError(StrategyError):
    """Exception raised during strategy execution"""

    pass


class StrategyTimeoutError(StrategyError):
    """Exception raised when strategy execution times out"""

    pass


class BaseStrategy(ABC, Generic[T]):
    """
    Base class for all strategies in the enterprise pattern.

    Provides comprehensive infrastructure for:
    - Performance monitoring
    - Error handling and validation
    - Caching mechanisms
    - Async/sync execution
    - Circuit breaker integration
    """

    def __init__(self, config: StrategyConfig):
        self.config = config
        self.metrics = StrategyMetrics()
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}

    @property
    def name(self) -> str:
        """Get strategy name"""
        return self.config.name

    @property
    def version(self) -> str:
        """Get strategy version"""
        return self.config.version

    @property
    def priority(self) -> StrategyPriority:
        """Get strategy priority"""
        return self.config.priority

    @abstractmethod
    async def execute_async(self, context: StrategyContext[T]) -> StrategyResult[T]:
        """Execute strategy asynchronously"""
        pass

    @abstractmethod
    def validate_context(self, context: StrategyContext[T]) -> List[str]:
        """
        Validate execution context

        Returns:
            List of validation error messages (empty if valid)
        """
        pass

    @abstractmethod
    def get_supported_context_types(self) -> List[type]:
        """Get list of supported context data types"""
        pass

    def execute(self, context: StrategyContext[T]) -> StrategyResult[T]:
        """Execute strategy synchronously"""
        return asyncio.run(self.execute_async(context))

    async def execute_with_monitoring(
        self, context: StrategyContext[T]
    ) -> StrategyResult[T]:
        """Execute strategy with comprehensive monitoring"""
        start_time = time.perf_counter()

        try:
            # Validation
            validation_errors = self.validate_context(context)
            if validation_errors:
                raise StrategyValidationError(
                    f"Context validation failed: {', '.join(validation_errors)}",
                    self.name,
                )

            # Check cache
            if self.config.cache_enabled:
                cache_key = self._get_cache_key(context)
                cached_result = self._get_from_cache(cache_key)
                if cached_result is not None:
                    cached_result.cache_hit = True
                    return cached_result

            # Execute with timeout
            if self.config.execution_mode == StrategyExecutionMode.ASYNC:
                result = await asyncio.wait_for(
                    self.execute_async(context), timeout=self.config.timeout_seconds
                )
            else:
                result = await self.execute_async(context)

            # Update result metadata
            execution_time = (time.perf_counter() - start_time) * 1000
            result.execution_time_ms = execution_time
            result.strategy_name = self.name
            result.strategy_version = self.version

            # Cache result if successful
            if result.is_success and self.config.cache_enabled:
                cache_key = self._get_cache_key(context)
                self._store_in_cache(cache_key, result)

            # Update metrics
            self.metrics.update_execution(execution_time, result.is_success)

            return result

        except asyncio.TimeoutError:
            execution_time = (time.perf_counter() - start_time) * 1000
            self.metrics.update_execution(execution_time, False)
            raise StrategyTimeoutError(
                f"Strategy {self.name} timed out after {self.config.timeout_seconds}s",
                self.name,
            )
        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            self.metrics.update_execution(execution_time, False)

            if isinstance(e, StrategyError):
                raise
            else:
                raise StrategyExecutionError(
                    f"Strategy {self.name} execution failed: {str(e)}", self.name, e
                )

    def get_performance_metrics(self) -> StrategyMetrics:
        """Get current performance metrics"""
        return self.metrics

    def get_health_status(self) -> Dict[str, Any]:
        """Get strategy health status"""
        return {
            "name": self.name,
            "version": self.version,
            "healthy": self.metrics.success_rate > 0.95,
            "performance_score": self.metrics.get_performance_score(),
            "execution_count": self.metrics.execution_count,
            "success_rate": self.metrics.success_rate,
            "average_execution_time": self.metrics.average_execution_time,
            "last_execution": self.metrics.last_execution.isoformat()
            if self.metrics.last_execution
            else None,
        }

    def reset_metrics(self) -> None:
        """Reset performance metrics"""
        self.metrics = StrategyMetrics()

    def _get_cache_key(self, context: StrategyContext[T]) -> str:
        """Generate cache key for context"""
        # Simple implementation - override for custom caching logic
        import hashlib

        cache_data = {
            "strategy": self.name,
            "version": self.version,
            "data": str(context.data),
            "metadata": context.metadata,
        }

        cache_string = str(sorted(cache_data.items()))
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[StrategyResult[T]]:
        """Get result from cache"""
        if cache_key not in self._cache:
            return None

        # Check TTL
        cache_time = self._cache_timestamps.get(cache_key)
        if cache_time:
            age_seconds = (datetime.utcnow() - cache_time).total_seconds()
            if age_seconds > self.config.cache_ttl_seconds:
                # Expired
                del self._cache[cache_key]
                del self._cache_timestamps[cache_key]
                return None

        return self._cache[cache_key]

    def _store_in_cache(self, cache_key: str, result: StrategyResult[T]) -> None:
        """Store result in cache"""
        self._cache[cache_key] = result
        self._cache_timestamps[cache_key] = datetime.utcnow()

        # Simple cache size management
        if len(self._cache) > 100:  # Max 100 entries
            oldest_key = min(
                self._cache_timestamps.keys(), key=lambda k: self._cache_timestamps[k]
            )
            del self._cache[oldest_key]
            del self._cache_timestamps[oldest_key]

    def clear_cache(self) -> None:
        """Clear strategy cache"""
        self._cache.clear()
        self._cache_timestamps.clear()

    @asynccontextmanager
    async def performance_context(self):
        """Context manager for performance monitoring"""
        start_time = time.perf_counter()
        start_memory = self._get_memory_usage()

        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = self._get_memory_usage()

            execution_time = (end_time - start_time) * 1000
            memory_delta = end_memory - start_memory

            self.metrics.update_execution(execution_time, True, memory_delta)

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            return 0.0

    def __str__(self) -> str:
        return f"{self.name} v{self.version} (Priority: {self.priority.name})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name} v{self.version}>"
