"""
Advanced PDF Service - Bridge between new PDF engine and existing CoachPro architecture
Integrates the new advanced PDF system with existing controllers and services
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from .pdf_engine import PDFEngine
from .pdf_engine.managers.style_manager import StyleManager
from .pdf_engine.core.professional_template_factory import ProfessionalTemplateFactory
from .pdf_template_service import PdfTemplateService


class AdvancedPdfService:
    """
    Advanced PDF service that bridges the new PDF engine with existing CoachPro architecture
    Provides backward compatibility while enabling new advanced features
    """

    def __init__(self):
        self.pdf_engine = PDFEngine(cache_enabled=True)
        self.style_manager = StyleManager()
        self.legacy_service = PdfTemplateService()

        # Initialize professional template factory
        self.professional_factory = ProfessionalTemplateFactory()

        # Replace the engine's template factory with our professional one
        self.pdf_engine.template_factory = self.professional_factory

        # Ensure default templates exist
        try:
            self.legacy_service.ensure_all_defaults_exist()
        except Exception:
            pass

    # ========== PROFESSIONAL PDF GENERATION ==========

    async def generate_professional_workout_pdf_async(
        self,
        workout_data: Dict[str, Any],
        output_path: str,
        template_style: str = "elite",  # elite, motivation, medical
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate professional workout PDF using new template system"""
        template_type = f"workout_{template_style}"
        template_config = {"variant": "default"}
        if style_overrides:
            template_config.update(style_overrides)

        # Create professional template with branding
        template = self.professional_factory.create_professional_template(
            template_type, workout_data, template_config, brand_config
        )

        return await self.pdf_engine.generate_async(
            template_type, workout_data, output_path, template_config, style_overrides
        )

    def generate_professional_workout_pdf_sync(
        self,
        workout_data: Dict[str, Any],
        output_path: str,
        template_style: str = "elite",
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Synchronous wrapper for professional workout PDF generation"""
        template_type = f"workout_{template_style}"
        template_config = {"variant": "default"}
        if style_overrides:
            template_config.update(style_overrides)

        try:
            result = self.pdf_engine.generate_sync(
                template_type, workout_data, output_path
            )
            # Ensure success field is present
            result["success"] = True
            return result
        except Exception as e:
            return {"success": False, "error": f"PDF generation failed: {str(e)}"}

    async def generate_professional_nutrition_pdf_async(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_style: str = "science",  # science, wellness, therapeutic
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate professional nutrition PDF using new template system"""
        template_type = f"nutrition_{template_style}"
        template_config = {"variant": "default"}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            template_type, nutrition_data, output_path, template_config, style_overrides
        )

    def generate_professional_nutrition_pdf_sync(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_style: str = "science",
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Synchronous wrapper for professional nutrition PDF generation"""
        template_type = f"nutrition_{template_style}"
        template_config = {"variant": "default"}
        if style_overrides:
            template_config.update(style_overrides)

        return self.pdf_engine.generate_sync(
            template_type, nutrition_data, output_path, template_config, style_overrides
        )

    # ========== NEW ADVANCED PDF GENERATION ==========

    async def generate_session_pdf_async(
        self,
        session_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "modern",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate session PDF using new advanced engine"""
        template_config = {"variant": template_variant}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            "session", session_data, output_path, template_config, style_overrides
        )

    async def generate_nutrition_pdf_async(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "detailed",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate nutrition PDF using new advanced engine"""
        template_config = {"variant": template_variant}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            "nutrition", nutrition_data, output_path, template_config, style_overrides
        )

    async def generate_program_pdf_async(
        self,
        program_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "weekly",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate program PDF using new advanced engine"""
        template_config = {"variant": template_variant, "layout": template_variant}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            "program", program_data, output_path, template_config, style_overrides
        )

    async def generate_meal_plan_pdf_async(
        self,
        meal_plan_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "detailed",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate meal plan PDF using new advanced engine"""
        template_config = {"variant": template_variant}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            "meal_plan", meal_plan_data, output_path, template_config, style_overrides
        )

    async def generate_progress_report_pdf_async(
        self,
        progress_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "comprehensive",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate progress report PDF using new advanced engine"""
        template_config = {"variant": template_variant}
        if style_overrides:
            template_config.update(style_overrides)

        return await self.pdf_engine.generate_async(
            "progress_report", progress_data, output_path, template_config, style_overrides
        )

    # ========== SYNCHRONOUS WRAPPERS ==========

    def generate_session_pdf_sync(
        self,
        session_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "modern",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Synchronous wrapper for session PDF generation"""
        return self.pdf_engine.generate_sync(
            "session", session_data, output_path,
            {"variant": template_variant}, style_overrides
        )

    def generate_nutrition_pdf_sync(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "detailed",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Synchronous wrapper for nutrition PDF generation"""
        return self.pdf_engine.generate_sync(
            "nutrition", nutrition_data, output_path,
            {"variant": template_variant}, style_overrides
        )

    def generate_program_pdf_sync(
        self,
        program_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "weekly",
        style_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Synchronous wrapper for program PDF generation"""
        return self.pdf_engine.generate_sync(
            "program", program_data, output_path,
            {"variant": template_variant, "layout": template_variant}, style_overrides
        )

    # ========== TEMPLATE PREVIEW AND MANAGEMENT ==========

    def generate_preview(
        self,
        template_type: str,
        sample_data: Dict[str, Any],
        template_config: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """Generate preview PDF for template editor"""
        preview_buffer = self.pdf_engine.generate_preview(
            template_type, sample_data, template_config, max_pages=2
        )
        return preview_buffer.getvalue()

    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get all available template types and variants"""
        return self.pdf_engine.get_available_templates()

    def get_professional_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about all professional templates"""
        return self.professional_factory.get_professional_templates()

    def get_template_themes(self) -> Dict[str, Any]:
        """Get available themes for templates"""
        return {
            "professional": self.style_manager.get_color_palette("professional"),
            "vibrant": self.style_manager.get_color_palette("vibrant"),
            "monochrome": self.style_manager.get_color_palette("monochrome"),
            "fitness": self.style_manager.get_color_palette("fitness"),
        }

    def create_custom_theme(
        self,
        theme_name: str,
        color_palette: str,
        font_family: str,
        layout_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create custom theme for templates"""
        return self.style_manager.create_custom_theme(
            theme_name, color_palette, font_family, layout_options
        )

    # ========== BATCH OPERATIONS ==========

    def batch_generate_pdfs(
        self, jobs: List[Dict[str, Any]], output_dir: str
    ) -> List[Dict[str, Any]]:
        """Batch generate multiple PDFs"""
        return self.pdf_engine.batch_generate(jobs, output_dir)

    # ========== PERFORMANCE MONITORING ==========

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get PDF generation performance statistics"""
        return self.pdf_engine.get_performance_stats()

    def clear_cache(self) -> None:
        """Clear PDF generation cache"""
        self.pdf_engine.clear_cache()

    # ========== BACKWARD COMPATIBILITY ==========

    def get_legacy_session_style(self, template_id: Optional[int] = None) -> Dict[str, Any]:
        """Get session style using legacy service (backward compatibility)"""
        return self.legacy_service.get_style("session", template_id)

    def list_legacy_templates(self, template_type: str) -> List[Dict[str, Any]]:
        """List templates using legacy service (backward compatibility)"""
        return self.legacy_service.list_templates(template_type)

    def save_legacy_template(
        self,
        template_type: str,
        name: str,
        style: Dict[str, Any],
        template_id: Optional[int] = None,
        set_default: bool = False,
    ) -> int:
        """Save template using legacy service (backward compatibility)"""
        return self.legacy_service.save_template(
            template_type, name, style, template_id, set_default
        )

    # ========== SAMPLE DATA GENERATION ==========

    def get_sample_data(self, template_type: str) -> Dict[str, Any]:
        """Get sample data for template preview"""
        sample_data = {
            "session": {
                "title": "Séance HIIT Cardio",
                "client_name": "Marie Dupont",
                "date": "2025-01-20",
                "duration": 45,
                "type": "Individuel",
                "blocks": [
                    {
                        "title": "Échauffement",
                        "format": "LIBRE",
                        "duration": 10,
                        "exercises": [
                            {"name": "Marche rapide", "reps": "5 min", "notes": "Intensité progressive"},
                            {"name": "Mobilisations articulaires", "reps": "10x", "notes": "Épaules, hanches"},
                        ]
                    },
                    {
                        "title": "Corps principal",
                        "format": "TABATA",
                        "duration": 20,
                        "exercises": [
                            {"name": "Burpees", "reps": "Maximum", "notes": "Technique parfaite"},
                            {"name": "Mountain Climbers", "reps": "Maximum", "notes": "Gainage serré"},
                            {"name": "Jump Squats", "reps": "Maximum", "notes": "Réception souple"},
                        ]
                    }
                ],
                "notes": "Hydratation régulière. Adapter l'intensité selon la forme du jour."
            },
            "nutrition": {
                "title": "Bilan Nutritionnel",
                "client_name": "Pierre Martin",
                "date": "2025-01-20",
                "personal_info": {
                    "age": 35,
                    "weight": 78.5,
                    "height": 175,
                    "gender": "Homme",
                    "activity_level": "Modéré",
                    "goal": "Perte de poids"
                },
                "nutrition_data": {
                    "maintenance_calories": 2200,
                    "target_calories": 1800,
                    "protein_g": 140,
                    "carbs_g": 180,
                    "fat_g": 60
                },
                "recommendations": [
                    "Privilégier les légumes à chaque repas",
                    "Hydratation : 2.5L d'eau par jour",
                    "Collations riches en protéines"
                ]
            },
            "program": {
                "title": "Programme Force 4 semaines",
                "client_name": "Sophie Leblanc",
                "duration_weeks": 4,
                "goal": "Développement de la force",
                "weeks": [
                    {
                        "week_number": 1,
                        "focus": "Adaptation",
                        "days": [
                            {
                                "day": "Lundi",
                                "type": "Force Haut",
                                "exercises": [
                                    {"name": "Développé couché", "sets": "4", "reps": "8-10", "weight": "70kg", "rest": "2min"},
                                    {"name": "Tractions", "sets": "3", "reps": "6-8", "rest": "2min"},
                                    {"name": "Dips", "sets": "3", "reps": "10-12", "rest": "90s"},
                                ]
                            },
                            {
                                "day": "Mardi",
                                "type": "Repos",
                                "exercises": []
                            }
                        ]
                    }
                ]
            },
            "meal_plan": {
                "title": "Plan Alimentaire Semaine",
                "client_name": "Antoine Rousseau",
                "week_start_date": "2025-01-20",
                "daily_meals": [
                    {
                        "day": "Lundi",
                        "date": "20/01/2025",
                        "meals": [
                            {
                                "type": "Petit-déjeuner",
                                "time": "7h30",
                                "name": "Bowl protéiné",
                                "ingredients": ["Avoine", "Protéines", "Banane", "Amandes"],
                                "calories": 420,
                                "macros": {"protein": 25, "carbs": 35, "fat": 15}
                            },
                            {
                                "type": "Déjeuner",
                                "time": "12h30",
                                "name": "Poulet grillé quinoa",
                                "ingredients": ["Blanc de poulet", "Quinoa", "Légumes verts"],
                                "calories": 580,
                                "macros": {"protein": 45, "carbs": 50, "fat": 12}
                            }
                        ]
                    }
                ],
                "shopping_list": [
                    {
                        "category": "Protéines",
                        "items": ["Blanc de poulet", "Œufs", "Thon"]
                    }
                ]
            },
            "progress_report": {
                "title": "Rapport de Progression - 3 Mois",
                "client_name": "Isabelle Moreau",
                "report_period": "Octobre - Décembre 2024",
                "summary": {
                    "total_sessions": 36,
                    "weight_change": -4.2,
                    "body_fat_change": -3.1,
                    "achievements": ["Objectif poids atteint", "Force développée", "Endurance améliorée"]
                },
                "measurements": [
                    {
                        "date": "2024-10-01",
                        "weight": 68.5,
                        "body_fat": 28.2,
                        "muscle_mass": 25.1,
                        "measurements": {"chest": 92, "waist": 76, "hips": 98}
                    },
                    {
                        "date": "2025-01-01",
                        "weight": 64.3,
                        "body_fat": 25.1,
                        "muscle_mass": 26.8,
                        "measurements": {"chest": 90, "waist": 71, "hips": 94}
                    }
                ]
            }
        }

        return sample_data.get(template_type, {})

    # ========== UTILITY METHODS ==========

    def validate_template_data(self, template_type: str, data: Dict[str, Any]) -> List[str]:
        """Validate data structure against template schema"""
        try:
            schema = self.pdf_engine.template_factory.get_template_schema(template_type)
            # Add validation logic here if needed
            return []
        except Exception as e:
            return [str(e)]

    def get_template_info(self, template_type: str) -> Dict[str, Any]:
        """Get information about a template type"""
        try:
            schema = self.pdf_engine.template_factory.get_template_schema(template_type)
            variants = self.pdf_engine.get_available_templates().get(template_type, [])

            return {
                "type": template_type,
                "variants": variants,
                "schema": schema,
                "sample_data": self.get_sample_data(template_type)
            }
        except Exception as e:
            return {"error": str(e)}