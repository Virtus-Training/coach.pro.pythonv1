"""
Performance Monitoring and A/B Testing Framework

Enterprise-grade monitoring with real-time metrics collection,
A/B testing capabilities, and intelligent performance optimization.
"""

import asyncio
import json
import logging
import statistics
import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .base import BaseStrategy, StrategyMetrics, StrategyResult

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics to collect"""

    COUNTER = "counter"
    HISTOGRAM = "histogram"
    GAUGE = "gauge"
    TIMER = "timer"


class ABTestStatus(Enum):
    """A/B test status"""

    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class MetricDataPoint:
    """Single metric data point"""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ABTestConfig:
    """Configuration for A/B testing"""

    test_id: str
    name: str
    description: str
    strategies: List[str]
    traffic_split: Dict[str, float]  # strategy_name -> percentage
    success_metrics: List[str]
    minimum_sample_size: int = 100
    confidence_level: float = 0.95
    max_duration_days: int = 30
    auto_promote_winner: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ABTestResult:
    """Result of an A/B test"""

    test_id: str
    strategy_name: str
    sample_size: int
    success_rate: float
    average_execution_time: float
    confidence_interval: tuple
    is_statistically_significant: bool
    p_value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class PerformanceMetric:
    """Performance metric with statistical analysis"""

    def __init__(
        self, name: str, metric_type: MetricType, max_data_points: int = 10000
    ):
        self.name = name
        self.metric_type = metric_type
        self.data_points: deque = deque(maxlen=max_data_points)
        self._lock = threading.RLock()

    def add_data_point(
        self,
        value: float,
        labels: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Add a new data point"""
        with self._lock:
            self.data_points.append(
                MetricDataPoint(
                    timestamp=datetime.utcnow(),
                    value=value,
                    labels=labels or {},
                    metadata=metadata or {},
                )
            )

    def get_statistics(
        self, time_window_minutes: Optional[int] = None
    ) -> Dict[str, float]:
        """Get statistical summary of the metric"""
        with self._lock:
            if not self.data_points:
                return {}

            # Filter by time window if specified
            if time_window_minutes:
                cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
                values = [
                    dp.value for dp in self.data_points if dp.timestamp >= cutoff_time
                ]
            else:
                values = [dp.value for dp in self.data_points]

            if not values:
                return {}

            return {
                "count": len(values),
                "sum": sum(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
                "min": min(values),
                "max": max(values),
                "percentile_95": self._percentile(values, 0.95),
                "percentile_99": self._percentile(values, 0.99),
            }

    def get_trend(self, time_window_minutes: int = 60) -> str:
        """Get trend direction over time window"""
        with self._lock:
            cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
            recent_points = [
                dp for dp in self.data_points if dp.timestamp >= cutoff_time
            ]

            if len(recent_points) < 2:
                return "insufficient_data"

            # Simple trend calculation
            first_half = recent_points[: len(recent_points) // 2]
            second_half = recent_points[len(recent_points) // 2 :]

            first_avg = statistics.mean([dp.value for dp in first_half])
            second_avg = statistics.mean([dp.value for dp in second_half])

            if second_avg > first_avg * 1.05:
                return "increasing"
            elif second_avg < first_avg * 0.95:
                return "decreasing"
            else:
                return "stable"

    @staticmethod
    def _percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = percentile * (len(sorted_values) - 1)

        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))


class MetricsCollector:
    """
    Centralized metrics collection system with real-time analytics.

    Features:
    - Multiple metric types (counter, histogram, gauge, timer)
    - Time-window based statistics
    - Trend analysis
    - Anomaly detection
    - Export capabilities
    """

    def __init__(self):
        self.metrics: Dict[str, PerformanceMetric] = {}
        self._lock = threading.RLock()
        self._collectors: Dict[str, Callable] = {}
        self._collection_intervals: Dict[str, int] = {}
        self._collection_tasks: Dict[str, asyncio.Task] = {}

    def create_metric(
        self, name: str, metric_type: MetricType, max_data_points: int = 10000
    ) -> PerformanceMetric:
        """Create a new metric"""
        with self._lock:
            if name in self.metrics:
                return self.metrics[name]

            metric = PerformanceMetric(name, metric_type, max_data_points)
            self.metrics[name] = metric
            logger.debug(f"Created metric: {name} ({metric_type.value})")
            return metric

    def record_counter(
        self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None
    ):
        """Record a counter metric"""
        metric = self.create_metric(name, MetricType.COUNTER)
        metric.add_data_point(value, labels)

    def record_histogram(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ):
        """Record a histogram metric"""
        metric = self.create_metric(name, MetricType.HISTOGRAM)
        metric.add_data_point(value, labels)

    def record_gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ):
        """Record a gauge metric"""
        metric = self.create_metric(name, MetricType.GAUGE)
        metric.add_data_point(value, labels)

    def record_timer(
        self, name: str, duration_ms: float, labels: Optional[Dict[str, str]] = None
    ):
        """Record a timer metric"""
        metric = self.create_metric(name, MetricType.TIMER)
        metric.add_data_point(duration_ms, labels)

    def get_metric(self, name: str) -> Optional[PerformanceMetric]:
        """Get a metric by name"""
        return self.metrics.get(name)

    def get_all_metrics_summary(
        self, time_window_minutes: Optional[int] = None
    ) -> Dict[str, Dict[str, float]]:
        """Get summary of all metrics"""
        summary = {}
        with self._lock:
            for name, metric in self.metrics.items():
                summary[name] = metric.get_statistics(time_window_minutes)
        return summary

    def register_custom_collector(
        self, name: str, collector_func: Callable, interval_seconds: int = 60
    ):
        """Register a custom metric collector"""
        self._collectors[name] = collector_func
        self._collection_intervals[name] = interval_seconds
        logger.info(
            f"Registered custom collector: {name} (interval: {interval_seconds}s)"
        )

    async def start_collection(self):
        """Start automatic metric collection"""
        for name, collector in self._collectors.items():
            interval = self._collection_intervals[name]
            task = asyncio.create_task(self._collection_loop(name, collector, interval))
            self._collection_tasks[name] = task

    async def stop_collection(self):
        """Stop automatic metric collection"""
        for name, task in self._collection_tasks.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._collection_tasks.clear()

    async def _collection_loop(self, name: str, collector: Callable, interval: int):
        """Collection loop for custom collectors"""
        while True:
            try:
                await asyncio.sleep(interval)

                # Execute collector
                if asyncio.iscoroutinefunction(collector):
                    await collector()
                else:
                    collector()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in collector {name}: {e}")

    def export_metrics(self, format_type: str = "json") -> str:
        """Export metrics in specified format"""
        if format_type == "json":
            return self._export_json()
        elif format_type == "prometheus":
            return self._export_prometheus()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _export_json(self) -> str:
        """Export metrics as JSON"""
        export_data = {"timestamp": datetime.utcnow().isoformat(), "metrics": {}}

        for name, metric in self.metrics.items():
            stats = metric.get_statistics()
            export_data["metrics"][name] = {
                "type": metric.metric_type.value,
                "statistics": stats,
                "trend": metric.get_trend(),
                "data_points_count": len(metric.data_points),
            }

        return json.dumps(export_data, indent=2)

    def _export_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        for name, metric in self.metrics.items():
            stats = metric.get_statistics()

            # Add metric metadata
            lines.append(f"# HELP {name} {metric.metric_type.value} metric")
            lines.append(f"# TYPE {name} {metric.metric_type.value}")

            # Add statistics
            for stat_name, value in stats.items():
                metric_name = f"{name}_{stat_name}"
                lines.append(f"{metric_name} {value}")

        return "\n".join(lines)


