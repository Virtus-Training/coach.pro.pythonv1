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
    StrategyConfig,
    StrategyContext,
    StrategyError,
    StrategyMetrics,
    StrategyResult,
)
from .circuit_breaker import CircuitBreaker, CircuitBreakerState, FallbackManager
from .monitoring import ABTestingFramework, MetricsCollector, PerformanceMonitor
from .registry import StrategyManager, StrategyRegistry, StrategySelector

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
