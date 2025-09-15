"""Compact visual card representing a workout block."""

import customtkinter as ctk

FORMAT_COLORS = {
    "EMOM": "#22D3EE",
    "AMRAP": "#F59E0B",
    "FOR_TIME": "#10B981",
    "For Time": "#10B981",
    "TABATA": "#A78BFA",
    "SETSxREPS": "#94A3B8",
    "SKILL": "#8B5CF6",  # Violet pour le travail technique
}

FORMAT_ICONS = {
    "EMOM": "⏰",
    "AMRAP": "🔄",
    "FOR_TIME": "⚡",
    "For Time": "⚡",
    "TABATA": "🔥",
    "SETSxREPS": "📊",
    "SKILL": "🎯",  # Cible pour le travail technique
}


class WorkoutBlock(ctk.CTkFrame):
    """Block card moderne avec design professionnel."""

    def __init__(self, parent, title: str, fmt: str, duration: str = ""):
        super().__init__(parent, fg_color=("gray95", "gray18"), corner_radius=12)
        color = FORMAT_COLORS.get(fmt.upper(), "#94A3B8")
        icon = FORMAT_ICONS.get(fmt.upper(), "🎯")

        # Configuration du grid principal
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header du bloc avec couleur et icône
        header_frame = ctk.CTkFrame(self, fg_color=color, corner_radius=8, height=50)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=16, pady=12)

        # Titre avec icône
        title_label = ctk.CTkLabel(
            header_content,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left")

        # Durée
        if duration:
            duration_label = ctk.CTkLabel(
                header_content,
                text=duration,
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            duration_label.pack(side="right")

        # Corps du bloc
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        self._ex_container = ctk.CTkFrame(body, fg_color="transparent")
        self._ex_container.grid(row=0, column=0, sticky="nsew")

        # Compteur d'exercices (sera mis à jour)
        self._exercise_count = 0
        self._count_label = None

    # ------------------------------------------------------------------
    def add_exercise(
        self,
        nom: str,
        reps: str | None,
        repos_s: int | None,
        muscle: str,
        equip: str,
    ) -> None:
        """Render un exercice avec design moderne."""

        self._exercise_count += 1

        # Wrapper avec alternance de couleurs
        bg_color = ("gray92", "gray22") if self._exercise_count % 2 == 0 else "transparent"
        wrapper = ctk.CTkFrame(self._ex_container, fg_color=bg_color, corner_radius=6)
        wrapper.pack(fill="x", pady=2, padx=2)

        # Container principal
        exercise_frame = ctk.CTkFrame(wrapper, fg_color="transparent")
        exercise_frame.pack(fill="x", padx=12, pady=8)

        # Ligne du haut : nom + prescriptions
        top_frame = ctk.CTkFrame(exercise_frame, fg_color="transparent")
        top_frame.pack(fill="x")

        # Icône d'exercice
        exercise_icons = {
            "poitrine": "💪", "chest": "💪",
            "dos": "🧗", "back": "🧗",
            "jambes": "🦵", "legs": "🦵",
            "epaules": "🏋️", "shoulders": "🏋️",
            "bras": "💪", "arms": "💪",
            "core": "🔥", "abdos": "🔥"
        }
        muscle_lower = muscle.lower() if muscle else ""
        icon = next((v for k, v in exercise_icons.items() if k in muscle_lower), "🎯")

        # Nom avec icône
        name_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            name_frame,
            text=f"{icon} {nom}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(side="left")

        # Prescriptions (reps + repos) dans des badges
        if reps or repos_s is not None:
            prescription_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
            prescription_frame.pack(side="right")

            if reps:
                reps_badge = ctk.CTkLabel(
                    prescription_frame,
                    text=reps,
                    fg_color="#4A90E2",
                    corner_radius=8,
                    padx=6, pady=2,
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color="white"
                )
                reps_badge.pack(side="left", padx=(0, 4))

            if repos_s is not None:
                repos_badge = ctk.CTkLabel(
                    prescription_frame,
                    text=f"{repos_s}s",
                    fg_color="#E74C3C",
                    corner_radius=8,
                    padx=6, pady=2,
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color="white"
                )
                repos_badge.pack(side="left")

        # Ligne du bas : muscle + équipement
        if muscle or equip:
            bottom_frame = ctk.CTkFrame(exercise_frame, fg_color="transparent")
            bottom_frame.pack(fill="x", pady=(4, 0))

            info_parts = []
            if muscle:
                info_parts.append(f"🎯 {muscle}")
            if equip:
                info_parts.append(f"🛠️ {equip}")

            info_text = " • ".join(info_parts)
            ctk.CTkLabel(
                bottom_frame,
                text=info_text,
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray60"),
                anchor="w"
            ).pack(side="left")


__all__ = ["WorkoutBlock", "FORMAT_COLORS", "FORMAT_ICONS"]
