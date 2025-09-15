"""
Enterprise Strategy Pattern System Demonstration

This demo showcases the complete strategy pattern implementation with:
- PDF generation strategies with fallback
- Nutrition calculation strategies
- Performance monitoring and A/B testing
- Circuit breakers and resilience patterns
- Real-time metrics and analytics
"""

import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Strategy framework imports

# PDF strategies
from core.strategies.pdf import (
    PDFComplexity,
    PDFFormat,
    PDFGenerationContext,
    PDFGenerationRequest,
    PDFGenerationStrategy,
    PDFQuality,
    PDFStrategyManager,
    PDFTemplate,
)

# Nutrition strategies


class EnterpriseStrategyDemo:
    """
    Comprehensive demonstration of the enterprise strategy system.

    This demo shows real-world usage scenarios including:
    - Strategy selection and execution
    - Performance monitoring
    - A/B testing
    - Fallback mechanisms
    - Analytics and reporting
    """

    def __init__(self):
        self.pdf_manager = PDFStrategyManager()
        # Note: Nutrition manager would be initialized here when complete
        # self.nutrition_manager = NutritionStrategyManager()

    async def run_complete_demo(self):
        """Run the complete enterprise strategy demonstration"""
        print("🚀 Enterprise Strategy Pattern System Demo")
        print("=" * 60)

        try:
            # 1. PDF Generation Demo
            await self._demo_pdf_generation()

            # 2. Performance Monitoring Demo
            await self._demo_performance_monitoring()

            # 3. A/B Testing Demo
            await self._demo_ab_testing()

            # 4. Fallback Mechanisms Demo
            await self._demo_fallback_mechanisms()

            # 5. System Analytics Demo
            await self._demo_system_analytics()

            print("\n✅ Demo completed successfully!")

        except Exception as e:
            logger.error(f"Demo failed: {e}")
            print(f"\n❌ Demo failed: {e}")

    async def _demo_pdf_generation(self):
        """Demonstrate PDF generation with multiple strategies"""
        print("\n📄 PDF Generation Strategy Demo")
        print("-" * 40)

        # Create sample workout data
        workout_data = {
            "title": "Séance Force - Jour 1",
            "session_info": {
                "date": "2024-01-15",
                "duration": 75,
                "type": "Musculation",
                "coach": "Marie Fitness",
            },
            "exercises": [
                {
                    "name": "Squat",
                    "sets": [
                        {"reps": 8, "weight": 100, "rest": 120},
                        {"reps": 8, "weight": 105, "rest": 120},
                        {"reps": 6, "weight": 110, "rest": 180},
                    ],
                    "notes": "Concentrez-vous sur la profondeur du mouvement",
                },
                {
                    "name": "Développé Couché",
                    "sets": [
                        {"reps": 10, "weight": 80, "rest": 90},
                        {"reps": 8, "weight": 85, "rest": 90},
                        {"reps": 6, "weight": 90, "rest": 120},
                    ],
                    "notes": "Contrôlez la descente de la barre",
                },
            ],
            "notes": "Excellent travail aujourd'hui! Augmentez les charges la semaine prochaine.",
        }

        # Create PDF template
        template = PDFTemplate(
            name="Workout Session Template",
            template_type="workout",
            layout="standard",
            styles={"theme": "professional"},
            sections=["header", "exercises", "notes"],
        )

        # Create PDF context
        pdf_context = PDFGenerationContext(
            template=template,
            data=workout_data,
            quality=PDFQuality.HIGH,
            format=PDFFormat.A4_PORTRAIT,
            complexity=PDFComplexity.MEDIUM,
        )

        # Test different strategies
        strategies_to_test = [
            PDFGenerationStrategy.AUTO,
            PDFGenerationStrategy.REPORTLAB,
            PDFGenerationStrategy.WEASYPRINT,
            PDFGenerationStrategy.FPDF,
        ]

        for strategy in strategies_to_test:
            try:
                print(f"\n📊 Testing {strategy.value} strategy...")

                request = PDFGenerationRequest(
                    context=pdf_context,
                    preferred_strategy=strategy,
                    quality_threshold=70.0,
                    enable_fallback=True,
                )

                result = await self.pdf_manager.generate_pdf(request)

                print(f"  ✅ Success with {result.generation_engine}")
                print(f"  📏 File size: {result.file_size_mb:.2f} MB")
                print(
                    f"  ⏱️  Generation time: {result.quality_metrics.generation_time_ms:.0f}ms"
                )
                print(
                    f"  🎯 Quality score: {result.quality_metrics.overall_quality_score:.1f}/100"
                )

                if result.warnings:
                    print(f"  ⚠️  Warnings: {', '.join(result.warnings)}")

            except Exception as e:
                print(f"  ❌ Failed: {e}")

    async def _demo_performance_monitoring(self):
        """Demonstrate performance monitoring capabilities"""
        print("\n📈 Performance Monitoring Demo")
        print("-" * 40)

        # Get performance report
        report = self.pdf_manager.get_performance_report()

        print("📊 System Health:")
        print(f"  Total strategies: {report['total_strategies']}")
        print(f"  Enabled strategies: {report['enabled_strategies']}")
        print(f"  System health: {report['system_health']['health_percentage']:.1f}%")

        print("\n🔧 Strategy Health:")
        for strategy_name, health in report["strategy_health"].items():
            print(f"  {strategy_name}:")
            print(f"    Health: {'✅' if health['healthy'] else '❌'}")
            print(f"    Performance: {health['performance_score']:.1f}/100")
            print(f"    Success rate: {health['success_rate']:.2%}")
            print(f"    Executions: {health['execution_count']}")

        print("\n💾 Fallback Status:")
        fallback_status = report["fallback_status"]
        print(
            f"  Degraded mode: {'❌' if not fallback_status['degraded_mode_active'] else '⚠️ ACTIVE'}"
        )
        print(f"  Fallback strategies: {fallback_status['total_fallback_strategies']}")
        print(f"  Cache size: {fallback_status['cache_size']}")

    async def _demo_ab_testing(self):
        """Demonstrate A/B testing capabilities"""
        print("\n🧪 A/B Testing Demo")
        print("-" * 40)

        try:
            # Start A/B test
            test_id = await self.pdf_manager.start_ab_test(
                test_name="PDF Engine Comparison",
                strategies=[
                    PDFGenerationStrategy.REPORTLAB,
                    PDFGenerationStrategy.WEASYPRINT,
                ],
                traffic_split={"reportlab_pdf": 50.0, "weasyprint_pdf": 50.0},
            )

            print(f"🧪 Started A/B test: {test_id}")

            # Simulate some test traffic
            test_data = {
                "title": "A/B Test Document",
                "sections": [
                    {
                        "title": "Test Section",
                        "content": "This is test content for A/B testing.",
                    }
                ],
            }

            template = PDFTemplate(
                name="AB Test Template", template_type="generic", layout="simple"
            )

            # Run multiple generations to collect data
            for i in range(5):
                context = PDFGenerationContext(
                    template=template, data=test_data, quality=PDFQuality.STANDARD
                )

                request = PDFGenerationRequest(
                    context=context,
                    preferred_strategy=PDFGenerationStrategy.AUTO,
                    enable_ab_testing=True,
                )

                result = await self.pdf_manager.generate_pdf(request)
                print(
                    f"  Test run {i + 1}: {result.generation_engine} ({result.quality_metrics.generation_time_ms:.0f}ms)"
                )

            print("✅ A/B test data collected for analysis")

        except Exception as e:
            print(f"❌ A/B testing demo failed: {e}")

    async def _demo_fallback_mechanisms(self):
        """Demonstrate fallback and circuit breaker mechanisms"""
        print("\n🛡️ Fallback Mechanisms Demo")
        print("-" * 40)

        # Create a problematic context to trigger fallbacks
        problematic_data = {
            "title": "Fallback Test Document",
            "sections": [
                {
                    "title": "Test Section",
                    "content": "Testing fallback mechanisms with complex data.",
                }
            ],
        }

        template = PDFTemplate(
            name="Fallback Test Template", template_type="generic", layout="complex"
        )

        context = PDFGenerationContext(
            template=template,
            data=problematic_data,
            quality=PDFQuality.HIGH,
            complexity=PDFComplexity.ADVANCED,
        )

        # Test with fallback enabled
        print("🔄 Testing with fallback enabled...")
        request = PDFGenerationRequest(
            context=context,
            preferred_strategy=PDFGenerationStrategy.AUTO,
            enable_fallback=True,
            quality_threshold=90.0,  # High threshold to potentially trigger fallbacks
        )

        try:
            result = await self.pdf_manager.generate_pdf(request)
            print(f"  ✅ Generated with {result.generation_engine}")
            if result.warnings:
                print(f"  ⚠️  Fallback warnings: {', '.join(result.warnings)}")

        except Exception as e:
            print(f"  ❌ Failed even with fallback: {e}")

        # Show circuit breaker status
        report = self.pdf_manager.get_performance_report()
        fallback_strategies = report["fallback_status"]["fallback_strategies"]

        print("\n🔌 Circuit Breaker Status:")
        for strategy in fallback_strategies:
            cb_status = strategy["circuit_breaker"]
            print(f"  {strategy['strategy_name']}:")
            print(f"    State: {cb_status['state']}")
            print(f"    Success rate: {cb_status['recent_success_rate']:.2%}")
            print(f"    Total calls: {cb_status['total_calls']}")

    async def _demo_system_analytics(self):
        """Demonstrate system analytics and optimization"""
        print("\n📊 System Analytics Demo")
        print("-" * 40)

        # Get comprehensive analytics
        report = self.pdf_manager.get_performance_report()

        print("📈 Performance Analytics:")

        # Strategy performance comparison
        performances = {}
        for strategy_name, metrics in report["performance_metrics"].items():
            if "overall_metrics" in metrics:
                overall = metrics["overall_metrics"]
                performances[strategy_name] = {
                    "score": overall.get("performance_score", 0),
                    "executions": overall.get("total_executions", 0),
                    "success_rate": overall.get("success_rate", 0),
                    "avg_time": overall.get("average_execution_time", 0),
                }

        # Sort by performance score
        sorted_strategies = sorted(
            performances.items(), key=lambda x: x[1]["score"], reverse=True
        )

        print("\n🏆 Strategy Performance Ranking:")
        for i, (strategy, perf) in enumerate(sorted_strategies, 1):
            print(f"  {i}. {strategy}:")
            print(f"     Score: {perf['score']:.1f}/100")
            print(f"     Executions: {perf['executions']}")
            print(f"     Success Rate: {perf['success_rate']:.2%}")
            print(f"     Avg Time: {perf['avg_time']:.0f}ms")

        # Run optimization
        print("\n🔧 Running Strategy Optimization...")
        optimization_result = await self.pdf_manager.optimize_strategies()

        print("Optimization Results:")
        for action in optimization_result["actions_taken"]:
            print(f"  ✅ {action}")

        for recommendation in optimization_result["recommendations"]:
            print(f"  💡 {recommendation}")

        # Show available strategies and capabilities
        print("\n📋 Available Strategies:")
        strategies = self.pdf_manager.get_available_strategies()

        for strategy in strategies:
            print(f"  📄 {strategy['name']} v{strategy['version']}")
            print(f"     Priority: {strategy['priority']}")
            print(
                f"     Status: {'✅ Enabled' if strategy['enabled'] else '❌ Disabled'}"
            )

            if "capabilities" in strategy:
                caps = strategy["capabilities"]
                print(f"     Quality: {caps['quality_level']}")
                print(f"     Charts: {'✅' if caps['supports_charts'] else '❌'}")
                print(f"     Images: {'✅' if caps['supports_images'] else '❌'}")

    async def _demo_nutrition_calculations(self):
        """Demonstrate nutrition calculation strategies (when implemented)"""
        print("\n🥗 Nutrition Calculation Demo")
        print("-" * 40)
        print("🚧 Nutrition strategies implementation in progress...")

        # This would be implemented when nutrition strategies are complete
        # Example of what it would look like:
        """
        # Create sample client data
        personal_metrics = PersonalMetrics(
            age=28,
            gender=Gender.MALE,
            height_cm=180,
            weight_kg=75,
            body_fat_percentage=12.0
        )

        nutrition_context = NutritionContext(
            personal_metrics=personal_metrics,
            activity_level=ActivityLevel.ACTIVE,
            nutrition_goal=NutritionGoal.MUSCLE_GAIN,
            training_days_per_week=4
        )

        # Test different calculation methods
        strategies = ['harris_benedict', 'mifflin_st_jeor', 'katch_mcardle']

        for strategy in strategies:
            result = await self.nutrition_manager.calculate_nutrition(
                context=nutrition_context,
                preferred_strategy=strategy
            )

            print(f"📊 {strategy} Results:")
            print(f"  BMR: {result.bmr:.0f} cal")
            print(f"  TDEE: {result.tdee:.0f} cal")
            print(f"  Target: {result.target_calories:.0f} cal")
            print(f"  Protein: {result.macronutrient_targets.protein_g:.0f}g")
            print(f"  Carbs: {result.macronutrient_targets.carbohydrates_g:.0f}g")
            print(f"  Fat: {result.macronutrient_targets.fat_g:.0f}g")
        """


async def main():
    """Main demo function"""
    demo = EnterpriseStrategyDemo()
    await demo.run_complete_demo()


if __name__ == "__main__":
    asyncio.run(main())
