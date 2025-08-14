import customtkinter as ctk

# Constants defining the form options
COURSE_TYPES = ["CAF", "Core & Glutes", "Cross-Training", "Hyrox"]
DURATIONS = ["45", "60"]
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
FORMATS = ["EMOM", "AMRAP", "For Time", "Tabata"]
INTENSITIES = ["Low", "Medium", "High"]


class FormCollectif(ctk.CTkFrame):
    """Formulaire pour la génération de cours collectifs."""

    def __init__(
        self,
        parent,
        generate_callback,
        open_preview_callback,
        toggle_form_callback,
    ):
        super().__init__(parent, fg_color="#222", corner_radius=10)
        self.configure(width=360)
        self.grid_columnconfigure(0, weight=1)

        # Ligne 1: Type de cours et Durée
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        row1.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(row1, text="Type de cours").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.course_var = ctk.StringVar(value=COURSE_TYPES[0])
        ctk.CTkOptionMenu(row1, variable=self.course_var, values=COURSE_TYPES).grid(
            row=0, column=1, sticky="ew", padx=(0, 12)
        )
        ctk.CTkLabel(row1, text="Durée").grid(row=0, column=2, sticky="w", padx=(4, 8))
        self.duration_var = ctk.StringVar(value=DURATIONS[0])
        ctk.CTkOptionMenu(row1, variable=self.duration_var, values=DURATIONS, width=80).grid(
            row=0, column=3, sticky="ew"
        )

        # Ligne 2: Intensité
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        row2.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row2, text="Intensité").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.intensity_var = ctk.StringVar(value=INTENSITIES[1])
        ctk.CTkOptionMenu(row2, variable=self.intensity_var, values=INTENSITIES).grid(
            row=0, column=1, sticky="ew", padx=(0, 12)
        )

        # Sliders
        sliders = ctk.CTkFrame(self, fg_color="transparent")
        sliders.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(sliders, text="Variabilité").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.variability = ctk.IntVar(value=50)
        ctk.CTkSlider(
            sliders,
            from_=0,
            to=100,
            number_of_steps=100,
            variable=self.variability,
            width=220,
        ).grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(sliders, text="Intensité (1-10)").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(6, 0)
        )
        self.intensity_cont = ctk.IntVar(value=6)
        ctk.CTkSlider(
            sliders,
            from_=1,
            to=10,
            number_of_steps=9,
            variable=self.intensity_cont,
            width=220,
        ).grid(row=1, column=1, sticky="ew", pady=(6, 0))
        ctk.CTkLabel(sliders, text="Densité").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=(6, 0)
        )
        self.density = ctk.IntVar(value=5)
        ctk.CTkSlider(
            sliders,
            from_=1,
            to=10,
            number_of_steps=9,
            variable=self.density,
            width=220,
        ).grid(row=2, column=1, sticky="ew", pady=(6, 0))

        # Matériel
        equip_frame = ctk.CTkFrame(self, fg_color="#1f1f1f")
        equip_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(equip_frame, text="Matériel disponible").grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 4)
        )
        grid = ctk.CTkFrame(equip_frame, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        grid.grid_columnconfigure((0, 1), weight=1)
        self.equip_vars = {}
        for i, label in enumerate(EQUIPMENTS):
            v = ctk.BooleanVar(value=label in ("Poids du corps",))
            ctk.CTkCheckBox(grid, text=label, variable=v).grid(
                row=i // 2, column=i % 2, sticky="w", padx=6, pady=4
            )
            self.equip_vars[label] = v

        # Formats
        formats_frame = ctk.CTkFrame(self, fg_color="transparent")
        formats_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=6)
        ctk.CTkLabel(formats_frame, text="Formats").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        self.format_vars = {
            f: ctk.BooleanVar(value=(f in ("AMRAP", "EMOM"))) for f in FORMATS
        }
        frm = ctk.CTkFrame(formats_frame, fg_color="transparent")
        frm.grid(row=1, column=0, sticky="ew")
        for i, f in enumerate(FORMATS):
            frm.grid_columnconfigure(i % 2, weight=1)
            ctk.CTkCheckBox(frm, text=f, variable=self.format_vars[f]).grid(
                row=i // 2, column=i % 2, sticky="w", padx=6, pady=2
            )

        # Boutons d'action
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=98, column=0, sticky="ew", padx=12, pady=(6, 12))
        for c in range(2):
            btns.grid_columnconfigure(c, weight=1)

        # Note: The "Regénérer tout" button has the same command as "Générer"
        ctk.CTkButton(btns, text="Générer", command=generate_callback).grid(
            row=0, column=0, sticky="ew", padx=4, pady=4
        )
        ctk.CTkButton(btns, text="Regénérer tout", command=generate_callback).grid(
            row=0, column=1, sticky="ew", padx=4, pady=4
        )
        ctk.CTkButton(btns, text="Agrandir l’aperçu", command=open_preview_callback).grid(
            row=1, column=0, sticky="ew", padx=4, pady=4
        )
        ctk.CTkButton(btns, text="Masquer le formulaire", command=toggle_form_callback).grid(
            row=1, column=1, sticky="ew", padx=4, pady=4
        )

    def get_params(self) -> dict:
        """Returns a dictionary of the current form parameters."""
        return {
            "course_type": self.course_var.get(),
            "duration_min": int(self.duration_var.get()),
            "intensity": self.intensity_var.get(),
            "variability": int(self.variability.get()),
            "intensity_cont": int(self.intensity_cont.get()),
            "density": int(self.density.get()),
            "equipment": [k for k, v in self.equip_vars.items() if v.get()],
            "enabled_formats": [f for f, var in self.format_vars.items() if var.get()],
        }
