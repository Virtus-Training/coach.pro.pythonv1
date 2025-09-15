"""
Style Manager - Centralized styling system for PDF templates
Handles themes, color palettes, fonts, and brand customization
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class StyleManager:
    """
    Centralized style management for consistent PDF appearance
    Supports theme switching and brand customization
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else self._get_default_config_path()
        self.themes = self._load_themes()
        self.brand_settings = self._load_brand_settings()

    def get_theme(self, theme_name: str = "default") -> Dict[str, Any]:
        """Get theme configuration"""
        return self.themes.get(theme_name, self.themes["default"])

    def get_color_palette(self, palette_name: str = "professional") -> Dict[str, str]:
        """Get color palette for consistent styling"""
        palettes = {
            "professional": {
                "primary": "#2563EB",
                "secondary": "#7C3AED",
                "accent": "#059669",
                "background": "#FFFFFF",
                "surface": "#F8FAFC",
                "text_primary": "#1F2937",
                "text_secondary": "#6B7280",
                "border": "#E5E7EB",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
            },
            "vibrant": {
                "primary": "#FF6B35",
                "secondary": "#F7931E",
                "accent": "#2E86AB",
                "background": "#FFFFFF",
                "surface": "#FFF8F5",
                "text_primary": "#2C3E50",
                "text_secondary": "#7F8C8D",
                "border": "#E8E8E8",
                "success": "#27AE60",
                "warning": "#F39C12",
                "error": "#E74C3C",
            },
            "monochrome": {
                "primary": "#000000",
                "secondary": "#4A4A4A",
                "accent": "#808080",
                "background": "#FFFFFF",
                "surface": "#F5F5F5",
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "border": "#CCCCCC",
                "success": "#666666",
                "warning": "#666666",
                "error": "#000000",
            },
            "fitness": {
                "primary": "#FF4500",
                "secondary": "#FF6347",
                "accent": "#32CD32",
                "background": "#FFFFFF",
                "surface": "#FFF5EE",
                "text_primary": "#2F4F4F",
                "text_secondary": "#708090",
                "border": "#DCDCDC",
                "success": "#228B22",
                "warning": "#FF8C00",
                "error": "#DC143C",
            },
        }
        return palettes.get(palette_name, palettes["professional"])

    def get_font_family(self, family_name: str = "modern") -> Dict[str, Dict[str, Any]]:
        """Get font family configuration"""
        families = {
            "modern": {
                "title": {"name": "Helvetica-Bold", "size": 24, "weight": "bold"},
                "subtitle": {"name": "Helvetica-Bold", "size": 18, "weight": "bold"},
                "heading": {"name": "Helvetica-Bold", "size": 14, "weight": "bold"},
                "subheading": {"name": "Helvetica", "size": 12, "weight": "normal"},
                "body": {"name": "Helvetica", "size": 10, "weight": "normal"},
                "caption": {"name": "Helvetica", "size": 8, "weight": "normal"},
                "code": {"name": "Courier", "size": 9, "weight": "normal"},
            },
            "classic": {
                "title": {"name": "Times-Bold", "size": 22, "weight": "bold"},
                "subtitle": {"name": "Times-Bold", "size": 16, "weight": "bold"},
                "heading": {"name": "Times-Bold", "size": 13, "weight": "bold"},
                "subheading": {"name": "Times-Roman", "size": 11, "weight": "normal"},
                "body": {"name": "Times-Roman", "size": 10, "weight": "normal"},
                "caption": {"name": "Times-Italic", "size": 8, "weight": "normal"},
                "code": {"name": "Courier", "size": 9, "weight": "normal"},
            },
            "sans": {
                "title": {"name": "Helvetica-Bold", "size": 26, "weight": "bold"},
                "subtitle": {"name": "Helvetica-Bold", "size": 20, "weight": "bold"},
                "heading": {"name": "Helvetica-Bold", "size": 15, "weight": "bold"},
                "subheading": {"name": "Helvetica", "size": 13, "weight": "normal"},
                "body": {"name": "Helvetica", "size": 11, "weight": "normal"},
                "caption": {"name": "Helvetica", "size": 9, "weight": "normal"},
                "code": {"name": "Courier", "size": 9, "weight": "normal"},
            },
        }
        return families.get(family_name, families["modern"])

    def create_custom_theme(
        self,
        theme_name: str,
        color_palette: str,
        font_family: str,
        layout_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create custom theme from components"""
        colors = self.get_color_palette(color_palette)
        fonts = self.get_font_family(font_family)

        layout = layout_options or self._get_default_layout()

        custom_theme = {
            "name": theme_name,
            "colors": colors,
            "fonts": fonts,
            "layout": layout,
            "created_at": str(time.time()),
        }

        # Save to themes
        self.themes[theme_name] = custom_theme
        self._save_themes()

        return custom_theme

    def apply_brand_customization(
        self, theme: Dict[str, Any], brand_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply brand-specific customizations to theme"""
        customized = theme.copy()

        # Override colors with brand colors
        if "colors" in brand_config:
            customized["colors"].update(brand_config["colors"])

        # Override fonts with brand fonts
        if "fonts" in brand_config:
            customized["fonts"].update(brand_config["fonts"])

        # Add brand assets
        if "logo" in brand_config:
            customized["brand"] = {
                "logo_path": brand_config["logo"],
                "logo_width": brand_config.get("logo_width", 70),
                "show_logo": brand_config.get("show_logo", True),
            }

        # Add brand text
        if "brand_name" in brand_config:
            customized["brand"] = customized.get("brand", {})
            customized["brand"]["name"] = brand_config["brand_name"]
            customized["brand"]["tagline"] = brand_config.get("tagline", "")

        return customized

    def get_template_styles(
        self, template_type: str, theme_name: str = "default"
    ) -> Dict[str, Any]:
        """Get optimized styles for specific template type"""
        theme = self.get_theme(theme_name)

        # Template-specific style optimizations
        if template_type == "session":
            return self._get_session_styles(theme)
        elif template_type == "nutrition":
            return self._get_nutrition_styles(theme)
        elif template_type == "program":
            return self._get_program_styles(theme)
        elif template_type == "meal_plan":
            return self._get_meal_plan_styles(theme)
        elif template_type == "progress_report":
            return self._get_progress_styles(theme)

        return theme

    def validate_theme(self, theme: Dict[str, Any]) -> List[str]:
        """Validate theme configuration and return errors"""
        errors = []
        required_keys = ["colors", "fonts", "layout"]

        for key in required_keys:
            if key not in theme:
                errors.append(f"Missing required key: {key}")

        # Validate colors
        if "colors" in theme:
            required_colors = ["primary", "background", "text_primary"]
            for color in required_colors:
                if color not in theme["colors"]:
                    errors.append(f"Missing required color: {color}")

        return errors

    def _load_themes(self) -> Dict[str, Any]:
        """Load themes from configuration file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        return self._get_default_themes()

    def _save_themes(self) -> None:
        """Save themes to configuration file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.themes, f, indent=2)

    def _load_brand_settings(self) -> Dict[str, Any]:
        """Load brand settings"""
        brand_path = self.config_path.parent / "brand_settings.json"
        if brand_path.exists():
            try:
                with open(brand_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _get_default_config_path(self) -> Path:
        """Get default configuration path"""
        return Path(__file__).parent.parent.parent.parent / "data" / "config" / "pdf_themes.json"

    def _get_default_themes(self) -> Dict[str, Any]:
        """Get default theme configurations"""
        return {
            "default": {
                "name": "Default",
                "colors": self.get_color_palette("professional"),
                "fonts": self.get_font_family("modern"),
                "layout": self._get_default_layout(),
            },
            "fitness": {
                "name": "Fitness",
                "colors": self.get_color_palette("fitness"),
                "fonts": self.get_font_family("sans"),
                "layout": self._get_default_layout(),
            },
            "minimal": {
                "name": "Minimal",
                "colors": self.get_color_palette("monochrome"),
                "fonts": self.get_font_family("classic"),
                "layout": self._get_default_layout(),
            },
        }

    def _get_default_layout(self) -> Dict[str, Any]:
        """Get default layout configuration"""
        return {
            "margins": {"top": 60, "bottom": 60, "left": 50, "right": 50},
            "header_height": 80,
            "footer_height": 40,
            "block_spacing": 20,
            "line_spacing": 1.2,
            "paragraph_spacing": 6,
        }

    def _get_session_styles(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimized styles for session templates"""
        styles = theme.copy()
        # Session-specific optimizations
        styles["table_styles"] = {
            "header_bg": theme["colors"]["primary"],
            "row_odd_bg": theme["colors"]["surface"],
            "row_even_bg": theme["colors"]["background"],
            "border_color": theme["colors"]["border"],
        }
        return styles

    def _get_nutrition_styles(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimized styles for nutrition templates"""
        styles = theme.copy()
        # Nutrition-specific colors for macros
        styles["macro_colors"] = {
            "protein": "#3C91E6",
            "carbs": "#FFAD05",
            "fat": "#E4572E",
        }
        return styles

    def _get_program_styles(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimized styles for program templates"""
        styles = theme.copy()
        # Program-specific styling
        styles["progression_colors"] = {
            "increase": theme["colors"]["success"],
            "maintain": theme["colors"]["accent"],
            "decrease": theme["colors"]["warning"],
        }
        return styles

    def _get_meal_plan_styles(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimized styles for meal plan templates"""
        styles = theme.copy()
        # Meal-specific colors
        styles["meal_colors"] = {
            "breakfast": "#FF6B35",
            "lunch": "#2E86AB",
            "dinner": "#7C3AED",
            "snack": "#10B981",
        }
        return styles

    def _get_progress_styles(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimized styles for progress report templates"""
        styles = theme.copy()
        # Progress-specific colors
        styles["progress_colors"] = {
            "improvement": theme["colors"]["success"],
            "regression": theme["colors"]["error"],
            "stable": theme["colors"]["accent"],
        }
        return styles