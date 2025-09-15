"""Preview rendering utilities for generated sessions."""

from __future__ import annotations

import customtkinter as ctk

from ui.components.workout_block import WorkoutBlock


def render_preview(container: ctk.CTkScrollableFrame, dto: dict) -> int:
    """Render the session preview inside ``container``.

    Returns the number of columns used so callers can avoid unnecessary
    re-renders on resize events.
    """
    for w in container.winfo_children():
        w.destroy()
    if hasattr(container, "_parent_canvas"):
        container._parent_canvas.yview_moveto(0.0)

    width = container.winfo_toplevel().winfo_width()
    cols = 2 if width >= 1200 else 1

    meta = dto.get("meta", {})
    if meta:
        # Header moderne avec gradient et icônes
        header = ctk.CTkFrame(
            container, fg_color=("gray90", "gray25"), corner_radius=12, height=80
        )
        header.pack(fill="x", padx=12, pady=(12, 16))
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=16)

        # Titre avec icône basée sur le type
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(fill="x")

        course_type = meta.get("course_type", "")
        course_icons = {
            "Cross-Training": "🏋️‍♂️",
            "Hyrox": "🏃‍♂️",
            "CAF": "💪",
            "Core & Glutes": "🔥",
            "TRX": "⚡",
        }
        icon = course_icons.get(course_type, "🎯")

        title_text = f"{icon} {meta.get('title', 'Séance')}"
        ctk.CTkLabel(
            title_frame, text=title_text, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        # Badges d'information
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(fill="x", pady=(8, 0))

        # Badge durée
        if meta.get("duration"):
            duration_badge = ctk.CTkLabel(
                info_frame,
                text=f"⏱️ {meta.get('duration')}",
                fg_color=("gray80", "gray30"),
                corner_radius=20,
                padx=12,
                pady=4,
                font=ctk.CTkFont(size=11, weight="bold"),
            )
            duration_badge.pack(side="left", padx=(0, 8))

        # Badge intensité
        if meta.get("intensity"):
            intensity_colors = {
                "Légère": ("lightgreen", "darkgreen"),
                "Moyenne": ("orange", "darkorange"),
                "Élevée": ("lightcoral", "darkred"),
                "Maximale": ("red", "darkred"),
            }
            intensity = meta.get("intensity")
            color = intensity_colors.get(intensity, ("gray", "gray"))

            intensity_badge = ctk.CTkLabel(
                info_frame,
                text=f"🔥 {intensity}",
                fg_color=color,
                corner_radius=20,
                padx=12,
                pady=4,
                font=ctk.CTkFont(size=11, weight="bold"),
            )
            intensity_badge.pack(side="left", padx=(0, 8))

        # Badge générateur IA
        if meta.get("smart_generated"):
            ai_badge = ctk.CTkLabel(
                info_frame,
                text="✨ IA",
                fg_color=("purple", "darkviolet"),
                corner_radius=20,
                padx=12,
                pady=4,
                font=ctk.CTkFont(size=11, weight="bold"),
            )
            ai_badge.pack(side="left")

    # Titre de section pour les blocs
    if dto.get("blocks"):
        section_header = ctk.CTkFrame(container, fg_color="transparent")
        section_header.pack(fill="x", padx=12, pady=(8, 16))

        blocks_count = len(dto.get("blocks", []))
        ctk.CTkLabel(
            section_header,
            text=f"📋 Structure de la séance ({blocks_count} blocs)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray50", "gray60"),
        ).pack(side="left")

    grid = ctk.CTkFrame(container, fg_color="transparent")
    grid.pack(fill="both", expand=True, padx=6, pady=6)
    for c in range(cols):
        grid.grid_columnconfigure(c, weight=1, uniform="blocks")

    for i, block in enumerate(dto.get("blocks", [])):
        wb = WorkoutBlock(
            grid, block["title"], block.get("format", ""), block.get("duration", "")
        )
        r, c = divmod(i, cols)
        wb.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
        for ex in block.get("exercises", []):
            wb.add_exercise(
                ex.get("nom", ""),
                ex.get("reps"),
                ex.get("repos_s"),
                ex.get("muscle", ""),
                ex.get("equip", ""),
            )

    return cols


__all__ = ["render_preview"]
