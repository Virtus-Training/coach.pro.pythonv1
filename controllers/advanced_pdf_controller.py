"""
Advanced PDF Controller - Enhanced PDF generation with new template system
Integrates advanced PDF engine with CoachPro UI
"""

from __future__ import annotations

import asyncio
import json
import tempfile
from typing import Any, Dict, List, Optional

from services.advanced_pdf_service import AdvancedPdfService


class AdvancedPdfController:
    """
    Advanced PDF controller with new template system
    Provides both synchronous and asynchronous PDF generation
    """

    def __init__(self, service: Optional[AdvancedPdfService] = None):
        self.service = service or AdvancedPdfService()

    # ========== PROFESSIONAL PDF GENERATION ==========

    def generate_professional_workout_pdf(
        self,
        workout_data: Dict[str, Any],
        output_path: str,
        template_style: str = "elite",  # elite, motivation, medical
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate professional workout PDF with commercial-grade templates"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_professional_workout_pdf_async(
                        workout_data,
                        output_path,
                        template_style,
                        brand_config,
                        style_overrides,
                    )
                )
            else:
                return self.service.generate_professional_workout_pdf_sync(
                    workout_data,
                    output_path,
                    template_style,
                    brand_config,
                    style_overrides,
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_professional_nutrition_pdf(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_style: str = "science",  # science, wellness, therapeutic
        brand_config: Optional[Dict[str, Any]] = None,
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate professional nutrition PDF with commercial-grade templates"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_professional_nutrition_pdf_async(
                        nutrition_data,
                        output_path,
                        template_style,
                        brand_config,
                        style_overrides,
                    )
                )
            else:
                return self.service.generate_professional_nutrition_pdf_sync(
                    nutrition_data,
                    output_path,
                    template_style,
                    brand_config,
                    style_overrides,
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_professional_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about all professional templates"""
        return self.service.get_professional_templates()

    # ========== NEW ADVANCED PDF GENERATION ==========

    def generate_session_pdf(
        self,
        session_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "modern",
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate session PDF with advanced template system"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_session_pdf_async(
                        session_data, output_path, template_variant, style_overrides
                    )
                )
            else:
                return self.service.generate_session_pdf_sync(
                    session_data, output_path, template_variant, style_overrides
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_nutrition_pdf(
        self,
        nutrition_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "detailed",
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate nutrition PDF with advanced template system"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_nutrition_pdf_async(
                        nutrition_data, output_path, template_variant, style_overrides
                    )
                )
            else:
                return self.service.generate_nutrition_pdf_sync(
                    nutrition_data, output_path, template_variant, style_overrides
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_program_pdf(
        self,
        program_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "weekly",
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate program PDF with advanced template system"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_program_pdf_async(
                        program_data, output_path, template_variant, style_overrides
                    )
                )
            else:
                return self.service.generate_program_pdf_sync(
                    program_data, output_path, template_variant, style_overrides
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_meal_plan_pdf(
        self,
        meal_plan_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "detailed",
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate meal plan PDF with advanced template system"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_meal_plan_pdf_async(
                        meal_plan_data, output_path, template_variant, style_overrides
                    )
                )
            else:
                return self.service.generate_meal_plan_pdf_sync(
                    meal_plan_data, output_path, template_variant, style_overrides
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_progress_report_pdf(
        self,
        progress_data: Dict[str, Any],
        output_path: str,
        template_variant: str = "comprehensive",
        style_overrides: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """Generate progress report PDF with advanced template system"""
        try:
            if async_mode:
                return asyncio.run(
                    self.service.generate_progress_report_pdf_async(
                        progress_data, output_path, template_variant, style_overrides
                    )
                )
            else:
                return self.service.generate_progress_report_pdf_sync(
                    progress_data, output_path, template_variant, style_overrides
                )
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== TEMPLATE MANAGEMENT ==========

    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get all available template types and variants"""
        return self.service.get_available_templates()

    def get_template_themes(self) -> Dict[str, Any]:
        """Get available themes for templates"""
        return self.service.get_template_themes()

    def create_custom_theme(
        self,
        theme_name: str,
        color_palette: str,
        font_family: str,
        layout_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create custom theme for templates"""
        try:
            theme = self.service.create_custom_theme(
                theme_name, color_palette, font_family, layout_options
            )
            return {"success": True, "theme": theme}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== TEMPLATE PREVIEW ==========

    def generate_preview(
        self,
        template_type: str,
        template_config: Optional[Dict[str, Any]] = None,
        use_sample_data: bool = True,
        custom_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate preview PDF for template editor"""
        try:
            # Use sample data or custom data
            if use_sample_data:
                sample_data = self.service.get_sample_data(template_type)
            else:
                sample_data = custom_data or {}

            # Generate preview in temporary file
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_path = temp_file.name

            preview_bytes = self.service.generate_preview(
                template_type, sample_data, template_config
            )

            # Save preview to temporary file
            with open(temp_path, "wb") as f:
                f.write(preview_bytes)

            return {
                "success": True,
                "preview_path": temp_path,
                "preview_size": len(preview_bytes),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_template_info(self, template_type: str) -> Dict[str, Any]:
        """Get comprehensive information about a template type"""
        return self.service.get_template_info(template_type)

    # ========== BATCH OPERATIONS ==========

    def batch_generate_pdfs(
        self,
        jobs: List[Dict[str, Any]],
        output_dir: str,
        progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Batch generate multiple PDFs with progress tracking

        Jobs format:
        [
            {
                "template_type": "session",
                "data": {...},
                "filename": "session_1",
                "template_config": {...},
                "style_overrides": {...}
            }
        ]
        """
        try:
            results = self.service.batch_generate_pdfs(jobs, output_dir)

            # Calculate success rate
            successful = sum(1 for r in results if r.get("success", False))
            total = len(results)

            return {
                "success": True,
                "total_jobs": total,
                "successful": successful,
                "failed": total - successful,
                "results": results,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== PERFORMANCE MONITORING ==========

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get PDF generation performance statistics"""
        return self.service.get_performance_stats()

    def clear_cache(self) -> Dict[str, Any]:
        """Clear PDF generation cache"""
        try:
            self.service.clear_cache()
            return {"success": True, "message": "Cache cleared successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== DATA VALIDATION ==========

    def validate_template_data(
        self, template_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate data structure against template schema"""
        errors = self.service.validate_template_data(template_type, data)
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

    # ========== UI INTEGRATION HELPERS ==========

    def get_ui_config(self, template_type: str) -> Dict[str, Any]:
        """Get UI configuration for template editor"""
        try:
            template_info = self.get_template_info(template_type)
            themes = self.get_template_themes()

            return {
                "template_info": template_info,
                "available_themes": themes,
                "color_palettes": {
                    "professional": "Professionnel",
                    "vibrant": "Dynamique",
                    "monochrome": "Monochrome",
                    "fitness": "Fitness",
                },
                "font_families": {
                    "modern": "Moderne",
                    "classic": "Classique",
                    "sans": "Sans-serif",
                },
                "template_variants": template_info.get("variants", []),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def export_template_config(self, template_config: Dict[str, Any]) -> str:
        """Export template configuration as JSON string"""
        try:
            return json.dumps(template_config, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def import_template_config(self, config_json: str) -> Dict[str, Any]:
        """Import template configuration from JSON string"""
        try:
            config = json.loads(config_json)
            return {"success": True, "config": config}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== BACKWARD COMPATIBILITY ==========

    def get_legacy_session_style(
        self, template_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get session style using legacy service (backward compatibility)"""
        return self.service.get_legacy_session_style(template_id)

    def list_legacy_templates(self, template_type: str) -> List[Dict[str, Any]]:
        """List templates using legacy service (backward compatibility)"""
        return self.service.list_legacy_templates(template_type)

    def save_legacy_template(
        self,
        template_type: str,
        name: str,
        style_json: str,
        template_id: Optional[int] = None,
        set_default: bool = False,
    ) -> Dict[str, Any]:
        """Save template using legacy service (backward compatibility)"""
        try:
            style = json.loads(style_json)
            template_id = self.service.save_legacy_template(
                template_type, name, style, template_id, set_default
            )
            return {"success": True, "template_id": template_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== QUICK PDF GENERATION SHORTCUTS ==========

    def quick_session_pdf(
        self, session_data: Dict[str, Any], output_path: str
    ) -> Dict[str, Any]:
        """Quick session PDF with default modern template"""
        return self.generate_session_pdf(session_data, output_path, "modern")

    def quick_nutrition_pdf(
        self, nutrition_data: Dict[str, Any], output_path: str
    ) -> Dict[str, Any]:
        """Quick nutrition PDF with default detailed template"""
        return self.generate_nutrition_pdf(nutrition_data, output_path, "detailed")

    def quick_program_pdf(
        self, program_data: Dict[str, Any], output_path: str
    ) -> Dict[str, Any]:
        """Quick program PDF with default weekly template"""
        return self.generate_program_pdf(program_data, output_path, "weekly")

    # ========== ERROR HANDLING ==========

    def handle_pdf_error(self, error: Exception, context: str) -> Dict[str, Any]:
        """Centralized error handling for PDF operations"""
        error_message = f"PDF {context} failed: {str(error)}"

        return {
            "success": False,
            "error": error_message,
            "context": context,
            "error_type": type(error).__name__,
        }
