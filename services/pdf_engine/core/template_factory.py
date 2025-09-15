"""
Template Factory - Creates PDF templates based on type and configuration
Supports dynamic loading and extensibility
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from ..templates.base_template import BaseTemplate
from ..templates.nutrition_template import NutritionTemplate
from ..templates.program_template import ProgramTemplate
from ..templates.session_template import SessionTemplate
from ..templates.meal_plan_template import MealPlanTemplate
from ..templates.progress_report_template import ProgressReportTemplate


class TemplateFactory:
    """
    Factory for creating PDF template instances
    Supports registration of custom templates for extensibility
    """

    def __init__(self):
        self._template_registry = {
            "session": SessionTemplate,
            "nutrition": NutritionTemplate,
            "program": ProgramTemplate,
            "meal_plan": MealPlanTemplate,
            "progress_report": ProgressReportTemplate,
        }
        self._template_variants = self._load_template_variants()

    def create_template(
        self,
        template_type: str,
        data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> BaseTemplate:
        """
        Create template instance based on type and configuration
        """
        if template_type not in self._template_registry:
            raise ValueError(f"Unknown template type: {template_type}")

        template_class = self._template_registry[template_type]

        # Load specific variant if requested
        variant_config = self._get_variant_config(template_type, config)

        return template_class(data, variant_config)

    def register_template(
        self, template_type: str, template_class: Type[BaseTemplate]
    ) -> None:
        """Register custom template class"""
        if not issubclass(template_class, BaseTemplate):
            raise ValueError("Template class must inherit from BaseTemplate")

        self._template_registry[template_type] = template_class

    def get_available_templates(self) -> Dict[str, List[str]]:
        """Return available template types and their variants"""
        result = {}
        for template_type in self._template_registry.keys():
            variants = list(self._template_variants.get(template_type, {}).keys())
            if not variants:
                variants = ["default"]
            result[template_type] = variants
        return result

    def get_template_schema(self, template_type: str) -> Dict[str, Any]:
        """Get data schema requirements for a template type"""
        if template_type not in self._template_registry:
            raise ValueError(f"Unknown template type: {template_type}")

        template_class = self._template_registry[template_type]
        if hasattr(template_class, 'get_data_schema'):
            return template_class.get_data_schema()

        return {"type": "object", "properties": {}}

    def _load_template_variants(self) -> Dict[str, Dict[str, Any]]:
        """Load template variants from configuration files"""
        variants = {
            "session": {
                "modern": {"style": "modern", "colors": "vibrant"},
                "classic": {"style": "classic", "colors": "professional"},
                "minimal": {"style": "minimal", "colors": "monochrome"},
            },
            "nutrition": {
                "detailed": {"show_macros": True, "show_timeline": True},
                "summary": {"show_macros": True, "show_timeline": False},
                "simple": {"show_macros": False, "show_timeline": False},
            },
            "program": {
                "weekly": {"layout": "weekly", "show_progression": True},
                "daily": {"layout": "daily", "show_progression": False},
                "compact": {"layout": "compact", "show_progression": True},
            },
            "meal_plan": {
                "detailed": {"show_recipes": True, "show_shopping_list": True},
                "overview": {"show_recipes": False, "show_shopping_list": True},
                "simple": {"show_recipes": False, "show_shopping_list": False},
            },
            "progress_report": {
                "comprehensive": {"show_charts": True, "show_photos": True, "show_measurements": True},
                "visual": {"show_charts": True, "show_photos": True, "show_measurements": False},
                "data": {"show_charts": True, "show_photos": False, "show_measurements": True},
            }
        }
        return variants

    def _get_variant_config(
        self, template_type: str, config: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get configuration for specific template variant"""
        # Return user config as-is since templates have their own defaults
        # Variants just override specific settings, not full configuration
        if not config:
            return {}

        variant = config.get("variant")
        if variant and variant in self._template_variants.get(template_type, {}):
            variant_config = self._template_variants[template_type][variant]
            # Merge variant config with user config
            merged_config = {**variant_config, **config}
            return merged_config

        return config