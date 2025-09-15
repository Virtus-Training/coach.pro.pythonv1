"""Nouveau formulaire pour la génération de séances collectives."""

import customtkinter as ctk

from ui.components.design_system.buttons import PrimaryButton
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle

# Types de cours (affichage) demandés
COURSE_TYPES_DISPLAY = [
    "Hyrox",
    "Crossfit",
    "CAF",
    "Core and glutes",
    "TRX",
]

# Mapping affichage -> valeurs attendues par les services
COURSE_TYPE_VALUE_MAP = {
    "Crossfit": "Cross-Training",
    "Core and glutes": "Core & Glutes",
}

# Options par défaut
DURATIONS = ["30", "45", "60", "90"]
DEFAULT_EQUIPMENTS = [
    "Haltères",
    "Barre",
    "Kettlebell",
    "Poids du corps",
    "Machine",
    "Élastiques",
    "TRX/anneaux",
    "Box",
    "Rameur",
    "Ski",
    "Sled",
]
FORMATS = [
    "EMOM",
    "AMRAP",
    "For Time",
    "SETSxREPS",
    "Circuit",
    "Intervalles",
    "Chipper",
    "Skill",  # Nouveau format pour travail technique
]
FOCUS_OPTIONS = ["Upper", "Lower", "Full-body", "Push", "Pull"]
OBJECTIVE_OPTIONS = [
    "Force",
    "Endurance",
    "Technique",
    "Dépense calorique",
    "Hypertrophie",
]
AUTO_INCLUDE_OPTIONS = ["Échauffement", "Finisher", "Retour au calme"]


