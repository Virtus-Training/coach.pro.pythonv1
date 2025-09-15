"""
Page de paramètres pour la génération de séances.
Interface moderne pour configurer les règles métier du générateur intelligent.
"""

from typing import Any, Dict, List

import customtkinter as ctk

from services.workout_config_service import WorkoutConfigService
from ui.components.modern_ui_kit import (
    AnimatedButton,
    GlassCard,
    ModernTabView,
    StatusIndicator,
    show_toast,
)


class WorkoutSettingsPage(ctk.CTkFrame):
    """Page de configuration des paramètres de génération de séances."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.config_service = WorkoutConfigService()
        self.config = self.config_service.get_config()
        self._create_interface()
        self._load_current_config()

    def _create_interface(self):
        """Crée l'interface de la page des paramètres."""

        # Container principal avec scroll
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=ctk.ThemeManager.theme["color"]["surface_light"]
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # === HEADER ===
        self._create_header()

        # === TABVIEW PRINCIPAL ===
        self.main_tabs = ModernTabView(self.main_container)
        self.main_tabs.pack(fill="both", expand=True, pady=(20, 0))

        # Créer les onglets
        self._create_muscle_balance_tab()
        self._create_format_rules_tab()
        self._create_exercise_preferences_tab()
        self._create_equipment_management_tab()
        self._create_advanced_settings_tab()

        # === FOOTER ACTIONS ===
        self._create_footer_actions()

    def _create_header(self):
        """Crée le header de la page."""
        header_card = GlassCard(
            self.main_container,
            fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"]
        )
        header_card.pack(fill="x", pady=(0, 20))

        header_content = ctk.CTkFrame(header_card.content_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True)
        header_content.grid_columnconfigure(0, weight=1)

        # Titre et description
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))

        title_label = ctk.CTkLabel(
            title_frame,
            text="⚙️ Paramètres de Génération",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"]
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Configurez les règles métier pour optimiser la génération automatique de séances",
            font=ctk.CTkFont(size=14),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            wraplength=500
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        # Status de configuration
        status_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")

        self.config_status = StatusIndicator(
            status_frame,
            status="success",
            text="Configuration chargée"
        )
        self.config_status.pack()

    def _create_muscle_balance_tab(self):
        """Onglet équilibrage musculaire."""
        muscle_tab = self.main_tabs.add_tab("muscle", "💪 Équilibrage Musculaire")

        # === RATIOS PRINCIPAUX ===
        ratios_card = GlassCard(muscle_tab, title="Ratios d'Équilibrage")
        ratios_card.pack(fill="x", pady=(0, 16))

        # Push/Pull Ratio
        self._create_slider_setting(
            ratios_card.content_frame,
            "Ratio Push/Pull",
            "Balance entre mouvements de poussée et traction",
            "push_pull_ratio",
            0.3, 0.9, 0.1
        )

        # Upper/Lower Ratio
        self._create_slider_setting(
            ratios_card.content_frame,
            "Ratio Haut/Bas du Corps",
            "Répartition entre exercices haut et bas du corps",
            "upper_lower_ratio",
            0.3, 0.9, 0.1
        )

        # Core Frequency
        self._create_slider_setting(
            ratios_card.content_frame,
            "Fréquence Gainage",
            "Pourcentage minimum d'exercices de gainage/core",
            "core_frequency",
            0.0, 0.6, 0.1
        )

        # === CONTRAINTES ANTI-RÉPÉTITION ===
        constraints_card = GlassCard(muscle_tab, title="Contraintes Anti-Répétition")
        constraints_card.pack(fill="x", pady=(16, 0))

        # Max exercices consécutifs même muscle
        self._create_number_setting(
            constraints_card.content_frame,
            "Max Exercices Consécutifs (même muscle)",
            "Nombre maximum d'exercices consécutifs du même groupe musculaire",
            "max_consecutive_same_muscle",
            1, 5
        )

    def _create_format_rules_tab(self):
        """Onglet règles par format."""
        format_tab = self.main_tabs.add_tab("formats", "🎯 Règles par Format")

        # Sous-tabs pour chaque format
        format_subtabs = ModernTabView(format_tab)
        format_subtabs.pack(fill="both", expand=True)

        formats = ["AMRAP", "EMOM", "For Time", "Tabata"]

        for format_name in formats:
            format_content = format_subtabs.add_tab(format_name.lower(), format_name)
            self._create_format_settings(format_content, format_name)

    def _create_format_settings(self, parent, format_name: str):
        """Crée les paramètres pour un format spécifique."""

        # Paramètres du format
        settings_card = GlassCard(parent, title=f"Paramètres {format_name}")
        settings_card.pack(fill="x", pady=(0, 16))

        # Nombre optimal d'exercices
        self._create_number_setting(
            settings_card.content_frame,
            "Nombre Optimal d'Exercices",
            f"Nombre d'exercices recommandé pour les blocs {format_name}",
            f"format_optimal_exercises_{format_name.lower()}",
            1, 8
        )

        # Fourchette de répétitions
        reps_frame = ctk.CTkFrame(settings_card.content_frame, fg_color="transparent")
        reps_frame.pack(fill="x", pady=8)
        reps_frame.grid_columnconfigure(1, weight=1)
        reps_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            reps_frame,
            text="Fourchette de Répétitions:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        # Min reps
        self.format_min_reps = ctk.CTkEntry(reps_frame, width=60)
        self.format_min_reps.grid(row=0, column=1, sticky="ew", padx=4)

        ctk.CTkLabel(reps_frame, text="à").grid(row=0, column=2, padx=8)

        # Max reps
        self.format_max_reps = ctk.CTkEntry(reps_frame, width=60)
        self.format_max_reps.grid(row=0, column=3, sticky="ew", padx=4)

        # Patterns préférés
        patterns_card = GlassCard(parent, title="Patterns de Mouvement Préférés")
        patterns_card.pack(fill="x", pady=(16, 0))

        patterns = ["Push", "Pull", "Squat", "Hinge", "Carry", "Lunge", "Twist", "Jump"]
        self._create_checkbox_group(
            patterns_card.content_frame,
            patterns,
            f"format_patterns_{format_name.lower()}"
        )

    def _create_exercise_preferences_tab(self):
        """Onglet préférences d'exercices."""
        preferences_tab = self.main_tabs.add_tab("preferences", "❤️ Préférences d'Exercices")

        # Exercices favoris
        favorites_card = GlassCard(preferences_tab, title="Exercices Favoris")
        favorites_card.pack(fill="x", pady=(0, 16))

        # Contextes : warmup, strength, conditioning, finisher
        contexts = [
            ("warmup", "Échauffement"),
            ("strength", "Renforcement"),
            ("conditioning", "Conditioning"),
            ("finisher", "Finisher")
        ]

        for context_key, context_label in contexts:
            self._create_favorite_exercises_section(
                favorites_card.content_frame, context_key, context_label
            )

        # Exercices à éviter
        restrictions_card = GlassCard(preferences_tab, title="Restrictions d'Exercices")
        restrictions_card.pack(fill="x", pady=(16, 0))

        self._create_exercise_restrictions_section(restrictions_card.content_frame)

    def _create_equipment_management_tab(self):
        """Onglet gestion équipement."""
        equipment_tab = self.main_tabs.add_tab("equipment", "🏋️ Gestion Équipement")

        # Équipement disponible
        available_card = GlassCard(equipment_tab, title="Équipement Disponible")
        available_card.pack(fill="x", pady=(0, 16))

        equipment_list = [
            "Poids du corps", "Haltères", "Barre", "Kettlebell", "Élastiques",
            "Machine", "Poulie", "TRX", "Anneaux", "Banc", "Box", "Battle Ropes"
        ]

        self._create_checkbox_group(
            available_card.content_frame,
            equipment_list,
            "available_equipment"
        )

        # Paramètres temporels
        timing_card = GlassCard(equipment_tab, title="Paramètres Temporels")
        timing_card.pack(fill="x", pady=(16, 0))

        # Temps de transition
        self._create_number_setting(
            timing_card.content_frame,
            "Temps Transition (secondes)",
            "Temps de transition entre exercices",
            "transition_time_sec",
            15, 120
        )

        # Temps changement équipement
        self._create_number_setting(
            timing_card.content_frame,
            "Temps Changement Équipement (secondes)",
            "Temps alloué pour changer d'équipement",
            "equipment_change_sec",
            30, 180
        )

    def _create_advanced_settings_tab(self):
        """Onglet paramètres avancés."""
        advanced_tab = self.main_tabs.add_tab("advanced", "🧠 Paramètres Avancés")

        # Règles physiologiques
        physio_card = GlassCard(advanced_tab, title="Règles Physiologiques")
        physio_card.pack(fill="x", pady=(0, 16))

        # Max exercices haute intensité consécutifs
        self._create_number_setting(
            physio_card.content_frame,
            "Max Exercices Haute Intensité Consécutifs",
            "Éviter la surcharge métabolique",
            "max_consecutive_high_intensity",
            1, 4
        )

        # Ratio exercices de récupération
        self._create_slider_setting(
            physio_card.content_frame,
            "Ratio Exercices de Récupération",
            "Pourcentage d'exercices de récupération/mobilité",
            "recovery_exercise_ratio",
            0.0, 0.5, 0.05
        )

        # Apprentissage et historique
        learning_card = GlassCard(advanced_tab, title="Apprentissage Automatique")
        learning_card.pack(fill="x", pady=(16, 0))

        # Boutons d'action pour l'apprentissage
        learning_actions = ctk.CTkFrame(learning_card.content_frame, fg_color="transparent")
        learning_actions.pack(fill="x", pady=8)

        clear_history_btn = AnimatedButton(
            learning_actions,
            text="🗑️ Effacer Historique",
            command=self._clear_learning_history,
            fg_color=ctk.ThemeManager.theme["color"]["warning"]
        )
        clear_history_btn.pack(side="left", padx=(0, 8))

        export_config_btn = AnimatedButton(
            learning_actions,
            text="📤 Exporter Config",
            command=self._export_config
        )
        export_config_btn.pack(side="left", padx=(0, 8))

        import_config_btn = AnimatedButton(
            learning_actions,
            text="📥 Importer Config",
            command=self._import_config
        )
        import_config_btn.pack(side="left")

    def _create_footer_actions(self):
        """Crée les boutons d'action du footer."""
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x", pady=(20, 0))

        # Boutons alignés à droite
        actions_frame = ctk.CTkFrame(footer, fg_color="transparent")
        actions_frame.pack(side="right")

        # Reset defaults
        reset_btn = AnimatedButton(
            actions_frame,
            text="🔄 Valeurs par Défaut",
            command=self._reset_to_defaults,
            fg_color=ctk.ThemeManager.theme["color"]["warning"]
        )
        reset_btn.pack(side="left", padx=(0, 8))

        # Annuler
        cancel_btn = AnimatedButton(
            actions_frame,
            text="❌ Annuler",
            command=self._cancel_changes,
            fg_color="transparent",
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"]["subtle_border"]
        )
        cancel_btn.pack(side="left", padx=(0, 8))

        # Sauvegarder
        save_btn = AnimatedButton(
            actions_frame,
            text="💾 Sauvegarder",
            command=self._save_config,
            fg_color=ctk.ThemeManager.theme["color"]["success"]
        )
        save_btn.pack(side="left")

    def _create_slider_setting(
        self, parent, title: str, description: str, key: str,
        min_val: float, max_val: float, step: float
    ):
        """Crée un paramètre avec slider."""
        setting_frame = ctk.CTkFrame(parent, fg_color="transparent")
        setting_frame.pack(fill="x", pady=8)
        setting_frame.grid_columnconfigure(0, weight=1)

        # Titre et description
        info_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=(0, 16))

        title_label = ctk.CTkLabel(
            info_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w")

        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            wraplength=300
        )
        desc_label.pack(anchor="w")

        # Slider et valeur
        control_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        control_frame.grid(row=0, column=1, sticky="e")

        slider = ctk.CTkSlider(
            control_frame,
            from_=min_val,
            to=max_val,
            number_of_steps=int((max_val - min_val) / step),
            width=200
        )
        slider.pack(side="left", padx=(0, 8))

        value_label = ctk.CTkLabel(
            control_frame,
            text="0.6",
            width=50,
            font=ctk.CTkFont(weight="bold")
        )
        value_label.pack(side="left")

        # Callback pour mise à jour valeur
        def update_value(value):
            value_label.configure(text=f"{value:.2f}")

        slider.configure(command=update_value)

        # Stocker référence pour lecture ultérieure
        setattr(self, f"slider_{key}", slider)
        setattr(self, f"label_{key}", value_label)

    def _create_number_setting(self, parent, title: str, description: str, key: str, min_val: int, max_val: int):
        """Crée un paramètre numérique."""
        setting_frame = ctk.CTkFrame(parent, fg_color="transparent")
        setting_frame.pack(fill="x", pady=8)
        setting_frame.grid_columnconfigure(0, weight=1)

        # Titre et description
        info_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=(0, 16))

        title_label = ctk.CTkLabel(
            info_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w")

        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            wraplength=300
        )
        desc_label.pack(anchor="w")

        # Entry numérique
        entry = ctk.CTkEntry(
            setting_frame,
            width=80,
            placeholder_text=str(min_val)
        )
        entry.grid(row=0, column=1, sticky="e")

        # Stocker référence
        setattr(self, f"entry_{key}", entry)

    def _create_checkbox_group(self, parent, options: List[str], key: str):
        """Crée un groupe de checkboxes."""
        group_frame = ctk.CTkFrame(parent, fg_color="transparent")
        group_frame.pack(fill="both", expand=True, pady=8)

        # Organiser en colonnes
        cols = 3
        checkboxes = {}

        for i, option in enumerate(options):
            row = i // cols
            col = i % cols

            checkbox = ctk.CTkCheckBox(
                group_frame,
                text=option,
                font=ctk.CTkFont(size=12)
            )
            checkbox.grid(row=row, column=col, sticky="w", padx=8, pady=4)
            checkboxes[option] = checkbox

        # Stocker référence
        setattr(self, f"checkboxes_{key}", checkboxes)

    def _create_favorite_exercises_section(self, parent, context_key: str, context_label: str):
        """Crée une section pour les exercices favoris d'un contexte."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=8)

        # Header de section
        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{context_label}:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Bouton ajouter
        add_btn = AnimatedButton(
            header_frame,
            text="➕ Ajouter",
            width=80,
            height=24,
            command=lambda: self._add_favorite_exercise(context_key)
        )
        add_btn.grid(row=0, column=1, sticky="e")

        # Liste des favoris actuels
        favorites_list = ctk.CTkScrollableFrame(
            section_frame,
            height=60,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"]
        )
        favorites_list.pack(fill="x")

        # Stocker référence
        setattr(self, f"favorites_list_{context_key}", favorites_list)

    def _create_exercise_restrictions_section(self, parent):
        """Crée la section des restrictions d'exercices."""
        # Exercices bannis
        banned_frame = ctk.CTkFrame(parent, fg_color="transparent")
        banned_frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            banned_frame,
            text="Exercices Interdits:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w")

        self.banned_list = ctk.CTkScrollableFrame(
            banned_frame,
            height=80,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"]
        )
        self.banned_list.pack(fill="x", pady=(4, 0))

    def _load_current_config(self):
        """Charge la configuration actuelle dans l'interface."""

        # Charger ratios musculaires
        muscle_rules = self.config.muscle_balance_rules

        try:
            if hasattr(self, 'slider_push_pull_ratio'):
                self.slider_push_pull_ratio.set(muscle_rules.get("push_pull_ratio", 0.6))
            if hasattr(self, 'slider_upper_lower_ratio'):
                self.slider_upper_lower_ratio.set(muscle_rules.get("upper_lower_ratio", 0.7))
            if hasattr(self, 'slider_core_frequency'):
                self.slider_core_frequency.set(muscle_rules.get("core_frequency", 0.3))
            if hasattr(self, 'entry_max_consecutive_same_muscle'):
                self.entry_max_consecutive_same_muscle.insert(0, str(muscle_rules.get("max_consecutive_same_muscle", 2)))
        except Exception as e:
            self.logger.warning(f"Erreur lors du chargement de la config: {e}")

        # TODO: Charger autres sections selon implémentation complète

        show_toast(self, "Configuration chargée", "success", 2000)

    def _save_config(self):
        """Sauvegarde la configuration."""
        try:
            # Collecter valeurs depuis interface
            updated_config = self._collect_config_from_ui()

            # Mettre à jour config
            self._apply_config_updates(updated_config)

            # Sauvegarder
            self.config_service.save_config()

            # Feedback utilisateur
            self.config_status.update_status("success", "Configuration sauvegardée")
            show_toast(self, "Configuration sauvegardée avec succès", "success", 3000)

        except Exception as e:
            show_toast(self, f"Erreur lors de la sauvegarde: {str(e)}", "error", 4000)

    def _collect_config_from_ui(self) -> Dict[str, Any]:
        """Collecte la configuration depuis l'interface."""
        config_updates = {}

        # Ratios musculaires
        muscle_balance = {}
        try:
            if hasattr(self, 'slider_push_pull_ratio'):
                muscle_balance["push_pull_ratio"] = self.slider_push_pull_ratio.get()
            if hasattr(self, 'slider_upper_lower_ratio'):
                muscle_balance["upper_lower_ratio"] = self.slider_upper_lower_ratio.get()
            if hasattr(self, 'slider_core_frequency'):
                muscle_balance["core_frequency"] = self.slider_core_frequency.get()
            if hasattr(self, 'entry_max_consecutive_same_muscle'):
                muscle_balance["max_consecutive_same_muscle"] = int(self.entry_max_consecutive_same_muscle.get() or 2)
        except (ValueError, AttributeError):
            pass  # Garder valeurs par défaut

        if muscle_balance:
            config_updates["muscle_balance_rules"] = muscle_balance

        # TODO: Collecter autres sections

        return config_updates

    def _apply_config_updates(self, updates: Dict[str, Any]):
        """Applique les mises à jour à la configuration."""
        if "muscle_balance_rules" in updates:
            self.config.muscle_balance_rules.update(updates["muscle_balance_rules"])

        # TODO: Appliquer autres updates

    def _cancel_changes(self):
        """Annule les modifications."""
        self._load_current_config()
        show_toast(self, "Modifications annulées", "info", 2000)

    def _reset_to_defaults(self):
        """Remet les paramètres par défaut."""
        # Confirmation
        def confirm_reset():
            self.config_service.reset_to_defaults()
            self.config = self.config_service.get_config()
            self._load_current_config()
            show_toast(self, "Paramètres remis par défaut", "success", 3000)

        # TODO: Implémenter dialogue de confirmation
        confirm_reset()

    def _clear_learning_history(self):
        """Efface l'historique d'apprentissage."""
        self.config.learning_preferences = {"successful_combinations": {}, "client_feedback_weights": {}}
        show_toast(self, "Historique d'apprentissage effacé", "info", 2000)

    def _export_config(self):
        """Exporte la configuration."""
        # TODO: Implémenter dialogue de sauvegarde fichier
        show_toast(self, "Export de configuration (à implémenter)", "info", 2000)

    def _import_config(self):
        """Importe une configuration."""
        # TODO: Implémenter dialogue d'ouverture fichier
        show_toast(self, "Import de configuration (à implémenter)", "info", 2000)

    def _add_favorite_exercise(self, context: str):
        """Ajoute un exercice favori."""
        # TODO: Implémenter sélecteur d'exercice
        show_toast(self, f"Ajout exercice favori pour {context} (à implémenter)", "info", 2000)
