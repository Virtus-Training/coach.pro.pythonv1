# Enterprise Strategy Pattern Integration Guide

## 🎯 Overview

This guide demonstrates how to integrate and use the enterprise-grade Strategy Pattern system in CoachPro. The system provides:

- **Multi-provider PDF generation** with automatic fallback
- **Scientific nutrition calculations** with multiple algorithms
- **AI-powered workout recommendations** with learning capabilities
- **Dynamic pricing strategies** with market optimization
- **Performance monitoring** and A/B testing
- **Circuit breakers** and resilience patterns

## 🚀 Quick Start

### 1. Basic PDF Generation

```python
from core.strategies.pdf import (
    PDFStrategyManager, PDFGenerationRequest, PDFGenerationContext,
    PDFTemplate, PDFQuality, PDFFormat
)

# Initialize manager
pdf_manager = PDFStrategyManager()

# Create template
template = PDFTemplate(
    name="Workout Session",
    template_type="workout",
    layout="standard"
)

# Prepare data
workout_data = {
    'title': 'Séance Force',
    'exercises': [...],
    'notes': 'Excellent travail!'
}

# Create context
context = PDFGenerationContext(
    template=template,
    data=workout_data,
    quality=PDFQuality.HIGH
)

# Generate PDF
request = PDFGenerationRequest(
    context=context,
    enable_fallback=True
)

result = await pdf_manager.generate_pdf(request)
pdf_bytes = result.pdf_data
```

### 2. Nutrition Calculations

```python
from core.strategies.nutrition import (
    NutritionContext, PersonalMetrics,
    Gender, ActivityLevel, NutritionGoal
)

# Create client profile
metrics = PersonalMetrics(
    age=28,
    gender=Gender.MALE,
    height_cm=180,
    weight_kg=75,
    body_fat_percentage=12.0
)

# Create nutrition context
context = NutritionContext(
    personal_metrics=metrics,
    activity_level=ActivityLevel.ACTIVE,
    nutrition_goal=NutritionGoal.MUSCLE_GAIN,
    training_days_per_week=4
)

# Calculate with Harris-Benedict
from core.strategies.nutrition import HarrisBenedictStrategy

strategy = HarrisBenedictStrategy()
result = await strategy.execute_with_monitoring(
    StrategyContext(data=context)
)

nutrition_plan = result.data
print(f"Target calories: {nutrition_plan.target_calories:.0f}")
print(f"Protein: {nutrition_plan.macronutrient_targets.protein_g:.0f}g")
```

### 3. Strategy Management

```python
from core.strategies import StrategyRegistry, StrategySelector

# Initialize registry
registry = StrategyRegistry()

# Auto-discover strategies
await registry.discover_strategies(['core/strategies'])

# Get available strategies
pdf_strategies = registry.get_strategies_by_category('pdf_generation')
nutrition_strategies = registry.get_strategies_by_category('nutrition_calculation')

# Select best strategy for context
selector = StrategySelector(registry)
best_strategy = selector.select_best_strategy('pdf_generation', context)
```

## 📊 Performance Monitoring

### Real-time Metrics

```python
from core.strategies.monitoring import MetricsCollector, PerformanceMonitor

# Initialize monitoring
metrics = MetricsCollector()
monitor = PerformanceMonitor(metrics)

# Track strategy execution
monitor.track_strategy_execution(strategy, result)

# Get performance report
report = monitor.get_strategy_performance_report('reportlab_pdf')
print(f"Average execution time: {report['execution_times']['avg']:.0f}ms")
print(f"Success rate: {report['overall_metrics']['success_rate']:.2%}")
```

### A/B Testing

```python
from core.strategies.monitoring import ABTestingFramework, ABTestConfig

# Create A/B test
config = ABTestConfig(
    test_id="pdf_engine_test",
    name="PDF Engine Comparison",
    strategies=["reportlab_pdf", "weasyprint_pdf"],
    traffic_split={"reportlab_pdf": 50.0, "weasyprint_pdf": 50.0},
    minimum_sample_size=100
)

ab_testing = ABTestingFramework(metrics)
test_id = ab_testing.create_ab_test(config)

# Assign users to strategies
strategy_name = ab_testing.assign_strategy(test_id, user_id)

# Record results
ab_testing.record_test_result(test_id, strategy_name, result, user_id)

# Analyze results
results = ab_testing.analyze_test_results(test_id)
winner = ab_testing.get_test_winner(test_id)
```

## 🛡️ Resilience Patterns

### Circuit Breakers

```python
from core.strategies.circuit_breaker import CircuitBreaker, CircuitBreakerConfig

# Configure circuit breaker
config = CircuitBreakerConfig(
    failure_threshold=5,
    recovery_timeout=60,
    success_threshold=3
)

circuit_breaker = CircuitBreaker("pdf_service", config)

# Execute with protection
async def protected_pdf_generation():
    return await circuit_breaker.call(
        generate_pdf_function,
        context
    )
```

