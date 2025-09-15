"""
Strategy Registry and Management Framework

Enterprise-grade strategy management with auto-discovery,
intelligent selection, and dynamic loading capabilities.
"""

import asyncio
import importlib
import inspect
import logging
import pkgutil
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, TypeVar

from .base import (
    BaseStrategy,
    StrategyConfig,
    StrategyContext,
    StrategyError,
    StrategyResult,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class StrategyRegistration:
    """Registration information for a strategy"""

    strategy_class: Type[BaseStrategy]
    config: StrategyConfig
    category: str
    tags: Set[str] = field(default_factory=set)
    requirements: Dict[str, str] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    instance: Optional[BaseStrategy] = None
    enabled: bool = True

    @property
    def full_name(self) -> str:
        """Get full strategy name with category"""
        return f"{self.category}.{self.config.name}"


class StrategyRegistry:
    """
    Central registry for all strategies in the system.

    Features:
    - Auto-discovery from modules
    - Category-based organization
    - Version management
    - Dependency resolution
    - Hot-reloading support
    """

    def __init__(self):
        self._strategies: Dict[str, Dict[str, StrategyRegistration]] = defaultdict(dict)
        self._instances: Dict[str, BaseStrategy] = {}
        self._lock = threading.RLock()
        self._discovery_paths: List[str] = []
        self._auto_discovery_enabled = True

    def register_strategy(
        self,
        strategy_class: Type[BaseStrategy],
        config: StrategyConfig,
        category: str,
        tags: Optional[Set[str]] = None,
        requirements: Optional[Dict[str, str]] = None,
    ) -> None:
        """Register a strategy in the registry"""
        with self._lock:
            tags = tags or set()
            requirements = requirements or {}

            registration = StrategyRegistration(
                strategy_class=strategy_class,
                config=config,
                category=category,
                tags=tags,
                requirements=requirements,
            )

            self._strategies[category][config.name] = registration

            logger.info(
                f"Registered strategy: {registration.full_name} v{config.version}"
            )

    def unregister_strategy(self, category: str, name: str) -> bool:
        """Unregister a strategy"""
        with self._lock:
            if category in self._strategies and name in self._strategies[category]:
                # Clean up instance if exists
                full_name = f"{category}.{name}"
                if full_name in self._instances:
                    del self._instances[full_name]

                del self._strategies[category][name]
                logger.info(f"Unregistered strategy: {category}.{name}")
                return True
            return False

    def get_strategy(self, category: str, name: str) -> Optional[BaseStrategy]:
        """Get strategy instance, creating if necessary"""
        with self._lock:
            full_name = f"{category}.{name}"

            # Return cached instance if exists
            if full_name in self._instances:
                return self._instances[full_name]

            # Get registration
            registration = self._strategies.get(category, {}).get(name)
            if not registration or not registration.enabled:
                return None

            try:
                # Create instance
                instance = registration.strategy_class(registration.config)
                self._instances[full_name] = instance
                registration.instance = instance

                logger.debug(f"Created strategy instance: {full_name}")
                return instance

            except Exception as e:
                logger.error(f"Failed to create strategy {full_name}: {e}")
                return None

    def get_strategies_by_category(self, category: str) -> List[BaseStrategy]:
        """Get all strategies in a category"""
        strategies = []
        if category in self._strategies:
            for name in self._strategies[category]:
                strategy = self.get_strategy(category, name)
                if strategy:
                    strategies.append(strategy)
        return strategies

    def get_strategies_by_tag(self, tag: str) -> List[BaseStrategy]:
        """Get all strategies with a specific tag"""
        strategies = []
        with self._lock:
            for category in self._strategies:
                for name, registration in self._strategies[category].items():
                    if tag in registration.tags and registration.enabled:
                        strategy = self.get_strategy(category, name)
                        if strategy:
                            strategies.append(strategy)
        return strategies

    def list_categories(self) -> List[str]:
        """List all strategy categories"""
        return list(self._strategies.keys())

    def list_strategies(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all strategies with metadata"""
        strategies = []
        with self._lock:
            categories = [category] if category else self._strategies.keys()

            for cat in categories:
                if cat not in self._strategies:
                    continue

                for name, registration in self._strategies[cat].items():
                    strategy_info = {
                        "category": cat,
                        "name": name,
                        "full_name": registration.full_name,
                        "version": registration.config.version,
                        "priority": registration.config.priority.name,
                        "tags": list(registration.tags),
                        "enabled": registration.enabled,
                        "registered_at": registration.registered_at.isoformat(),
                        "has_instance": registration.instance is not None,
                    }

                    if registration.instance:
                        strategy_info["health"] = (
                            registration.instance.get_health_status()
                        )

                    strategies.append(strategy_info)

        return strategies

    def enable_strategy(self, category: str, name: str) -> bool:
        """Enable a strategy"""
        with self._lock:
            registration = self._strategies.get(category, {}).get(name)
            if registration:
                registration.enabled = True
                logger.info(f"Enabled strategy: {category}.{name}")
                return True
            return False

    def disable_strategy(self, category: str, name: str) -> bool:
        """Disable a strategy"""
        with self._lock:
            registration = self._strategies.get(category, {}).get(name)
            if registration:
                registration.enabled = False
                # Remove instance to prevent usage
                full_name = f"{category}.{name}"
                if full_name in self._instances:
                    del self._instances[full_name]
                    registration.instance = None
                logger.info(f"Disabled strategy: {category}.{name}")
                return True
            return False

    def add_discovery_path(self, path: str) -> None:
        """Add a path for strategy auto-discovery"""
        if path not in self._discovery_paths:
            self._discovery_paths.append(path)
            logger.debug(f"Added discovery path: {path}")

    async def discover_strategies(self, paths: Optional[List[str]] = None) -> int:
        """Discover and register strategies from specified paths"""
        if not self._auto_discovery_enabled:
            return 0

        discovery_paths = paths or self._discovery_paths
        discovered_count = 0

        for path in discovery_paths:
            try:
                count = await self._discover_from_path(path)
                discovered_count += count
            except Exception as e:
                logger.error(f"Failed to discover strategies from {path}: {e}")

        logger.info(f"Discovered {discovered_count} strategies")
        return discovered_count

    async def _discover_from_path(self, path: str) -> int:
        """Discover strategies from a specific path"""
        discovered_count = 0
        path_obj = Path(path)

        if not path_obj.exists():
            logger.warning(f"Discovery path does not exist: {path}")
            return 0

        # Walk through Python modules
        for module_info in pkgutil.walk_packages([str(path_obj)]):
            try:
                module = importlib.import_module(module_info.name)
                count = await self._discover_from_module(module)
                discovered_count += count
            except Exception as e:
                logger.debug(f"Failed to import module {module_info.name}: {e}")

        return discovered_count

    async def _discover_from_module(self, module) -> int:
        """Discover strategies from a module"""
        discovered_count = 0

        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseStrategy)
                and obj != BaseStrategy
            ):
                try:
                    # Look for strategy configuration
                    if hasattr(obj, "_strategy_config"):
                        config = obj._strategy_config
                        category = getattr(obj, "_strategy_category", "default")
                        tags = getattr(obj, "_strategy_tags", set())

                        self.register_strategy(obj, config, category, tags)
                        discovered_count += 1

                except Exception as e:
                    logger.error(f"Failed to register discovered strategy {name}: {e}")

        return discovered_count

    def clear_registry(self) -> None:
        """Clear all registered strategies"""
        with self._lock:
            self._instances.clear()
            self._strategies.clear()
            logger.info("Registry cleared")

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        with self._lock:
            total_strategies = sum(len(cats) for cats in self._strategies.values())
            total_instances = len(self._instances)
            enabled_count = 0
            disabled_count = 0

            for category in self._strategies.values():
                for registration in category.values():
                    if registration.enabled:
                        enabled_count += 1
                    else:
                        disabled_count += 1

            return {
                "total_strategies": total_strategies,
                "total_instances": total_instances,
                "enabled_strategies": enabled_count,
                "disabled_strategies": disabled_count,
                "categories": len(self._strategies),
                "discovery_paths": len(self._discovery_paths),
            }


class StrategySelector:
    """
    Intelligent strategy selection with ML-based optimization.

    Features:
    - Performance-based selection
    - A/B testing integration
    - Context-aware routing
    - Load balancing
    - Fallback mechanisms
    """

    def __init__(self, registry: StrategyRegistry):
        self.registry = registry
        self._selection_history: List[Dict[str, Any]] = []
        self._performance_weights = {
            "success_rate": 0.4,
            "execution_time": 0.3,
            "reliability": 0.2,
            "cpu_usage": 0.1,
        }

    def select_best_strategy(
        self,
        category: str,
        context: StrategyContext,
        excluded_strategies: Optional[Set[str]] = None,
    ) -> Optional[BaseStrategy]:
        """Select the best strategy for given context"""
        candidates = self._get_candidate_strategies(
            category, context, excluded_strategies
        )

        if not candidates:
            return None

        if len(candidates) == 1:
            return candidates[0]

        # Score and rank candidates
        scored_candidates = []
        for strategy in candidates:
            score = self._calculate_strategy_score(strategy, context)
            scored_candidates.append((strategy, score))

        # Sort by score (highest first)
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        selected_strategy = scored_candidates[0][0]

        # Record selection for learning
        self._record_selection(category, selected_strategy, context, scored_candidates)

        return selected_strategy

    def select_strategies_for_ab_test(
        self, category: str, context: StrategyContext, test_percentage: float = 10.0
    ) -> List[BaseStrategy]:
        """Select strategies for A/B testing"""
        candidates = self._get_candidate_strategies(category, context)

        if len(candidates) < 2:
            return candidates

        # For A/B testing, select top performers plus some random candidates
        top_performers = self._get_top_performers(candidates, max_count=2)

        # Add random candidates for exploration
        remaining = [s for s in candidates if s not in top_performers]
        if remaining:
            import random

            additional = random.sample(remaining, min(2, len(remaining)))
            return top_performers + additional

        return top_performers

    def _get_candidate_strategies(
        self,
        category: str,
        context: StrategyContext,
        excluded: Optional[Set[str]] = None,
    ) -> List[BaseStrategy]:
        """Get candidate strategies for selection"""
        excluded = excluded or set()
        candidates = []

        strategies = self.registry.get_strategies_by_category(category)
        for strategy in strategies:
            if strategy.name in excluded:
                continue

            # Check if strategy supports the context type
            if not self._is_strategy_compatible(strategy, context):
                continue

            # Check if strategy is healthy
            health = strategy.get_health_status()
            if not health.get("healthy", False):
                continue

            candidates.append(strategy)

        return candidates

    def _is_strategy_compatible(
        self, strategy: BaseStrategy, context: StrategyContext
    ) -> bool:
        """Check if strategy is compatible with context"""
        try:
            supported_types = strategy.get_supported_context_types()
            context_type = type(context.data)

            return any(
                issubclass(context_type, supported_type)
                for supported_type in supported_types
            )
        except Exception:
            return False

    def _calculate_strategy_score(
        self, strategy: BaseStrategy, context: StrategyContext
    ) -> float:
        """Calculate strategy score for selection"""
        strategy.get_performance_metrics()
        health = strategy.get_health_status()

        # Base performance score
        performance_score = health.get("performance_score", 0.0)

        # Adjust for current load and recent performance
        load_factor = self._calculate_load_factor(strategy)
        recent_performance = self._get_recent_performance(strategy)

        # Context-specific adjustments
        context_score = self._calculate_context_score(strategy, context)

        # Weighted final score
        final_score = (
            performance_score * 0.4
            + load_factor * 0.2
            + recent_performance * 0.2
            + context_score * 0.2
        )

        return final_score

    def _calculate_load_factor(self, strategy: BaseStrategy) -> float:
        """Calculate current load factor for strategy"""
        # Simple implementation - can be enhanced with actual load monitoring
        metrics = strategy.get_performance_metrics()

        # Prefer strategies with lower recent usage
        if metrics.execution_count == 0:
            return 100.0  # New strategy gets high score

        # Factor in execution frequency
        if metrics.last_execution:
            time_since_last = (
                datetime.utcnow() - metrics.last_execution
            ).total_seconds()
            return min(
                100.0, time_since_last / 60.0
            )  # Higher score if not used recently

        return 50.0

    def _get_recent_performance(self, strategy: BaseStrategy) -> float:
        """Get recent performance score"""
        metrics = strategy.get_performance_metrics()

        # Simple implementation - use overall success rate
        return metrics.success_rate * 100

    def _calculate_context_score(
        self, strategy: BaseStrategy, context: StrategyContext
    ) -> float:
        """Calculate context-specific score"""
        # Basic implementation - can be enhanced with ML-based scoring
        base_score = 50.0

        # Adjust based on context metadata
        if hasattr(strategy, "preferred_contexts"):
            for pref_context in strategy.preferred_contexts:
                if isinstance(context.data, pref_context):
                    base_score += 25.0
                    break

        return min(100.0, base_score)

    def _get_top_performers(
        self, strategies: List[BaseStrategy], max_count: int = 3
    ) -> List[BaseStrategy]:
        """Get top performing strategies"""
        scored = [
            (s, s.get_performance_metrics().get_performance_score()) for s in strategies
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:max_count]]

    def _record_selection(
        self,
        category: str,
        selected_strategy: BaseStrategy,
        context: StrategyContext,
        scored_candidates: List[tuple],
    ):
        """Record strategy selection for learning"""
        selection_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category,
            "selected_strategy": selected_strategy.name,
            "context_type": type(context.data).__name__,
            "candidate_scores": [
                {"strategy": s.name, "score": score} for s, score in scored_candidates
            ],
        }

        self._selection_history.append(selection_record)

        # Keep only recent history (last 1000 selections)
        if len(self._selection_history) > 1000:
            self._selection_history = self._selection_history[-1000:]

    def get_selection_analytics(self) -> Dict[str, Any]:
        """Get analytics on strategy selection patterns"""
        if not self._selection_history:
            return {}

        strategy_usage = defaultdict(int)
        category_usage = defaultdict(int)

        for record in self._selection_history:
            strategy_usage[record["selected_strategy"]] += 1
            category_usage[record["category"]] += 1

        return {
            "total_selections": len(self._selection_history),
            "strategy_usage": dict(strategy_usage),
            "category_usage": dict(category_usage),
            "most_used_strategy": max(strategy_usage.items(), key=lambda x: x[1])[0]
            if strategy_usage
            else None,
            "selection_history_size": len(self._selection_history),
        }


class StrategyManager:
    """
    High-level strategy management with orchestration capabilities.

    Features:
    - Strategy lifecycle management
    - Parallel execution
    - Pipeline orchestration
    - Error handling and recovery
    - Performance optimization
    """

    def __init__(self, registry: StrategyRegistry, selector: StrategySelector):
        self.registry = registry
        self.selector = selector
        self._execution_pool = None
        self._max_concurrent_executions = 10

    async def execute_strategy(
        self,
        category: str,
        context: StrategyContext,
        strategy_name: Optional[str] = None,
        fallback_enabled: bool = True,
    ) -> StrategyResult:
        """Execute a single strategy with fallback support"""

        # Get specific strategy or select best one
        if strategy_name:
            strategy = self.registry.get_strategy(category, strategy_name)
            if not strategy:
                raise StrategyError(f"Strategy not found: {category}.{strategy_name}")
        else:
            strategy = self.selector.select_best_strategy(category, context)
            if not strategy:
                raise StrategyError(
                    f"No suitable strategy found for category: {category}"
                )

        try:
            return await strategy.execute_with_monitoring(context)
        except Exception:
            if fallback_enabled:
                return await self._try_fallback_strategies(
                    category, context, {strategy.name}
                )
            raise

    async def execute_parallel_strategies(
        self, category: str, context: StrategyContext, max_strategies: int = 3
    ) -> List[StrategyResult]:
        """Execute multiple strategies in parallel for comparison"""

        strategies = self.selector.select_strategies_for_ab_test(category, context)
        strategies = strategies[:max_strategies]

        if not strategies:
            return []

        # Execute in parallel
        tasks = [strategy.execute_with_monitoring(context) for strategy in strategies]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = StrategyResult(
                    data=None,
                    success=False,
                    strategy_name=strategies[i].name,
                    error_message=str(result),
                )
                final_results.append(error_result)
            else:
                final_results.append(result)

        return final_results

    async def execute_pipeline(
        self, pipeline_config: List[Dict[str, Any]], initial_context: StrategyContext
    ) -> StrategyResult:
        """Execute a pipeline of strategies"""

        current_context = initial_context
        pipeline_results = []

        for step in pipeline_config:
            category = step["category"]
            strategy_name = step.get("strategy_name")
            transform_func = step.get("transform_function")

            try:
                result = await self.execute_strategy(
                    category, current_context, strategy_name
                )

                pipeline_results.append(result)

                if not result.is_success:
                    # Pipeline failed
                    return StrategyResult(
                        data=pipeline_results,
                        success=False,
                        error_message=f"Pipeline failed at step {category}: {result.error_message}",
                    )

                # Transform context for next step if function provided
                if transform_func and callable(transform_func):
                    current_context = transform_func(current_context, result)

            except Exception as e:
                return StrategyResult(
                    data=pipeline_results,
                    success=False,
                    error_message=f"Pipeline failed at step {category}: {str(e)}",
                )

        return StrategyResult(
            data=pipeline_results,
            success=True,
            metadata={"pipeline_steps": len(pipeline_config)},
        )

    async def _try_fallback_strategies(
        self, category: str, context: StrategyContext, excluded_strategies: Set[str]
    ) -> StrategyResult:
        """Try fallback strategies when primary strategy fails"""

        fallback_strategy = self.selector.select_best_strategy(
            category, context, excluded_strategies
        )

        if not fallback_strategy:
            raise StrategyError(
                f"No fallback strategy available for category: {category}"
            )

        try:
            result = await fallback_strategy.execute_with_monitoring(context)
            result.fallback_used = True
            return result
        except Exception:
            # Try one more fallback
            excluded_strategies.add(fallback_strategy.name)
            next_fallback = self.selector.select_best_strategy(
                category, context, excluded_strategies
            )

            if next_fallback:
                result = await next_fallback.execute_with_monitoring(context)
                result.fallback_used = True
                return result

            raise StrategyError(
                f"All fallback strategies failed for category: {category}"
            )

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        registry_stats = self.registry.get_registry_stats()
        selection_analytics = self.selector.get_selection_analytics()

        all_strategies = []
        for category in self.registry.list_categories():
            strategies = self.registry.get_strategies_by_category(category)
            all_strategies.extend(strategies)

        healthy_strategies = sum(
            1 for s in all_strategies if s.get_health_status().get("healthy", False)
        )

        return {
            "registry_stats": registry_stats,
            "selection_analytics": selection_analytics,
            "healthy_strategies": healthy_strategies,
            "total_strategies": len(all_strategies),
            "health_percentage": (healthy_strategies / len(all_strategies) * 100)
            if all_strategies
            else 0,
        }