class FormCollectif(Card):
    """Formulaire détaillé pour générer une séance collective."""

    def __init__(
        self,
        parent,
        button_parent=None,
        generate_callback=None,
        equipment_options: list[str] | None = None,
    ) -> None:
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

        equipment_options = equipment_options or DEFAULT_EQUIPMENTS

        # En-tête avec indicateurs visuels
        header_frame = ctk.CTkFrame(
            self, fg_color=("gray95", "gray20"), corner_radius=12
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 12))
        header_frame.grid_columnconfigure(0, weight=1)

        CardTitle(header_frame, text="🎯 Configuration de séance").grid(
            row=0, column=0, sticky="w", padx=16, pady=(12, 4)
        )

        # Sous-titre informatif
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Personnalisez votre entraînement selon vos objectifs",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        # Section paramètres principaux avec styling moderne
        main_params_frame = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        main_params_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        main_params_frame.grid_columnconfigure((0, 1), weight=1)

        # Type de séance
        ctk.CTkLabel(
            main_params_frame, text="🏋️ Type de séance", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))
        self.course_type_var = ctk.StringVar(value="Crossfit")
        course_menu = ctk.CTkOptionMenu(
            main_params_frame,
            variable=self.course_type_var,
            values=COURSE_TYPES_DISPLAY,
            fg_color=("gray90", "gray25"),
            button_color=("gray80", "gray30"),
        )
        course_menu.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

        # Durée avec indicateur visuel
        ctk.CTkLabel(
            main_params_frame, text="⏱️ Durée", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=1, sticky="w", padx=16, pady=(12, 4))
        self.duration_var = ctk.StringVar(value="45")
        duration_menu = ctk.CTkOptionMenu(
            main_params_frame,
            variable=self.duration_var,
            values=DURATIONS,
            fg_color=("gray90", "gray25"),
            button_color=("gray80", "gray30"),
        )
        duration_menu.grid(row=1, column=1, sticky="ew", padx=16, pady=(0, 12))

        # Section Intensité avec design moderne
        intensity_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        intensity_section.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        intensity_section.grid_columnconfigure(0, weight=1)

        # En-tête avec icône
        intensity_header = ctk.CTkFrame(intensity_section, fg_color="transparent")
        intensity_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))
        CardTitle(intensity_header, text="🔥 Intensité de la séance").pack(side="left")

        # Contrôle
        intensity_controls = ctk.CTkFrame(intensity_section, fg_color="transparent")
        intensity_controls.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        intensity_controls.grid_columnconfigure(0, weight=1)

        self.intensity_var = ctk.StringVar(value="Moyenne")
        intensity_options = ["Légère", "Moyenne", "Élevée", "Maximale"]
        intensity_menu = ctk.CTkOptionMenu(
            intensity_controls,
            variable=self.intensity_var,
            values=intensity_options,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("gray90", "gray25"),
            button_color=("gray80", "gray30"),
        )
        intensity_menu.grid(row=0, column=0, sticky="ew")

        # Section équipement avec design moderne
        equip_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        equip_section.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))

        # En-tête équipement
        equip_header = ctk.CTkFrame(equip_section, fg_color="transparent")
        equip_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))

        CardTitle(equip_header, text="🏋️‍♀️ Équipement disponible").pack(side="left")

        # Compteur d'équipement sélectionné
        self.equip_count_label = ctk.CTkLabel(
            equip_header,
            text="(0 sélectionnés)",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.equip_count_label.pack(side="right")
        equip_grid = ctk.CTkFrame(equip_section, fg_color="transparent")
        equip_grid.grid(row=1, column=0, sticky="ew")
        equip_grid.grid_columnconfigure((0, 1), weight=1)
        self.equipment_vars: dict[str, ctk.BooleanVar] = {}
        for idx, label in enumerate(equipment_options):
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(
                equip_grid,
                text=label,
                variable=var,
                command=self._update_equipment_count,
            )
            checkbox.grid(row=idx // 2, column=idx % 2, sticky="w", padx=8, pady=6)
            self.equipment_vars[label] = var

        # Ajouter padding au bas de la section équipement
        ctk.CTkFrame(equip_section, height=12, fg_color="transparent").grid(
            row=2, column=0
        )

        # Section Variabilité avec design moderne
        variability_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        variability_section.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))
        variability_section.grid_columnconfigure(1, weight=1)

        # En-tête avec icône et description
        var_header = ctk.CTkFrame(variability_section, fg_color="transparent")
        var_header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 8)
        )
        CardTitle(var_header, text="🔀 Variabilité").pack(side="left")

        # Contrôle avec valeur affichée
        var_controls = ctk.CTkFrame(variability_section, fg_color="transparent")
        var_controls.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        var_controls.grid_columnconfigure(1, weight=1)

        self.variability_var = ctk.DoubleVar(value=50)
        self.variability_value_label = ctk.CTkLabel(
            var_controls, text="50%", font=ctk.CTkFont(weight="bold")
        )
        self.variability_value_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        variability_slider = ctk.CTkSlider(
            var_controls,
            from_=0,
            to=100,
            variable=self.variability_var,
            command=self._update_variability_display,
        )
        variability_slider.grid(row=0, column=1, sticky="ew")

        # Section Volume avec design moderne
        volume_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        volume_section.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 12))
        volume_section.grid_columnconfigure(1, weight=1)

        # En-tête avec icône et description
        vol_header = ctk.CTkFrame(volume_section, fg_color="transparent")
        vol_header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 8)
        )
        CardTitle(vol_header, text="📊 Volume d'entraînement").pack(side="left")

        # Contrôle avec valeur affichée
        vol_controls = ctk.CTkFrame(volume_section, fg_color="transparent")
        vol_controls.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        vol_controls.grid_columnconfigure(1, weight=1)

        self.volume_var = ctk.DoubleVar(value=50)
        self.volume_value_label = ctk.CTkLabel(
            vol_controls, text="50%", font=ctk.CTkFont(weight="bold")
        )
        self.volume_value_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        volume_slider = ctk.CTkSlider(
            vol_controls,
            from_=0,
            to=100,
            variable=self.volume_var,
            command=self._update_volume_display,
        )
        volume_slider.grid(row=0, column=1, sticky="ew")

        # Note: Section formats supprimée - gérée par la structure personnalisée

        # Section Continuum avec design moderne
        continuum_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        continuum_section.grid(row=7, column=0, sticky="ew", padx=16, pady=(0, 12))
        continuum_section.grid_columnconfigure(1, weight=1)

        # En-tête avec icône et description
        cont_header = ctk.CTkFrame(continuum_section, fg_color="transparent")
        cont_header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 8)
        )
        CardTitle(cont_header, text="⚡ Continuum Cardio → Renforcement").pack(
            side="left"
        )

        # Contrôle avec valeur affichée
        cont_controls = ctk.CTkFrame(continuum_section, fg_color="transparent")
        cont_controls.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        cont_controls.grid_columnconfigure(1, weight=1)

        self.continuum_var = ctk.DoubleVar(value=0)
        self.continuum_value_label = ctk.CTkLabel(
            cont_controls, text="Équilibré", font=ctk.CTkFont(weight="bold")
        )
        self.continuum_value_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        continuum_slider = ctk.CTkSlider(
            cont_controls,
            from_=-100,
            to=100,
            variable=self.continuum_var,
            command=self._update_continuum_display,
        )
        continuum_slider.grid(row=0, column=1, sticky="ew")

        # Section Focus avec design moderne
        focus_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        focus_section.grid(row=8, column=0, sticky="ew", padx=16, pady=(0, 12))
        focus_section.grid_columnconfigure(1, weight=1)

        # En-tête avec icône
        focus_header = ctk.CTkFrame(focus_section, fg_color="transparent")
        focus_header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 8)
        )
        CardTitle(focus_header, text="🎯 Focus musculation").pack(side="left")

        # Contrôle
        focus_controls = ctk.CTkFrame(focus_section, fg_color="transparent")
        focus_controls.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        focus_controls.grid_columnconfigure(0, weight=1)

        self.focus_var = ctk.StringVar(value="Full-body")
        focus_menu = ctk.CTkOptionMenu(
            focus_controls,
            variable=self.focus_var,
            values=FOCUS_OPTIONS,
            font=ctk.CTkFont(weight="bold"),
        )
        focus_menu.grid(row=0, column=0, sticky="ew")

        # Section Objectif avec design moderne
        objective_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        objective_section.grid(row=9, column=0, sticky="ew", padx=16, pady=(0, 12))
        objective_section.grid_columnconfigure(1, weight=1)

        # En-tête avec icône
        obj_header = ctk.CTkFrame(objective_section, fg_color="transparent")
        obj_header.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 8)
        )
        CardTitle(obj_header, text="🏆 Objectif principal").pack(side="left")

        # Contrôle
        obj_controls = ctk.CTkFrame(objective_section, fg_color="transparent")
        obj_controls.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        obj_controls.grid_columnconfigure(0, weight=1)

        self.objective_var = ctk.StringVar(value="Force")
        objective_menu = ctk.CTkOptionMenu(
            obj_controls,
            variable=self.objective_var,
            values=OBJECTIVE_OPTIONS,
            font=ctk.CTkFont(weight="bold"),
        )
        objective_menu.grid(row=0, column=0, sticky="ew")

        # Section Auto-inclusion avec design moderne
        auto_section = ctk.CTkFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        auto_section.grid(row=10, column=0, sticky="ew", padx=16, pady=(0, 12))

        # En-tête avec icône
        auto_header = ctk.CTkFrame(auto_section, fg_color="transparent")
        auto_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))
        CardTitle(auto_header, text="✨ Inclure automatiquement").pack(side="left")

        # Grid pour les options
        auto_grid = ctk.CTkFrame(auto_section, fg_color="transparent")
        auto_grid.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.auto_vars: dict[str, ctk.BooleanVar] = {}
        for idx, opt in enumerate(AUTO_INCLUDE_OPTIONS):
            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(
                auto_grid, text=opt, variable=var, font=ctk.CTkFont(size=12)
            )
            checkbox.grid(row=idx, column=0, sticky="w", padx=8, pady=6)
            self.auto_vars[opt] = var

        # Blocs personnalisés (optionnel)
        custom_section = ctk.CTkFrame(self, fg_color="transparent")
        custom_section.grid(row=12, column=0, sticky="ew", padx=16, pady=(8, 8))

        # En-tête avec icône
        header_frame = ctk.CTkFrame(custom_section, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        CardTitle(header_frame, text="Structure personnalisée").pack(side="left")

        # Toggle avec description
        toggle_frame = ctk.CTkFrame(
            custom_section, fg_color=("gray90", "gray20"), corner_radius=8
        )
        toggle_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        toggle_frame.grid_columnconfigure(0, weight=1)

        self.use_custom_blocks = ctk.BooleanVar(value=False)
        toggle_checkbox = ctk.CTkCheckBox(
            toggle_frame,
            text="Créer une structure sur mesure",
            variable=self.use_custom_blocks,
            command=self._toggle_custom_blocks,
            font=ctk.CTkFont(weight="bold"),
        )
        toggle_checkbox.grid(row=0, column=0, sticky="w", padx=12, pady=8)

        help_label = ctk.CTkLabel(
            toggle_frame,
            text="Définissez manuellement le nombre et le type de chaque bloc",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        help_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        # Zone des blocs (masquée par défaut)
        self.blocks_wrap = ctk.CTkFrame(custom_section, fg_color="transparent")
        self.blocks_wrap.grid(row=2, column=0, sticky="ew")
        self.blocks_wrap.grid_remove()

        # Contrôles: nombre de blocs avec style amélioré
        self.block_count_var = ctk.StringVar(value="3")
        count_frame = ctk.CTkFrame(
            self.blocks_wrap, fg_color=("gray95", "gray15"), corner_radius=6
        )
        count_frame.pack(fill="x", pady=(0, 12))

        count_row = ctk.CTkFrame(count_frame, fg_color="transparent")
        count_row.pack(fill="x", padx=12, pady=8)

        ctk.CTkLabel(
            count_row, text="Nombre de blocs:", font=ctk.CTkFont(weight="bold")
        ).pack(side="left")
        self.block_count_cb = ctk.CTkComboBox(
            count_row,
            values=[str(i) for i in range(1, 7)],
            variable=self.block_count_var,
            width=80,
            command=self._on_block_count_change,
        )
        self.block_count_cb.pack(side="left", padx=(8, 0))

        # Éditeur de blocs
        self.blocks_editor = ctk.CTkFrame(self.blocks_wrap, fg_color="transparent")
        self.blocks_editor.pack(fill="x")
        self._blocks_rows: list[tuple[ctk.StringVar, ctk.StringVar]] = []
        self._rebuild_blocks_editor()

        # Bouton d'action (dans la zone fixe si fournie, sinon dans le formulaire)
        button_container = button_parent if button_parent is not None else self
        if button_parent is not None:
            # Bouton dans la zone fixe
            PrimaryButton(
                button_container, text="Générer la séance", command=generate_callback
            ).pack(fill="x", padx=16, pady=8)
        else:
            # Bouton dans le formulaire (comportement par défaut)
            PrimaryButton(
                button_container, text="Générer la séance", command=generate_callback
            ).grid(row=12, column=0, sticky="ew", padx=16, pady=(0, 16))

    def get_params(self) -> dict:
        """Retourne les valeurs du formulaire sous forme de dictionnaire."""
        payload = {
            "course_type": COURSE_TYPE_VALUE_MAP.get(
                self.course_type_var.get(), self.course_type_var.get()
            ),
            "duration": int(self.duration_var.get()),
            "equipment": [k for k, v in self.equipment_vars.items() if v.get()],
            "variability": int(self.variability_var.get()),
            "volume": int(self.volume_var.get()),
            "continuum": int(self.continuum_var.get()),
            "focus": self.focus_var.get(),
            "objective": self.objective_var.get(),
            "auto_include": [k for k, v in self.auto_vars.items() if v.get()],
            "intensity": self.intensity_var.get(),
        }

        if getattr(self, "use_custom_blocks", None) and self.use_custom_blocks.get():
            blocks: list[dict] = []
            blocks_rows = getattr(self, "_blocks_rows", [])

            for i, (fmt_var, dur_var) in enumerate(blocks_rows):
                try:
                    dur = int(dur_var.get())
                except Exception:
                    dur = 10

                block_type = fmt_var.get() or "AMRAP"
                blocks.append({"type": block_type, "duration_min": dur})

            payload["custom_blocks"] = blocks

        return payload

    def _toggle_custom_blocks(self):
        if self.use_custom_blocks.get():
            self.blocks_wrap.grid()
        else:
            self.blocks_wrap.grid_remove()

    def _on_block_count_change(self, value=None):
        """Callback appelé quand le nombre de blocs change."""
        # Forcer la synchronisation si une valeur est passée
        if value is not None:
            self.block_count_var.set(value)

        # Petit délai pour s'assurer que l'UI est prête
        self.after(10, self._rebuild_blocks_editor)

    def _rebuild_blocks_editor(self):
        # Nettoyer complètement l'éditeur
        for w in self.blocks_editor.winfo_children():
            w.destroy()
        self._blocks_rows.clear()

        # Forcer un rafraîchissement de l'interface
        self.blocks_editor.update_idletasks()

        try:
            n = int(self.block_count_var.get())
        except Exception:
            n = 3

        for i in range(max(1, min(6, n))):
            # Container pour chaque bloc avec styling amélioré
            block_container = ctk.CTkFrame(
                self.blocks_editor, fg_color=("gray92", "gray14"), corner_radius=8
            )
            block_container.pack(fill="x", pady=6, padx=4)
            block_container.grid_columnconfigure(1, weight=1)

            # Configuration intelligente par défaut selon position
            default_format = self._get_default_format_for_position(i, n)
            default_duration = self._get_default_duration_for_position(i, n)

            # Label avec icône selon type de bloc
            block_icon = self._get_block_icon(i, n)
            ctk.CTkLabel(
                block_container,
                text=f"{block_icon} Bloc {i + 1}",
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(8, 4))

            # Ligne de configuration
            ctk.CTkLabel(block_container, text="Format:").grid(
                row=1, column=0, sticky="w", padx=(12, 4), pady=(0, 8)
            )
            fmt_var = ctk.StringVar(value=default_format)
            format_menu = ctk.CTkOptionMenu(
                block_container, variable=fmt_var, values=FORMATS, width=120
            )
            format_menu.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 8))

            # Durée avec validation
            duration_frame = ctk.CTkFrame(block_container, fg_color="transparent")
            duration_frame.grid(row=1, column=2, sticky="e", padx=(0, 12), pady=(0, 8))
            ctk.CTkLabel(duration_frame, text="Durée:").pack(side="left", padx=(0, 4))
            dur_var = ctk.StringVar(value=str(default_duration))
            dur_entry = ctk.CTkEntry(duration_frame, textvariable=dur_var, width=50)
            dur_entry.pack(side="left")
            ctk.CTkLabel(duration_frame, text="min", font=ctk.CTkFont(size=11)).pack(
                side="left", padx=(2, 0)
            )

            self._blocks_rows.append((fmt_var, dur_var))

        # Forcer un dernier rafraîchissement
        self.blocks_editor.update_idletasks()

    def _get_default_format_for_position(self, position: int, total: int) -> str:
        """Retourne un format par défaut intelligent selon la position dans la séance."""
        if position == 0:
            return "SETSxREPS"  # Warmup/activation
        elif position == total - 1 and total > 1:
            return "EMOM"  # Finisher
        else:
            return "AMRAP"  # Main work

    def _get_default_duration_for_position(self, position: int, total: int) -> int:
        """Retourne une durée par défaut intelligente selon la position."""
        if position == 0:
            return 8  # Warmup plus court
        elif position == total - 1 and total > 1:
            return 5  # Finisher court et intense
        else:
            return 15  # Main work plus long

    def _get_block_icon(self, position: int, total: int) -> str:
        """Retourne une icône appropriée selon le type de bloc."""
        if position == 0:
            return "[WU]"  # Warmup
        elif position == total - 1 and total > 1:
            return "[FN]"  # Finisher
        else:
            return "[MW]"  # Main work

    def _update_equipment_count(self):
        """Met à jour le compteur d'équipement sélectionné."""
        count = sum(1 for var in self.equipment_vars.values() if var.get())
        self.equip_count_label.configure(
            text=f"({count} sélectionné{'s' if count > 1 else ''})"
        )

    def _update_variability_display(self, value):
        """Met à jour l'affichage de la valeur de variabilité."""
        self.variability_value_label.configure(text=f"{int(float(value))}%")

    def _update_volume_display(self, value):
        """Met à jour l'affichage de la valeur de volume."""
        self.volume_value_label.configure(text=f"{int(float(value))}%")

    def _update_continuum_display(self, value):
        """Met à jour l'affichage de la valeur de continuum."""
        val = int(float(value))
        if val < -50:
            text = "Cardio"
        elif val > 50:
            text = "Renforcement"
        else:
            text = "Équilibré"
        self.continuum_value_label.configure(text=text)


__all__ = ["FormCollectif"]
