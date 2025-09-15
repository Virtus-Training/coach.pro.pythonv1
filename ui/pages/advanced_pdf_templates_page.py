"""
Advanced PDF Templates Page - Modern template editor interface
Professional template management with live preview and style customization
"""

from __future__ import annotations

import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Any, Dict

import customtkinter as ctk

from controllers.advanced_pdf_controller import AdvancedPdfController


class AdvancedPdfTemplatesPage(ctk.CTkFrame):
    """
    Professional PDF template editor with live preview
    Modern UI for managing and customizing PDF templates
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = AdvancedPdfController()
        self.current_template_type = "session"
        self.current_config = {}
        self.preview_path = None

        self._setup_ui()
        self._load_initial_data()

    def _setup_ui(self):
        """Setup modern UI layout"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self._create_header()

        # Main content
        self._create_main_content()

    def _create_header(self):
        """Create page header with title and actions"""
        header_frame = ctk.CTkFrame(self, height=80, corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎨 Éditeur de Templates PDF Avancé",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(side="left", padx=20, pady=20)

        # Action buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=20, pady=15)

        self.preview_btn = ctk.CTkButton(
            actions_frame,
            text="👀 Aperçu",
            command=self._generate_preview,
            width=120,
            height=35,
        )
        self.preview_btn.pack(side="right", padx=(0, 10))

        self.export_btn = ctk.CTkButton(
            actions_frame,
            text="💾 Exporter",
            command=self._export_template,
            width=120,
            height=35,
        )
        self.export_btn.pack(side="right", padx=(0, 10))

        self.import_btn = ctk.CTkButton(
            actions_frame,
            text="📁 Importer",
            command=self._import_template,
            width=120,
            height=35,
        )
        self.import_btn.pack(side="right", padx=(0, 10))

    def _create_main_content(self):
        """Create main content area with three columns"""
        content_frame = ctk.CTkFrame(self, corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left panel - Template selection and configuration
        self._create_template_panel(content_frame)

        # Center panel - Style customization
        self._create_style_panel(content_frame)

        # Right panel - Preview and actions
        self._create_preview_panel(content_frame)

    def _create_template_panel(self, parent):
        """Create template selection and basic configuration panel"""
        template_panel = ctk.CTkFrame(parent, corner_radius=10)
        template_panel.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        template_panel.grid_columnconfigure(0, weight=1)

        # Panel header
        header_label = ctk.CTkLabel(
            template_panel,
            text="🏗️ Configuration Template",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Template type selection
        type_frame = ctk.CTkFrame(template_panel, fg_color="transparent")
        type_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        type_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(type_frame, text="Type de document:").grid(
            row=0, column=0, sticky="w"
        )

        self.template_type_var = ctk.StringVar(value="session")
        self.template_type_combo = ctk.CTkComboBox(
            type_frame,
            variable=self.template_type_var,
            values=["session", "nutrition", "program", "meal_plan", "progress_report"],
            command=self._on_template_type_change,
            width=200,
        )
        self.template_type_combo.grid(
            row=1, column=0, sticky="ew", columnspan=2, pady=5
        )

        # Template variant selection
        variant_frame = ctk.CTkFrame(template_panel, fg_color="transparent")
        variant_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        variant_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(variant_frame, text="Variante:").grid(row=0, column=0, sticky="w")

        self.template_variant_var = ctk.StringVar(value="modern")
        self.template_variant_combo = ctk.CTkComboBox(
            variant_frame,
            variable=self.template_variant_var,
            values=["modern", "classic", "minimal"],
            command=self._on_variant_change,
            width=200,
        )
        self.template_variant_combo.grid(
            row=1, column=0, sticky="ew", columnspan=2, pady=5
        )

        # Theme selection
        theme_frame = ctk.CTkFrame(template_panel, fg_color="transparent")
        theme_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        theme_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(theme_frame, text="Thème:").grid(row=0, column=0, sticky="w")

        self.theme_var = ctk.StringVar(value="professional")
        self.theme_combo = ctk.CTkComboBox(
            theme_frame,
            variable=self.theme_var,
            values=["professional", "vibrant", "monochrome", "fitness"],
            command=self._on_theme_change,
            width=200,
        )
        self.theme_combo.grid(row=1, column=0, sticky="ew", columnspan=2, pady=5)

        # Template info display
        info_frame = ctk.CTkScrollableFrame(
            template_panel,
            label_text="ℹ️ Informations Template",
            height=200,
        )
        info_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
        template_panel.grid_rowconfigure(4, weight=1)

        # Remplacer CTkTextbox par CTkLabel pour éviter l'erreur de thème
        self.info_text = ctk.CTkLabel(
            info_frame,
            text="Sélectionnez un template pour voir les informations",
            font=ctk.CTkFont(family="monospace", size=10),
            justify="left",
            anchor="nw",
        )
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_style_panel(self, parent):
        """Create style customization panel"""
        style_panel = ctk.CTkFrame(parent, corner_radius=10)
        style_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
        style_panel.grid_columnconfigure(0, weight=1)

        # Panel header
        header_label = ctk.CTkLabel(
            style_panel,
            text="🎨 Personnalisation des Styles",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Scrollable frame for style options
        self.style_scroll = ctk.CTkScrollableFrame(
            style_panel, label_text="Options de Style"
        )
        self.style_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        style_panel.grid_rowconfigure(1, weight=1)

        self._create_style_controls()

    def _create_style_controls(self):
        """Create dynamic style controls based on template type"""
        # Clear existing controls
        for widget in self.style_scroll.winfo_children():
            widget.destroy()

        self.style_controls = {}

        # Color controls
        colors_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
        colors_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            colors_frame,
            text="🎨 Couleurs",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Primary color
        color_frame = ctk.CTkFrame(colors_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=5)
        color_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(color_frame, text="Couleur principale:").grid(
            row=0, column=0, sticky="w"
        )

        self.primary_color_var = ctk.StringVar(value="#2563EB")
        self.primary_color_entry = ctk.CTkEntry(
            color_frame, textvariable=self.primary_color_var, placeholder_text="#RRGGBB"
        )
        self.primary_color_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.primary_color_entry.bind("<KeyRelease>", self._on_style_change)

        # Secondary color
        color_frame2 = ctk.CTkFrame(colors_frame, fg_color="transparent")
        color_frame2.pack(fill="x", pady=5)
        color_frame2.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(color_frame2, text="Couleur secondaire:").grid(
            row=0, column=0, sticky="w"
        )

        self.secondary_color_var = ctk.StringVar(value="#7C3AED")
        self.secondary_color_entry = ctk.CTkEntry(
            color_frame2,
            textvariable=self.secondary_color_var,
            placeholder_text="#RRGGBB",
        )
        self.secondary_color_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.secondary_color_entry.bind("<KeyRelease>", self._on_style_change)

        # Font controls
        fonts_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
        fonts_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            fonts_frame,
            text="🔤 Police",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Font family
        font_frame = ctk.CTkFrame(fonts_frame, fg_color="transparent")
        font_frame.pack(fill="x", pady=5)
        font_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(font_frame, text="Famille de police:").grid(
            row=0, column=0, sticky="w"
        )

        self.font_family_var = ctk.StringVar(value="modern")
        self.font_family_combo = ctk.CTkComboBox(
            font_frame,
            variable=self.font_family_var,
            values=["modern", "classic", "sans"],
            command=self._on_style_change,
        )
        self.font_family_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Layout controls
        layout_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
        layout_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            layout_frame,
            text="📏 Mise en page",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Show logo option
        self.show_logo_var = ctk.BooleanVar(value=True)
        self.show_logo_cb = ctk.CTkCheckBox(
            layout_frame,
            text="Afficher le logo",
            variable=self.show_logo_var,
            command=self._on_style_change,
        )
        self.show_logo_cb.pack(anchor="w", pady=2)

        # Show page numbers option
        self.show_page_numbers_var = ctk.BooleanVar(value=True)
        self.show_page_numbers_cb = ctk.CTkCheckBox(
            layout_frame,
            text="Numéros de page",
            variable=self.show_page_numbers_var,
            command=self._on_style_change,
        )
        self.show_page_numbers_cb.pack(anchor="w", pady=2)

        # Template-specific controls
        self._add_template_specific_controls()

    def _add_template_specific_controls(self):
        """Add controls specific to current template type"""
        template_type = self.template_type_var.get()

        # Session-specific controls
        if template_type == "session":
            session_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
            session_frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                session_frame,
                text="🏋️ Options Séance",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(anchor="w", pady=(0, 10))

            self.show_icons_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                session_frame,
                text="Afficher les icônes",
                variable=self.show_icons_var,
                command=self._on_style_change,
            ).pack(anchor="w", pady=2)

            self.show_duration_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                session_frame,
                text="Afficher la durée",
                variable=self.show_duration_var,
                command=self._on_style_change,
            ).pack(anchor="w", pady=2)

        # Nutrition-specific controls
        elif template_type == "nutrition":
            nutrition_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
            nutrition_frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                nutrition_frame,
                text="🥗 Options Nutrition",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(anchor="w", pady=(0, 10))

            self.show_macro_chart_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                nutrition_frame,
                text="Graphique macronutriments",
                variable=self.show_macro_chart_var,
                command=self._on_style_change,
            ).pack(anchor="w", pady=2)

            self.show_recommendations_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                nutrition_frame,
                text="Recommandations",
                variable=self.show_recommendations_var,
                command=self._on_style_change,
            ).pack(anchor="w", pady=2)

        # Program-specific controls
        elif template_type == "program":
            program_frame = ctk.CTkFrame(self.style_scroll, fg_color="transparent")
            program_frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                program_frame,
                text="📅 Options Programme",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(anchor="w", pady=(0, 10))

            layout_frame = ctk.CTkFrame(program_frame, fg_color="transparent")
            layout_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(layout_frame, text="Mise en page:").pack(anchor="w")

            self.program_layout_var = ctk.StringVar(value="weekly")
            ctk.CTkComboBox(
                layout_frame,
                variable=self.program_layout_var,
                values=["weekly", "daily", "compact"],
                command=self._on_style_change,
            ).pack(fill="x", pady=2)

            self.show_progression_var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                program_frame,
                text="Afficher la progression",
                variable=self.show_progression_var,
                command=self._on_style_change,
            ).pack(anchor="w", pady=2)

    def _create_preview_panel(self, parent):
        """Create preview and actions panel"""
        preview_panel = ctk.CTkFrame(parent, corner_radius=10)
        preview_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)
        preview_panel.grid_columnconfigure(0, weight=1)

        # Panel header
        header_label = ctk.CTkLabel(
            preview_panel,
            text="👁️ Aperçu & Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Preview status
        self.preview_status = ctk.CTkLabel(
            preview_panel,
            text="Cliquez sur 'Aperçu' pour voir le rendu",
            text_color="gray",
        )
        self.preview_status.grid(row=1, column=0, padx=20, pady=10)

        # Preview actions
        actions_frame = ctk.CTkFrame(preview_panel, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.generate_preview_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Générer Aperçu",
            command=self._generate_preview,
        )
        self.generate_preview_btn.pack(fill="x", pady=5)

        self.open_preview_btn = ctk.CTkButton(
            actions_frame,
            text="📄 Ouvrir PDF",
            command=self._open_preview,
            state="disabled",
        )
        self.open_preview_btn.pack(fill="x", pady=5)

        # Template management
        management_frame = ctk.CTkFrame(preview_panel, fg_color="transparent")
        management_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=20)

        ctk.CTkLabel(
            management_frame,
            text="💾 Gestion",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        self.save_template_btn = ctk.CTkButton(
            management_frame,
            text="💾 Sauvegarder Template",
            command=self._save_template,
        )
        self.save_template_btn.pack(fill="x", pady=5)

        self.load_template_btn = ctk.CTkButton(
            management_frame,
            text="📁 Charger Template",
            command=self._load_template,
        )
        self.load_template_btn.pack(fill="x", pady=5)

        # Performance stats
        stats_frame = ctk.CTkFrame(preview_panel, fg_color="transparent")
        stats_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=20)

        ctk.CTkLabel(
            stats_frame,
            text="📊 Performance",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        self.stats_text = ctk.CTkLabel(
            stats_frame,
            text="Aucune statistique disponible",
            font=ctk.CTkFont(family="monospace", size=9),
            justify="left",
            anchor="nw",
        )
        self.stats_text.pack(fill="both", expand=True)

        self.refresh_stats_btn = ctk.CTkButton(
            stats_frame,
            text="🔄 Actualiser Stats",
            command=self._refresh_stats,
            height=25,
        )
        self.refresh_stats_btn.pack(fill="x", pady=(5, 0))

    def _load_initial_data(self):
        """Load initial data and update UI"""
        self._update_template_info()
        self._refresh_stats()

    def _on_template_type_change(self, *args):
        """Handle template type change"""
        self.current_template_type = self.template_type_var.get()
        self._update_variants()
        self._create_style_controls()
        self._update_template_info()

    def _on_variant_change(self, *args):
        """Handle variant change"""
        self._update_template_info()

    def _on_theme_change(self, *args):
        """Handle theme change"""
        self._update_colors_from_theme()

    def _on_style_change(self, *args):
        """Handle style control changes"""
        self._update_current_config()

    def _update_variants(self):
        """Update available variants for current template type"""
        try:
            template_info = self.controller.get_template_info(
                self.current_template_type
            )
            variants = template_info.get("variants", ["default"])
            self.template_variant_combo.configure(values=variants)
            if variants:
                self.template_variant_var.set(variants[0])
        except Exception:
            self.template_variant_combo.configure(values=["default"])
            self.template_variant_var.set("default")

    def _update_template_info(self):
        """Update template information display"""
        try:
            template_info = self.controller.get_template_info(
                self.current_template_type
            )
            info_text = json.dumps(template_info, indent=2, ensure_ascii=False)
            self.info_text.configure(text=info_text)
        except Exception as e:
            self.info_text.configure(text=f"Erreur: {str(e)}")

    def _update_colors_from_theme(self):
        """Update color controls based on selected theme"""
        try:
            themes = self.controller.get_template_themes()
            theme_name = self.theme_var.get()
            theme_colors = themes.get(theme_name, {})

            if "primary" in theme_colors:
                self.primary_color_var.set(theme_colors["primary"])
            if "secondary" in theme_colors:
                self.secondary_color_var.set(theme_colors["secondary"])

        except Exception:
            pass

    def _update_current_config(self):
        """Update current template configuration"""
        self.current_config = {
            "variant": self.template_variant_var.get(),
            "colors": {
                "primary": self.primary_color_var.get(),
                "secondary": self.secondary_color_var.get(),
            },
            "fonts": {
                "family": self.font_family_var.get(),
            },
            "header": {
                "show_logo": self.show_logo_var.get(),
            },
            "footer": {
                "show_page_numbers": self.show_page_numbers_var.get(),
            },
        }

        # Add template-specific config
        template_type = self.template_type_var.get()
        if template_type == "session":
            self.current_config["blocks"] = {
                "show_icons": getattr(
                    self, "show_icons_var", ctk.BooleanVar(True)
                ).get(),
                "show_duration": getattr(
                    self, "show_duration_var", ctk.BooleanVar(True)
                ).get(),
            }
        elif template_type == "nutrition":
            self.current_config["show_macro_chart"] = getattr(
                self, "show_macro_chart_var", ctk.BooleanVar(True)
            ).get()
            self.current_config["show_recommendations"] = getattr(
                self, "show_recommendations_var", ctk.BooleanVar(True)
            ).get()
        elif template_type == "program":
            self.current_config["layout"] = getattr(
                self, "program_layout_var", ctk.StringVar("weekly")
            ).get()
            self.current_config["show_progression"] = getattr(
                self, "show_progression_var", ctk.BooleanVar(True)
            ).get()

    def _generate_preview(self):
        """Generate PDF preview"""
        try:
            self.preview_status.configure(text="⏳ Génération de l'aperçu...")
            self.generate_preview_btn.configure(state="disabled")

            self._update_current_config()

            result = self.controller.generate_preview(
                self.current_template_type, self.current_config, use_sample_data=True
            )

            if result.get("success"):
                self.preview_path = result.get("preview_path")
                file_size = result.get("preview_size", 0)

                self.preview_status.configure(
                    text=f"✅ Aperçu généré ({file_size // 1024} KB)",
                    text_color="green",
                )
                self.open_preview_btn.configure(state="normal")
            else:
                error = result.get("error", "Erreur inconnue")
                self.preview_status.configure(
                    text=f"❌ Erreur: {error}", text_color="red"
                )

        except Exception as e:
            self.preview_status.configure(text=f"❌ Erreur: {str(e)}", text_color="red")
        finally:
            self.generate_preview_btn.configure(state="normal")

    def _open_preview(self):
        """Open generated preview PDF"""
        if self.preview_path and Path(self.preview_path).exists():
            try:
                os.startfile(self.preview_path)  # Windows
            except AttributeError:
                os.system(f"open '{self.preview_path}'")  # macOS
            except:
                os.system(f"xdg-open '{self.preview_path}'")  # Linux

    def _export_template(self):
        """Export current template configuration"""
        try:
            self._update_current_config()

            # Add metadata
            export_data = {
                "metadata": {
                    "template_type": self.current_template_type,
                    "name": f"Template {self.current_template_type.title()}",
                    "version": "1.0",
                    "created_with": "CoachPro Advanced PDF Editor",
                },
                "config": self.current_config,
            }

            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                title="Exporter Template",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                defaultextension=".json",
            )

            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Succès", f"Template exporté vers:\n{file_path}")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible d'exporter le template:\n{str(e)}"
            )

    def _import_template(self):
        """Import template configuration"""
        try:
            file_path = filedialog.askopenfilename(
                title="Importer Template",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            )

            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    import_data = json.load(f)

                # Extract configuration
                if "config" in import_data:
                    config = import_data["config"]
                else:
                    config = import_data  # Assume whole file is config

                # Update template type if specified
                if "metadata" in import_data:
                    template_type = import_data["metadata"].get("template_type")
                    if template_type:
                        self.template_type_var.set(template_type)
                        self._on_template_type_change()

                # Update UI controls with imported values
                self._load_config_to_ui(config)

                messagebox.showinfo("Succès", "Template importé avec succès!")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible d'importer le template:\n{str(e)}"
            )

    def _load_config_to_ui(self, config: Dict[str, Any]):
        """Load configuration values to UI controls"""
        try:
            # Variant
            if "variant" in config:
                self.template_variant_var.set(config["variant"])

            # Colors
            colors = config.get("colors", {})
            if "primary" in colors:
                self.primary_color_var.set(colors["primary"])
            if "secondary" in colors:
                self.secondary_color_var.set(colors["secondary"])

            # Fonts
            fonts = config.get("fonts", {})
            if "family" in fonts:
                self.font_family_var.set(fonts["family"])

            # Header/Footer options
            header = config.get("header", {})
            if "show_logo" in header:
                self.show_logo_var.set(header["show_logo"])

            footer = config.get("footer", {})
            if "show_page_numbers" in footer:
                self.show_page_numbers_var.set(footer["show_page_numbers"])

            # Template-specific options
            template_type = self.template_type_var.get()
            if template_type == "session":
                blocks = config.get("blocks", {})
                if hasattr(self, "show_icons_var") and "show_icons" in blocks:
                    self.show_icons_var.set(blocks["show_icons"])
                if hasattr(self, "show_duration_var") and "show_duration" in blocks:
                    self.show_duration_var.set(blocks["show_duration"])

            elif template_type == "nutrition":
                if (
                    hasattr(self, "show_macro_chart_var")
                    and "show_macro_chart" in config
                ):
                    self.show_macro_chart_var.set(config["show_macro_chart"])
                if (
                    hasattr(self, "show_recommendations_var")
                    and "show_recommendations" in config
                ):
                    self.show_recommendations_var.set(config["show_recommendations"])

            elif template_type == "program":
                if hasattr(self, "program_layout_var") and "layout" in config:
                    self.program_layout_var.set(config["layout"])
                if (
                    hasattr(self, "show_progression_var")
                    and "show_progression" in config
                ):
                    self.show_progression_var.set(config["show_progression"])

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Erreur lors du chargement de la configuration:\n{str(e)}"
            )

    def _save_template(self):
        """Save current template to database"""
        try:
            self._update_current_config()

            # Ask for template name
            dialog = ctk.CTkInputDialog(
                text="Nom du template:", title="Sauvegarder Template"
            )
            template_name = dialog.get_input()

            if template_name:
                # Convert config to JSON string for legacy compatibility
                style_json = json.dumps(self.current_config)

                result = self.controller.save_legacy_template(
                    self.current_template_type,
                    template_name,
                    style_json,
                    set_default=False,
                )

                if result.get("success"):
                    messagebox.showinfo(
                        "Succès", f"Template '{template_name}' sauvegardé!"
                    )
                else:
                    error = result.get("error", "Erreur inconnue")
                    messagebox.showerror(
                        "Erreur", f"Impossible de sauvegarder:\n{error}"
                    )

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")

    def _load_template(self):
        """Load template from database"""
        try:
            templates = self.controller.list_legacy_templates(
                self.current_template_type
            )

            if not templates:
                messagebox.showinfo("Information", "Aucun template sauvegardé trouvé.")
                return

            # Create selection dialog
            dialog_window = ctk.CTkToplevel(self)
            dialog_window.title("Charger Template")
            dialog_window.geometry("400x300")
            dialog_window.transient(self)
            dialog_window.grab_set()

            # Template list
            ctk.CTkLabel(
                dialog_window,
                text="Sélectionner un template:",
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(pady=20)

            template_listbox = tk.Listbox(dialog_window, height=10)
            template_listbox.pack(fill="both", expand=True, padx=20, pady=10)

            for template in templates:
                template_listbox.insert(
                    "end", f"{template['name']} (ID: {template['id']})"
                )

            # Buttons
            button_frame = ctk.CTkFrame(dialog_window, fg_color="transparent")
            button_frame.pack(fill="x", padx=20, pady=10)

            def load_selected():
                selection = template_listbox.curselection()
                if selection:
                    template = templates[selection[0]]
                    template_id = template["id"]

                    # Load template style
                    style = self.controller.get_legacy_session_style(template_id)
                    self._load_config_to_ui(style)

                    dialog_window.destroy()
                    messagebox.showinfo(
                        "Succès", f"Template '{template['name']}' chargé!"
                    )

            ctk.CTkButton(button_frame, text="Charger", command=load_selected).pack(
                side="right", padx=5
            )

            ctk.CTkButton(
                button_frame, text="Annuler", command=dialog_window.destroy
            ).pack(side="right")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement:\n{str(e)}")

    def _refresh_stats(self):
        """Refresh performance statistics"""
        try:
            stats = self.controller.get_performance_stats()

            stats_text = f"""📊 Statistiques de performance:

Documents générés: {stats.get("total_documents", 0)}
Temps total: {stats.get("total_time", 0):.2f}s
Temps moyen: {stats.get("average_time", 0):.2f}s

Cache:
"""
            cache_stats = stats.get("cache_stats")
            if cache_stats:
                stats_text += f"""  Hits: {cache_stats.get("hits", 0)}
  Misses: {cache_stats.get("misses", 0)}
  Taux: {cache_stats.get("hit_rate", 0):.1%}
  Taille: {cache_stats.get("total_size_mb", 0):.1f} MB"""
            else:
                stats_text += "  Cache désactivé"

            self.stats_text.configure(text=stats_text)

        except Exception as e:
            self.stats_text.configure(text=f"Erreur: {str(e)}")


# Make the page available for import
__all__ = ["AdvancedPdfTemplatesPage"]
