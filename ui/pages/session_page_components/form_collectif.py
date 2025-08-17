"""UI components for collective session generation form."""

import customtkinter as ctk

from ui.components.design_system.buttons import PrimaryButton
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle

# Constants defining the form options
COURSE_TYPES = ["CAF", "Core & Glutes", "Cross-Training", "Hyrox"]
DURATIONS = ["45", "60"]
INTENSITIES = ["Faible", "Moyenne", "Haute"]
EQUIPMENTS = [
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


class FormCollectif(Card):
    """Formulaire pour la génération de cours collectifs."""

    def __init__(self, parent, generate_callback=None):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

        # Section: Paramètres Principaux
        params = ctk.CTkFrame(self, fg_color="transparent")
        params.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        params.grid_columnconfigure(1, weight=1)

        CardTitle(params, text="Paramètres Principaux").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        ctk.CTkLabel(params, text="Type de cours").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 8)
        )
        self.course_var = ctk.StringVar(value=COURSE_TYPES[0])
        ctk.CTkOptionMenu(
            params, variable=self.course_var, values=COURSE_TYPES
        ).grid(row=1, column=1, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(params, text="Durée (min)").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 8)
        )
        self.duration_var = ctk.StringVar(value=DURATIONS[0])
        ctk.CTkOptionMenu(
            params, variable=self.duration_var, values=DURATIONS
        ).grid(row=2, column=1, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(params, text="Intensité").grid(
            row=3, column=0, sticky="w", padx=(0, 8)
        )
        self.intensity_var = ctk.StringVar(value=INTENSITIES[0])
        ctk.CTkOptionMenu(
            params, variable=self.intensity_var, values=INTENSITIES
        ).grid(row=3, column=1, sticky="ew")

        # Section: Matériel Disponible
        equip_section = ctk.CTkFrame(self, fg_color="transparent")
        equip_section.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

        CardTitle(equip_section, text="Matériel Disponible").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        grid = ctk.CTkFrame(equip_section, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew")
        grid.grid_columnconfigure((0, 1), weight=1)

        self.equipment_vars = {}
        for idx, label in enumerate(EQUIPMENTS):
            var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(grid, text=label, variable=var).grid(
                row=idx // 2, column=idx % 2, sticky="w", padx=4, pady=4
            )
            self.equipment_vars[label] = var

        # Action button
        PrimaryButton(
            self, text="Générer la séance", command=generate_callback
        ).grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

    def get_params(self) -> dict:
        """Retourne les paramètres du formulaire."""
        return {
            "course_type": self.course_var.get(),
            "duration": self.duration_var.get(),
            "intensity": self.intensity_var.get(),
            "equipment": [k for k, v in self.equipment_vars.items() if v.get()],
        }

