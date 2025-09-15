"""
Professional Template Factory - Advanced template system rivaling industry leaders
Creates 12 professional-grade templates with commercial design quality
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .template_factory import TemplateFactory
from ..templates.base_template import BaseTemplate

# Professional Templates - All 12 templates implemented
from ..templates.professional.workout_elite_template import WorkoutEliteTemplate
from ..templates.professional.workout_motivation_template import WorkoutMotivationTemplate
from ..templates.professional.workout_medical_template import WorkoutMedicalTemplate
from ..templates.professional.nutrition_science_template import NutritionScienceTemplate
from ..templates.professional.nutrition_wellness_template import NutritionWellnessTemplate
from ..templates.professional.nutrition_therapeutic_template import NutritionTherapeuticTemplate
from ..templates.professional.nutrition_sheet_education_template import NutritionSheetEducationTemplate
from ..templates.professional.nutrition_sheet_quickref_template import NutritionSheetQuickRefTemplate
from ..templates.professional.nutrition_sheet_scientific_template import NutritionSheetScientificTemplate
from ..templates.professional.session_premium_template import SessionPremiumTemplate
from ..templates.professional.session_group_template import SessionGroupTemplate
from ..templates.professional.session_home_template import SessionHomeTemplate


class ProfessionalTemplateFactory(TemplateFactory):
    """
    Professional-grade template factory with 12 commercial templates
    Designed to rival Trainerize, MyFitnessPal Premium, and top coaching platforms
    """

    def __init__(self):
        super().__init__()

        # Professional Template Registry - All 12 Templates Implemented
        self._professional_registry = {
            # WORKOUT PROGRAMS (3 Templates)
            "workout_elite": WorkoutEliteTemplate,        # Elite Performance - Premium minimalist
            "workout_motivation": WorkoutMotivationTemplate, # Motivation+ - Energetic gamified
            "workout_medical": WorkoutMedicalTemplate,    # Medical Pro - Clinical scientific

            # NUTRITION PLANS (3 Templates)
            "nutrition_science": NutritionScienceTemplate,     # Data-driven precision
            "nutrition_wellness": NutritionWellnessTemplate,   # Lifestyle wellness
            "nutrition_therapeutic": NutritionTherapeuticTemplate, # Medical compliance

            # NUTRITION SHEETS (3 Templates)
            "nutrition_sheet_education": NutritionSheetEducationTemplate,   # Educational focus
            "nutrition_sheet_quickref": NutritionSheetQuickRefTemplate,     # Quick reference
            "nutrition_sheet_scientific": NutritionSheetScientificTemplate, # Scientific report

            # SINGLE SESSIONS (3 Templates)
            "session_premium": SessionPremiumTemplate,   # Premium luxury
            "session_group": SessionGroupTemplate,       # Group energy
            "session_home": SessionHomeTemplate,         # Home efficient
        }

        # Merge with existing registry
        self._template_registry.update(self._professional_registry)

        # Load professional variants
        self._professional_variants = self._load_professional_variants()
        self._template_variants.update(self._professional_variants)

        # Load brand standards
        self._brand_standards = self._load_brand_standards()

        # Performance tracking
        self._template_usage = {}

    def create_template(
        self,
        template_type: str,
        data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> BaseTemplate:
        """
        Override parent create_template to use professional templates
        """
        if template_type in self._professional_registry:
            return self.create_professional_template(template_type, data, config)
        else:
            # Fallback to parent implementation for standard templates
            return super().create_template(template_type, data, config)

    def create_professional_template(
        self,
        template_type: str,
        data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
        brand_config: Optional[Dict[str, Any]] = None
    ) -> BaseTemplate:
        """
        Create professional template with brand customization
        Supports white-label branding for coaches
        """
        if template_type not in self._professional_registry:
            # Fallback to standard templates
            return super().create_template(template_type, data, config)

        # Track usage analytics
        self._track_template_usage(template_type)

        # Apply brand configuration
        if brand_config:
            config = self._apply_brand_config(config or {}, brand_config)

        template_class = self._professional_registry[template_type]
        variant_config = self._get_professional_variant_config(template_type, config)

        return template_class(data, variant_config)

    def get_professional_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about all professional templates"""
        return {
            "workout_programs": {
                "elite": {
                    "name": "Elite Performance",
                    "description": "Premium minimalist design for high-end coaching",
                    "target": "Coachs haut de gamme, athlètes avancés",
                    "features": ["Graphiques progression", "Zones anatomiques", "QR codes vidéos"],
                    "style": "Premium, minimaliste, focus données"
                },
                "motivation": {
                    "name": "Motivation+",
                    "description": "Énergique et gamifié pour engagement maximal",
                    "target": "Fitness grand public, débutants, groupe classes",
                    "features": ["Citations motivantes", "Challenges", "Badges réussite"],
                    "style": "Énergique, coloré, gamification"
                },
                "medical": {
                    "name": "Medical Pro",
                    "description": "Format médical pour rééducation et coaching thérapeutique",
                    "target": "Kinésithérapie, rééducation, coaching thérapeutique",
                    "features": ["Contre-indications", "Adaptations", "Suivi médical"],
                    "style": "Médical, épuré, scientifique"
                }
            },
            "nutrition_plans": {
                "science": {
                    "name": "Nutrition Science",
                    "description": "Data-driven avec graphiques avancés et précision",
                    "target": "Nutritionnistes, bodybuilders, athlètes performance",
                    "features": ["Camemberts", "Histogrammes", "Tableaux nutritionnels"],
                    "style": "Data-driven, graphiques avancés, précision"
                },
                "wellness": {
                    "name": "Lifestyle Wellness",
                    "description": "Lifestyle photographique et inspirant",
                    "target": "Coaching wellness, perte de poids, grand public",
                    "features": ["Photos HD repas", "Lifestyle tips", "Planification hebdo"],
                    "style": "Lifestyle, photographique, inspirant"
                },
                "therapeutic": {
                    "name": "Therapeutic Diet",
                    "description": "Format médical avec compliance et traçabilité",
                    "target": "Diététiciens, pathologies, régimes stricts",
                    "features": ["Alertes allergènes", "Substitutions", "Monitoring"],
                    "style": "Médical, compliance, traçabilité"
                }
            },
            "nutrition_sheets": {
                "education": {
                    "name": "Education Focus",
                    "description": "Pédagogique avec infographies accessibles",
                    "target": "Éducation nutritionnelle, prévention, sensibilisation",
                    "features": ["Schémas", "Comparaisons", "Tips pratiques"],
                    "style": "Pédagogique, infographique, accessible"
                },
                "quickref": {
                    "name": "Quick Reference",
                    "description": "Concis et actionnable pour usage rapide",
                    "target": "Aide-mémoires, consultations rapides",
                    "features": ["Actions concrètes", "Rappels", "Résumés"],
                    "style": "Concis, actionnable, mémorable"
                },
                "scientific": {
                    "name": "Scientific Report",
                    "description": "Format académique avec evidence-based",
                    "target": "Professionnels santé, recherche, formation",
                    "features": ["Bibliographie", "Études", "Analyses approfondies"],
                    "style": "Académique, détaillé, evidence-based"
                }
            },
            "single_sessions": {
                "premium": {
                    "name": "Workout Premium",
                    "description": "Luxe personnalisé pour personal training haut de gamme",
                    "target": "Personal training haut de gamme, séances privées",
                    "features": ["Coaching notes", "Adaptations temps réel"],
                    "style": "Luxe, personnalisé, détaillé"
                },
                "group": {
                    "name": "Group Energy",
                    "description": "Dynamique pour cours collectifs et team training",
                    "target": "Cours collectifs, team training, événements",
                    "features": ["Playlist", "Variations niveaux", "Team building"],
                    "style": "Dynamique, collectif, motivant"
                },
                "home": {
                    "name": "Home Efficient",
                    "description": "Pratique pour home training avec équipement minimal",
                    "target": "Home training, confinements, déplacements",
                    "features": ["Setup photos", "Substitutions matériel"],
                    "style": "Pratique, équipement minimal, efficace"
                }
            }
        }

    def _load_professional_variants(self) -> Dict[str, Dict[str, Any]]:
        """Load professional template variants with advanced configurations"""
        return {
            "workout_elite": {
                "default": {
                    "theme": "elite_professional",
                    "layout": "grid_structured",
                    "components": ["progress_graphs", "anatomy_zones", "qr_videos"],
                    "density": "high_data",
                    "branding": "premium_minimal"
                },
                "executive": {
                    "theme": "executive_monochrome",
                    "layout": "executive_timeline",
                    "components": ["roi_metrics", "efficiency_scores"],
                    "density": "ultra_condensed"
                }
            },
            "workout_motivation": {
                "default": {
                    "theme": "energetic_vibrant",
                    "layout": "card_dynamic",
                    "components": ["motivational_quotes", "achievement_badges", "progress_bars"],
                    "gamification": True,
                    "color_intensity": "high"
                },
                "youth": {
                    "theme": "playful_bright",
                    "components": ["emoji_rewards", "level_system", "team_challenges"],
                    "gamification": True
                }
            },
            "workout_medical": {
                "default": {
                    "theme": "medical_clinical",
                    "layout": "medical_structured",
                    "components": ["contraindications", "adaptations", "medical_notes"],
                    "compliance": True,
                    "documentation_level": "complete"
                }
            },
            "nutrition_science": {
                "default": {
                    "theme": "data_precision",
                    "layout": "dashboard_analytics",
                    "components": ["macro_charts", "micro_breakdown", "biomarkers"],
                    "chart_types": ["pie", "bar", "line", "radar"],
                    "precision": "scientific"
                }
            },
            "nutrition_wellness": {
                "default": {
                    "theme": "lifestyle_photography",
                    "layout": "instagram_grid",
                    "components": ["hd_photos", "lifestyle_tips", "weekly_planning"],
                    "visual_emphasis": "photography"
                }
            },
            "nutrition_therapeutic": {
                "default": {
                    "theme": "medical_compliance",
                    "layout": "clinical_format",
                    "components": ["allergen_alerts", "substitutions", "monitoring"],
                    "compliance": True,
                    "allergen_tracking": True
                }
            },
            "nutrition_sheet_education": {
                "default": {
                    "theme": "educational_accessible",
                    "layout": "pedagogical_cards",
                    "components": ["infographics", "learning_objectives", "practical_tips"],
                    "accessibility_level": "high",
                    "pedagogical_approach": "progressive"
                }
            },
            "nutrition_sheet_quickref": {
                "default": {
                    "theme": "emergency_reference",
                    "layout": "ultra_concise",
                    "components": ["quick_actions", "emergency_tips", "key_numbers"],
                    "density": "ultra_high",
                    "action_focused": True
                }
            },
            "nutrition_sheet_scientific": {
                "default": {
                    "theme": "academic_professional",
                    "layout": "journal_format",
                    "components": ["bibliography", "statistical_analysis", "evidence_grading"],
                    "citation_style": "apa",
                    "peer_review_format": True
                }
            },
            "session_premium": {
                "default": {
                    "theme": "luxury_personalized",
                    "layout": "vip_detailed",
                    "components": ["coach_notes", "real_time_adaptations"],
                    "personalization": "maximum"
                }
            },
            "session_group": {
                "default": {
                    "theme": "dynamic_collective",
                    "layout": "group_synchronized",
                    "components": ["playlist", "level_variations", "team_elements"],
                    "group_features": True
                }
            },
            "session_home": {
                "default": {
                    "theme": "practical_efficient",
                    "layout": "space_adaptive",
                    "components": ["setup_photos", "equipment_substitutions"],
                    "space_optimization": True
                }
            }
        }

    def _load_brand_standards(self) -> Dict[str, Any]:
        """Load brand standards for white-label customization"""
        return {
            "logo_placement": {
                "header": {"position": "top_right", "max_height": 40},
                "footer": {"position": "bottom_center", "max_height": 20},
                "watermark": {"opacity": 0.1, "position": "center"}
            },
            "color_customization": {
                "primary": "brand_primary",
                "secondary": "brand_secondary",
                "accent": "brand_accent",
                "override_system": True
            },
            "typography": {
                "custom_fonts": True,
                "font_families": ["brand_primary", "brand_secondary"],
                "fallback": ["Helvetica", "Arial"]
            },
            "compliance": {
                "gdpr": True,
                "healthcare": True,
                "professional_standards": True
            }
        }

    def _apply_brand_config(self, config: Dict[str, Any], brand: Dict[str, Any]) -> Dict[str, Any]:
        """Apply brand configuration to template config"""
        branded_config = config.copy()

        # Apply brand colors
        if "colors" in brand:
            branded_config["colors"] = {**branded_config.get("colors", {}), **brand["colors"]}

        # Apply brand fonts
        if "fonts" in brand:
            branded_config["fonts"] = {**branded_config.get("fonts", {}), **brand["fonts"]}

        # Apply logo configuration
        if "logo" in brand:
            branded_config["logo"] = brand["logo"]

        # Apply custom elements
        if "custom_elements" in brand:
            branded_config["custom_elements"] = brand["custom_elements"]

        return branded_config

    def _get_professional_variant_config(
        self, template_type: str, config: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get configuration for professional template variant"""
        if not config:
            return {}

        variant = config.get("variant", "default")
        if variant in self._professional_variants.get(template_type, {}):
            variant_config = self._professional_variants[template_type][variant]
            return {**variant_config, **config}

        return config

    def _track_template_usage(self, template_type: str) -> None:
        """Track template usage for analytics"""
        if template_type not in self._template_usage:
            self._template_usage[template_type] = 0
        self._template_usage[template_type] += 1

    def get_usage_analytics(self) -> Dict[str, Any]:
        """Get template usage analytics"""
        total_usage = sum(self._template_usage.values())
        return {
            "total_generations": total_usage,
            "template_breakdown": self._template_usage,
            "most_popular": max(self._template_usage.items(), key=lambda x: x[1]) if self._template_usage else None
        }

    def validate_professional_data(self, template_type: str, data: Dict[str, Any]) -> List[str]:
        """Validate data against professional template requirements"""
        errors = []

        if template_type.startswith("workout_"):
            required_fields = ["title", "client_name", "exercises"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")

        elif template_type.startswith("nutrition_"):
            required_fields = ["title", "client_name", "nutrition_data"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")

        elif template_type.startswith("session_"):
            required_fields = ["title", "blocks"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")

        return errors

    def get_template_themes(self) -> Dict[str, Any]:
        """Get available themes optimized for each template type"""
        return {
            "elite_professional": {
                "colors": {"primary": "#1a365d", "secondary": "#2d3748", "accent": "#3182ce"},
                "fonts": {"primary": "Helvetica-Bold", "secondary": "Helvetica"},
                "style": "Premium minimalist with data focus"
            },
            "energetic_vibrant": {
                "colors": {"primary": "#e53e3e", "secondary": "#fd6b00", "accent": "#38d9a9"},
                "fonts": {"primary": "Arial-Bold", "secondary": "Arial"},
                "style": "High energy with gamification elements"
            },
            "medical_clinical": {
                "colors": {"primary": "#2b6cb0", "secondary": "#4a5568", "accent": "#48bb78"},
                "fonts": {"primary": "Times-Bold", "secondary": "Times-Roman"},
                "style": "Clinical professional with compliance focus"
            },
            "data_precision": {
                "colors": {"primary": "#1a202c", "secondary": "#4a5568", "accent": "#0bc5ea"},
                "fonts": {"primary": "Helvetica-Bold", "secondary": "Courier"},
                "style": "Data-driven with advanced analytics"
            },
            "lifestyle_photography": {
                "colors": {"primary": "#744210", "secondary": "#9c7346", "accent": "#68d391"},
                "fonts": {"primary": "Georgia-Bold", "secondary": "Georgia"},
                "style": "Lifestyle focused with visual emphasis"
            }
        }