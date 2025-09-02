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
        generate_callback=None,
        equipment_options: list[str] | None = None,
    ) -> None:
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

        equipment_options = equipment_options or DEFAULT_EQUIPMENTS

        CardTitle(self, text="Paramètres de séance").grid(
            row=0, column=0, sticky="w", padx=16, pady=(16, 12)
        )

        # Durée de séance
        # Type de séance
        course_row = ctk.CTkFrame(self, fg_color="transparent")
        course_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        course_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(course_row, text="Type de séance").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.course_type_var = ctk.StringVar(value="Crossfit")
        ctk.CTkOptionMenu(
            course_row, variable=self.course_type_var, values=COURSE_TYPES_DISPLAY
        ).grid(row=0, column=1, sticky="ew")

        # DurǸe de sǸance
        duration_row = ctk.CTkFrame(self, fg_color="transparent")
        duration_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
        duration_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(duration_row, text="Durée de séance").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.duration_var = ctk.StringVar(value="45")
        ctk.CTkOptionMenu(
            duration_row, variable=self.duration_var, values=DURATIONS
        ).grid(row=0, column=1, sticky="ew")

        # Matériel disponible
        equip_section = ctk.CTkFrame(self, fg_color="transparent")
        equip_section.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 8))
        CardTitle(equip_section, text="Matériel disponible").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        equip_grid = ctk.CTkFrame(equip_section, fg_color="transparent")
        equip_grid.grid(row=1, column=0, sticky="ew")
        equip_grid.grid_columnconfigure((0, 1), weight=1)
        self.equipment_vars: dict[str, ctk.BooleanVar] = {}
        for idx, label in enumerate(equipment_options):
            var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(equip_grid, text=label, variable=var).grid(
                row=idx // 2, column=idx % 2, sticky="w", padx=4, pady=4
            )
            self.equipment_vars[label] = var

        # Variabilité
        variability_row = ctk.CTkFrame(self, fg_color="transparent")
        variability_row.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 8))
        variability_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(variability_row, text="Variabilité").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.variability_var = ctk.DoubleVar(value=50)
        ctk.CTkSlider(
            variability_row, from_=0, to=100, variable=self.variability_var
        ).grid(row=0, column=1, sticky="ew")

        # Volume
        volume_row = ctk.CTkFrame(self, fg_color="transparent")
        volume_row.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 8))
        volume_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(volume_row, text="Volume").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.volume_var = ctk.DoubleVar(value=50)
        ctk.CTkSlider(volume_row, from_=0, to=100, variable=self.volume_var).grid(
            row=0, column=1, sticky="ew"
        )

        # Formats
        format_section = ctk.CTkFrame(self, fg_color="transparent")
        format_section.grid(row=6, column=0, sticky="ew", padx=16, pady=(0, 8))
        CardTitle(format_section, text="Format").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        format_grid = ctk.CTkFrame(format_section, fg_color="transparent")
        format_grid.grid(row=1, column=0, sticky="ew")
        format_grid.grid_columnconfigure((0, 1), weight=1)
        self.format_vars: dict[str, ctk.BooleanVar] = {}
        for idx, fmt in enumerate(FORMATS):
            var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(format_grid, text=fmt, variable=var).grid(
                row=idx // 2, column=idx % 2, sticky="w", padx=4, pady=4
            )
            self.format_vars[fmt] = var

        # Continuum Cardio ↔ Renfo
        continuum_row = ctk.CTkFrame(self, fg_color="transparent")
        continuum_row.grid(row=7, column=0, sticky="ew", padx=16, pady=(0, 8))
        continuum_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(continuum_row, text="Continuum Cardio ↔ Renfo").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.continuum_var = ctk.DoubleVar(value=0)
        ctk.CTkSlider(
            continuum_row, from_=-100, to=100, variable=self.continuum_var
        ).grid(row=0, column=1, sticky="ew")

        # Focus
        focus_row = ctk.CTkFrame(self, fg_color="transparent")
        focus_row.grid(row=8, column=0, sticky="ew", padx=16, pady=(0, 8))
        focus_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(focus_row, text="Focus").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.focus_var = ctk.StringVar(value="Full-body")
        ctk.CTkOptionMenu(
            focus_row, variable=self.focus_var, values=FOCUS_OPTIONS
        ).grid(row=0, column=1, sticky="ew")

        # Objectif
        obj_row = ctk.CTkFrame(self, fg_color="transparent")
        obj_row.grid(row=9, column=0, sticky="ew", padx=16, pady=(0, 8))
        obj_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(obj_row, text="Objectif").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.objective_var = ctk.StringVar(value="Force")
        ctk.CTkOptionMenu(
            obj_row, variable=self.objective_var, values=OBJECTIVE_OPTIONS
        ).grid(row=0, column=1, sticky="ew")

        # Inclure automatiquement
        auto_section = ctk.CTkFrame(self, fg_color="transparent")
        auto_section.grid(row=10, column=0, sticky="ew", padx=16, pady=(0, 8))
        CardTitle(auto_section, text="Inclure automatiquement").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        auto_grid = ctk.CTkFrame(auto_section, fg_color="transparent")
        auto_grid.grid(row=1, column=0, sticky="w")
        self.auto_vars: dict[str, ctk.BooleanVar] = {}
        for idx, opt in enumerate(AUTO_INCLUDE_OPTIONS):
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(auto_grid, text=opt, variable=var).grid(
                row=idx, column=0, sticky="w", padx=4, pady=4
            )
            self.auto_vars[opt] = var

        # Bouton d'action
        PrimaryButton(self, text="Générer la séance", command=generate_callback).grid(
            row=11, column=0, sticky="ew", padx=16, pady=(0, 16)
        )

    def get_params(self) -> dict:
        """Retourne les valeurs du formulaire sous forme de dictionnaire."""
        return {
            "course_type": COURSE_TYPE_VALUE_MAP.get(
                self.course_type_var.get(), self.course_type_var.get()
            ),
            "duration": int(self.duration_var.get()),
            "equipment": [k for k, v in self.equipment_vars.items() if v.get()],
            "variability": int(self.variability_var.get()),
            "volume": int(self.volume_var.get()),
            "formats": [k for k, v in self.format_vars.items() if v.get()],
            "continuum": int(self.continuum_var.get()),
            "focus": self.focus_var.get(),
            "objective": self.objective_var.get(),
            "auto_include": [k for k, v in self.auto_vars.items() if v.get()],
        }


__all__ = ["FormCollectif"]
