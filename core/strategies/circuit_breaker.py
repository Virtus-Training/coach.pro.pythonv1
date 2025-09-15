"""
Circuit Breaker and Fallback Management

Enterprise-grade resilience patterns with circuit breakers,
fallback mechanisms, and self-healing capabilities.
"""

import asyncio
import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

from .base import BaseStrategy, StrategyContext, StrategyError, StrategyResult

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitBreakerState(Enum):
    """Circuit breaker states"""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit is open, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service has recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""

    failure_threshold: int = 5  # Number of failures to open circuit
    recovery_timeout: int = 60  # Seconds before trying to recover
    success_threshold: int = 3  # Successful calls to close circuit in half-open state
    timeout_duration: float = 30.0  # Request timeout in seconds
    monitor_window_size: int = 100  # Size of sliding window for monitoring
    failure_rate_threshold: float = 0.5  # Failure rate to open circuit (0-1)


@dataclass
class FallbackConfig:
    """Configuration for fallback mechanisms"""

    max_fallback_attempts: int = 3
    fallback_timeout: float = 10.0
    prefer_cached_result: bool = True
    fallback_strategies: List[str] = field(default_factory=list)
    degraded_mode_enabled: bool = True
    circuit_breaker_enabled: bool = True


class CircuitBreakerError(StrategyError):
    """Exception raised when circuit breaker is open"""

    pass


class FallbackError(StrategyError):
    """Exception raised when all fallback strategies fail"""

    pass


class CircuitBreaker:
    """
    Circuit breaker implementation with sliding window monitoring.

    Features:
    - Configurable failure thresholds
    - Sliding window failure rate monitoring
    - Automatic recovery testing
    - Detailed state tracking and metrics
    """

    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state_change_time = datetime.utcnow()
        self.call_history: deque = deque(maxlen=config.monitor_window_size)
        self._lock = threading.RLock()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        with self._lock:
            # Check if we should allow the call
            if not self._should_allow_call():
                raise CircuitBreakerError(
                    f"Circuit breaker {self.name} is OPEN", self.name
                )

        start_time = time.time()
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self._execute_async(func, *args, **kwargs),
                timeout=self.config.timeout_duration,
            )

            # Record success
            execution_time = time.time() - start_time
            self._record_success(execution_time)

            return result

        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            self._record_failure(execution_time, "timeout")
            raise StrategyError(
                f"Function call timed out after {self.config.timeout_duration}s"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._record_failure(execution_time, str(e))
            raise

    async def _execute_async(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function, handling both sync and async"""
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            # Run in thread pool for sync functions
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, func, *args, **kwargs)

    def _should_allow_call(self) -> bool:
        """Determine if call should be allowed based on circuit state"""
        current_time = datetime.utcnow()

        if self.state == CircuitBreakerState.CLOSED:
            return True

        elif self.state == CircuitBreakerState.OPEN:
            # Check if recovery timeout has passed
            if (
                self.last_failure_time
                and current_time - self.last_failure_time
                >= timedelta(seconds=self.config.recovery_timeout)
            ):
                self._transition_to_half_open()
                return True
            return False

        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True

        return False

    def _record_success(self, execution_time: float):
        """Record successful execution"""
        with self._lock:
            self.call_history.append(
                {
                    "timestamp": datetime.utcnow(),
                    "success": True,
                    "execution_time": execution_time,
                }
            )

            if self.state == CircuitBreakerState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self._transition_to_closed()
            elif self.state == CircuitBreakerState.CLOSED:
                # Reset failure count on success
                self.failure_count = 0

    def _record_failure(self, execution_time: float, error_message: str):
        """Record failed execution"""
        with self._lock:
            self.call_history.append(
                {
                    "timestamp": datetime.utcnow(),
                    "success": False,
                    "execution_time": execution_time,
                    "error": error_message,
                }
            )

            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()

            if self.state == CircuitBreakerState.CLOSED:
                if self._should_open_circuit():
                    self._transition_to_open()
            elif self.state == CircuitBreakerState.HALF_OPEN:
                self._transition_to_open()

    def _should_open_circuit(self) -> bool:
        """Check if circuit should be opened based on failure criteria"""
        # Check simple failure count threshold
        if self.failure_count >= self.config.failure_threshold:
            return True

        # Check failure rate in sliding window
        if len(self.call_history) >= self.config.monitor_window_size:
            recent_failures = sum(
                1 for call in self.call_history if not call["success"]
            )
            failure_rate = recent_failures / len(self.call_history)
            return failure_rate >= self.config.failure_rate_threshold

        return False

    def _transition_to_open(self):
        """Transition circuit breaker to OPEN state"""
        self.state = CircuitBreakerState.OPEN
        self.state_change_time = datetime.utcnow()
        logger.warning(f"Circuit breaker {self.name} transitioned to OPEN")

    def _transition_to_half_open(self):
        """Transition circuit breaker to HALF_OPEN state"""
        self.state = CircuitBreakerState.HALF_OPEN
        self.state_change_time = datetime.utcnow()
        self.success_count = 0
        logger.info(f"Circuit breaker {self.name} transitioned to HALF_OPEN")

    def _transition_to_closed(self):
        """Transition circuit breaker to CLOSED state"""
        self.state = CircuitBreakerState.CLOSED
        self.state_change_time = datetime.utcnow()
        self.failure_count = 0
        self.success_count = 0
        logger.info(f"Circuit breaker {self.name} transitioned to CLOSED")

    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information"""
        recent_calls = list(self.call_history)[-20:]  # Last 20 calls
        success_count = sum(1 for call in recent_calls if call["success"])
        len(recent_calls) - success_count

        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time.isoformat()
            if self.last_failure_time
            else None,
            "state_change_time": self.state_change_time.isoformat(),
            "recent_success_rate": (success_count / len(recent_calls))
            if recent_calls
            else 1.0,
            "total_calls": len(self.call_history),
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "recovery_timeout": self.config.recovery_timeout,
                "success_threshold": self.config.success_threshold,
            },
        }

    def reset(self):
        """Reset circuit breaker to initial state"""
        with self._lock:
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = None
            self.state_change_time = datetime.utcnow()
            self.call_history.clear()
            logger.info(f"Circuit breaker {self.name} reset")


