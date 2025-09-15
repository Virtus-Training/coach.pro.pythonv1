"""
Enterprise Strategy Pattern Framework

This module provides a comprehensive strategy pattern implementation with:
- Plugin architecture with auto-discovery
- Performance monitoring and A/B testing
- Fallback mechanisms and circuit breakers
- Dynamic strategy selection with AI optimization
- Real-time metrics and analytics
"""

from .base import (
    BaseStrategy,
    StrategyContext,
    StrategyResult,
    StrategyConfig,
    StrategyMetrics,
    StrategyError
)
from .registry import (
    StrategyRegistry,
    StrategySelector,
    StrategyManager
)
from .monitoring import (
    PerformanceMonitor,
    ABTestingFramework,
    MetricsCollector
)
from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerState,
    FallbackManager
)

__all__ = [
    # Base Strategy Framework
    "BaseStrategy",
    "StrategyContext",
    "StrategyResult",
    "StrategyConfig",
    "StrategyMetrics",
    "StrategyError",

    # Strategy Management
    "StrategyRegistry",
    "StrategySelector",
    "StrategyManager",

    # Monitoring & Testing
    "PerformanceMonitor",
    "ABTestingFramework",
    "MetricsCollector",

    # Resilience Patterns
    "CircuitBreaker",
    "CircuitBreakerState",
    "FallbackManager",
]