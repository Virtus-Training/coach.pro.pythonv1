"""
Formulaire modernisé pour la création/modification d'exercices.
Inspiré des meilleures pratiques UI/UX des apps fitness modernes.
"""

from __future__ import annotations

import tkinter as tk
from typing import Callable, List, Optional

import customtkinter as ctk

from models.exercices import Exercise
from ui.components.design_system import (
    AccordionSection,
    ChipCheckboxGroup,
    ChipRadioGroup,
)

# Constantes réutilisées
MUSCLE_GROUPS = [
    "Poitrine",
    "Dos",
    "Épaules",
    "Jambes",
    "Fessiers",
    "Biceps",
    "Triceps",
    "Abdominaux",
    "Lombaires",
    "Mollets",
    "Avant-bras",
]

EQUIPMENT_OPTIONS = [
    "Poids du corps",
    "Haltères",
    "Barre",
    "Kettlebell",
    "Élastiques",
    "Machine",
    "Poulie",
    "TRX",
    "Anneaux",
    "Banc",
]

TAG_OPTIONS = [
    "Unilatéral",
    "Bilatéral",
    "Explosif",
    "Tempo lent",
    "Isométrie",
    "Mobilité",
]
COURSE_TAGS = ["CAF", "Core & Glutes", "Cross-Training", "Crossfit", "Hyrox", "TRX"]
MOVEMENT_PATTERNS = [
    "Push",
    "Pull",
    "Squat",
    "Hinge",
    "Carry",
    "Lunge",
    "Twist",
    "Gait",
    "Jump",
]
EFFORT_TYPES = ["Force", "Hypertrophie", "Endurance", "Cardio", "Technique", "Mobilité"]
MOVEMENT_CATEGORIES = ["Polyarticulaire", "Isolation", "Gainage"]


