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
        header = ctk.CTkFrame(container, fg_color="#1d2228", corner_radius=8)
        header.pack(fill="x", padx=12, pady=(12, 6))
        ctk.CTkLabel(header, text=meta.get("title", ""), font=("", 13, "bold")).pack(
            side="left", padx=12, pady=8
        )
        ctk.CTkLabel(
            header,
            text=meta.get("duration", ""),
            text_color="#9ca3af",
            font=("", 12),
        ).pack(side="left", padx=12, pady=8)

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
