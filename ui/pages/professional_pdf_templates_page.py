"""
Professional PDF Templates Page - Premium template showcase and editor
Commercial-grade templates with advanced customization
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Any, Dict

import customtkinter as ctk

from controllers.advanced_pdf_controller import AdvancedPdfController


class ProfessionalPdfTemplatesPage(ctk.CTkFrame):
    """
    Professional PDF template showcase with commercial-grade templates
    Features premium UI and advanced customization options
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = AdvancedPdfController()
        self.professional_templates = {}
        self.current_template_type = "workout_elite"
        self.current_config = {}
        self.preview_path = None

        self._setup_ui()
        self._load_professional_templates()

    def _setup_ui(self):
        """Setup professional UI layout"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Professional header
        self._create_professional_header()

        # Main content with template showcase
        self._create_professional_content()

    def _create_professional_header(self):
        """Create professional header with premium styling"""
        header_frame = ctk.CTkFrame(self, height=120, corner_radius=15)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)

        # Premium title with gradient effect
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            title_frame,
            text="🏆 TEMPLATES PDF PROFESSIONNELS",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#2563EB",
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Niveau commercial • Rivalise avec Trainerize Pro & MyFitnessPal Premium",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="#64748b",
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Quick stats
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(side="right", padx=20, pady=15)

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="4 Templates Professionnels\nGénération <3s • Cache Intelligent",
            font=ctk.CTkFont(size=12),
            text_color="#475569",
            justify="right",
        )
        self.stats_label.pack()

    def _create_professional_content(self):
        """Create main content with template showcase"""
        content_frame = ctk.CTkFrame(self, corner_radius=15)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left panel - Template showcase
        self._create_template_showcase(content_frame)

        # Right panel - Advanced controls
        self._create_advanced_controls(content_frame)

    def _create_template_showcase(self, parent):
        """Create professional template showcase"""
        showcase_panel = ctk.CTkFrame(parent, corner_radius=15)
        showcase_panel.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        showcase_panel.grid_columnconfigure(0, weight=1)

        # Showcase header
        header_label = ctk.CTkLabel(
            showcase_panel,
            text="🎨 GALERIE TEMPLATES PREMIUM",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        header_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))

        # Template categories
        categories_frame = ctk.CTkFrame(showcase_panel, fg_color="transparent")
        categories_frame.grid(row=1, column=0, sticky="ew", padx=20)
        categories_frame.grid_columnconfigure((0, 1), weight=1)

        # Workout templates category
        self._create_category_section(
            categories_frame, "💪 PROGRAMMES D'ENTRAÎNEMENT", "workout_programs", 0, 0
        )

        # Nutrition templates category
        self._create_category_section(
            categories_frame, "🥗 PLANS ALIMENTAIRES", "nutrition_plans", 0, 1
        )

        # Template details panel
        self.details_panel = ctk.CTkScrollableFrame(
            showcase_panel, label_text="📋 Détails Template", height=300
        )
        self.details_panel.grid(row=2, column=0, sticky="nsew", padx=20, pady=15)
        showcase_panel.grid_rowconfigure(2, weight=1)

        # Initially show Elite template details
        self._show_template_details("workout_elite")

    def _create_category_section(self, parent, title, category, row, col):
        """Create a category section with template cards"""
        category_frame = ctk.CTkFrame(parent, corner_radius=10)
        category_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Category title
        ctk.CTkLabel(
            category_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(15, 10))

        # Template cards based on category
        if category == "workout_programs":
            templates = [
                (
                    "workout_elite",
                    "🏆 Elite Performance",
                    "#1a365d",
                    "Premium minimalist",
                ),
                (
                    "workout_motivation",
                    "🔥 Motivation+",
                    "#e53e3e",
                    "Gamification énergique",
                ),
                ("workout_medical", "🏥 Medical Pro", "#2b6cb0", "Compliance médicale"),
            ]
        else:  # nutrition_plans
            templates = [
                (
                    "nutrition_science",
                    "🔬 Nutrition Science",
                    "#1a202c",
                    "Data-driven précision",
                ),
                (
                    "nutrition_wellness",
                    "🌿 Lifestyle Wellness",
                    "#744210",
                    "Lifestyle photography",
                ),
                (
                    "nutrition_therapeutic",
                    "⚕️ Therapeutic Diet",
                    "#2b6cb0",
                    "Medical compliance",
                ),
            ]

        for template_id, name, color, description in templates:
            self._create_template_card(
                category_frame, template_id, name, color, description
            )

    def _create_template_card(self, parent, template_id, name, color, description):
        """Create a professional template card"""
        card_frame = ctk.CTkFrame(parent, corner_radius=8, height=80)
        card_frame.pack(fill="x", padx=10, pady=5)
        card_frame.pack_propagate(False)

        # Template name and description
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        name_label = ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color,
        )
        name_label.pack(anchor="w")

        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=10),
            text_color="gray",
        )
        desc_label.pack(anchor="w")

        # Action buttons
        actions_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=10)

        select_btn = ctk.CTkButton(
            actions_frame,
            text="Sélectionner",
            command=lambda: self._select_template(template_id),
            width=90,
            height=25,
            font=ctk.CTkFont(size=10),
        )
        select_btn.pack(side="right", padx=2)

        preview_btn = ctk.CTkButton(
            actions_frame,
            text="Aperçu",
            command=lambda: self._show_template_details(template_id),
            width=70,
            height=25,
            font=ctk.CTkFont(size=10),
            fg_color="gray",
        )
        preview_btn.pack(side="right", padx=2)

    def _create_advanced_controls(self, parent):
        """Create advanced controls panel"""
        controls_panel = ctk.CTkFrame(parent, corner_radius=15)
        controls_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        controls_panel.grid_columnconfigure(0, weight=1)

        # Controls header
        header_label = ctk.CTkLabel(
            controls_panel,
            text="⚙️ CONTRÔLES AVANCÉS",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))

        # Current template info
        self._create_current_template_info(controls_panel)

        # Customization controls
        self._create_customization_controls(controls_panel)

        # Generation controls
        self._create_generation_controls(controls_panel)

        # Performance monitoring
        self._create_performance_monitoring(controls_panel)

    def _create_current_template_info(self, parent):
        """Create current template information section"""
        info_frame = ctk.CTkFrame(parent, corner_radius=10)
        info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            info_frame,
            text="📋 Template Actuel",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(pady=(15, 10))

        self.current_template_label = ctk.CTkLabel(
            info_frame,
            text="Elite Performance\nPremium minimalist avec analytics",
            font=ctk.CTkFont(size=10),
            justify="center",
        )
        self.current_template_label.pack(pady=(0, 15))

    def _create_customization_controls(self, parent):
        """Create customization controls"""
        custom_frame = ctk.CTkScrollableFrame(
            parent, label_text="🎨 Personnalisation", height=200
        )
        custom_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 15))
        parent.grid_rowconfigure(2, weight=1)

        # Brand colors
        color_frame = ctk.CTkFrame(custom_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            color_frame, text="Couleur principale:", font=ctk.CTkFont(size=10)
        ).pack(anchor="w")
        self.primary_color_var = ctk.StringVar(value="#2563EB")
        self.primary_color_entry = ctk.CTkEntry(
            color_frame,
            textvariable=self.primary_color_var,
            placeholder_text="#RRGGBB",
            height=25,
        )
        self.primary_color_entry.pack(fill="x", pady=2)

        # Logo upload
        logo_frame = ctk.CTkFrame(custom_frame, fg_color="transparent")
        logo_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            logo_frame, text="Logo personnalisé:", font=ctk.CTkFont(size=10)
        ).pack(anchor="w")
        self.logo_btn = ctk.CTkButton(
            logo_frame,
            text="📁 Choisir Logo",
            command=self._select_logo,
            height=25,
            font=ctk.CTkFont(size=10),
        )
        self.logo_btn.pack(fill="x", pady=2)

        # White-label options
        self.white_label_var = ctk.BooleanVar(value=False)
        self.white_label_cb = ctk.CTkCheckBox(
            custom_frame,
            text="Mode White-label",
            variable=self.white_label_var,
            font=ctk.CTkFont(size=10),
        )
        self.white_label_cb.pack(anchor="w", pady=5)

    def _create_generation_controls(self, parent):
        """Create PDF generation controls"""
        gen_frame = ctk.CTkFrame(parent, corner_radius=10)
        gen_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            gen_frame,
            text="⚡ Génération",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(pady=(15, 10))

        # Quick generation buttons
        self.demo_btn = ctk.CTkButton(
            gen_frame,
            text="🎯 Démo avec Données",
            command=self._generate_demo_pdf,
            height=35,
        )
        self.demo_btn.pack(fill="x", padx=15, pady=2)

        self.preview_btn = ctk.CTkButton(
            gen_frame,
            text="👀 Aperçu Rapide",
            command=self._generate_preview,
            height=35,
            fg_color="gray",
        )
        self.preview_btn.pack(fill="x", padx=15, pady=2)

        self.export_btn = ctk.CTkButton(
            gen_frame,
            text="💾 Exporter PDF",
            command=self._export_pdf,
            height=35,
            fg_color="#059669",
        )
        self.export_btn.pack(fill="x", padx=15, pady=(2, 15))

    def _create_performance_monitoring(self, parent):
        """Create performance monitoring section"""
        perf_frame = ctk.CTkFrame(parent, corner_radius=10)
        perf_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            perf_frame,
            text="📊 Performance",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(pady=(15, 10))

        self.perf_label = ctk.CTkLabel(
            perf_frame,
            text="Aucune génération récente",
            font=ctk.CTkFont(family="monospace", size=9),
            justify="left",
        )
        self.perf_label.pack(pady=(0, 10))

        self.refresh_stats_btn = ctk.CTkButton(
            perf_frame,
            text="🔄 Actualiser",
            command=self._refresh_performance_stats,
            height=25,
            font=ctk.CTkFont(size=10),
        )
        self.refresh_stats_btn.pack(fill="x", padx=15, pady=(0, 15))

    def _load_professional_templates(self):
        """Load professional templates information"""
        try:
            self.professional_templates = self.controller.get_professional_templates()
            self._refresh_performance_stats()
        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de charger les templates: {str(e)}"
            )

    def _select_template(self, template_id):
        """Select a template for customization"""
        self.current_template_type = template_id
        self._show_template_details(template_id)
        self._update_current_template_display(template_id)

    def _show_template_details(self, template_id):
        """Show detailed template information"""
        # Clear existing content
        for widget in self.details_panel.winfo_children():
            widget.destroy()

        if template_id not in self.professional_templates:
            # Try to find in sub-categories
            found_template = None
            for category, templates in self.professional_templates.items():
                if template_id in templates:
                    found_template = templates[template_id]
                    break

            if not found_template:
                ctk.CTkLabel(
                    self.details_panel, text="Template non trouvé", text_color="red"
                ).pack(pady=20)
                return

            template_info = found_template
        else:
            template_info = self.professional_templates[template_id]

        # Template name and description
        name_label = ctk.CTkLabel(
            self.details_panel,
            text=template_info.get("name", template_id),
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        name_label.pack(pady=(10, 5))

        desc_label = ctk.CTkLabel(
            self.details_panel,
            text=template_info.get("description", "Aucune description"),
            font=ctk.CTkFont(size=12),
            wraplength=300,
            justify="center",
        )
        desc_label.pack(pady=(0, 15))

        # Features
        features_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
        features_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            features_frame,
            text="✨ Fonctionnalités:",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w")

        features = template_info.get("features", [])
        for feature in features:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=f"• {feature}",
                font=ctk.CTkFont(size=10),
            )
            feature_label.pack(anchor="w", padx=20)

        # Target audience
        target_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
        target_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            target_frame,
            text="🎯 Audience cible:",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            target_frame,
            text=template_info.get("target", "Tous types de coaches"),
            font=ctk.CTkFont(size=10),
            wraplength=300,
            justify="left",
        ).pack(anchor="w", padx=20)

    def _update_current_template_display(self, template_id):
        """Update current template display"""
        template_names = {
            "workout_elite": "Elite Performance\nPremium minimalist",
            "workout_motivation": "Motivation+\nGamification énergique",
            "workout_medical": "Medical Pro\nCompliance médicale",
            "nutrition_science": "Nutrition Science\nData-driven précision",
            "nutrition_wellness": "Lifestyle Wellness\nLifestyle photography",
            "nutrition_therapeutic": "Therapeutic Diet\nMedical compliance",
        }

        display_text = template_names.get(template_id, template_id)
        self.current_template_label.configure(text=display_text)

    def _select_logo(self):
        """Select logo file"""
        file_path = filedialog.askopenfilename(
            title="Choisir un logo",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.logo_btn.configure(text=f"📁 {Path(file_path).name}")

    def _generate_demo_pdf(self):
        """Generate demo PDF with sample data"""
        try:
            self.demo_btn.configure(state="disabled", text="⏳ Génération...")

            # Create sample data based on template type
            if self.current_template_type.startswith("workout_"):
                sample_data = self._get_sample_workout_data()
                style = self.current_template_type.split("_")[
                    1
                ]  # elite, motivation, medical

                # Generate PDF
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as temp_file:
                    temp_path = temp_file.name

                result = self.controller.generate_professional_workout_pdf(
                    sample_data, temp_path, style
                )

            elif self.current_template_type.startswith("nutrition_"):
                sample_data = self._get_sample_nutrition_data()
                style = self.current_template_type.split("_")[
                    1
                ]  # science, wellness, therapeutic

                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as temp_file:
                    temp_path = temp_file.name

                result = self.controller.generate_professional_nutrition_pdf(
                    sample_data, temp_path, style
                )

            if result.get("success"):
                # Open PDF
                os.startfile(temp_path)  # Windows
                messagebox.showinfo(
                    "Succès",
                    f"PDF généré avec succès !\nTemps: {result.get('generation_time', 0):.2f}s",
                )
            else:
                messagebox.showerror("Erreur", result.get("error", "Erreur inconnue"))

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {str(e)}")
        finally:
            self.demo_btn.configure(state="normal", text="🎯 Démo avec Données")

    def _generate_preview(self):
        """Generate quick preview"""
        messagebox.showinfo(
            "Info", "Génération d'aperçu rapide en cours de développement..."
        )

    def _export_pdf(self):
        """Export PDF with current settings"""
        file_path = filedialog.asksaveasfilename(
            title="Exporter PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            defaultextension=".pdf",
        )

        if file_path:
            # Use demo generation for now
            try:
                if self.current_template_type.startswith("workout_"):
                    sample_data = self._get_sample_workout_data()
                    style = self.current_template_type.split("_")[1]
                    result = self.controller.generate_professional_workout_pdf(
                        sample_data, file_path, style
                    )
                elif self.current_template_type.startswith("nutrition_"):
                    sample_data = self._get_sample_nutrition_data()
                    style = self.current_template_type.split("_")[1]
                    result = self.controller.generate_professional_nutrition_pdf(
                        sample_data, file_path, style
                    )

                if result.get("success"):
                    messagebox.showinfo("Succès", f"PDF exporté vers:\n{file_path}")
                else:
                    messagebox.showerror(
                        "Erreur", result.get("error", "Erreur inconnue")
                    )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def _refresh_performance_stats(self):
        """Refresh performance statistics"""
        try:
            stats = self.controller.get_performance_stats()

            stats_text = f"""Docs: {stats.get("total_documents", 0)}