### Fallback Management

```python
from core.strategies.circuit_breaker import FallbackManager, FallbackConfig

# Configure fallbacks
config = FallbackConfig(
    max_fallback_attempts=3,
    prefer_cached_result=True,
    degraded_mode_enabled=True
)

fallback_manager = FallbackManager(config)

# Add fallback strategies (in priority order)
fallback_manager.add_fallback_strategy(reportlab_strategy, priority=1)
fallback_manager.add_fallback_strategy(weasyprint_strategy, priority=2)
fallback_manager.add_fallback_strategy(fpdf_strategy, priority=3)

# Execute with fallback
result = await fallback_manager.execute_with_fallback(
    primary_strategy,
    context
)
```

## 🎨 Custom Strategy Development

### Creating a Custom PDF Strategy

```python
from core.strategies.base import BaseStrategy, StrategyConfig
from core.strategies.pdf.base import PDFGenerationContext, PDFGenerationResult

class CustomPDFStrategy(BaseStrategy[PDFGenerationContext]):
    def __init__(self):
        config = StrategyConfig(
            name="custom_pdf",
            version="1.0.0",
            priority=StrategyPriority.NORMAL
        )
        super().__init__(config)

        # Strategy metadata for auto-discovery
        self._strategy_category = "pdf_generation"
        self._strategy_tags = {"custom", "specialized"}

    async def execute_async(self, context: StrategyContext) -> StrategyResult:
        # Implement your custom PDF generation logic
        pdf_data = await self._generate_custom_pdf(context.data)

        result = PDFGenerationResult(
            pdf_data=pdf_data,
            generation_engine="Custom",
            template_used=context.data.template.name
        )

        return StrategyResult(
            data=result,
            success=True,
            strategy_name=self.name
        )

    def validate_context(self, context) -> List[str]:
        # Validate input context
        return []

    def get_supported_context_types(self) -> List[type]:
        return [PDFGenerationContext]
```

### Register Custom Strategy

```python
# Manual registration
registry.register_strategy(
    CustomPDFStrategy,
    config,
    "pdf_generation",
    tags={"custom", "specialized"}
)

# Or use auto-discovery by adding strategy to appropriate module
```

## 🧪 Testing Strategies

### Unit Testing

```python
import pytest
from core.strategies.pdf import ReportLabPDFStrategy

@pytest.mark.asyncio
async def test_reportlab_strategy():
    strategy = ReportLabPDFStrategy()

    # Create test context
    context = create_test_pdf_context()

    # Execute strategy
    result = await strategy.execute_with_monitoring(context)

    # Validate result
    assert result.is_success
    assert result.data.pdf_data is not None
    assert result.data.quality_metrics.overall_quality_score > 70
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_pdf_strategy_integration():
    manager = PDFStrategyManager()

    # Test all available strategies
    strategies = manager.get_available_strategies()

    for strategy_info in strategies:
        if strategy_info['enabled']:
            request = create_test_request(strategy_info['name'])
            result = await manager.generate_pdf(request)

            assert result.success
            assert len(result.pdf_data) > 0
```

### Performance Testing

```python
@pytest.mark.asyncio
async def test_strategy_performance():
    strategy = ReportLabPDFStrategy()
    context = create_test_context()

    # Measure execution time
    start_time = time.time()
    result = await strategy.execute_with_monitoring(context)
    execution_time = (time.time() - start_time) * 1000

    # Performance assertions
    assert execution_time < 5000  # Max 5 seconds
    assert result.data.quality_metrics.generation_time_ms < 10000
```

## 📈 Analytics and Optimization

### Performance Analytics

```python
def analyze_strategy_performance():
    # Get performance data
    report = pdf_manager.get_performance_report()

    # Strategy comparison
    strategies = report['strategy_health']

    best_performance = max(
        strategies.items(),
        key=lambda x: x[1]['performance_score']
    )

    print(f"Best performing strategy: {best_performance[0]}")

    # Identify optimization opportunities
    slow_strategies = [
        name for name, health in strategies.items()
        if health['average_execution_time'] > 5000
    ]

    return {
        'best_strategy': best_performance[0],
        'optimization_candidates': slow_strategies
    }
```

### Automated Optimization

```python
async def optimize_system():
    # Run optimization
    result = await pdf_manager.optimize_strategies()

    # Apply recommendations
    for recommendation in result['recommendations']:
        if 'performance below threshold' in recommendation:
            # Reset metrics for underperforming strategies
            strategy_name = extract_strategy_name(recommendation)
            strategy = registry.get_strategy('pdf_generation', strategy_name)
            strategy.reset_metrics()

    # Clear caches
    for strategy in registry.get_strategies_by_category('pdf_generation'):
        strategy.clear_cache()

    return result
```