class ModernExerciseForm(ctk.CTkToplevel):
    """Formulaire d'exercice modernisé avec UX améliorée."""

    def __init__(
        self, master, on_submit: Callable, exercise: Optional[Exercise] = None
    ):
        super().__init__(
            master, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )

        self._on_submit = on_submit
        self._is_edit_mode = exercise is not None
        self._setup_window()
        self._create_ui()
        self._bind_events()

        if exercise:
            self._populate_form(exercise)

        self._update_summary()
        self._update_submit_state()
        self._setup_modal_behavior()

    def _setup_window(self):
        """Configuration de la fenêtre."""
        title = "✏️ Modifier l'exercice" if self._is_edit_mode else "✨ Nouvel exercice"
        self.title(title)
        self.geometry("900x750")
        self.minsize(700, 600)
        self.resizable(True, True)

    def _create_ui(self):
        """Création de l'interface utilisateur."""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header moderne
        self._create_header(main_container)

        # Layout principal 2 colonnes
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Colonne principale (formulaire)
        self._create_main_form(content_frame)

        # Sidebar (aperçu temps réel)
        self._create_sidebar(content_frame)

        # Footer avec actions
        self._create_footer(main_container)

    def _create_header(self, parent):
        """Header avec badge de mode et titre."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x")

        # Badge de mode
        badge_color = "#3B82F6" if self._is_edit_mode else "#10B981"
        badge_text = "MODIFICATION" if self._is_edit_mode else "CRÉATION"

        mode_badge = ctk.CTkLabel(
            header,
            text=badge_text,
            fg_color=badge_color,
            corner_radius=12,
            padx=12,
            pady=6,
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        mode_badge.pack(side="left")

        # Titre principal
        title = ctk.CTkLabel(
            header,
            text="Configuration de l'exercice",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
        title.pack(side="left", padx=(16, 0))

    def _create_main_form(self, parent):
        """Formulaire principal avec sections organisées."""
        self.form_container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_button_color=ctk.ThemeManager.theme["color"].get(
                "surface_light", "#374151"
            ),
        )
        self.form_container.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        # === SECTION ESSENTIELLE ===
        essentials = self._create_section_card(
            "🎯 Informations essentielles", always_open=True
        )

        # Nom avec validation visuelle
        self._create_name_field(essentials)

        # Groupe musculaire principal
        self.grp_groupe = ChipRadioGroup(
            essentials,
            label="Groupe musculaire principal *",
            options=MUSCLE_GROUPS,
            helper="Muscle principalement sollicité",
            selected_color="#10B981",
            on_change=self._on_field_change,
        )
        self.grp_groupe.pack(fill="x", pady=(16, 0))

        # === SECTION MOUVEMENT ===
        movement = self._create_section_card(
            "🏃 Caractéristiques du mouvement", always_open=True
        )

        self.grp_pattern = ChipRadioGroup(
            movement,
            label="Pattern de mouvement",
            options=MOVEMENT_PATTERNS,
            helper="Type de mouvement biomécanique",
            selected_color="#3B82F6",
            on_change=self._on_field_change,
        )
        self.grp_pattern.pack(fill="x", pady=(0, 12))

        self.grp_type = ChipRadioGroup(
            movement,
            label="Type d'effort",
            options=EFFORT_TYPES,
            helper="Objectif principal de l'exercice",
            selected_color="#8B5CF6",
            on_change=self._on_field_change,
        )
        self.grp_type.pack(fill="x")

        # === SECTIONS AVANCÉES (accordéons) ===
        self._create_equipment_section()
        self._create_tags_section()
        self._create_advanced_section()

    def _create_section_card(
        self, title: str, always_open: bool = False
    ) -> ctk.CTkFrame:
        """Crée une carte de section moderne."""
        if always_open:
            section = ctk.CTkFrame(
                self.form_container,
                fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
                corner_radius=12,
                border_width=1,
                border_color=ctk.ThemeManager.theme["color"].get(
                    "surface_light", "#374151"
                ),
            )
            section.pack(fill="x", pady=(0, 16))

            # Header de section
            header = ctk.CTkFrame(section, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=(16, 8))

            ctk.CTkLabel(
                header,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            ).pack(anchor="w")

            # Container pour le contenu
            content = ctk.CTkFrame(section, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=20, pady=(0, 16))
            return content
        else:
            # Utilise AccordionSection existant
            accordion = AccordionSection(
                self.form_container, title=title, initially_open=False
            )
            accordion.pack(fill="x", pady=(0, 16))
            return accordion.body

    def _create_name_field(self, parent):
        """Champ nom avec validation visuelle."""
        name_container = ctk.CTkFrame(parent, fg_color="transparent")
        name_container.pack(fill="x", pady=(0, 16))

        # Label avec indicateur requis
        label_frame = ctk.CTkFrame(name_container, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(
            label_frame,
            text="Nom de l'exercice",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        ).pack(side="left")

        ctk.CTkLabel(
            label_frame,
            text="*",
            text_color="#EF4444",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=(4, 0))

        # Entry avec style moderne
        self.in_nom = ctk.CTkEntry(
            name_container,
            placeholder_text="Ex: Développé couché haltères",
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=8,
        )
        self.in_nom.pack(fill="x")

        # Indicateur de validation
        self.name_status = ctk.CTkLabel(
            name_container, text="", font=ctk.CTkFont(size=11), height=20
        )
        self.name_status.pack(fill="x", pady=(4, 0))

    def _create_equipment_section(self):
        """Section équipements."""
        equipment_section = self._create_section_card(
            "🏋️ Équipements", always_open=False
        )

        self.grp_equip = ChipCheckboxGroup(
            equipment_section,
            label="Matériel requis",
            options=EQUIPMENT_OPTIONS,
            helper="Sélection multiple possible",
            selected_color="#F59E0B",
            on_change=self._on_field_change,
        )
        self.grp_equip.pack(fill="x")

    def _create_tags_section(self):
        """Section tags et cours collectifs."""
        tags_section = self._create_section_card("🏷️ Tags et cours", always_open=False)

        self.grp_course = ChipCheckboxGroup(
            tags_section,
            label="Cours collectifs",
            options=COURSE_TAGS,
            helper="Types de cours où cet exercice est utilisé",
            selected_color="#F97316",
            on_change=self._on_field_change,
        )
        self.grp_course.pack(fill="x", pady=(0, 12))

        self.grp_tags = ChipCheckboxGroup(
            tags_section,
            label="Tags spécialisés",
            options=TAG_OPTIONS,
            helper="Caractéristiques particulières",
            selected_color="#EC4899",
            on_change=self._on_field_change,
        )
        self.grp_tags.pack(fill="x")

    def _create_advanced_section(self):
        """Section paramètres avancés."""
        advanced_section = self._create_section_card(
            "⚙️ Paramètres avancés", always_open=False
        )

        # Catégorie de mouvement
        self.grp_category = ChipRadioGroup(
            advanced_section,
            label="Catégorie de mouvement",
            options=MOVEMENT_CATEGORIES,
            helper="Classification biomécanique",
            selected_color="#059669",
            on_change=self._on_field_change,
        )
        self.grp_category.pack(fill="x", pady=(0, 16))

        # Paramètres numériques
        params_frame = ctk.CTkFrame(advanced_section, fg_color="transparent")
        params_frame.pack(fill="x")
        params_frame.grid_columnconfigure(1, weight=1)

        # Switch chargeable
        self.var_charge = ctk.BooleanVar(value=False)
        self.sw_charge = ctk.CTkSwitch(
            params_frame,
            text="Exercice chargeable",
            variable=self.var_charge,
            command=self._on_field_change,
        )
        self.sw_charge.grid(row=0, column=0, sticky="w", pady=8)

        # Coefficient de volume
        coeff_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        coeff_frame.grid(row=0, column=1, sticky="ew", padx=(16, 0))

        ctk.CTkLabel(
            coeff_frame, text="Coefficient de volume", font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        self.in_coeff = ctk.CTkEntry(
            coeff_frame, placeholder_text="1.0", width=80, font=ctk.CTkFont(size=12)
        )
        self.in_coeff.pack(fill="x", pady=(2, 0))

    def _create_sidebar(self, parent):
        """Sidebar avec aperçu temps réel."""
        sidebar = ctk.CTkFrame(
            parent,
            corner_radius=12,
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"].get(
                "surface_light", "#374151"
            ),
        )
        sidebar.grid(row=0, column=1, sticky="nsew")

        # Header du sidebar
        sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_header.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            sidebar_header,
            text="🎯 Aperçu en temps réel",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        ).pack(anchor="w")

        # Zone de summary avec scroll
        self.summary_frame = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent", height=400
        )
        self.summary_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _create_footer(self, parent):
        """Footer avec boutons d'action."""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x", pady=(20, 0))

        # Boutons alignés à droite
        btn_container = ctk.CTkFrame(footer, fg_color="transparent")
        btn_container.pack(side="right")

        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            btn_container,
            text="Annuler",
            command=self.destroy,
            fg_color="transparent",
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"].get(
                "surface_light", "#374151"
            ),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            hover_color=ctk.ThemeManager.theme["color"].get("surface_light", "#374151"),
            font=ctk.CTkFont(size=13),
        )
        cancel_btn.pack(side="left", padx=(0, 8))

        # Bouton Valider + Nouveau (si création)
        if not self._is_edit_mode:
            self.btn_submit_new = ctk.CTkButton(
                btn_container,
                text="Valider + Nouveau",
                command=lambda: self._submit(reset_after=True),
                fg_color="#6366F1",
                hover_color="#4F46E5",
                font=ctk.CTkFont(size=13, weight="bold"),
            )
            self.btn_submit_new.pack(side="left", padx=(0, 8))

        # Bouton Valider principal
        self.btn_submit = ctk.CTkButton(
            btn_container,
            text="Valider",
            command=self._submit,
            fg_color="#10B981",
            hover_color="#059669",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=100,
        )
        self.btn_submit.pack(side="left")

    def _bind_events(self):
        """Configuration des événements clavier et validation."""
        self.in_nom.bind("<KeyRelease>", self._on_name_change)
        self.in_coeff.bind("<KeyRelease>", self._on_field_change)

        # Raccourcis clavier
        self.bind("<Control-Return>", lambda e: self._submit())
        self.bind("<Escape>", lambda e: self.destroy())

        # Focus sur nom au démarrage
        self.after(100, lambda: self.in_nom.focus_set())

    def _on_name_change(self, event=None):
        """Validation temps réel du nom."""
        name = self.in_nom.get().strip()
        if not name:
            self.name_status.configure(text="⚠️ Nom requis", text_color="#EF4444")
        elif len(name) < 3:
            self.name_status.configure(text="⚠️ Nom trop court", text_color="#F59E0B")
        else:
            self.name_status.configure(text="✅ Nom valide", text_color="#10B981")

        self._on_field_change()

    def _on_field_change(self, _=None):
        """Callback pour mise à jour temps réel."""
        self._update_summary()
        self._update_submit_state()
        self._animate_preview()

    def _animate_preview(self):
        """Micro-animation du preview pour feedback utilisateur."""
        try:
            original_color = self.summary_frame.cget("fg_color")
            self.summary_frame.configure(fg_color="#10B981")
            self.after(
                150, lambda: self.summary_frame.configure(fg_color=original_color)
            )
        except:
            pass

    def _update_summary(self):
        """Mise à jour de l'aperçu temps réel."""
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        # Nom de l'exercice
        name = self.in_nom.get().strip()
        if name:
            name_label = ctk.CTkLabel(
                self.summary_frame,
                text=name,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            )
            name_label.pack(anchor="w", pady=(0, 12))

        # Création des sections de résumé
        colors = {
            "group": "#10B981",
            "pattern": "#3B82F6",
            "category": "#059669",
            "type": "#8B5CF6",
            "equip": "#F59E0B",
            "course": "#F97316",
            "tags": "#EC4899",
            "meta": "#6B7280",
        }

        self._add_summary_section(
            "Groupe", [self.grp_groupe.get_value()], colors["group"]
        )
        self._add_summary_section(
            "Mouvement", [self.grp_pattern.get_value()], colors["pattern"]
        )
        self._add_summary_section("Type", [self.grp_type.get_value()], colors["type"])
        self._add_summary_section(
            "Catégorie", [self.grp_category.get_value()], colors["category"]
        )

        # Sections multiples
        equips = (
            self.grp_equip.get_values() if hasattr(self.grp_equip, "get_values") else []
        )
        courses = (
            self.grp_course.get_values()
            if hasattr(self.grp_course, "get_values")
            else []
        )
        tags = (
            self.grp_tags.get_values() if hasattr(self.grp_tags, "get_values") else []
        )

        self._add_summary_section("Équipements", equips, colors["equip"])
        self._add_summary_section("Cours", courses, colors["course"])
        self._add_summary_section("Tags", tags, colors["tags"])

        # Paramètres
        params = []
        if self.var_charge.get():
            params.append("Chargeable")
        coeff = self.in_coeff.get().strip() or "1.0"
        params.append(f"Coeff: {coeff}")

        self._add_summary_section("Paramètres", params, colors["meta"])

    def _add_summary_section(self, title: str, items: List[str], color: str):
        """Ajoute une section au résumé."""
        valid_items = [item for item in items if item and item.strip()]
        if not valid_items:
            return

        section = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        section.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
        ).pack(anchor="w", pady=(0, 4))

        chips_frame = ctk.CTkFrame(section, fg_color="transparent")
        chips_frame.pack(fill="x")

        for item in valid_items:
            chip = ctk.CTkFrame(chips_frame, fg_color=color, corner_radius=12)
            chip.pack(side="left", padx=(0, 4), pady=(0, 2))

            ctk.CTkLabel(
                chip,
                text=str(item),
                padx=8,
                pady=4,
                text_color="white",
                font=ctk.CTkFont(size=10, weight="bold"),
            ).pack()

    def _update_submit_state(self):
        """Mise à jour de l'état des boutons de soumission."""
        is_valid = self._is_form_valid()
        state = "normal" if is_valid else "disabled"

        self.btn_submit.configure(state=state)
        if hasattr(self, "btn_submit_new"):
            self.btn_submit_new.configure(state=state)

    def _is_form_valid(self) -> bool:
        """Validation du formulaire."""
        name = self.in_nom.get().strip()
        if not name or len(name) < 3:
            return False

        coeff_val = self.in_coeff.get().strip()
        if coeff_val:
            try:
                float(coeff_val)
            except ValueError:
                return False

        return True

    def _setup_modal_behavior(self):
        """Configuration du comportement modal."""
        try:
            self.transient(self.master)
            self.grab_set()
            self.lift()
            self.focus_force()

            # Centrer la fenêtre
            self.after(10, self._center_window)
        except Exception:
            pass

    def _center_window(self):
        """Centre la fenêtre sur l'écran."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _populate_form(self, exercise: Exercise):
        """Pré-remplit le formulaire avec les données d'un exercice."""
        self.in_nom.insert(0, exercise.nom)

        if exercise.groupe_musculaire_principal:
            self.grp_groupe.set_value(exercise.groupe_musculaire_principal)

        if exercise.movement_pattern:
            self.grp_pattern.set_value(exercise.movement_pattern)

        if exercise.type_effort:
            self.grp_type.set_value(exercise.type_effort)

        if hasattr(exercise, "movement_category") and exercise.movement_category:
            self.grp_category.set_value(exercise.movement_category)

        # Équipements
        if exercise.equipement:
            equips = [
                e.strip() for e in str(exercise.equipement).split(",") if e.strip()
            ]
            self.grp_equip.set_values(equips)

        # Tags
        if exercise.tags:
            all_tags = [t.strip() for t in str(exercise.tags).split(",") if t.strip()]
            course_tags = [t for t in all_tags if t in COURSE_TAGS]
            other_tags = [t for t in all_tags if t in TAG_OPTIONS]

            if course_tags:
                self.grp_course.set_values(course_tags)
            if other_tags:
                self.grp_tags.set_values(other_tags)

        # Paramètres
        self.var_charge.set(bool(exercise.est_chargeable))
        self.in_coeff.insert(0, str(exercise.coefficient_volume or 1.0))

    def _submit(self, reset_after: bool = False):
        """Soumission du formulaire."""
        if not self._is_form_valid():
            return

        name = self.in_nom.get().strip()
        try:
            coeff = float(self.in_coeff.get().strip() or 1.0)
        except ValueError:
            return

        # Collecte des tags
        all_tags = []
        all_tags.extend(
            self.grp_tags.get_values() if hasattr(self.grp_tags, "get_values") else []
        )
        all_tags.extend(
            self.grp_course.get_values()
            if hasattr(self.grp_course, "get_values")
            else []
        )
        tags_csv = ",".join(sorted(set(all_tags))) if all_tags else None

        # Équipements
        equips = (
            self.grp_equip.get_values() if hasattr(self.grp_equip, "get_values") else []
        )
        equip_csv = ",".join(sorted(equips)) if equips else None

        payload = {
            "nom": name,
            "groupe": self.grp_groupe.get_value() or "",
            "equip": equip_csv,
            "tags": tags_csv,
            "pattern": self.grp_pattern.get_value(),
            "category": self.grp_category.get_value(),
            "type_effort": self.grp_type.get_value() or "",
            "coeff": coeff,
            "charge": bool(self.var_charge.get()),
        }

        self._on_submit(payload)

        if reset_after:
            self._reset_form()
            self.in_nom.focus_set()
        else:
            self.destroy()

    def _reset_form(self):
        """Remet à zéro le formulaire pour une nouvelle saisie."""
        self.in_nom.delete(0, tk.END)
        self.grp_groupe.set_value(None)
        self.grp_pattern.set_value(None)
        self.grp_type.set_value(None)
        self.grp_category.set_value(None)
        self.grp_equip.set_values([])
        self.grp_course.set_values([])
        self.grp_tags.set_values([])
        self.var_charge.set(False)
        self.in_coeff.delete(0, tk.END)
        self.in_coeff.insert(0, "1.0")
        self.name_status.configure(text="")