class PerformanceMonitor:
    """
    Real-time performance monitoring for strategies.

    Features:
    - Strategy-specific metrics tracking
    - Performance threshold alerts
    - Automatic performance optimization recommendations
    - Historical performance analysis
    """

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.strategy_metrics: Dict[str, StrategyMetrics] = {}
        self.performance_thresholds = {
            "max_execution_time_ms": 5000,
            "min_success_rate": 0.95,
            "max_error_rate": 0.05,
            "max_memory_usage_mb": 1000,
        }
        self.alert_callbacks: List[Callable] = []

    def track_strategy_execution(self, strategy: BaseStrategy, result: StrategyResult):
        """Track strategy execution metrics"""
        strategy_name = f"{strategy.name}_v{strategy.version}"

        # Record core metrics
        self.metrics_collector.record_timer(
            f"strategy_execution_time_{strategy_name}",
            result.execution_time_ms,
            {"strategy": strategy.name, "version": strategy.version},
        )

        self.metrics_collector.record_counter(
            f"strategy_executions_{strategy_name}",
            1.0,
            {"strategy": strategy.name, "success": str(result.success)},
        )

        if not result.success:
            self.metrics_collector.record_counter(
                f"strategy_errors_{strategy_name}",
                1.0,
                {"strategy": strategy.name, "error": result.error_message or "unknown"},
            )

        # Check performance thresholds
        self._check_performance_thresholds(strategy, result)

        # Update strategy-specific metrics
        if strategy_name not in self.strategy_metrics:
            self.strategy_metrics[strategy_name] = StrategyMetrics()

        metrics = self.strategy_metrics[strategy_name]
        metrics.update_execution(result.execution_time_ms, result.success)

    def get_strategy_performance_report(
        self, strategy_name: str, time_window_minutes: int = 60
    ) -> Dict[str, Any]:
        """Get comprehensive performance report for a strategy"""
        report = {}

        # Get metrics from collector
        execution_time_metric = self.metrics_collector.get_metric(
            f"strategy_execution_time_{strategy_name}"
        )
        if execution_time_metric:
            report["execution_times"] = execution_time_metric.get_statistics(
                time_window_minutes
            )

        execution_count_metric = self.metrics_collector.get_metric(
            f"strategy_executions_{strategy_name}"
        )
        if execution_count_metric:
            report["execution_counts"] = execution_count_metric.get_statistics(
                time_window_minutes
            )

        error_metric = self.metrics_collector.get_metric(
            f"strategy_errors_{strategy_name}"
        )
        if error_metric:
            report["errors"] = error_metric.get_statistics(time_window_minutes)

        # Add strategy-specific metrics if available
        if strategy_name in self.strategy_metrics:
            metrics = self.strategy_metrics[strategy_name]
            report["overall_metrics"] = {
                "total_executions": metrics.execution_count,
                "success_rate": metrics.success_rate,
                "average_execution_time": metrics.average_execution_time,
                "performance_score": metrics.get_performance_score(),
            }

        return report

    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get current performance alerts"""
        alerts = []

        for strategy_name, metrics in self.strategy_metrics.items():
            # Check execution time threshold
            if (
                metrics.average_execution_time
                > self.performance_thresholds["max_execution_time_ms"]
            ):
                alerts.append(
                    {
                        "type": "slow_execution",
                        "strategy": strategy_name,
                        "current_value": metrics.average_execution_time,
                        "threshold": self.performance_thresholds[
                            "max_execution_time_ms"
                        ],
                        "severity": "warning",
                    }
                )

            # Check success rate threshold
            if metrics.success_rate < self.performance_thresholds["min_success_rate"]:
                alerts.append(
                    {
                        "type": "low_success_rate",
                        "strategy": strategy_name,
                        "current_value": metrics.success_rate,
                        "threshold": self.performance_thresholds["min_success_rate"],
                        "severity": "critical",
                    }
                )

        return alerts

    def add_alert_callback(self, callback: Callable):
        """Add callback for performance alerts"""
        self.alert_callbacks.append(callback)

    def _check_performance_thresholds(
        self, strategy: BaseStrategy, result: StrategyResult
    ):
        """Check if performance thresholds are exceeded"""
        strategy_name = f"{strategy.name}_v{strategy.version}"
        alerts = []

        # Check execution time
        if (
            result.execution_time_ms
            > self.performance_thresholds["max_execution_time_ms"]
        ):
            alerts.append(
                {
                    "type": "execution_time_exceeded",
                    "strategy": strategy_name,
                    "value": result.execution_time_ms,
                    "threshold": self.performance_thresholds["max_execution_time_ms"],
                }
            )

        # Trigger alert callbacks
        for alert in alerts:
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")


class ABTestingFramework:
    """
    A/B testing framework for strategy comparison and optimization.

    Features:
    - Multi-variate testing support
    - Statistical significance testing
    - Automatic winner promotion
    - Real-time test monitoring
    - Segmented user testing
    """

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.active_tests: Dict[str, ABTestConfig] = {}
        self.test_results: Dict[str, Dict[str, ABTestResult]] = {}
        self.test_assignments: Dict[
            str, Dict[str, str]
        ] = {}  # user_id -> test_id -> strategy
        self._lock = threading.RLock()

    def create_ab_test(self, config: ABTestConfig) -> str:
        """Create a new A/B test"""
        with self._lock:
            # Validate configuration
            total_traffic = sum(config.traffic_split.values())
            if abs(total_traffic - 100.0) > 0.01:
                raise ValueError(
                    f"Traffic split must sum to 100%, got {total_traffic}%"
                )

            self.active_tests[config.test_id] = config
            self.test_results[config.test_id] = {}
            self.test_assignments[config.test_id] = {}

            logger.info(f"Created A/B test: {config.name} ({config.test_id})")
            return config.test_id

    def assign_strategy(self, test_id: str, user_id: str) -> Optional[str]:
        """Assign a strategy to a user for A/B testing"""
        with self._lock:
            if test_id not in self.active_tests:
                return None

            config = self.active_tests[test_id]

            # Check if user already assigned
            if user_id in self.test_assignments[test_id]:
                return self.test_assignments[test_id][user_id]

            # Assign strategy based on traffic split
            import random

            rand_value = random.uniform(0, 100)

            cumulative_percentage = 0
            for strategy_name, percentage in config.traffic_split.items():
                cumulative_percentage += percentage
                if rand_value <= cumulative_percentage:
                    self.test_assignments[test_id][user_id] = strategy_name
                    return strategy_name

            # Fallback to first strategy
            first_strategy = list(config.traffic_split.keys())[0]
            self.test_assignments[test_id][user_id] = first_strategy
            return first_strategy

    def record_test_result(
        self, test_id: str, strategy_name: str, result: StrategyResult, user_id: str
    ):
        """Record a test result for analysis"""
        with self._lock:
            if test_id not in self.active_tests:
                return

            # Record metrics for this test
            labels = {"test_id": test_id, "strategy": strategy_name, "user_id": user_id}

            self.metrics_collector.record_timer(
                "ab_test_execution_time", result.execution_time_ms, labels
            )

            self.metrics_collector.record_counter(
                "ab_test_executions", 1.0, {**labels, "success": str(result.success)}
            )

            if not result.success:
                self.metrics_collector.record_counter("ab_test_errors", 1.0, labels)

    def analyze_test_results(self, test_id: str) -> Dict[str, ABTestResult]:
        """Analyze A/B test results with statistical significance"""
        if test_id not in self.active_tests:
            return {}

        config = self.active_tests[test_id]
        results = {}

        for strategy_name in config.strategies:
            # Get metrics for this strategy
            execution_metric = self.metrics_collector.get_metric(
                "ab_test_execution_time"
            )
            success_metric = self.metrics_collector.get_metric("ab_test_executions")
            self.metrics_collector.get_metric("ab_test_errors")

            if not execution_metric or not success_metric:
                continue

            # Filter data points for this test and strategy
            strategy_executions = [
                dp
                for dp in success_metric.data_points
                if dp.labels.get("test_id") == test_id
                and dp.labels.get("strategy") == strategy_name
            ]

            if not strategy_executions:
                continue

            successful_executions = [
                dp for dp in strategy_executions if dp.labels.get("success") == "True"
            ]

            sample_size = len(strategy_executions)
            success_rate = (
                len(successful_executions) / sample_size if sample_size > 0 else 0
            )

            # Get execution times
            execution_times = [
                dp.value
                for dp in execution_metric.data_points
                if dp.labels.get("test_id") == test_id
                and dp.labels.get("strategy") == strategy_name
            ]

            avg_execution_time = (
                statistics.mean(execution_times) if execution_times else 0
            )

            # Statistical significance testing (simplified)
            is_significant = sample_size >= config.minimum_sample_size
            confidence_interval = self._calculate_confidence_interval(
                success_rate, sample_size, config.confidence_level
            )
            p_value = self._calculate_p_value(strategy_name, test_id, config)

            results[strategy_name] = ABTestResult(
                test_id=test_id,
                strategy_name=strategy_name,
                sample_size=sample_size,
                success_rate=success_rate,
                average_execution_time=avg_execution_time,
                confidence_interval=confidence_interval,
                is_statistically_significant=is_significant,
                p_value=p_value,
            )

        self.test_results[test_id] = results
        return results

    def get_test_winner(self, test_id: str) -> Optional[str]:
        """Get the winning strategy from A/B test"""
        results = self.analyze_test_results(test_id)

        if not results:
            return None

        # Find strategy with best performance (highest success rate, then lowest execution time)
        best_strategy = None
        best_score = -1

        for strategy_name, result in results.items():
            if not result.is_statistically_significant:
                continue

            # Composite score: success rate (0.7) + execution time penalty (0.3)
            execution_score = max(
                0, 1 - (result.average_execution_time / 10000)
            )  # Normalize to 0-1
            score = result.success_rate * 0.7 + execution_score * 0.3

            if score > best_score:
                best_score = score
                best_strategy = strategy_name

        return best_strategy

    def stop_test(self, test_id: str) -> bool:
        """Stop an A/B test"""
        with self._lock:
            if test_id in self.active_tests:
                del self.active_tests[test_id]
                logger.info(f"Stopped A/B test: {test_id}")
                return True
            return False

    def get_test_summary(self, test_id: str) -> Dict[str, Any]:
        """Get comprehensive test summary"""
        if test_id not in self.active_tests:
            return {}

        config = self.active_tests[test_id]
        results = self.test_results.get(test_id, {})
        winner = self.get_test_winner(test_id)

        return {
            "test_id": test_id,
            "name": config.name,
            "status": "running",
            "strategies": config.strategies,
            "traffic_split": config.traffic_split,
            "total_participants": len(self.test_assignments.get(test_id, {})),
            "results": {
                name: {
                    "sample_size": result.sample_size,
                    "success_rate": result.success_rate,
                    "avg_execution_time": result.average_execution_time,
                    "is_significant": result.is_statistically_significant,
                }
                for name, result in results.items()
            },
            "winner": winner,
            "confidence_level": config.confidence_level,
        }

    def _calculate_confidence_interval(
        self, success_rate: float, sample_size: int, confidence_level: float
    ) -> tuple:
        """Calculate confidence interval for success rate"""
        if sample_size == 0:
            return (0.0, 0.0)

        import math

        # Z-score for confidence level (simplified - using 1.96 for 95%)
        z_score = 1.96 if confidence_level >= 0.95 else 1.64

        # Standard error
        se = math.sqrt((success_rate * (1 - success_rate)) / sample_size)

        # Margin of error
        margin = z_score * se

        return (max(0, success_rate - margin), min(1, success_rate + margin))

    def _calculate_p_value(
        self, strategy_name: str, test_id: str, config: ABTestConfig
    ) -> float:
        """Calculate p-value for statistical significance (simplified)"""
        # Simplified implementation - in production use proper statistical testing
        results = self.test_results.get(test_id, {})

        if len(results) < 2:
            return 1.0

        strategy_result = results.get(strategy_name)
        if not strategy_result:
            return 1.0

        # Compare with other strategies
        other_results = [r for name, r in results.items() if name != strategy_name]
        if not other_results:
            return 1.0

        # Simplified p-value calculation
        best_other = max(other_results, key=lambda r: r.success_rate)

        if strategy_result.sample_size < 30 or best_other.sample_size < 30:
            return 1.0  # Insufficient sample size

        # Very simplified - use proper statistical test in production
        if strategy_result.success_rate > best_other.success_rate:
            return 0.05 if strategy_result.sample_size > 100 else 0.1
        else:
            return 0.5
