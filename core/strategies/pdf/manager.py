"""
PDF Strategy Manager

Enterprise-grade PDF generation management with automatic strategy
selection, quality assessment, and intelligent fallback mechanisms.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from ..base import StrategyContext
from ..registry import StrategyRegistry, StrategySelector, StrategyManager
from ..monitoring import MetricsCollector, PerformanceMonitor, ABTestingFramework
from ..circuit_breaker import FallbackManager, FallbackConfig

from .base import (
    PDFGenerationContext, PDFGenerationResult, PDFQuality,
    PDFComplexity, PDFFormat, PDFQualityMetrics
)
from .reportlab_strategy import ReportLabPDFStrategy
from .weasyprint_strategy import WeasyPrintPDFStrategy
from .fpdf_strategy import FPDFStrategy

logger = logging.getLogger(__name__)


class PDFGenerationStrategy(Enum):
    """Available PDF generation strategies"""
    REPORTLAB = "reportlab_pdf"
    WEASYPRINT = "weasyprint_pdf"
    FPDF = "fpdf_pdf"
    AUTO = "auto"


@dataclass
class PDFGenerationRequest:
    """Request for PDF generation"""
    context: PDFGenerationContext
    preferred_strategy: Optional[PDFGenerationStrategy] = PDFGenerationStrategy.AUTO
    quality_threshold: float = 70.0  # Minimum quality score
    max_generation_time_ms: float = 30000  # 30 seconds
    enable_fallback: bool = True
    enable_ab_testing: bool = False


class PDFStrategyManager:
    """
    Comprehensive PDF generation management system.

    Features:
    - Intelligent strategy selection based on document complexity
    - Quality assessment and optimization
    - Performance monitoring and A/B testing
    - Automatic fallback mechanisms
    - Caching and optimization
    """

    def __init__(self):
        self.registry = StrategyRegistry()
        self.metrics_collector = MetricsCollector()
        self.performance_monitor = PerformanceMonitor(self.metrics_collector)
        self.ab_testing = ABTestingFramework(self.metrics_collector)

        # Initialize strategy selector and manager
        self.selector = StrategySelector(self.registry)
        self.strategy_manager = StrategyManager(self.registry, self.selector)

        # Initialize fallback manager
        fallback_config = FallbackConfig(
            max_fallback_attempts=3,
            fallback_timeout=15.0,
            prefer_cached_result=True,
            degraded_mode_enabled=True
        )
        self.fallback_manager = FallbackManager(fallback_config)

        # Strategy configurations
        self._strategy_preferences = {
            PDFComplexity.SIMPLE: [PDFGenerationStrategy.FPDF, PDFGenerationStrategy.REPORTLAB],
            PDFComplexity.MEDIUM: [PDFGenerationStrategy.REPORTLAB, PDFGenerationStrategy.WEASYPRINT],
            PDFComplexity.COMPLEX: [PDFGenerationStrategy.REPORTLAB, PDFGenerationStrategy.WEASYPRINT],
            PDFComplexity.ADVANCED: [PDFGenerationStrategy.REPORTLAB, PDFGenerationStrategy.WEASYPRINT]
        }

        # Initialize strategies
        self._initialize_strategies()

    def _initialize_strategies(self):
        """Initialize and register all PDF generation strategies"""
        try:
            # Register ReportLab strategy
            reportlab_strategy = ReportLabPDFStrategy()
            self.registry.register_strategy(
                reportlab_strategy.__class__,
                reportlab_strategy.config,
                "pdf_generation",
                {"professional", "complex_layouts", "high_performance"}
            )

            # Add as fallback
            self.fallback_manager.add_fallback_strategy(reportlab_strategy, priority=1)

            logger.info("Registered ReportLab PDF strategy")

        except Exception as e:
            logger.error(f"Failed to initialize ReportLab strategy: {e}")

        try:
            # Register WeasyPrint strategy
            weasyprint_strategy = WeasyPrintPDFStrategy()
            if weasyprint_strategy.available:
                self.registry.register_strategy(
                    weasyprint_strategy.__class__,
                    weasyprint_strategy.config,
                    "pdf_generation",
                    {"html_css", "modern_layouts", "responsive"}
                )

                # Add as fallback
                self.fallback_manager.add_fallback_strategy(weasyprint_strategy, priority=2)

                logger.info("Registered WeasyPrint PDF strategy")
            else:
                logger.warning("WeasyPrint not available, skipping registration")

        except Exception as e:
            logger.error(f"Failed to initialize WeasyPrint strategy: {e}")

        try:
            # Register FPDF strategy
            fpdf_strategy = FPDFStrategy()
            if fpdf_strategy.available:
                self.registry.register_strategy(
                    fpdf_strategy.__class__,
                    fpdf_strategy.config,
                    "pdf_generation",
                    {"lightweight", "fallback", "simple"}
                )

                # Add as emergency fallback
                self.fallback_manager.add_fallback_strategy(fpdf_strategy, priority=3)

                logger.info("Registered FPDF PDF strategy")
            else:
                logger.warning("FPDF not available, skipping registration")

        except Exception as e:
            logger.error(f"Failed to initialize FPDF strategy: {e}")

    async def generate_pdf(self, request: PDFGenerationRequest) -> PDFGenerationResult:
        """
        Generate PDF with intelligent strategy selection and fallback.

        Args:
            request: PDF generation request with context and preferences

        Returns:
            PDFGenerationResult with generated PDF data and quality metrics
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Create strategy context
            strategy_context = StrategyContext(
                data=request.context,
                request_id=f"pdf_{start_time}",
                metadata={
                    "preferred_strategy": request.preferred_strategy.value if request.preferred_strategy else None,
                    "quality_threshold": request.quality_threshold,
                    "max_generation_time": request.max_generation_time_ms
                }
            )

            # Select strategy
            if request.preferred_strategy == PDFGenerationStrategy.AUTO:
                strategy = self._select_optimal_strategy(request.context)
            else:
                strategy = self.registry.get_strategy("pdf_generation", request.preferred_strategy.value)

            if not strategy:
                # Use fallback if no strategy found
                if request.enable_fallback:
                    return await self._generate_with_fallback(strategy_context)
                else:
                    raise Exception("No suitable PDF strategy available")

            # Generate with selected strategy and fallback support
            if request.enable_fallback:
                result = await self.fallback_manager.execute_with_fallback(
                    strategy,
                    strategy_context,
                    enable_cache=True
                )
            else:
                result = await strategy.execute_with_monitoring(strategy_context)

            # Extract PDF result
            if result.is_success and result.data:
                pdf_result = result.data

                # Quality assessment
                if pdf_result.quality_metrics.overall_quality_score < request.quality_threshold:
                    logger.warning(
                        f"PDF quality ({pdf_result.quality_metrics.overall_quality_score:.1f}) "
                        f"below threshold ({request.quality_threshold})"
                    )

                    # Try better strategy if available
                    if request.enable_fallback:
                        better_result = await self._try_better_quality_strategy(
                            strategy_context,
                            request.quality_threshold,
                            strategy.name
                        )
                        if better_result:
                            pdf_result = better_result

                # Record metrics
                self.performance_monitor.track_strategy_execution(strategy, result)

                # A/B testing if enabled
                if request.enable_ab_testing:
                    await self._record_ab_test_result(strategy_context, strategy, result)

                return pdf_result
            else:
                raise Exception(result.error_message or "PDF generation failed")

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")

            # Try emergency fallback
            if request.enable_fallback:
                try:
                    return await self._emergency_fallback(request.context)
                except Exception as fallback_error:
                    logger.error(f"Emergency fallback failed: {fallback_error}")

            raise e

    def _select_optimal_strategy(self, context: PDFGenerationContext) -> Optional[Any]:
        """Select optimal strategy based on document characteristics"""
        # Get preferred strategies for complexity level
        preferred_strategies = self._strategy_preferences.get(
            context.complexity,
            [PDFGenerationStrategy.REPORTLAB]
        )

        # Try to get the first available preferred strategy
        for strategy_enum in preferred_strategies:
            strategy = self.registry.get_strategy("pdf_generation", strategy_enum.value)
            if strategy:
                # Additional checks
                if self._is_strategy_suitable(strategy, context):
                    return strategy

        # Fallback to any available strategy
        strategies = self.registry.get_strategies_by_category("pdf_generation")
        for strategy in strategies:
            if self._is_strategy_suitable(strategy, context):
                return strategy

        return None

    def _is_strategy_suitable(self, strategy: Any, context: PDFGenerationContext) -> bool:
        """Check if strategy is suitable for the given context"""
        try:
            # Check if strategy can handle the complexity
            if hasattr(strategy, 'max_complexity'):
                if context.complexity.value > strategy.max_complexity:
                    return False

            # Check quality requirements
            if context.quality == PDFQuality.PRINT_READY:
                # Only high-quality strategies for print-ready
                if strategy.name == "fpdf_pdf":
                    return False

            # Check feature requirements
            if context.include_charts and strategy.name == "fpdf_pdf":
                return False

            # Check performance requirements
            if context.prefer_speed_over_quality and strategy.name == "reportlab_pdf":
                # ReportLab might be slower for simple documents
                if context.complexity == PDFComplexity.SIMPLE:
                    return False

            return True

        except Exception as e:
            logger.debug(f"Error checking strategy suitability: {e}")
            return True  # Default to allowing the strategy

    async def _generate_with_fallback(self, context: StrategyContext) -> PDFGenerationResult:
        """Generate PDF using fallback mechanisms"""
        # Try to get best strategy first
        best_strategy = self.selector.select_best_strategy("pdf_generation", context)

        if best_strategy:
            result = await self.fallback_manager.execute_with_fallback(
                best_strategy,
                context,
                enable_cache=True
            )

            if result.is_success and result.data:
                return result.data

        # If all fails, use emergency fallback
        return await self._emergency_fallback(context.data)

    async def _try_better_quality_strategy(
        self,
        context: StrategyContext,
        quality_threshold: float,
        exclude_strategy: str
    ) -> Optional[PDFGenerationResult]:
        """Try a different strategy for better quality"""
        try:
            # Get alternative strategies
            strategies = self.registry.get_strategies_by_category("pdf_generation")

            for strategy in strategies:
                if strategy.name == exclude_strategy:
                    continue

                # Try higher-quality strategy
                if strategy.name in ["reportlab_pdf", "weasyprint_pdf"]:
                    result = await strategy.execute_with_monitoring(context)

                    if (result.is_success and result.data and
                        result.data.quality_metrics.overall_quality_score >= quality_threshold):
                        logger.info(f"Improved quality with {strategy.name}")
                        return result.data

        except Exception as e:
            logger.debug(f"Failed to improve quality: {e}")

        return None

    async def _emergency_fallback(self, context: PDFGenerationContext) -> PDFGenerationResult:
        """Emergency fallback for critical failures"""
        logger.warning("Using emergency fallback for PDF generation")

        # Create minimal PDF with basic information
        from .fpdf_strategy import FPDFStrategy

        try:
            emergency_strategy = FPDFStrategy()
            if emergency_strategy.available:
                emergency_context = StrategyContext(data=context)
                result = await emergency_strategy.execute_with_monitoring(emergency_context)

                if result.is_success and result.data:
                    result.data.warnings.append("Generated using emergency fallback - limited functionality")
                    return result.data
        except Exception as e:
            logger.error(f"Emergency fallback failed: {e}")

        # Absolute last resort - create minimal PDF data
        minimal_pdf = self._create_minimal_pdf(context)
        return PDFGenerationResult(
            pdf_data=minimal_pdf,
            quality_metrics=PDFQualityMetrics(
                file_size_kb=len(minimal_pdf) / 1024,
                generation_time_ms=100,
                page_count=1,
                overall_quality_score=30.0
            ),
            generation_engine="Emergency",
            template_used="minimal",
            success=True,
            warnings=["Minimal PDF generated due to system failures"]
        )

    def _create_minimal_pdf(self, context: PDFGenerationContext) -> bytes:
        """Create minimal PDF as absolute fallback"""
        # This is a very basic PDF structure
        # In practice, you might want to use a more sophisticated minimal PDF generator
        minimal_content = f"""
        %PDF-1.4
        1 0 obj
        <</Type/Catalog/Pages 2 0 R>>
        endobj
        2 0 obj
        <</Type/Pages/Kids[3 0 R]/Count 1>>
        endobj
        3 0 obj
        <</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>
        endobj
        4 0 obj
        <</Length 44>>
        stream
        BT
        /F1 12 Tf
        72 720 Td
        ({context.template.name} - Service temporairement indisponible) Tj
        ET
        endstream
        endobj
        xref
        0 5
        0000000000 65535 f
        0000000009 00000 n
        0000000058 00000 n
        0000000115 00000 n
        0000000189 00000 n
        trailer
        <</Size 5/Root 1 0 R>>
        startxref
        285
        %%EOF
        """
        return minimal_content.encode('utf-8')

    async def _record_ab_test_result(self, context: StrategyContext, strategy: Any, result: Any):
        """Record result for A/B testing"""
        try:
            # This would integrate with the A/B testing framework
            # For now, just log the performance
            self.metrics_collector.record_timer(
                "pdf_ab_test_execution",
                result.execution_time_ms,
                {
                    "strategy": strategy.name,
                    "complexity": context.data.complexity.value,
                    "quality": context.data.quality.value
                }
            )
        except Exception as e:
            logger.debug(f"Failed to record A/B test result: {e}")

    async def start_ab_test(
        self,
        test_name: str,
        strategies: List[PDFGenerationStrategy],
        traffic_split: Dict[str, float]
    ) -> str:
        """Start A/B test for PDF strategies"""
        from ..monitoring import ABTestConfig

        config = ABTestConfig(
            test_id=f"pdf_test_{int(asyncio.get_event_loop().time())}",
            name=test_name,
            description=f"A/B test for PDF generation strategies",
            strategies=[s.value for s in strategies],
            traffic_split=traffic_split,
            success_metrics=["execution_time", "quality_score", "success_rate"],
            minimum_sample_size=50,
            max_duration_days=7
        )

        return self.ab_testing.create_ab_test(config)

    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        strategies = self.registry.list_strategies("pdf_generation")

        report = {
            "total_strategies": len(strategies),
            "enabled_strategies": len([s for s in strategies if s["enabled"]]),
            "strategy_health": {},
            "performance_metrics": {},
            "fallback_status": self.fallback_manager.get_fallback_status(),
            "system_health": self.strategy_manager.get_system_health()
        }

        # Get individual strategy reports
        for strategy_info in strategies:
            strategy_name = strategy_info["name"]
            strategy = self.registry.get_strategy("pdf_generation", strategy_name)

            if strategy:
                report["strategy_health"][strategy_name] = strategy.get_health_status()
                report["performance_metrics"][strategy_name] = self.performance_monitor.get_strategy_performance_report(
                    f"{strategy_name}_v{strategy_info['version']}"
                )

        return report

    async def optimize_strategies(self) -> Dict[str, Any]:
        """Optimize strategy performance and selection"""
        optimization_results = {
            "actions_taken": [],
            "performance_improvements": {},
            "recommendations": []
        }

        try:
            # Analyze performance metrics
            strategies = self.registry.get_strategies_by_category("pdf_generation")

            for strategy in strategies:
                health = strategy.get_health_status()

                # Check if strategy needs optimization
                if health["performance_score"] < 70:
                    optimization_results["recommendations"].append(
                        f"Strategy {strategy.name} performance below threshold: {health['performance_score']:.1f}"
                    )

                # Reset metrics if strategy is underperforming
                if health["success_rate"] < 0.8:
                    strategy.reset_metrics()
                    optimization_results["actions_taken"].append(f"Reset metrics for {strategy.name}")

            # Clear caches for better performance
            for strategy in strategies:
                strategy.clear_cache()

            optimization_results["actions_taken"].append("Cleared all strategy caches")

        except Exception as e:
            logger.error(f"Strategy optimization failed: {e}")
            optimization_results["error"] = str(e)

        return optimization_results

    def get_available_strategies(self) -> List[Dict[str, Any]]:
        """Get list of available PDF generation strategies"""
        strategies = self.registry.list_strategies("pdf_generation")

        for strategy_info in strategies:
            strategy = self.registry.get_strategy("pdf_generation", strategy_info["name"])
            if strategy:
                strategy_info["capabilities"] = {
                    "max_complexity": getattr(strategy, "max_complexity", "unknown"),
                    "supports_charts": strategy_info["name"] != "fpdf_pdf",
                    "supports_images": True,
                    "quality_level": "high" if strategy_info["name"] == "reportlab_pdf" else "medium"
                }

        return strategies