class FallbackStrategy(Generic[T]):
    """
    Individual fallback strategy with its own circuit breaker and metrics.
    """

    def __init__(self, strategy: BaseStrategy, priority: int = 1):
        self.strategy = strategy
        self.priority = priority
        self.circuit_breaker = CircuitBreaker(
            f"fallback_{strategy.name}",
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30),
        )
        self.usage_count = 0
        self.success_count = 0

    async def execute(self, context: StrategyContext[T]) -> StrategyResult[T]:
        """Execute fallback strategy with circuit breaker protection"""
        self.usage_count += 1

        try:
            result = await self.circuit_breaker.call(
                self.strategy.execute_with_monitoring, context
            )
            self.success_count += 1
            result.fallback_used = True
            return result

        except Exception as e:
            logger.error(f"Fallback strategy {self.strategy.name} failed: {e}")
            raise

    @property
    def success_rate(self) -> float:
        """Get success rate of this fallback strategy"""
        return self.success_count / self.usage_count if self.usage_count > 0 else 0.0

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of fallback strategy"""
        return {
            "strategy_name": self.strategy.name,
            "priority": self.priority,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate,
            "circuit_breaker": self.circuit_breaker.get_state_info(),
        }


class FallbackManager(Generic[T]):
    """
    Comprehensive fallback management with multiple strategies,
    automatic selection, and degraded mode operation.
    """

    def __init__(self, config: FallbackConfig):
        self.config = config
        self.fallback_strategies: List[FallbackStrategy[T]] = []
        self.cache: Dict[str, StrategyResult[T]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        self.degraded_mode_active = False
        self._lock = threading.RLock()

    def add_fallback_strategy(self, strategy: BaseStrategy, priority: int = 1):
        """Add a fallback strategy"""
        with self._lock:
            fallback = FallbackStrategy(strategy, priority)
            self.fallback_strategies.append(fallback)
            # Sort by priority (lower number = higher priority)
            self.fallback_strategies.sort(key=lambda x: x.priority)
            logger.info(
                f"Added fallback strategy: {strategy.name} (priority: {priority})"
            )

    def remove_fallback_strategy(self, strategy_name: str) -> bool:
        """Remove a fallback strategy by name"""
        with self._lock:
            for i, fallback in enumerate(self.fallback_strategies):
                if fallback.strategy.name == strategy_name:
                    del self.fallback_strategies[i]
                    logger.info(f"Removed fallback strategy: {strategy_name}")
                    return True
            return False

    async def execute_with_fallback(
        self,
        primary_strategy: BaseStrategy,
        context: StrategyContext[T],
        enable_cache: bool = True,
    ) -> StrategyResult[T]:
        """
        Execute strategy with comprehensive fallback support.

        Flow:
        1. Try primary strategy
        2. If fails, try fallback strategies in priority order
        3. If all fail, try cached result
        4. If no cache, enter degraded mode
        """

        # Try to get cached result first if enabled
        if enable_cache and self.config.prefer_cached_result:
            cached_result = self._get_cached_result(context)
            if cached_result:
                cached_result.cache_hit = True
                cached_result.fallback_used = True
                return cached_result

        # Try primary strategy
        try:
            result = await primary_strategy.execute_with_monitoring(context)

            # Cache successful result
            if result.is_success and enable_cache:
                self._cache_result(context, result)

            return result

        except Exception as primary_error:
            logger.warning(
                f"Primary strategy {primary_strategy.name} failed: {primary_error}"
            )

            # Try fallback strategies
            return await self._try_fallback_strategies(context, primary_error)

    async def _try_fallback_strategies(
        self, context: StrategyContext[T], primary_error: Exception
    ) -> StrategyResult[T]:
        """Try fallback strategies in priority order"""

        attempts = 0
        last_error = primary_error

        for fallback in self.fallback_strategies:
            if attempts >= self.config.max_fallback_attempts:
                break

            # Skip if circuit breaker is open
            if fallback.circuit_breaker.state == CircuitBreakerState.OPEN:
                logger.debug(
                    f"Skipping fallback {fallback.strategy.name} - circuit breaker open"
                )
                continue

            try:
                logger.info(f"Trying fallback strategy: {fallback.strategy.name}")
                result = await fallback.execute(context)

                # Cache successful fallback result
                self._cache_result(context, result)

                logger.info(f"Fallback strategy {fallback.strategy.name} succeeded")
                return result

            except Exception as fallback_error:
                logger.warning(
                    f"Fallback strategy {fallback.strategy.name} failed: {fallback_error}"
                )
                last_error = fallback_error
                attempts += 1

        # All fallback strategies failed, try cached result
        cached_result = self._get_cached_result(context)
        if cached_result:
            logger.info("Using cached result as last resort")
            cached_result.cache_hit = True
            cached_result.fallback_used = True
            cached_result.add_warning(
                "Using stale cached result - all strategies failed"
            )
            return cached_result

        # Enter degraded mode if enabled
        if self.config.degraded_mode_enabled:
            return await self._enter_degraded_mode(context, last_error)

        # Complete failure
        raise FallbackError(
            f"All fallback strategies failed. Last error: {last_error}",
            "fallback_manager",
            last_error,
        )

    async def _enter_degraded_mode(
        self, context: StrategyContext[T], last_error: Exception
    ) -> StrategyResult[T]:
        """Enter degraded mode with minimal functionality"""

        self.degraded_mode_active = True
        logger.warning("Entering degraded mode")

        # Create a minimal result
        degraded_result = StrategyResult(
            data=self._create_degraded_response(context),
            success=True,
            strategy_name="degraded_mode",
            fallback_used=True,
        )

        degraded_result.add_warning(
            "Operating in degraded mode - limited functionality"
        )
        degraded_result.metadata["degraded_mode"] = True
        degraded_result.metadata["original_error"] = str(last_error)

        return degraded_result

    def _create_degraded_response(self, context: StrategyContext[T]) -> Any:
        """Create a minimal response for degraded mode"""
        # This should be overridden by specific implementations
        return {
            "status": "degraded",
            "message": "Service temporarily unavailable - operating in degraded mode",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _get_cache_key(self, context: StrategyContext[T]) -> str:
        """Generate cache key for context"""
        import hashlib

        cache_data = {
            "data": str(context.data),
            "user_id": context.user_id,
            "metadata": str(sorted(context.metadata.items())),
        }

        cache_string = str(sorted(cache_data.items()))
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _cache_result(self, context: StrategyContext[T], result: StrategyResult[T]):
        """Cache strategy result"""
        cache_key = self._get_cache_key(context)

        with self._lock:
            self.cache[cache_key] = result
            self.cache_timestamps[cache_key] = datetime.utcnow()

            # Clean up old cache entries
            self._cleanup_cache()

    def _get_cached_result(
        self, context: StrategyContext[T]
    ) -> Optional[StrategyResult[T]]:
        """Get cached result if available and valid"""
        cache_key = self._get_cache_key(context)

        with self._lock:
            if cache_key not in self.cache:
                return None

            # Check if cache is still valid (30 minutes TTL)
            cache_time = self.cache_timestamps.get(cache_key)
            if cache_time:
                age = datetime.utcnow() - cache_time
                if age > timedelta(minutes=30):
                    # Cache expired
                    del self.cache[cache_key]
                    del self.cache_timestamps[cache_key]
                    return None

            return self.cache[cache_key]

    def _cleanup_cache(self):
        """Clean up old cache entries"""
        if len(self.cache) <= 100:  # Keep cache size manageable
            return

        # Remove oldest entries
        sorted_entries = sorted(self.cache_timestamps.items(), key=lambda x: x[1])

        # Remove oldest 20 entries
        for cache_key, _ in sorted_entries[:20]:
            if cache_key in self.cache:
                del self.cache[cache_key]
            if cache_key in self.cache_timestamps:
                del self.cache_timestamps[cache_key]

    def get_fallback_status(self) -> Dict[str, Any]:
        """Get status of all fallback strategies"""
        with self._lock:
            return {
                "degraded_mode_active": self.degraded_mode_active,
                "total_fallback_strategies": len(self.fallback_strategies),
                "cache_size": len(self.cache),
                "fallback_strategies": [
                    fallback.get_health_status()
                    for fallback in self.fallback_strategies
                ],
                "config": {
                    "max_fallback_attempts": self.config.max_fallback_attempts,
                    "fallback_timeout": self.config.fallback_timeout,
                    "degraded_mode_enabled": self.config.degraded_mode_enabled,
                },
            }

    def clear_cache(self):
        """Clear all cached results"""
        with self._lock:
            self.cache.clear()
            self.cache_timestamps.clear()
            logger.info("Fallback cache cleared")

    def exit_degraded_mode(self):
        """Exit degraded mode"""
        self.degraded_mode_active = False
        logger.info("Exited degraded mode")

    def reset_circuit_breakers(self):
        """Reset all circuit breakers"""
        for fallback in self.fallback_strategies:
            fallback.circuit_breaker.reset()
        logger.info("All circuit breakers reset")