Temps moy: {stats.get("average_time", 0):.2f}s
Cache: {stats.get("cache_stats", {}).get("hit_rate", 0):.1%}"""

            self.perf_label.configure(text=stats_text)

        except Exception as e:
            self.perf_label.configure(text=f"Erreur: {str(e)}")

    def _get_sample_workout_data(self) -> Dict[str, Any]:
        """Get sample workout data"""
        return {
            "title": "Programme Elite Performance",
            "client_name": "Alexandre Martin",
            "program_overview": {
                "primary_goal": "Force maximale",
                "duration_weeks": 8,
                "sessions_per_week": 4,
                "intensity_level": "Élevé",
                "target_areas": ["Poitrine", "Dos", "Jambes"],
            },
            "performance_metrics": {
                "strength_progress": 85,
                "endurance_progress": 70,
                "flexibility_progress": 60,
            },
            "target_muscle_groups": ["chest", "shoulders", "legs"],
            "workout_blocks": [
                {
                    "title": "Force Maximale",
                    "duration": 45,
                    "format": "PRINCIPAL",
                    "exercises": [
                        {"name": "Squat", "reps": "5x3", "notes": "90% 1RM"},
                        {"name": "Développé couché", "reps": "5x3", "notes": "85% 1RM"},
                        {"name": "Soulevé de terre", "reps": "4x2", "notes": "95% 1RM"},
                    ],
                }
            ],
        }

    def _get_sample_nutrition_data(self) -> Dict[str, Any]:
        """Get sample nutrition data"""
        return {
            "client_name": "Sophie Leblanc",
            "analysis_date": "2025-01-13",
            "biometrics": {
                "age": 28,
                "weight": 65.5,
                "height": 170,
                "body_fat": 22.5,
                "lean_mass": 50.8,
            },
            "nutrition_analytics": {
                "tdee": 2100,
                "target_calories": 1800,
                "protein_g": 130,
                "carbs_g": 180,
                "fat_g": 70,
                "fiber_target": 28,
                "water_target": 33,
            },
            "micronutrient_analysis": {
                "vit_d": 18,
                "b12": 3.2,
                "iron": 12,
                "magnesium": 280,
                "zinc": 9.5,
                "omega3": 1.8,
            },
        }


# Make the page available for import
__all__ = ["ProfessionalPdfTemplatesPage"]