## 🔧 Configuration

### Environment Configuration

```bash
# .env file
COACH_STRATEGY_CACHE_ENABLED=true
COACH_STRATEGY_CACHE_TTL=3600
COACH_CIRCUIT_BREAKER_ENABLED=true
COACH_AB_TESTING_ENABLED=true
COACH_PERFORMANCE_MONITORING=true
COACH_FALLBACK_ENABLED=true
COACH_DEGRADED_MODE_ENABLED=true
```

### Runtime Configuration

```python
# Configure strategy manager
pdf_manager = PDFStrategyManager()

# Adjust thresholds
pdf_manager.performance_monitor.performance_thresholds.update({
    'max_execution_time_ms': 10000,
    'min_success_rate': 0.95
})

# Configure fallback behavior
pdf_manager.fallback_manager.config.max_fallback_attempts = 2
pdf_manager.fallback_manager.config.fallback_timeout = 10.0
```

## 🚨 Error Handling

### Strategy Errors

```python
from core.strategies.base import StrategyError, StrategyValidationError

try:
    result = await strategy.execute_with_monitoring(context)
except StrategyValidationError as e:
    logger.error(f"Validation failed: {e}")
    # Handle validation errors
except StrategyTimeoutError as e:
    logger.error(f"Strategy timed out: {e}")
    # Handle timeout
except StrategyError as e:
    logger.error(f"Strategy execution failed: {e}")
    # Handle general strategy errors
```

### Circuit Breaker Events

```python
def handle_circuit_breaker_opened(strategy_name):
    logger.warning(f"Circuit breaker opened for {strategy_name}")
    # Notify monitoring system
    # Switch to fallback strategy
    # Alert administrators

circuit_breaker.add_state_change_callback(handle_circuit_breaker_opened)
```

## 📋 Best Practices

### 1. Strategy Selection

- Use `AUTO` mode for intelligent selection
- Specify strategy only when you have specific requirements
- Always enable fallback for production systems
- Monitor strategy performance and adjust selection logic

### 2. Performance Optimization

- Enable caching for frequently used contexts
- Set appropriate timeouts based on use case
- Monitor memory usage in long-running processes
- Use circuit breakers to prevent cascade failures

### 3. Error Handling

- Always handle strategy exceptions gracefully
- Provide meaningful error messages to users
- Log detailed error information for debugging
- Implement proper retry logic with exponential backoff

### 4. Testing

- Test all strategies with representative data
- Include performance tests in CI/CD pipeline
- Test fallback scenarios and degraded mode
- Validate quality metrics and thresholds

### 5. Monitoring

- Monitor strategy performance in real-time
- Set up alerts for performance degradation
- Track success rates and error patterns
- Analyze A/B test results regularly

## 🔄 Migration Guide

### From Existing PDF Service

```python
# Old approach
from services.pdf_generator import PDFGenerator

pdf_gen = PDFGenerator()
pdf_data = pdf_gen.generate_workout_pdf(session_data)

# New approach with strategies
from core.strategies.pdf import PDFStrategyManager

pdf_manager = PDFStrategyManager()
request = PDFGenerationRequest(
    context=PDFGenerationContext(
        template=workout_template,
        data=session_data
    ),
    preferred_strategy=PDFGenerationStrategy.AUTO,
    enable_fallback=True
)

result = await pdf_manager.generate_pdf(request)
pdf_data = result.pdf_data
```

### Gradual Migration Strategy

1. **Phase 1**: Implement strategy framework alongside existing code
2. **Phase 2**: Route new features through strategy system
3. **Phase 3**: Migrate existing functionality module by module
4. **Phase 4**: Remove legacy code and fully adopt strategies

## 📚 Advanced Topics

### Custom Metrics Collection

```python
# Define custom metrics
class CustomMetricsCollector(MetricsCollector):
    def collect_business_metrics(self, strategy_name, result):
        # Collect business-specific metrics
        self.record_gauge(
            f"business_value_{strategy_name}",
            self.calculate_business_value(result)
        )

# Use custom collector
custom_metrics = CustomMetricsCollector()
monitor = PerformanceMonitor(custom_metrics)
```

### Machine Learning Integration

```python
# ML-based strategy selection
class MLStrategySelector(StrategySelector):
    def __init__(self, registry, ml_model):
        super().__init__(registry)
        self.ml_model = ml_model

    def select_best_strategy(self, category, context, excluded=None):
        # Use ML model to predict best strategy
        features = self.extract_features(context)
        prediction = self.ml_model.predict(features)

        strategy_name = self.decode_prediction(prediction)
        return self.registry.get_strategy(category, strategy_name)
```

This integration guide provides comprehensive examples for implementing and using the enterprise Strategy Pattern system in CoachPro. The system is designed to be extensible, performant, and production-ready with enterprise-grade features.